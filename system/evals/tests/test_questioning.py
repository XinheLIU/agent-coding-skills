"""Questioning source/package checks and authored fixtures, never model behavior."""
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
PROTOCOL = SUITE / "protocols/questioning.md"
DEMAND = SUITE / "skills-src/plan/acs-validate-demand"
FIXTURE = SUITE / "evals/fixtures/acs-validate-demand-questioning.json"


def fixture_errors(fixture: dict) -> list[str]:
    """Check the observable round contract, without pretending to execute a skill."""
    errors = []
    candidates = {item["id"]: item for item in fixture["candidates"]}
    actions = {
        "lookup fact": {"sub-agent", "direct lookup"},
        "observable fact": {"acs-validate-prototype"},
        "mechanical decision": {"decide and record"},
        "taste decision": {"decide and show at next gate"},
        "user challenge": {"ask"},
    }
    for candidate in candidates.values():
        if candidate["action"] not in actions.get(candidate["classification"], set()) or not candidate["basis"]:
            errors.append("classifier route")
    questions = fixture["round"]
    if not 1 <= len(questions) <= 5:
        errors.append("round cap")
    if [item["number"] for item in questions] != list(range(1, len(questions) + 1)):
        errors.append("numbered block")
    for question in questions:
        candidate = candidates.get(question["id"])
        if candidate is None or candidate["action"] != "ask":
            errors.append("question classifier")
        if not set(question["prerequisites"]).issubset(fixture["settled"]):
            errors.append("unsettled premise")
        if not all(question[field] for field in ("label", "question", "recommendation", "reason")):
            errors.append("recommendation format")
        if question["yes_accepts"] != question["recommendation"]:
            errors.append("yes polarity")
    skipped = {q["id"] for q in questions} - fixture["replies"].keys()
    findings = {item["id"]: item for item in fixture["findings"]}
    for identifier in skipped:
        finding = findings.get(identifier, {})
        if finding.get("grade") != "Inferred" or not finding.get("consequence") or finding.get("disposition") not in {"assumption", "re-ask"}:
            errors.append("skipped finding")
    return errors


class QuestioningTests(unittest.TestCase):
    def test_registered_protocol_and_compatibility_aliases(self) -> None:
        registry = json.loads((SUITE / "protocols/registry.json").read_text())
        self.assertIn("questioning", registry["protocols"])
        entry = registry["protocols"]["questioning"]
        self.assertEqual(entry["id"], "protocol:acs:questioning")
        self.assertEqual(entry["canonical"], "protocols/questioning.md")
        self.assertEqual(entry["version"], "1.0.0")
        self.assertEqual(validator.validate_protocols(), [])
        for alias in (SUITE / "skills-src/plan").glob("*/references/shared-understanding.md"):
            self.assertEqual(alias.resolve(), PROTOCOL.resolve())

    def test_callers_use_canonical_protocol_without_conflicting_rules(self) -> None:
        callers = {
            "skills-src/authoring/acs-challenge-approach/SKILL.md": 1,
            "skills-src/test/review/acs-review-code-quality/SKILL.md": 1,
            "skills-src/design/ux/acs-design-interaction-flow/SKILL.md": 2,
            "skills-src/plan/acs-validate-demand/SKILL.md": 2,
            "skills-src/plan/acs-validate-demand/references/framework.md": 1,
            "skills-src/plan/acs-brainstorm/SKILL.md": 1,
            "skills-src/plan/acs-brainstorm/references/jtbd.md": 1,
        }
        for relative, minimum in callers.items():
            with self.subTest(caller=relative):
                text = (SUITE / relative).read_text()
                self.assertGreaterEqual(text.count("protocols/questioning.md"), minimum)
                self.assertNotRegex(text, r"(?i)one question at a time|one at a time|Never batch|NOT batched|never one at a time|4–5 questions|block of 4–5|Stop after each file|one issue, one")
        protocol = PROTOCOL.read_text()
        for required in ("## Classify before asking", "## Frontier rounds", "## Question blocks", "## Skipped questions are findings", "## The close", '"yes" accepts', "at most five", "acs-validate-prototype", "sub-agent", "Mechanical decision", "Taste decision", "User challenge"):
            self.assertIn(required, protocol)

    def test_authored_validate_demand_round(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not a model transcript", fixture["evidence_kind"])
        self.assertEqual(fixture["skill"], "acs-validate-demand")
        self.assertEqual(fixture_errors(fixture), [])
        self.assertEqual({q["classification"] for q in fixture["candidates"]}, {"lookup fact", "observable fact", "mechanical decision", "taste decision", "user challenge"})
        self.assertEqual(fixture["deferred"][0]["id"], "wedge")
        self.assertNotIn("wedge", {q["id"] for q in fixture["round"]})

    def test_fixture_rejects_contract_violations(self) -> None:
        original = json.loads(FIXTURE.read_text())
        mutations = {
            "round cap": lambda f: f["round"].append(copy.deepcopy(f["round"][0])),
            "question classifier": lambda f: f["candidates"][4].update(action="decide and record"),
            "classifier route": lambda f: f["candidates"][1].update(action="ask"),
            "unsettled premise": lambda f: f["round"][0].update(prerequisites=["actor"]),
            "yes polarity": lambda f: f["round"][0].update(yes_accepts="Reject recommendation"),
            "skipped finding": lambda f: f.update(findings=[]),
            "recommendation format": lambda f: f["round"][0].update(reason=""),
        }
        for expected, mutate in mutations.items():
            with self.subTest(violation=expected):
                fixture = copy.deepcopy(original)
                mutate(fixture)
                self.assertIn(expected, fixture_errors(fixture))

    def test_validate_demand_standalone_retains_protocol_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, DEMAND)
            installed = root / "installed/acs-validate-demand"
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            contract = installed / "resources/protocols/questioning.md"
            self.assertTrue(contract.is_file())
            self.assertIn("## Classify before asking", contract.read_text())
            self.assertIn("## Frontier rounds", (installed / "references/shared-understanding.md").read_text())
            self.assertIn("resources/protocols/questioning.md", (installed / "SKILL.md").read_text())
            self.assertFalse(any(p.is_symlink() for p in installed.rglob("*")))


if __name__ == "__main__":
    unittest.main()
