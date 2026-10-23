"""Rigor-tier source/closure checks and a scripted one-ticket delivery, not a model run."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from test_packages import builder, validator

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
IMPLEMENT = SUITE / "skills-src/build/acs-implement"


class RigorTierTests(unittest.TestCase):
    def test_entry_routes_and_canonical_policy_are_connected(self) -> None:
        workflow = (SUITE / "workflows/README.md").read_text()
        for required in (
            "**Spike**", "**Bounded (default)**", "**Architectural**",
            "Before invoking the first skill", "single configured recovery entry",
            "Spike → Bounded → Architectural", "nothing downgrades mid-task",
            "A reply approves the stage actually presented.",
            "Reuse recorded approval", "../protocols/questioning.md",
            "**cost-optimized model**", "**frontier model**", "final gate",
            "revision-bound evidence contract",
        ):
            self.assertIn(required, workflow)
        coordinator = (SUITE / "protocols/context-coordination.md").read_text()
        self.assertIn("../workflows/README.md#rigor-tiers", coordinator)
        self.assertIn("standalone skill entry", coordinator)
        self.assertIn("approval reference or pending gate", coordinator)
        quickstart = (ROOT / "README.md").read_text().split("## Quick start", 1)[1].split("## Architecture", 1)[0]
        self.assertIn("Bounded is the default", quickstart)
        self.assertIn("before the first skill", quickstart)
        build = (SUITE / "workflows/build.md").read_text()
        self.assertIn("SKILL.md#bounded-entry", build)
        self.assertIn("graph sequence below is the Architectural route", build)

    def test_bounded_bypass_preserves_evidence_and_questioning(self) -> None:
        text = (IMPLEMENT / "SKILL.md").read_text()
        bounded = text.split("## Bounded entry", 1)[1].split("## Reuse or prepare", 1)[0]
        for required in (
            "reuse or create one canonical ticket", "protocols/questioning.md",
            "approval reference", "serial `acs-tdd`", "No `acs-plan-delivery` invocation",
            "HTML delivery plan is required", "immutable BASE", "source fingerprint",
            "evidence sidecar/checker", "stop dependent work",
            "Do not silently expand Bounded into a graph",
        ):
            self.assertIn(required, bounded)
        self.assertIn("For Architectural work, refresh", text)
        self.assertIn("Reject `STALE-REVISION`", text)
        self.assertIn("scripts/check-evidence.py", text)
        self.assertIn("Code-level green is not done", text)

    def test_standalone_implement_retains_tiers_and_gates_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, IMPLEMENT)
            installed = root / "installed/acs-implement"
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            resources = installed / "resources"
            self.assertIn("**Bounded (default)**", (resources / "workflows/README.md").read_text())
            self.assertTrue((resources / "protocols/questioning.md").is_file())
            self.assertTrue((installed / "scripts/check-evidence.py").is_file())
            self.assertFalse(any(p.is_symlink() for p in installed.rglob("*")))

    def test_scripted_bounded_ticket_red_green_cli_and_revision_binding(self) -> None:
        """Execute actual subprocesses; authored design/approval is only fixture input."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = root / ".scratch/run/state.md"
            state.parent.mkdir(parents=True)
            state.write_text(
                "# Scripted fixture, not a user conversation\n"
                "Rigor tier: Bounded\nReason: repair an existing CLI greeting.\n"
                "Stage: implementation\nApproval: authored fixture precondition, not a human reply.\n"
                "Model class: none (script); sensors: red/green and final CLI check.\n"
            )
            tasks = root / "docs/changes/greeting/tasks"
            tasks.mkdir(parents=True)
            ticket = tasks / "T1.md"
            ticket.write_text(
                "# T1: Preserve greeting capitalization\n\nLast updated: 2026-10-23\n\n"
                "Parent: greeting\nType: implementation\nStatus: pending\nReadiness: ready\n"
                "depends_on: none\naffects: greet.py\n\n## Scope\nRepair the existing CLI.\n\n"
                "## Inputs\nDesign: remove lowercasing; preserve the CLI argument.\n"
                "Approval: authored fixture precondition; not a model transcript.\n\n"
                "## Verification\nAC-1: CLI argument ACS prints Hello, ACS!.\n\n"
                "## Blockers\nnone\n\n## Evidence\nPending actual execution.\n"
            )
            app = root / "greet.py"
            app.write_text("import sys\nprint(f'Hello, {sys.argv[1].lower()}!')\n")
            check = root / "test_greet.py"
            check.write_text(
                "import subprocess, sys, unittest\n"
                "class GreetingTest(unittest.TestCase):\n"
                " def test_cli_preserves_case(self):\n"
                "  result = subprocess.run([sys.executable, 'greet.py', 'ACS'], check=True, capture_output=True, text=True)\n"
                "  self.assertEqual(result.stdout, 'Hello, ACS!\\n')\n"
            )

            def identity() -> str:
                digest = hashlib.sha256()
                for path in (app, check):
                    digest.update(path.name.encode() + b"\0" + path.read_bytes() + b"\0")
                return "sha256:" + digest.hexdigest()

            base = identity()
            command = [sys.executable, "-m", "unittest", "-v"]
            red = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(red.returncode, 1, red.stdout + red.stderr)
            self.assertIn("Hello, acs!", red.stderr)
            (root / "red.log").write_text(red.stdout + red.stderr)
            app.write_text(app.read_text().replace("sys.argv[1].lower()", "sys.argv[1]"))
            revision = identity()
            rows = []
            for args in (command, [sys.executable, "greet.py", "ACS"]):
                result = subprocess.run(args, cwd=root, capture_output=True, text=True)
                timestamp = datetime.now(timezone.utc).isoformat()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                if args[-1] == "ACS":
                    self.assertEqual(result.stdout, "Hello, ACS!\n")
                rows.append({"criterion": "AC-1", "command": f"cwd={root}; {args!r}",
                             "revision": revision, "timestamp": timestamp, "result": "passed"})
            evidence = root / "T1.json"
            evidence.write_text(json.dumps({"base": base, "rows": rows}))
            checker = [sys.executable, str(IMPLEMENT / "scripts/check-evidence.py"), str(evidence),
                       "--base", base, "--revision", revision]
            accepted = subprocess.run(checker, cwd=root, capture_output=True, text=True)
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertIn("PASS: 2 evidence row(s)", accepted.stdout)
            ticket.write_text(ticket.read_text().replace("Status: pending", "Status: done").replace(
                "Pending actual execution.", f"AC-1: unit test and CLI passed; {revision}; sidecar: ../../../../T1.json"))
            self.assertEqual(len(list(tasks.glob("*.md"))), 1)
            self.assertFalse(list(root.rglob("*.html")))
            self.assertFalse(list(root.rglob("spec.md")))
            # A post-check change must invalidate the same collected evidence.
            app.write_text(app.read_text() + "# source changed after verification\n")
            stale = subprocess.run(checker[:-1] + [identity()], cwd=root, capture_output=True, text=True)
            self.assertEqual(stale.returncode, 1)
            self.assertIn("STALE-REVISION", stale.stderr)


if __name__ == "__main__":
    unittest.main()
