"""B10 package contracts and local rehearsals; no agent/provider behavior claim."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from test_packages import builder, validator

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
DEPLOY = SUITE / "skills-src/deploy"
CHECKER = SUITE / "skills-src/build/acs-implement/scripts/check-evidence.py"
FIXTURE = SUITE / "evals/fixtures/acs-release-tail.json"


def trace_errors(kind: str, events: list[dict]) -> list[str]:
    """Validate authored scenario expectations, never simulate agent compliance."""
    if kind == "merge_error":
        if [event["action"] for event in events] != [
            "merge_error", "read_server_state", "bind_merged_revision"
        ]:
            return ["merge error must read state without retry"]
        if events[1].get("state") != "merged" or not events[1].get("revision"):
            return ["unconfirmed merge must block"]
        if events[2].get("revision") != events[1]["revision"]:
            return ["wrong merged revision"]
    elif kind == "dry_run":
        if any(event.get("mutating") or event["action"] not in {
            "read_configuration", "preview", "record_outcome"
        } for event in events):
            return ["dry run must not mutate"]
        if not events or events[-1].get("outcome") != "not released":
            return ["dry run must record not released"]
    elif kind == "canary":
        prior = None
        count = 0
        for event in events:
            key = (event.get("artifact"), event.get("environment"), event.get("pattern"))
            if not event.get("valid") or not event.get("pattern"):
                prior, count = None, 0
            else:
                count = count + 1 if prior == key else 1
                prior = key
            if event.get("alert") != (count >= 2):
                return ["alert requires two consecutive valid matching checks"]
    return []


def configuration_errors(configuration: dict) -> list[str]:
    """Fixture admission guard: missing consumer settings cannot run the rehearsal."""
    return [f"unset {key}" for key in ("commands", "environment")
            if not configuration.get(key)]


class ReleaseTailTests(unittest.TestCase):
    def test_discovery_catalog_and_plugin_mapping(self) -> None:
        catalog = json.loads((ROOT / "catalog/skill-set.json").read_text())
        category = next(row for row in catalog["categories"] if row["id"] == "deploy")
        self.assertEqual(category["skills"], ["acs-ship", "acs-release"])
        self.assertEqual(builder.CATEGORY_TO_PLUGIN["deploy"], "acs-deploy")
        for name in category["skills"]:
            self.assertEqual((SUITE / "skills" / name).resolve(), DEPLOY / name)

    def test_skill_hard_rules_and_source_compaction(self) -> None:
        required = {
            "acs-ship": ["Rerun verification every invocation", "at most three review fix rounds",
                         "converged: false", "Only actions are idempotent", "Stop list",
                         "Never-stop list", "operational retries", "--base", "--revision",
                         "PR not opened", "Unset commands or environments block execution"],
            "acs-release": ["never retry the merge", "First-use dry run", "not released",
                            "A rebuilt artifact cannot inherit verification", "two consecutive valid checks",
                            "exhausted freezes feature releases", "Missing budget/policy blocks",
                            "never delays a configured immediate safety stop", "--base", "--revision",
                            "Unset commands or environments block execution"],
        }
        for name, phrases in required.items():
            text = (DEPLOY / name / "SKILL.md").read_text()
            for phrase in phrases:
                self.assertIn(phrase, text)
            self.assertLessEqual(len(text.encode()), 5000)
            self.assertTrue(text.rstrip().endswith("<!-- compaction-core:end -->"))

    def test_relocated_skills_keep_checker_templates_and_shared_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for name in ("acs-ship", "acs-release"):
                exported = Path(temporary) / (name + "-export")
                builder.build_standalone_skill(SUITE, exported, DEPLOY / name)
                installed = Path(temporary) / name
                exported.rename(installed)
                self.assertEqual(validator.validate_package(installed), [])
                text = (installed / "SKILL.md").read_text()
                self.assertIn("existing authorization persists", text)
                self.assertNotIn("[Shared semantics]", text)
                # Token-independent conservative byte cap includes injected semantics.
                self.assertLessEqual(len(text.encode()), 5000)
                checker_link = re.search(r"\]\(([^)]+check-evidence.py)\)", text)
                self.assertIsNotNone(checker_link)
                checker = installed / checker_link[1]
                result = subprocess.run([sys.executable, str(checker), "--help"],
                                        capture_output=True, text=True, cwd=installed)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("--revision", result.stdout)
                self.assertFalse(any(p.is_symlink() for p in installed.rglob("*")))

    def test_authored_traces_and_negative_mutations(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not model transcripts", fixture["evidence_kind"])
        for kind in ("merge_error", "dry_run", "canary"):
            self.assertEqual(trace_errors(kind, fixture[kind]), [])
        retry = copy.deepcopy(fixture["merge_error"])
        retry.insert(1, {"action": "merge"})
        self.assertTrue(trace_errors("merge_error", retry))
        for state in ("open", "unknown"):
            events = copy.deepcopy(fixture["merge_error"])
            events[1]["state"] = state
            self.assertEqual(trace_errors("merge_error", events), ["unconfirmed merge must block"])
        events = copy.deepcopy(fixture["merge_error"])
        events[2]["revision"] = "old-head"
        self.assertTrue(trace_errors("merge_error", events))
        for action in ("deploy", "merge", "create_pr", "migrate", "set_flag", "rollback"):
            events = copy.deepcopy(fixture["dry_run"])
            events.insert(1, {"action": action})
            self.assertTrue(trace_errors("dry_run", events))
        events = copy.deepcopy(fixture["dry_run"])
        events[-1]["outcome"] = "released"
        self.assertTrue(trace_errors("dry_run", events))
        for index in (0, 2, 4, 5):
            events = copy.deepcopy(fixture["canary"])
            events[index]["alert"] = True
            self.assertTrue(trace_errors("canary", events))

    def test_local_scratch_branch_pr_body_and_current_evidence(self) -> None:
        # Actual local command execution on an unborn scratch branch; no commit,
        # network, PR write or agent invocation. This rehearses the evidence path.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", "--initial-branch=b10-ship-fixture", str(root)], check=True)
            branch = subprocess.check_output(["git", "-C", str(root), "branch", "--show-current"], text=True).strip()
            self.assertEqual(branch, "b10-ship-fixture")
            source = root / "check.py"
            source.write_text("print('fixture criterion passed')\n")
            command = [sys.executable, "check.py"]
            config = {"commands": [command], "environment": "local-scratch/config-v1"}
            self.assertEqual(configuration_errors(config), [])
            for key in config:
                missing = dict(config)
                missing[key] = [] if key == "commands" else ""
                self.assertEqual(configuration_errors(missing), [f"unset {key}"])
            revision = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            rows = []
            for _ in range(2):  # Existing action state must not suppress verification.
                result = subprocess.run(command, cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout.strip(), "fixture criterion passed")
                rows.append({"criterion": "fixture-local-check", "command": " ".join(command),
                             "revision": revision, "timestamp": datetime.now(timezone.utc).isoformat(),
                             "result": "passed"})
            evidence = root / "evidence.json"
            evidence.write_text(json.dumps({"base": "unborn-fixture-base", "rows": rows}))
            check = [sys.executable, str(CHECKER), str(evidence), "--base", "unborn-fixture-base", "--revision", revision]
            result = subprocess.run(check, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            body = (DEPLOY / "acs-ship/references/pr-body.md").read_text().split("```markdown\n")[1].split("```")[0]
            replacements = {
                "Concrete trigger and resulting behavior; canonical change/ticket reference": "B10 local rehearsal: verify fixture before PR preparation",
                "Observed problem": "No current local evidence", "Verified result": "Two local checks passed",
                "current full tree fingerprint and branch revision": revision + "; unborn " + branch,
                "target branch and revision": "fixture-only; no remote", "immutable dispatch identity": "unborn-fixture-base",
                "identity and revision": config["environment"], "ID": rows[0]["criterion"],
                "executed command": rows[0]["command"], "tested fingerprint": revision,
                "RFC3339": rows[-1]["timestamp"], "observed result and retained reference": "passed; evidence.json",
                "current review reference": "authored fixture only; agent review unverified", "true/false": "false",
                "used": "0", "policy cap": "3", "required gates and current results": "local check passed; external CI unavailable",
                "none or blocking effect": "no external authorization; PR blocked",
                "low / elevated / blocked, with reason; migration, compatibility, rollout and rollback implications": "blocked: local rehearsal only; production unverified",
                "Unverified behavior and unresolved decisions; do not infer deploy readiness from PR readiness": "PR not opened; not released",
            }
            for key, value in replacements.items():
                body = body.replace("<" + key + ">", value)
            self.assertNotRegex(body, r"<[^>]+>")
            (root / "pr-body.md").write_text(body)
            for phrase in ("## Merge danger", "## Stop lists", revision, "PR not opened"):
                self.assertIn(phrase, body)
            source.write_text("print('changed after verification')\n")
            changed = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            result = subprocess.run(check[:-1] + [changed], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("STALE-REVISION", result.stderr)
            self.assertEqual(subprocess.check_output(["git", "-C", str(root), "diff", "--cached", "--name-only"]), b"")


if __name__ == "__main__":
    unittest.main()
