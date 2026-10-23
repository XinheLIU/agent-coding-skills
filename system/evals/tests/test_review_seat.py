"""B7 authored contract traces, not a live scheduler or observed model review."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from test_packages import builder, load, validator

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
IMPLEMENT = SUITE / "skills-src/build/acs-implement"
SCHEMA = json.loads((IMPLEMENT / "references/state-schema.json").read_text())
EVIDENCE = load("review_evidence", IMPLEMENT / "scripts/check-evidence.py")


def package_errors(package: dict, root: Path, base: str, revision: str, inputs: str) -> list[str]:
    """Fixture oracle for package rules; actual host must resolve these inputs itself."""
    contract = SCHEMA["$defs"]["review_package"]
    if (set(package) != set(contract["required"])
            or any(not isinstance(value, str) or not value.strip() for value in package.values())):
        return ["INVALID-REVIEW-PACKAGE"]
    if (package["base"], package["revision"], package["input_revision"]) != (base, revision, inputs):
        return ["INVALID-REVIEW-PACKAGE"]
    try:
        if any(not (root / package[key]).read_text().strip()
               for key in ("brief", "acceptance_criteria", "diff")):
            return ["INVALID-REVIEW-PACKAGE"]
    except (OSError, UnicodeError):
        return ["INVALID-REVIEW-PACKAGE"]
    return []


def transition(review: dict, rounds: int, retries: int = 0, *, authorized: bool = True,
               operational_failure: bool = False, revision: str = "tree:current",
               inputs: str = "inputs:accepted") -> tuple[str, int, int, str]:
    """Authored review decision oracle, deliberately not a product runtime binding."""
    if not authorized or rounds < 0 or retries < 0:
        return "blocked", rounds, retries, "authorization/history"
    if operational_failure:
        return ("failed", rounds, retries + 1, "operational retry") if retries < 2 else (
            "blocked", rounds, retries, "retry budget")
    if (review["revision"], review["input_revision"]) != (revision, inputs):
        return "blocked", rounds, retries, "stale review"
    if review["cannot_verify"] or review["spec"] == "cannot_verify":
        return "blocked", rounds, retries, "verification gap"
    if review["spec"] == "pass" and review["quality"] == "pass":
        return "done", rounds, retries, "accepted"
    if rounds >= 5:
        return "blocked", rounds, retries, "B8 ruling"
    return "fix_round", rounds + 1, retries, "resume" if rounds < 3 else "fresh"


class ReviewSeatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = dict(brief="brief.md", acceptance_criteria="criteria.md", diff="diff.patch",
                            base="tree:base", revision="tree:current", input_revision="inputs:accepted")
        self.review = dict(spec="pass", quality="pass", cannot_verify=[],
                           revision="tree:current", input_revision="inputs:accepted")

    def test_package_positive_and_missing_empty_unreadable_stale_or_report_negative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for key in ("brief", "acceptance_criteria", "diff"):
                (root / self.package[key]).write_text(f"Accepted fixture {key}\n")
            check = lambda package: package_errors(package, root, "tree:base", "tree:current", "inputs:accepted")
            self.assertEqual(check(self.package), [])
            for key in self.package:
                for mutation in ("missing", "blank", "invalid"):
                    with self.subTest(key=key, mutation=mutation):
                        package = copy.deepcopy(self.package)
                        if mutation == "missing":
                            del package[key]
                        else:
                            package[key] = " " if mutation == "blank" else "unavailable-or-stale"
                        self.assertEqual(check(package), ["INVALID-REVIEW-PACKAGE"])
            self.assertEqual(check({**self.package, "implementer_report": "report.md"}),
                             ["INVALID-REVIEW-PACKAGE"])
            (root / "brief.md").write_text("")
            self.assertEqual(check(self.package), ["INVALID-REVIEW-PACKAGE"])

    def test_scratch_ticket_enters_review_fix_round_and_done_with_current_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "execution.json"
            ticket = {"id": "fixture", "status": "in_review", "fix_rounds_used": 0,
                      "review_package": self.package}
            path.write_text(json.dumps(ticket))
            review = {**self.review, "spec": "fail"}
            status, rounds, retries, executor = transition(review, 0)
            self.assertEqual((status, rounds, retries, executor), ("fix_round", 1, 0, "resume"))
            ticket.update(status=status, fix_rounds_used=rounds, fix_base="tree:current",
                          review_result_path="review.json")
            path.write_text(json.dumps(ticket))
            self.assertEqual(json.loads(path.read_text())["status"], "fix_round")
            ticket["status"] = "in_review"
            ticket["review_package"]["revision"] = "tree:fixed"
            evidence = {"base": "tree:base", "rows": [{"criterion": "AC-1", "command": "python3 fixture.py",
                        "result": "passed", "revision": "tree:fixed", "timestamp": "2026-10-23T12:00:00Z"}]}
            self.assertEqual(EVIDENCE.evidence_errors(evidence, base="tree:base", revision="tree:fixed"), [])
            self.assertTrue(any("STALE-REVISION" in e for e in EVIDENCE.evidence_errors(evidence, base="tree:base", revision="tree:new")))
            fixed = {**self.review, "revision": "tree:fixed"}
            self.assertEqual(transition(fixed, rounds, revision="tree:fixed")[0], "done")

    def test_five_rounds_and_operational_retries_do_not_reset_each_other(self) -> None:
        review = {**self.review, "quality": "changes_requested"}
        for rounds in range(5):
            self.assertEqual(transition(review, rounds, 1),
                             ("fix_round", rounds + 1, 1, "resume" if rounds < 3 else "fresh"))
        self.assertEqual(transition(review, 5), ("blocked", 5, 0, "B8 ruling"))
        self.assertEqual(transition(review, 4, 1, operational_failure=True), ("failed", 4, 2, "operational retry"))
        self.assertEqual(transition(review, 4, 2, operational_failure=True), ("blocked", 4, 2, "retry budget"))
        self.assertEqual(transition(review, 0, authorized=False)[0], "blocked")
        self.assertEqual(transition(review, -1)[0], "blocked")

    def test_unverifiable_and_stale_verdicts_never_complete(self) -> None:
        for field, value in (("cannot_verify", ["AC-1 needs a local run"]), ("revision", "tree:old"),
                             ("input_revision", "inputs:old")):
            self.assertEqual(transition({**self.review, field: value}, 0)[0], "blocked")
        self.assertEqual(transition({**self.review, "spec": "cannot_verify"}, 0)[0], "blocked")
        self.assertNotEqual(transition({**self.review, "spec": "fail"}, 0)[0], "done")

    def test_protocol_caller_and_schema_agree_on_gate(self) -> None:
        text = (SUITE / "protocols/orchestration.md").read_text()
        for phrase in ("review(ticket, package)", "in_review", "fix_round", "retrievable source snapshot",
                       "INVALID-REVIEW-PACKAGE", "Never pass the implementer's report", "including during re-review",
                       "Spec compliance", "Quality", "Cannot verify from the diff", "FIX_BASE",
                       "1–3 resume the implementer", "4–5 use a fresh implementer", "round 6",
                       "separate counters", "Neither counter resets the other", "coordinator never fixes code",
                       "never spawn sub-agents", "self-review cannot fill the independent review seat",
                       "Source or consumed-input changes invalidate the verdict", "acs-review-code-quality"):
            self.assertIn(phrase, text)
        caller = (IMPLEMENT / "SKILL.md").read_text()
        self.assertIn("#ticket-review-gate", caller)
        self.assertIn("review, and reclaim are the five operations", caller)
        ticket = SCHEMA["properties"]["tickets"]["items"]
        self.assertIn("in_review", ticket["properties"]["status"]["enum"])
        self.assertIn("fix_round", ticket["properties"]["status"]["enum"])
        self.assertEqual(ticket["properties"]["fix_rounds_used"]["maximum"], 5)
        self.assertEqual(ticket["allOf"][0]["then"]["required"], ["fix_rounds_used", "review_package"])
        self.assertFalse(SCHEMA["$defs"]["review_package"]["additionalProperties"])

    def test_relocated_package_retains_review_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "standalone"
            builder.build_standalone_skill(SUITE, output, IMPLEMENT)
            self.assertEqual(validator.validate_package(output), [])
            self.assertIn("## Ticket review gate", (output / "resources/protocols/orchestration.md").read_text())
            schema = json.loads((output / "references/state-schema.json").read_text())
            self.assertEqual(schema, SCHEMA)
            self.assertIn("existing authorization persists", (output / "SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
