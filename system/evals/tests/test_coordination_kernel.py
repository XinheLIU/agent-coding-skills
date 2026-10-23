"""B23 local CLI fixtures; no model, host dispatch, or remote tracker claims."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "scripts/acs-coordination.py"
spec = importlib.util.spec_from_file_location("coordination_kernel", CLI)
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)


class CoordinationKernelTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def ticket(self, change="change", name="T1", deps="none", status="pending"):
        path = self.root / change / "tasks" / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {name}: Test\n\nType: implementation\nStatus: {status}\nReadiness: ready\ndepends_on: {deps}\n")
        return path

    def run_cli(self, *args, code=0, cwd=None):
        process = subprocess.run([sys.executable, "-B", str(CLI), *map(str, args)],
                                 cwd=cwd, capture_output=True, text=True)
        self.assertEqual(process.returncode, code, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def test_resolution_from_foreign_cwd_and_symlink(self):
        ticket = self.ticket()
        alias = self.root / "alias"
        alias.symlink_to(self.root / "change", target_is_directory=True)
        result = self.run_cli("resolve", alias, "--ticket", "change/T1", cwd=self.root)
        self.assertEqual(result["id"], "change/T1")
        self.assertEqual(result["source_file"], str(ticket))
        self.assertEqual(result["source_revision"], "sha256:" + hashlib.sha256(ticket.read_bytes()).hexdigest())

    def test_ambiguous_and_unknown_identity_fail(self):
        self.ticket("one")
        self.ticket("two")
        for name in ("T1", "absent"):
            report = self.run_cli("resolve", self.root, "--ticket", name, code=1)
            self.assertIn("IDENTITY-UNRESOLVED", report["errors"][0])
        self.assertEqual(self.run_cli("resolve", self.root, "--ticket", "two/T1")["id"], "two/T1")

    def test_status_reuses_b14_and_blocks_missing_dependency(self):
        self.ticket()
        self.ticket(name="T2", deps="missing")
        actual = self.run_cli("status", self.root)
        scanner = kernel.load_module("scanner", kernel.SCANNER)
        self.assertEqual(actual, scanner.status_report(scanner.scan(self.root)))
        self.assertEqual(actual["frontier"], ["change/T1"])
        self.assertEqual(actual["tickets"][1]["missing_dependencies"], ["change/missing"])
        self.assertIn("not whether its prerequisites", actual["warnings"][0])

    def test_cycle_fails_even_with_missing_dependency(self):
        self.ticket(deps="T2, absent")
        self.ticket(name="T2", deps="T1")
        result = self.run_cli("status", self.root, code=1)
        self.assertIn("Dependency cycle", result["errors"][0])

    def binding(self, record, source, revision=None):
        revision = revision or "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
        record.write_text("# Record\n\n```acs-consumed-revisions\n" + json.dumps([
            {"source": source.name, "revision": revision, "scope": "acceptance criterion C1"}
        ]) + "\n```\n")

    def test_fresh_changed_and_missing_premise_never_rewrite_status(self):
        source = self.root / "premise.txt"
        source.write_text("accepted")
        record = self.root / "consumer.md"
        self.binding(record, source)
        before = record.read_bytes()
        self.assertEqual(self.run_cli("freshness", record)["bindings"][0]["freshness"], "current")
        source.write_text("revised")
        result = self.run_cli("freshness", self.root, code=1)
        self.assertEqual(result["needs_review"][0]["reason"], "CHANGED-PREMISE")
        source.unlink()
        result = self.run_cli("freshness", record, code=1)
        self.assertEqual(result["needs_review"][0]["reason"], "SOURCE-UNAVAILABLE")
        self.assertEqual(record.read_bytes(), before)

    def test_unbound_and_unsupported_are_not_current(self):
        record = self.root / "record.md"
        record.write_text("# Record\n")
        report = self.run_cli("freshness", self.root)
        self.assertEqual(report["unassessed"], [str(record)])
        self.assertEqual(report["bindings"], [])
        self.binding(record, record, "git:unknown")
        report = self.run_cli("freshness", record, code=1)
        self.assertEqual(report["needs_review"][0]["reason"], "UNSUPPORTED-REVISION")

    def test_malformed_bindings_and_absent_root_fail(self):
        record = self.root / "record.md"
        for value in ("{}", "[]", '[{"source":"s"}]', "no json"):
            record.write_text(f"```acs-consumed-revisions\n{value}\n```\n")
            report = self.run_cli("freshness", record, code=1)
            self.assertIn("INVALID-BINDINGS", report["errors"][0])
        record.write_text("```acs-consumed-revisions\n[]\n")
        self.assertIn("malformed fence", self.run_cli("freshness", record, code=1)["errors"][0])
        self.run_cli("freshness", self.root / "absent", code=1)

    def test_verify_fresh_stale_base_and_blank_identity(self):
        evidence = self.root / "evidence.json"
        evidence.write_text(json.dumps({"base": "base", "rows": [{
            "criterion": "C1", "command": "do not execute me", "revision": "current",
            "timestamp": "2026-10-23T00:00:00Z", "result": "passed"
        }]}))
        self.assertTrue(self.run_cli("verify", evidence, "--base", "base", "--revision", "current")["passed"])
        for base, revision, reason in (("base", "changed", "STALE-REVISION"),
                                       ("other", "current", "BASE-MISMATCH"),
                                       ("", "current", "INVALID-IDENTITY")):
            result = self.run_cli("verify", evidence, "--base", base, "--revision", revision, code=1)
            self.assertIn(reason, result["errors"][0])

    def test_catalog_command_propagates_real_budget_failure(self):
        # A complete tiny inventory exercises kernel -> validator subprocesses.
        suite = self.root / "system"
        skill = suite / "skills-src/test/acs-example/SKILL.md"
        skill.parent.mkdir(parents=True)
        (suite / "skills").mkdir()
        (suite / "skills/acs-example").symlink_to(skill.parent)
        for host in ("claude", "codex"):
            directory = suite / f".{host}-plugin"
            directory.mkdir()
            (directory / "plugin.json").write_text(json.dumps({
                "name": "agent-coding-skills", "skills": "./skills/"}))
        catalog = self.root / "catalog/skill-set.json"
        catalog.parent.mkdir()
        catalog.write_text(json.dumps({
            "schemaVersion": 1, "id": "agent-coding-skills",
            "sourcePattern": "system/skills-src/{category}/{skill}/SKILL.md",
            "categories": [{"id": "test", "skills": ["acs-example"]}]}))
        protocol = suite / "protocols/skill-declarations.md"
        protocol.parent.mkdir()
        protocol.write_text("## Handoff consumers\n")
        validator = suite / "evals/validate_suite.py"
        validator.parent.mkdir()
        validator.write_bytes((ROOT / "system/evals/validate_suite.py").read_bytes())
        cli = self.root / "scripts/acs-coordination.py"
        cli.parent.mkdir()
        cli.write_bytes(CLI.read_bytes())
        for size, expected in ((260, True), (300, False)):
            skill.write_text("---\nname: acs-example\ndescription: Use when " + "x" * (size - 9)
                             + "\n---\n\n```yaml\ncontext:\n" + "".join(
                                 f"  {field}: []\n" for field in
                                 ("requires", "retrieves", "produces", "updates", "invalidates", "handoff_to")
                             ) + "```\n")
            process = subprocess.run([sys.executable, "-B", str(cli), "checks", "--only", "catalog"],
                                     capture_output=True, text=True)
            self.assertEqual(process.returncode, int(not expected), process.stdout + process.stderr)
            report = json.loads(process.stdout)
            self.assertEqual(report["passed"], expected)
            if not expected:
                self.assertIn("300 bytes; limit is 260", report["checks"][0]["stdout"])

    def test_derived_check_rejects_drift_without_repair(self):
        output = self.root / "plugins"
        process = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/build-plugins.py"),
                                  "--output", str(output)], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertTrue(self.run_cli("checks", "--only", "derived", "--plugins", output)["passed"])
        target = output / "acs-build/skills/acs-tdd/SKILL.md"
        target.write_text(target.read_text() + "\nUnexpected derived drift\n")
        changed = target.read_bytes()
        report = self.run_cli("checks", "--only", "derived", "--plugins", output, code=1)
        self.assertIn("STALE", report["checks"][0]["stdout"])
        self.assertEqual(target.read_bytes(), changed)

    def test_checks_use_check_only_and_collect_all_failures(self):
        with patch.object(kernel.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "STALE", "")) as run:
            report = kernel.checks(self.root / "plugins", "all")
            self.assertFalse(report["passed"])
            self.assertEqual(run.call_count, 3)
            self.assertIn("--check", report["checks"][2]["command"])
            self.assertIn(str(self.root / "plugins"), report["checks"][2]["command"])

    def test_status_does_not_write_to_read_tree(self):
        self.ticket()
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.run_cli("resolve", self.root)
        self.run_cli("status", self.root)
        self.run_cli("freshness", self.root)
        after = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
