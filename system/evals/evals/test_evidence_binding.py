"""Deterministic evidence fixtures, not model or host-dispatch evaluations."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "system/skills-src/build/acs-implement/scripts/check-evidence.py"
TEMPLATE = ROOT / "system/skills-src/build/acs-implement/references/evidence-template.md"


class EvidenceBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence = {
            "base": "git:dispatch-base",
            "rows": [{"criterion": "AC-1", "command": "python3 -m unittest",
                      "revision": "sha256:completion-tree", "timestamp": "2026-10-23T07:00:00Z",
                      "result": "passed"}],
        }

    def check(self, evidence: object) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text(json.dumps(evidence))
            return subprocess.run(
                [sys.executable, str(CHECKER), str(path), "--base", "git:dispatch-base",
                 "--revision", "sha256:completion-tree"], capture_output=True, text=True)

    def test_current_completion_passes_even_when_base_differs(self) -> None:
        result = self.check(self.evidence)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: 1 evidence row", result.stdout)

    def test_stale_revision_has_named_rejection(self) -> None:
        self.evidence["rows"][0]["revision"] = self.evidence["base"]
        result = self.check(self.evidence)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("STALE-REVISION", result.stderr)

    def test_each_row_is_checked(self) -> None:
        self.evidence["rows"].append({**self.evidence["rows"][0], "revision": "old"})
        self.assertIn("row 2: STALE-REVISION", self.check(self.evidence).stderr)

    def test_missing_or_blank_binding_fields_fail(self) -> None:
        for field in ("criterion", "command", "revision", "timestamp", "result"):
            for value in (None, "", " ", 42):
                with self.subTest(field=field, value=value):
                    evidence = json.loads(json.dumps(self.evidence))
                    if value is None:
                        del evidence["rows"][0][field]
                    else:
                        evidence["rows"][0][field] = value
                    result = self.check(evidence)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("INVALID-FIELD", result.stderr)

    def test_timestamp_requires_valid_date_and_timezone(self) -> None:
        for timestamp in ("yesterday", "2026-02-30T07:00:00Z", "2026-10-23T07:00:00"):
            with self.subTest(timestamp=timestamp):
                self.evidence["rows"][0]["timestamp"] = timestamp
                self.assertIn("INVALID-TIMESTAMP", self.check(self.evidence).stderr)

    def test_offset_timestamp_is_valid(self) -> None:
        self.evidence["rows"][0]["timestamp"] = "2026-10-23T09:00:00+02:00"
        self.assertEqual(self.check(self.evidence).returncode, 0)

    def test_wrong_or_missing_base_fails(self) -> None:
        for base in (None, "other-dispatch"):
            self.evidence["base"] = base
            self.assertIn("BASE-MISMATCH", self.check(self.evidence).stderr)

    def test_empty_or_malformed_evidence_fails(self) -> None:
        for evidence in ({}, [], {"base": "git:dispatch-base", "rows": []},
                         {"base": "git:dispatch-base", "rows": ["green"]}):
            with self.subTest(evidence=evidence):
                result = self.check(evidence)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("INVALID-EVIDENCE", result.stderr)

    def test_failed_or_not_run_checks_cannot_claim_green(self) -> None:
        for result in ("failed", "not-run", "green"):
            self.evidence["rows"][0]["result"] = result
            self.assertIn("CHECK-NOT-PASSED", self.check(self.evidence).stderr)

    def test_missing_file_is_named(self) -> None:
        result = subprocess.run([sys.executable, str(CHECKER), "/nonexistent/evidence.json",
                                 "--base", "base", "--revision", "tree"],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INVALID-EVIDENCE", result.stderr)

    def test_template_example_has_complete_revision_binding(self) -> None:
        text = TEMPLATE.read_text()
        examples = text.split("```json\n")[1:]
        self.assertTrue(examples)
        for example in examples:
            evidence = json.loads(example.split("```", 1)[0])
            self.assertEqual(evidence["base"], self.evidence["base"])
            self.assertEqual(self.check(evidence).returncode, 0)


if __name__ == "__main__":
    unittest.main()
