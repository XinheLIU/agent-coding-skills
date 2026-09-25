"""Artifact-level regression fixtures; these do not simulate agent judgment."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "validate_suite.py"
spec = importlib.util.spec_from_file_location("validate_suite", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DeclarationTests(unittest.TestCase):
    def test_empty_lists_are_valid(self) -> None:
        declaration = "```yaml\ncontext:\n" + "".join(
            f"  {field}: []\n" for field in sorted(validator.FIELDS)
        ) + "```\n"
        self.assertEqual(validator.declaration_errors(declaration), [])

    def test_handoff_must_name_a_defined_consumer(self) -> None:
        declaration = "```yaml\ncontext:\n" + "".join(
            f"  {field}: []\n" for field in sorted(validator.FIELDS)
        ) + "```\n"
        for selector in ("context_management", "unknown_consumer"):
            with self.subTest(selector=selector):
                self.assertTrue(validator.declaration_errors(
                    declaration.replace("handoff_to: []", f"handoff_to: [{selector}]")))
        self.assertEqual(validator.declaration_errors(
            declaration.replace("handoff_to: []", "handoff_to: [coordinator]")), [])

    def test_duplicate_field_cannot_hide_missing_field(self) -> None:
        declaration = "```yaml\ncontext:\n" + "".join(
            f"  {field}: []\n" for field in sorted(validator.FIELDS)
        ) + "```\n"
        broken = declaration.replace("handoff_to", "requires")
        self.assertTrue(validator.declaration_errors(broken))

    def test_non_list_or_duplicate_selector_is_rejected(self) -> None:
        declaration = "```yaml\ncontext:\n" + "".join(
            f"  {field}: []\n" for field in sorted(validator.FIELDS)
        ) + "```\n"
        for value in ("change.requirements", "[change.requirements, change.requirements]"):
            with self.subTest(value=value):
                self.assertTrue(validator.declaration_errors(declaration.replace("requires: []", f"requires: {value}")))


class RetentionReferencesTests(unittest.TestCase):
    def test_missing_link_outside_suite_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "system"
            root.mkdir()
            skill = root / "SKILL.md"
            skill.write_text("[Coordination](../workflows/context-coordination.md)\n")
            self.assertTrue(validator.reference_errors(skill, root))

    def test_retained_change_is_readable_without_run_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            change = root / "docs/changes/EXP-42"
            change.mkdir(parents=True)
            run = root / ".scratch/export"
            run.mkdir(parents=True)
            (change / "ticket.md").write_text("# EXP-42\n\n[Requirements](spec.md#ac-9)\n[Decision](decision.md#d-4)\n[Verification](verification.md)\n[Release](release.md)\n")
            (change / "spec.md").write_text("# EXP-42 requirements\n\n## AC-9\nCompletion is visible.\n")
            (change / "decision.md").write_text("# D-4\n\nAccepted: inline notification avoids a blocking modal.\n[AC-9](spec.md#ac-9), revision req-v3.\n")
            (change / "verification.md").write_text("# Verification\n\n[AC-9](spec.md#ac-9) → export_test: PASS. Code abc123, env staging-v4. Failures: none. Omission: mobile not assessed.\n")
            (change / "release.md").write_text("# Release\n\n[EXP-42](ticket.md), artifact sha256:42, build abc123, staging-v4. [Evidence](verification.md). Rollback: prior artifact sha256:41.\n")
            (run / "raw.log").write_text("temporary verbose test output\n")
            (run / "handoff.md").write_text("# Handoff\n\n[EXP-42](../../docs/changes/EXP-42/ticket.md)\n")
            for path in root.rglob("*.md"):
                self.assertEqual(validator.reference_errors(path, root), [])
            for path in run.iterdir():
                path.unlink()
            run.rmdir()
            for path in change.glob("*.md"):
                self.assertEqual(validator.reference_errors(path, root), [])

    def test_cleanup_detects_rationale_still_in_deleted_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            record = root / "decision.md"
            record.write_text("# D-4\n\n[Basis](.scratch/decision.md#rationale)\n")
            self.assertEqual(validator.reference_errors(record, root), ["broken reference: .scratch/decision.md#rationale"])

    def test_changed_record_id_breaks_the_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            product = root / "product.html"
            product.write_text('<article id="ticket-exp-42" data-kind="roadmap-ticket">EXP-42</article>')
            handoff = root / "handoff.md"
            handoff.write_text("# Handoff\n\n[EXP-42](product.html#ticket-exp-42)\n")
            self.assertEqual(validator.reference_errors(handoff, root), [])
            product.write_text('<article id="ticket-exp-43">Renumbered</article>')
            self.assertEqual(validator.reference_errors(handoff, root), ["missing anchor: product.html#ticket-exp-42"])


if __name__ == "__main__":
    unittest.main()
