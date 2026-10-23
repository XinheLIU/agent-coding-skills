"""Security rubric source contracts and authored cases, not observed model behavior."""
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
SKILL = SUITE / "skills-src/test/review/acs-review-code-quality"
FIXTURE = SUITE / "evals/fixtures/acs-security-evidence.json"
PARTS = {"entrypoint", "boundary_crossing", "demonstrated_impact"}
# Mandatory rules remain in SKILL.md; the compaction test checks this same set
# in source and packaged prefixes. Formatting and provenance may live locally.
SECURITY_CORE_RULES = (
    "security claims from every lens, including auth and db",
    "neither severity, a scanner warning, nor reviewer agreement proves a claim",
    "P0/P1/P2 with concrete impact and realistic attacker prerequisites",
    "label hypothetical impact as conditional",
    "A pattern or advisory score alone is insufficient",
    "N/10 with rationale, unknowns and counterevidence",
    "do not raise confidence merely because severity is high",
    "Unquoted claims remain unverified at ≤ 5/10",
    "Static tracing never proves runtime execution or a tested repair",
    "including an unresolved candidate",
    "source revisions and inspected quotes",
    "explicitly records `unknown` and the next check",
    "**Entrypoint:**", "attacker-controlled input, caller and prerequisites",
    "Trust follows who wrote a value, including environment, job and model inputs",
    "**Boundary crossing:**", "its invariant and relevant protective controls",
    "**Demonstrated impact:**", "specific unauthorized effect and its evidence",
    "actual command, environment and observed security assertion with a legitimate control",
    "`candidate` means one or more parts or relevant control checks remain unresolved",
    "`supported-static` requires all three parts and inspection of relevant controls",
    "`supported-reproduced` additionally requires recorded execution evidence",
    "`disproved` requires concrete counterevidence defeating the scoped claim",
    "disposition evidence, not a vulnerability",
    "Unknown reachability remains unknown, not unreachable",
    "Record reachability separately as `reachable`, `unknown`, or `unreachable`",
    "only inspected evidence ruling out the path in the stated scope permits `unreachable`",
    "Missing hardening alone needs a concrete failure scenario",
    "candidates and disproved claims in separate appendix subsections",
    "outside supported totals, priorities and blocking verdicts",
    "Supported findings still obey the quote gate and existing confidence/axis rules",
    "`supported` never means a repair passed or the review is complete",
    "When an authorized independent reviewer is available",
    "only a neutral ID, scope/revision, locations and source evidence, boundary invariant, environment assumptions and this rubric",
    "Withhold the producer's conclusion, severity, confidence, evidence-state label and proposed fix until the challenger records its own assessment",
    "inspect callers, middleware, configuration, validation, legitimate behavior and mitigations",
    "Preserve the exact input and response, dissent, assumptions and reconciliation",
    "reconcile against evidence, never by vote",
    "sequential challenge; independent reviewer unavailable",
    "retain that limitation",
    "Do not expand access or claim an independent transcript from a self-review or authored example",
)


