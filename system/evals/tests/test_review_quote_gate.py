"""Review quote-gate source contracts and authored examples, not model behavior."""
from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from test_packages import builder, validator

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
PROTOCOL = SUITE / "protocols/engineering-memory.md"
SKILLS = (
    SUITE / "skills-src/test/review/acs-review-code-quality",
    SUITE / "skills-src/design/technical/acs-trace-requirements",
)
FIXTURE = SUITE / "evals/fixtures/acs-review-quote-gate.json"
RULES = (
    "If you cannot quote the motivating line, the finding is unverified",
    "Code that handles a deliverable is not the deliverable",
)
GATE_LINK = "protocols/engineering-memory.md#review-evidence-gate"


def fixture_errors(fixture: dict) -> list[str]:
    """Validate authored outputs against the gate; does not execute the skill."""
    errors = []
    for finding in fixture["findings"]:
        result = finding["result"]
        quoted = bool(finding["quote"] and finding["source"] and finding["source_text"]
                      and finding["quote"] == finding["source_text"])
        if result["confidence"] > finding["initial_confidence"]:
            errors.append("confidence inflation")
        if not quoted:
            if result["confidence"] > 5 or result["verification"] != "unverified":
                errors.append("unquoted gate")
            if result["placement"] != "appendix" or result["blocks"]:
                errors.append("unverified promotion")
            if result["ledger_confidence"] != "LOW":
                errors.append("trace confidence")
    statuses = {"unreachable": "UNVERIFIABLE", "missing": "MISSING",
                "incomplete": "PARTIAL", "present": "REACHABLE"}
    for artifact in fixture["artifacts"]:
        if artifact["status"] != statuses[artifact["inspection"]]:
            errors.append("artifact status")
        if not artifact["evidence"] or not artifact["next_check"]:
            errors.append("artifact evidence")
    return errors


class ReviewQuoteGateTests(unittest.TestCase):
    def test_both_skills_cite_same_canonical_rules(self) -> None:
        protocol = PROTOCOL.read_text()
        self.assertIn("### Review evidence gate", protocol)
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                text = (skill / "SKILL.md").read_text()
                self.assertIn(GATE_LINK, text)
                for rule in RULES:
                    self.assertEqual(protocol.count(rule), 1)
                    self.assertEqual(text.count(rule), 1)
                self.assertIn("`UNVERIFIABLE`, not `DONE`", text)
        for required in ("never raise a lower score", "LOW", "unverified; confidence ≤ 5/10",
                         "A path, paraphrase, or unrelated quote is insufficient",
                         "A quote is necessary, not sufficient", "source revision"):
            self.assertIn(required, protocol)

    def test_review_applies_gate_before_interaction_and_retains_appendix(self) -> None:
        text = (SKILLS[0] / "SKILL.md").read_text()
        interactive = text.split("**Interactive flow.**", 1)[1].split("## Evidence identity", 1)[0]
        self.assertLess(interactive.index(GATE_LINK), interactive.index("confidence ≥ 7"))
        for required in ("protocols/questioning.md", "unverified entries", "Evidence: <verbatim",
                         "Confidence rules (the [review evidence gate]", "Unquoted: `unverified`",
                         "excluded from main findings, priorities, and blocking verdicts",
                         "A static code review cannot stand in for executed acceptance evidence"):
            self.assertIn(required, text)
        self.assertNotIn("{all findings ≥ 7 confidence", text)

    def test_trace_keeps_wiring_and_artifact_evidence_distinct(self) -> None:
        text = (SKILLS[1] / "SKILL.md").read_text()
        for status in ("REACHABLE", "PARTIAL", "MISSING", "DIVERGENT", "UNEXPECTED", "UNASSESSED", "UNVERIFIABLE"):
            self.assertIn(f"| `{status}` |", text)
        for required in ("`UNVERIFIABLE` takes precedence", "`REACHABLE` never means `DONE`",
                         "use LOW", "unverified; confidence ≤ 5/10", "outside summaries",
                         "Confirmed absence or incompleteness remains `MISSING` or `PARTIAL`",
                         "matrix still retains `UNVERIFIABLE` criteria"):
            self.assertIn(required, text)

    def test_authored_boundary_examples(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not a model transcript", fixture["evidence_kind"])
        self.assertEqual(fixture_errors(fixture), [])
        cases = {case["id"]: case for case in fixture["findings"]}
        self.assertEqual(cases["no-quote-high-confidence"]["result"]["confidence"], 5)
        self.assertEqual(cases["no-quote-low-confidence"]["result"]["confidence"], 3)
        self.assertEqual(cases["paraphrase-is-not-quote"]["result"]["verification"], "unverified")
        artifact = fixture["artifacts"][0]
        self.assertTrue(artifact["handler_exists"] and artifact["handler_tests_pass"])
        self.assertEqual(artifact["status"], "UNVERIFIABLE")

    def test_examples_reject_gate_bypasses(self) -> None:
        original = json.loads(FIXTURE.read_text())
        mutations = {
            "unquoted gate": lambda f: f["findings"][0]["result"].update(confidence=7),
            "unverified promotion": lambda f: f["findings"][0]["result"].update(placement="main", blocks=True),
            "trace confidence": lambda f: f["findings"][0]["result"].update(ledger_confidence="MEDIUM"),
            "confidence inflation": lambda f: f["findings"][1]["result"].update(confidence=5),
            "artifact status": lambda f: f["artifacts"][0].update(status="DONE"),
            "artifact evidence": lambda f: f["artifacts"][0].update(next_check=""),
        }
        for expected, mutate in mutations.items():
            with self.subTest(violation=expected):
                fixture = copy.deepcopy(original)
                mutate(fixture)
                self.assertIn(expected, fixture_errors(fixture))
        for wrong in ("REACHABLE", "MISSING", "PARTIAL"):
            fixture = copy.deepcopy(original)
            fixture["artifacts"][0]["status"] = wrong
            self.assertIn("artifact status", fixture_errors(fixture))

    def test_standalone_skills_keep_gate_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for skill in SKILLS:
                with self.subTest(skill=skill.name):
                    output = root / "export"
                    builder.build_standalone_skill(SUITE, output, skill)
                    installed = root / "installed" / skill.name
                    installed.parent.mkdir(exist_ok=True)
                    shutil.move(str(output), installed)
                    self.assertEqual(validator.validate_package(installed), [])
                    self.assertIn("resources/" + GATE_LINK, (installed / "SKILL.md").read_text())
                    self.assertEqual((installed / "resources/protocols/engineering-memory.md").read_text(),
                                     PROTOCOL.read_text())
                    self.assertFalse(any(p.is_symlink() for p in installed.rglob("*")))

    def test_provenance_names_both_sources(self) -> None:
        notice = (SUITE / "THIRD_PARTY_NOTICES.md").read_text()
        for text in (notice, PROTOCOL.read_text()):
            for source in ("review/SKILL.md", "ship/sections/plan-completion.md",
                           "35dd014c580037d1c009776d8b0584587c1bd42c"):
                self.assertIn(source, text)


if __name__ == "__main__":
    unittest.main()
