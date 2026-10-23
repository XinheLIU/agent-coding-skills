"""Deterministic catalog fixtures; these do not measure model invocation behavior."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_suite import catalog_budget_errors

VALIDATOR = Path(__file__).resolve().parents[1] / "validate_suite.py"


class CatalogBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.suite = Path(self.temporary.name) / "system"

    def skill(self, description: str, *, name: str = "acs-example", fields: str = "") -> Path:
        path = self.suite / "skills-src" / "test" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\ndescription: {description}\n{fields}---\n", encoding="utf-8")
        return path

    def test_exact_single_description_byte_boundary(self) -> None:
        self.skill("Use when " + "x" * 251)
        self.assertEqual(catalog_budget_errors(self.suite), [])
        self.skill("Use when " + "x" * 252)
        self.assertTrue(any("261 bytes; limit is 260" in e for e in catalog_budget_errors(self.suite)))

    def test_counts_utf8_bytes_not_characters(self) -> None:
        self.skill("Use when " + "é" * 126)
        self.assertTrue(any("261 bytes; limit is 260" in e for e in catalog_budget_errors(self.suite)))

    def test_exact_total_byte_boundary(self) -> None:
        for index in range(20):
            self.skill("Use when " + "x" * 241, name=f"acs-example-{index}")
        self.assertEqual(catalog_budget_errors(self.suite), [])
        self.skill("Use when " + "x" * 242, name="acs-example-0")
        self.assertEqual(catalog_budget_errors(self.suite), [
            "catalog: model-invocable descriptions total 5001 bytes; limit is 5000",
        ])

    def test_only_explicitly_disabled_skills_are_exempt(self) -> None:
        self.skill("Workflow: " + "x" * 6000, fields="disable-model-invocation: true\n")
        self.assertEqual(catalog_budget_errors(self.suite), [])
        self.skill("Use when " + "x" * 291, fields="disable-model-invocation: false\n")
        self.assertTrue(any("300 bytes; limit is 260" in e for e in catalog_budget_errors(self.suite)))

    def test_invalid_invocation_flag_cannot_bypass_budget(self) -> None:
        for flag in ['"true"', "yes", "true\ndisable-model-invocation: false"]:
            with self.subTest(flag=flag):
                self.skill("Use when needed.", fields=f"disable-model-invocation: {flag}\n")
                self.assertTrue(any("literal boolean" in e for e in catalog_budget_errors(self.suite)))

    def test_body_and_discovery_aliases_do_not_consume_budget(self) -> None:
        path = self.skill("Use when context is missing.")
        path.write_text(path.read_text() + "\nWorkflow: " + "x" * 6000)
        (self.suite / "skills").mkdir()
        (self.suite / "skills/acs-example").symlink_to(path.parent)
        self.assertEqual(catalog_budget_errors(self.suite), [])

    def test_supported_scalar_forms_are_decoded_before_counting(self) -> None:
        description = "Use when " + "é" * 125
        for scalar in [description, json.dumps(description), "'" + description + "'",
                       ">\n  Use when\n  " + "é" * 125, "|-\n  " + description]:
            with self.subTest(scalar=scalar):
                self.skill(scalar)
                self.assertEqual(catalog_budget_errors(self.suite), [])

    def test_invalid_or_duplicate_descriptions_fail_closed(self) -> None:
        for scalar in ['"unclosed', "*alias", "", "Use when needed.\ndescription: Use when repeated."]:
            with self.subTest(scalar=scalar):
                self.skill(scalar)
                self.assertTrue(catalog_budget_errors(self.suite))

    def test_use_when_prefix_is_required(self) -> None:
        self.skill("Audit a codebase for production readiness.")
        self.assertTrue(any("must start with" in e for e in catalog_budget_errors(self.suite)))

    def test_workflow_shortcuts_are_rejected_even_with_trigger_prefix(self) -> None:
        for description in [
            "Use when reviewing code; then write findings.",
            "Use when reviewing code. Produces a merge verdict.",
            "Use when reviewing code. Run tests and write findings.",
            "Use when reviewing code; this skill applies seven lenses.",
            "Use when reviewing code: inspect → test → report.",
        ]:
            with self.subTest(description=description):
                self.skill(description)
                self.assertTrue(any("workflow-summary" in e for e in catalog_budget_errors(self.suite)))

    def test_cli_exits_nonzero_for_300_byte_fixture(self) -> None:
        self.skill("Use when " + "x" * 291)
        # A minimal valid inventory keeps the failure attributable to the budget.
        (self.suite / "skills").mkdir()
        (self.suite / "skills/acs-example").symlink_to(self.suite / "skills-src/test/acs-example")
        for host in ("claude", "codex"):
            directory = self.suite / f".{host}-plugin"
            directory.mkdir()
            (directory / "plugin.json").write_text(json.dumps({
                "name": "agent-coding-skills", "skills": "./skills/",
            }))
        catalog = self.suite.parent / "catalog/skill-set.json"
        catalog.parent.mkdir()
        catalog.write_text(json.dumps({
            "schemaVersion": 1, "id": "agent-coding-skills",
            "sourcePattern": "system/skills-src/{category}/{skill}/SKILL.md",
            "categories": [{"id": "test", "skills": ["acs-example"]}],
        }))
        protocol = self.suite / "protocols/skill-declarations.md"
        protocol.parent.mkdir()
        protocol.write_text("## Handoff consumers\n")
        skill = self.suite / "skills-src/test/acs-example/SKILL.md"
        skill.write_text(skill.read_text() + "\n```yaml\ncontext:\n" + "".join(
            f"  {field}: []\n" for field in
            ("requires", "retrieves", "produces", "updates", "invalidates", "handoff_to")
        ) + "```\n")
        script = self.suite / "evals/validate_suite.py"
        script.parent.mkdir()
        script.write_bytes(VALIDATOR.read_bytes())
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "skills-src/test/acs-example/SKILL.md: description is 300 bytes; limit is 260",
            "1 source skills; inventory, catalog budget, declarations, local links/anchors: FAIL",
        ])
        skill.write_text(skill.read_text().replace("x" * 291, "x" * 251))
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
