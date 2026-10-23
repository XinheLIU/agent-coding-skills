"""B8 source/package contracts and authored traces; no observed model behavior."""
from __future__ import annotations

import copy
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from test_packages import builder, validator

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
FIXTURE = SUITE / "evals/fixtures/rulings.json"
STOP_CLASSES = {
    "Irreversible or destructive operation", "Security-sensitive action",
    "Externally visible action", "Hopeless plan",
}


def trace_errors(case: dict) -> list[str]:
    """An authored-trace oracle, not an executor or evidence of agent judgment."""
    errors = []
    decision = case["decision"]
    blocked = (decision["classification"] == "User challenge"
               or not decision["authorized"] or decision["explicit_gate"]
               or decision["stop_class"] == "Hopeless plan")
    if case["action"] != ("stop dependent work" if blocked else "continue"):
        errors.append("authorization stop")
    ruling = case.get("ruling")
    if not blocked:
        if not ruling or not re.fullmatch(r"Ruling: .+ — .+ — .+", ruling["text"]):
            errors.append("missing ruling")
        elif (not ruling["recovery_entry"] or not ruling["revision"]
              or ruling["classification"] != decision["classification"]):
            errors.append("ruling provenance")
        if decision["classification"] == "Taste decision" and not case["review_due"]:
            errors.append("taste review")
    if ruling and ruling["consequential"] and not ruling["persistent_reference"]:
        errors.append("missing promotion")
    envelope = case["handoff"]
    if "rulings_made" not in envelope or envelope["rulings_made"] != ([ruling] if ruling else []):
        errors.append("handoff rulings")
    attempts = case["attempts"]
    limit = case["retry_limit"]
    if not 0 <= limit <= 2 or len(attempts) > limit + 1:
        errors.append("retry budget")
    if blocked and attempts:
        errors.append("attempt after stop")
    for index, attempt in enumerate(attempts):
        if attempt["retries_used"] != index:
            errors.append("retry counter")
        if not attempt["revision"] or not attempt["evidence"]:
            errors.append("attempt evidence")
        if index:
            previous = attempts[index - 1]
            if (previous["result"] != "failed" or previous["stop_reason"]
                    or not attempt["correction"] or not attempt["recorded_before_retry"]):
                errors.append("unsafe retry")
    if attempts and attempts[-1]["result"] == "failed":
        if not case["stop_reason"] or not case["dependents_blocked"]:
            errors.append("failure disposition")
        if len(attempts) == limit + 1 and case["stop_reason"] != "budget exhausted":
            errors.append("budget disposition")
    return errors