def fixture_errors(fixture: dict) -> list[str]:
    """Check authored examples for inconsistent claims; does not run the skill."""
    errors = []
    for finding in fixture["findings"]:
        evidence = finding["evidence"]
        if set(evidence) != PARTS:
            errors.append("missing evidence part")
            continue
        if any(not part["detail"] for part in evidence.values()):
            errors.append("missing evidence detail")
        for part in evidence.values():
            if part["status"] in {"shown", "refuted"} and not (part["source"] and part["quote"]):
                errors.append("missing quote")
        supported = finding["evidence_state"].startswith("supported-")
        if supported and (any(part["status"] != "shown" for part in evidence.values())
                          or not finding["controls"] or finding["reachability"] != "reachable"):
            errors.append("unsupported promotion")
        if finding["evidence_state"] == "supported-reproduced":
            record = finding["reproduction"] or {}
            if not all(record.get(key) for key in ("command", "environment", "security_assertion", "legitimate_control")):
                errors.append("missing reproduction evidence")
        if finding["reachability"] == "unreachable" or finding["evidence_state"] == "disproved":
            if not any(part["status"] == "refuted" for part in evidence.values()):
                errors.append("unknown treated as disproved")
        if finding["placement"] == "main" and not supported:
            errors.append("candidate promoted to main")
        if not (finding["severity"] in {"P0", "P1", "P2"}
                and 0 <= finding["confidence"] <= 10
                and finding["severity_rationale"] and finding["confidence_rationale"]):
            errors.append("missing separate judgments")
    exchange = fixture["challenger_exchange"]
    allowed = {"neutral_id", "scope_revision", "locations", "source_evidence", "invariant",
               "environment_assumptions", "rubric"}
    if set(exchange["input"]) != allowed:
        errors.append("challenger input leak")
    if exchange["producer_private"]["conclusion"] in json.dumps(exchange["input"]):
        errors.append("challenger input leak")
    return errors


class SecurityEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = json.loads(FIXTURE.read_text())

    def test_rubric_and_finding_format_keep_three_judgments_and_parts(self) -> None:
        text = (SKILL / "SKILL.md").read_text()
        rubric = text.split("### Security evidence rubric", 1)[1].split("## Consolidation", 1)[0]
        for field in ("Severity", "Confidence", "Evidence state"):
            self.assertIn(f"| {field} |", rubric)
        formats = (SKILL / "references/review-formats.md").read_text()
        self.assertIn("references/review-formats.md", text)
        for field in ("Severity", "Confidence rationale", "Evidence state", "Entrypoint",
                      "Boundary crossing", "Demonstrated impact", "Reachability", "Challenge"):
            self.assertIn(f"  {field}:", formats)
        for rule in SECURITY_CORE_RULES:
            self.assertIn(rule, rubric)

    def test_existing_gates_and_lens_routing_remain(self) -> None:
        text = (SKILL / "SKILL.md").read_text()
        for required in ("docs/shared-semantics.md#execution", "protocols/questioning.md",
                         "protocols/engineering-memory.md#review-evidence-gate",
                         "If you cannot quote the motivating line, the finding is unverified",
                         "Code that handles a deliverable is not the deliverable",
                         "Standards and Spec separate", "never reranked together",
                         "Route design-level issues to separate ARC/MOD/CON/TST cross-references, never code findings",
                         "authn/authz architecture → ARC/CON"):
            self.assertIn(required, text)
        formats = (SKILL / "references/review-formats.md").read_text()
        for required in ("Authn/authz architecture (trust boundaries, role topology) | — | ARC / CON",
                         "Standards and Spec findings stay in separate subsections"):
            self.assertIn(required, formats)
        lens = (SKILL / "references/domain-lenses.md").read_text()
        self.assertIn("../SKILL.md#security-evidence-rubric", lens)
        self.assertIn("security claims from any lens, including auth and db", lens)
        self.assertIn("review evidence gate takes precedence", lens)

    def test_five_authored_cases_classify_consistently(self) -> None:
        self.assertEqual(fixture_errors(self.fixture), [])
        cases = self.fixture["findings"]
        self.assertEqual(len(cases), 5)
        self.assertEqual([case["evidence_state"] for case in cases], [
            "supported-static", "supported-reproduced", "candidate", "disproved", "candidate",
        ])
        self.assertEqual(cases[2]["reachability"], "unknown")
        self.assertEqual(cases[2]["severity"], "P0")
        self.assertEqual(cases[2]["placement"], "appendix")
        self.assertFalse(cases[1]["reproduction"]["observed"])
        self.assertIn("not a model transcript", self.fixture["evidence_kind"])

    def test_missing_evidence_cannot_be_promoted(self) -> None:
        for part in PARTS:
            fixture = copy.deepcopy(self.fixture)
            fixture["findings"][0]["evidence"].pop(part)
            self.assertIn("missing evidence part", fixture_errors(fixture))
            fixture = copy.deepcopy(self.fixture)
            fixture["findings"][0]["evidence"][part]["status"] = "unknown"
            self.assertIn("unsupported promotion", fixture_errors(fixture))
        for key in ("command", "environment", "security_assertion", "legitimate_control"):
            fixture = copy.deepcopy(self.fixture)
            fixture["findings"][1]["reproduction"].pop(key)
            self.assertIn("missing reproduction evidence", fixture_errors(fixture))

    def test_rejects_unknown_reachability_and_reporting_bypasses(self) -> None:
        mutations = {
            "unknown treated as disproved": lambda f: f["findings"][2].update(reachability="unreachable", evidence_state="disproved"),
            "unsupported promotion": lambda f: f["findings"][2].update(evidence_state="supported-static"),
            "candidate promoted to main": lambda f: f["findings"][2].update(placement="main"),
            "missing quote": lambda f: f["findings"][0]["evidence"]["entrypoint"].update(quote=None),
            "missing separate judgments": lambda f: f["findings"][0].update(confidence_rationale=""),
        }
        for expected, mutate in mutations.items():
            with self.subTest(violation=expected):
                fixture = copy.deepcopy(self.fixture)
                mutate(fixture)
                self.assertIn(expected, fixture_errors(fixture))

    def test_authored_challenger_receives_evidence_without_conclusion(self) -> None:
        exchange = self.fixture["challenger_exchange"]
        self.assertIn("no independent model was invoked", exchange["evidence_kind"])
        self.assertEqual(exchange["input"]["source_evidence"]["parts"], self.fixture["findings"][2]["evidence"])
        self.assertEqual(exchange["response"]["evidence_state"], "candidate")
        self.assertEqual(exchange["response"]["reachability"], "unknown")
        self.assertTrue(exchange["response"]["counterevidence"] and exchange["reconciliation"])
        for field, value in exchange["producer_private"].items():
            fixture = copy.deepcopy(self.fixture)
            fixture["challenger_exchange"]["input"][field] = value
            self.assertIn("challenger input leak", fixture_errors(fixture))
        fixture = copy.deepcopy(self.fixture)
        fixture["challenger_exchange"]["input"]["rubric"] += exchange["producer_private"]["conclusion"]
        self.assertIn("challenger input leak", fixture_errors(fixture))

    def test_provenance_is_pinned_in_linked_formats(self) -> None:
        self.assertIn("[format and provenance](references/review-formats.md)",
                      (SKILL / "SKILL.md").read_text())
        text = (SKILL / "references/review-formats.md").read_text()
        self.assertIn("35dd014c580037d1c009776d8b0584587c1bd42c/cso/SKILL.md.tmpl", text)
        self.assertIn("aeac41d/skills/security-and-hardening/SKILL.md", text)

    def test_standalone_relocation_preserves_rubric_links_and_shared_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, SKILL)
            installed = root / "installed" / SKILL.name
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            text = (installed / "SKILL.md").read_text()
            self.assertIn("### Security evidence rubric", text)
            for rule in SECURITY_CORE_RULES:
                self.assertIn(rule, text)
            self.assertIn("  Challenge:", (installed / "references/review-formats.md").read_text())
            self.assertIn("Shared semantics: [shared protocol](resources/protocols/skill-declarations.md", text)
            self.assertIn("shared execution: [Coordination](resources/protocols/context-coordination.md)", text)
            self.assertNotIn("docs/shared-semantics.md#execution", text)
            self.assertIn("../SKILL.md#security-evidence-rubric", (installed / "references/domain-lenses.md").read_text())
            self.assertFalse(any(path.is_symlink() for path in installed.rglob("*")))


if __name__ == "__main__":
    unittest.main()
