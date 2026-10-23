"""B18 source contracts and an authored regression fixture, not a model run."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from test_packages import builder, validator

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "system/skills-src/authoring/acs-review-agent-instructions/SKILL.md"


class LessonLadderTests(unittest.TestCase):
    def intake(self) -> str:
        return SKILL.read_text().split("### Intake\n", 1)[1].split("\n### Review", 1)[0]

    def test_acs_review_agent_instructions_enforces_ladder_and_recorded_failure_proof(self) -> None:
        intake = self.intake()
        rungs = ["| Architecture |", "| Types |", "| Lint |", "| Test |", "| Documentation |"]
        positions = [intake.index(rung) for rung in rungs]
        self.assertEqual(positions, sorted(positions))
        for requirement in (
            "highest applicable rung", "why each higher rung cannot prevent this failure",
            "existing check", "unwired or broken", "error names the fix",
            "Each new check must fail on the recorded mistake",
            "same check unchanged on the corrected code",
            "expected failure reason", "import or setup error",
            "command", "fingerprint", "timestamp", "evidence contract",
        ):
            self.assertIn(requirement, intake)
        self.assertNotIn("Intake is complete when the new instruction", intake)

    def test_acs_review_agent_instructions_requires_explicit_fallback_and_narrow_scope(self) -> None:
        intake = self.intake()
        for requirement in (
            "no check is possible", "instruction fallback", "why architecture, types, lint, and tests cannot enforce",
            "Missing tools, permission, or a runnable reproducer", "incomplete",
            "Root instruction file", "Nearest scoped instruction file",
            "Canonical document or skill, with a trigger pointer",
            "Configured run recovery entry or linked effort artifact",
            "does not duplicate another canonical rule",
            "technically accurate review sounded dismissive", "word ban cannot enforce that judgment",
        ):
            self.assertIn(requirement, intake)

    def test_acs_review_agent_instructions_standalone_keeps_evidence_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="acs-lesson-package-") as temporary:
            output = Path(temporary) / "acs-review-agent-instructions"
            builder.build_standalone_skill(ROOT / "system", output, SKILL.parent)
            self.assertEqual(validator.validate_package(output), [])
            text = (output / "SKILL.md").read_text()
            self.assertIn("Each new check must fail on the recorded mistake", text)
            self.assertIn("#evidence-contract", text)
            self.assertTrue(any("## Evidence contract" in path.read_text()
                                for path in output.rglob("*.md")))

    def test_recorded_empty_recipient_lesson_fails_old_code_then_passes_fix(self) -> None:
        # Authored lesson and expected result; these are not a production incident.
        lesson = {
            "failure": "An empty recipient list was accepted because all([]) is true.",
            "expected": "recipients_valid([]) is False; a nonempty valid list is True",
            "consequence": "A notification was accepted without any recipient.",
            "rung": "Test",
            "higher_rungs": {
                "architecture": "The existing public validator owns this runtime decision.",
                "types": "A list type admits empty lists in this Python API.",
                "lint": "all() is legitimate elsewhere; this is a runtime domain condition.",
            },
        }
        check = (
            "import unittest\nfrom recipients import recipients_valid\n\n"
            "class RecipientTests(unittest.TestCase):\n"
            "    def test_empty_list_is_rejected(self):\n"
            "        self.assertFalse(recipients_valid([]), 'empty recipient list accepted')\n"
            "    def test_valid_recipient_is_accepted(self):\n"
            "        self.assertTrue(recipients_valid(['person@example.org']))\n"
            "    def test_invalid_recipient_is_rejected(self):\n"
            "        self.assertFalse(recipients_valid(['invalid']))\n"
        )
        runs = []
        with tempfile.TemporaryDirectory(prefix="acs-lesson-ladder-") as temporary:
            work = Path(temporary)
            (work / "test_recipients.py").write_text(check)
            for phase, body in (
                ("recorded-mistake", "all('@' in address for address in recipients)"),
                ("corrected", "bool(recipients) and all('@' in address for address in recipients)"),
            ):
                (work / "recipients.py").write_text(f"def recipients_valid(recipients):\n    return {body}\n")
                paths = ["recipients.py", "test_recipients.py"]
                before = {name: hashlib.sha256((work / name).read_bytes()).hexdigest() for name in paths}
                command = [sys.executable, "-B", "-m", "unittest", "-v", "test_recipients.py"]
                result = subprocess.run(command, cwd=work, capture_output=True, text=True)
                runs.append({"phase": phase, "command": command, "cwd": str(work),
                             "fingerprint": before, "timestamp": datetime.now(timezone.utc).isoformat(),
                             "exit_code": result.returncode, "output": result.stdout + result.stderr})
                self.assertEqual(before, {name: hashlib.sha256((work / name).read_bytes()).hexdigest()
                                          for name in paths})
                self.assertEqual(result.returncode, 1 if phase == "recorded-mistake" else 0, runs[-1])
                if phase == "recorded-mistake":
                    self.assertIn("AssertionError: True is not false : empty recipient list accepted", runs[-1]["output"])
                    self.assertIn("FAILED (failures=1)", runs[-1]["output"])
            self.assertEqual((work / "test_recipients.py").read_text(), check)
        self.assertEqual(runs[0]["fingerprint"]["test_recipients.py"], runs[1]["fingerprint"]["test_recipients.py"])
        self.assertNotEqual(runs[0]["fingerprint"]["recipients.py"], runs[1]["fingerprint"]["recipients.py"])
        print(json.dumps({"evidence_kind": "authored lesson with actual subprocess runs; not a model transcript",
                          "lesson": lesson, "runs": runs}, indent=2))


if __name__ == "__main__":
    unittest.main()
