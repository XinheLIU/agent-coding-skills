"""acs-shape-solution authored scope fixtures and source/package checks, not model runs."""
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
SHAPE = SUITE / "skills-src/plan/acs-shape-solution"
FIXTURE = SUITE / "evals/fixtures/acs-shape-solution-scope-postures.json"
POSTURES = {"Expansion", "Selective expansion", "Hold", "Reduction"}


def fixture_errors(case: dict) -> list[str]:
    """Check authored boundary examples; this does not execute skill instructions."""
    errors = []
    record = case["record"]
    if case["posture"] not in POSTURES or record.get("Scope posture") != case["posture"] or not case["basis"]:
        errors.append("posture record")
    exclusions = record.get("NOT in scope", "")
    if not exclusions:
        errors.append("exclusion record")
    accepted = set(case["baseline"])
    for change in case["changes"]:
        operation, disposition = change["operation"], change["disposition"]
        if operation not in {"add", "remove"} or disposition not in {"approved", "rejected", "deferred", "pending"}:
            errors.append("invalid change")
            continue
        if case["posture"] == "Hold":
            errors.append("hold drift")
        if case["posture"] == "Reduction" and operation == "add":
            errors.append("reduction drift")
        if disposition == "approved":
            if not change["approval"]:
                errors.append("missing opt-in")
            if operation == "add":
                accepted.add(change["item"])
            else:
                accepted.discard(change["item"])
        excluded = (operation == "add" and disposition in {"rejected", "deferred"}) or (operation == "remove" and disposition == "approved")
        if excluded and (change["item"] not in exclusions or not change["reason"]):
            errors.append("missing exclusion")
    if accepted != set(case["accepted_scope"]):
        errors.append("silent scope change")
    return errors


class ScopePostureTests(unittest.TestCase):
    def test_phase_c_defines_postures_and_record_contract(self) -> None:
        text = (SHAPE / "SKILL.md").read_text()
        phase = text.split("## Phase C —", 1)[1].split("## Phase C2", 1)[0]
        for posture in POSTURES:
            self.assertIn(f"**{posture}**", phase)
        for required in (
            "### Scope postures", "[Expansion posture](#scope-postures)",
            "Raise concerns once", "Every addition or removal requires explicit user opt-in",
            "Reuse existing explicit approval", "skipped or unanswered choice is pending",
            "Scope posture:", "NOT in scope:", "scope-decisions", "discovery.html",
            "Return this record's anchor", "2–3 distinct options",
        ):
            self.assertIn(required, phase)
        self.assertNotIn("Expand posture", text)
        self.assertNotIn("Boil the Ocean", text)

    def test_authored_cases_cover_all_four_postures(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not a model transcript", fixture["evidence_kind"])
        self.assertEqual(fixture["skill"], "acs-shape-solution")
        self.assertEqual({case["posture"] for case in fixture["cases"]}, POSTURES)
        for case in fixture["cases"]:
            with self.subTest(posture=case["posture"]):
                self.assertEqual(fixture_errors(case), [])

    def test_fixtures_reject_unapproved_changes_and_missing_records(self) -> None:
        cases = json.loads(FIXTURE.read_text())["cases"]
        mutations = [
            (0, "missing opt-in", lambda c: c["changes"][0].update(approval=None)),
            (0, "missing exclusion", lambda c: c["record"].update({"NOT in scope": "none recorded"})),
            (1, "silent scope change", lambda c: c["accepted_scope"].append("team dashboard")),
            (2, "posture record", lambda c: c["record"].pop("Scope posture")),
            (2, "exclusion record", lambda c: c["record"].pop("NOT in scope")),
            (3, "silent scope change", lambda c: c["accepted_scope"].remove("CSV export")),
        ]
        for index, error, mutate in mutations:
            with self.subTest(violation=error, case=index):
                case = copy.deepcopy(cases[index])
                mutate(case)
                self.assertIn(error, fixture_errors(case))

    def test_notice_names_pinned_source_and_landing_anchor(self) -> None:
        notice = (SUITE / "THIRD_PARTY_NOTICES.md").read_text()
        self.assertIn("plan-ceo-review/SKILL.md.tmpl", notice)
        self.assertIn("35dd014c580037d1c009776d8b0584587c1bd42c", notice)
        self.assertIn("skills-src/plan/acs-shape-solution/SKILL.md#scope-postures", notice)
        self.assertNotIn("have no current home", notice)

    def test_shape_solution_standalone_retains_postures_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, SHAPE)
            installed = root / "installed/acs-shape-solution"
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            text = (installed / "SKILL.md").read_text()
            self.assertIn("### Scope postures", text)
            self.assertIn("[Expansion posture](#scope-postures)", text)
            self.assertIn("NOT in scope:", text)
            self.assertFalse(any(p.is_symlink() for p in installed.rglob("*")))


if __name__ == "__main__":
    unittest.main()