class RulingsTests(unittest.TestCase):
    def test_taxonomy_rulings_and_stop_classes_preserve_authorization(self) -> None:
        text = (SUITE / "protocols/context-coordination.md").read_text()
        section = text.split("## Execution-time rulings\n", 1)[1].split("## Transition", 1)[0]
        for phrase in ("questioning.md#classify-before-asking", "Mechanical decision", "Taste decision",
                       "User challenge", "Ruling: <what> — <why> — <cost if wrong>",
                       "single configured recovery entry", "Persistent Changes", "next existing review gate",
                       "block only dependent work", "explicit user gates", "missing required capabilities",
                       "do not ask again", "grants no authority", "5bf4e78", "35dd014"):
            self.assertIn(phrase, section)
        stop_table = section.split("| Stop class |", 1)[1].split("\n\n", 1)[0]
        actual = {line.split("|")[1].strip() for line in stop_table.splitlines()
                  if line.startswith("| ") and not line.startswith("| ---")}
        self.assertEqual(actual, STOP_CLASSES)
        self.assertEqual(stop_table.count("if missing or insufficient, stop and ask before acting"), 3)
        self.assertIn("No workflow automatically authorizes sending messages, installing dependencies, committing, publishing, or deploying.", text)

    def test_bounded_retry_contract_and_caller(self) -> None:
        text = (SUITE / "protocols/orchestration.md").read_text()
        section = text.split("## Failure policy\n", 1)[1].split("## Handoff", 1)[0]
        for phrase in ("two autonomous retries per ticket", "three attempts total", "stricter existing budget wins",
                       "retries_used: 0", "Before each retry, increment and persist", "does not reset",
                       "prior counts cannot be recovered", "pending authorization or user challenge",
                       "explicit gate", "four stop classes", "hopeless plan", "missing required capability",
                       "no evidence-backed correction", "Stop at budget exhaustion", "unknown outcome",
                       "immutable BASE", "fresh evidence", "never weakens criteria, tests, or verification gates",
                       "Preserve earlier attempt history"):
            self.assertIn(phrase, section)
        caller = (SUITE / "skills-src/build/acs-implement/SKILL.md").read_text()
        self.assertIn("orchestration-protocol.md#failure-policy", caller)
        self.assertIn("Rulings made", caller)
        self.assertNotIn("the user retries specific tickets", caller + text)

    def test_shared_envelope_schema_and_section_list(self) -> None:
        text = (SUITE / "protocols/skill-declarations.md").read_text()
        section = text.split("## Handoff envelope\n", 1)[1].split("## Coordinated", 1)[0]
        schema = section.split("```text\n", 1)[1].split("```", 1)[0]
        self.assertIn("Rulings made: [Ruling: <what> — <why> — <cost if wrong>; record reference + review due]", schema)
        self.assertIn("use an empty list when no rulings were made", section)
        self.assertIn("not an accepted decision unless acceptance is recorded", section)
        self.assertIn("Rulings made", (SUITE / "protocols/orchestration.md").read_text().split("## Handoff envelope", 1)[1])

    def test_authored_fixture_cases(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not observed model behavior", fixture["evidence_kind"])
        self.assertEqual({c["id"] for c in fixture["cases"]}, {
            "taste-continues", "mechanical-retry-succeeds", "retry-exhausted", "retry-hopeless",
            "destructive-stop", "security-stop", "external-stop", "hopeless-stop",
            "user-challenge-stop", "explicit-gate-stop", "authorized-destructive-continues",
        })
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(trace_errors(case), [])

    def test_mutations_reject_missing_rulings_unauthorized_work_and_unbounded_retries(self) -> None:
        cases = {c["id"]: c for c in json.loads(FIXTURE.read_text())["cases"]}
        mutations = [
            ("taste-continues", "missing ruling", lambda c: c.update(ruling=None)),
            ("taste-continues", "taste review", lambda c: c.update(review_due=False)),
            ("taste-continues", "missing promotion", lambda c: c["ruling"].update(persistent_reference="")),
            ("taste-continues", "handoff rulings", lambda c: c["handoff"].update(rulings_made=[])),
            ("destructive-stop", "authorization stop", lambda c: c.update(action="continue")),
            ("user-challenge-stop", "authorization stop", lambda c: c.update(action="continue")),
            ("explicit-gate-stop", "authorization stop", lambda c: c.update(action="continue")),
            ("retry-exhausted", "retry budget", lambda c: c["attempts"].append(copy.deepcopy(c["attempts"][-1]))),
            ("mechanical-retry-succeeds", "retry counter", lambda c: c["attempts"][1].update(retries_used=0)),
            ("mechanical-retry-succeeds", "unsafe retry", lambda c: c["attempts"][1].update(recorded_before_retry=False)),
            ("mechanical-retry-succeeds", "unsafe retry", lambda c: c["attempts"][0].update(stop_reason="missing required capability")),
        ]
        for name, expected, mutate in mutations:
            with self.subTest(case=name, violation=expected):
                case = copy.deepcopy(cases[name])
                mutate(case)
                self.assertIn(expected, trace_errors(case))

    def test_relocated_implement_preserves_rulings_retries_and_shared_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, SUITE / "skills-src/build/acs-implement")
            installed = root / "installed/acs-implement"
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            protocols = installed / "resources/protocols"
            self.assertIn("## Execution-time rulings", (protocols / "context-coordination.md").read_text())
            self.assertIn("two autonomous retries per ticket", (protocols / "orchestration.md").read_text())
            self.assertIn("Rulings made", (protocols / "skill-declarations.md").read_text())
            source = (SUITE / "skills-src/build/acs-implement/SKILL.md").read_text()
            packaged = (installed / "SKILL.md").read_text()
            self.assertEqual(source.count("[Shared semantics]("), 1)
            self.assertEqual(packaged.count("Shared semantics:"), 1)
            self.assertIn("existing authorization persists", packaged)
            self.assertIn("resources/protocols/skill-declarations.md", packaged)


if __name__ == "__main__":
    unittest.main()
