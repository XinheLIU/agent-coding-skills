"""B4 source contracts and an authored ticket fixture; not a model behavior run."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "system/skills-src/build/acs-tdd/SKILL.md"


class TddSeamsTests(unittest.TestCase):
    def test_acs_tdd_requires_an_accepted_seam_and_independent_oracle(self) -> None:
        text = SKILL.read_text()
        prepare = text.split("## Prepare the behavior slice\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("only at a seam named in an accepted TST", prepare)
        self.assertIn("confirmed by the user when no TST exists", prepare)
        self.assertIn("reconcile the TST before writing the test", prepare)
        for name in ("Implementation-coupled", "Tautological", "Horizontal slicing"):
            self.assertIn(f"**{name}**", text)
        self.assertIn("Expected values come from an independent source of truth", text)

    def test_acs_tdd_ends_at_green_and_hands_refactoring_to_review(self) -> None:
        text = SKILL.read_text()
        loop = text.split("## Red → green\n", 1)[1].split("\n## ", 1)[0]
        review = text.split("## Review and handoff\n", 1)[1]
        self.assertNotIn("refactor", loop.lower())
        self.assertIn("End this loop at green", loop)
        self.assertIn("Refactoring belongs to review", review)
        self.assertIn("acs-refactor-code", review)
        self.assertIn("Current State/ADR contract", review)
        self.assertIn("criterion → test/evidence → revision mapping", review)
        for binding in ("preserve dispatch BASE", "tested source revision/tree fingerprint",
                        "actual completion timestamp with timezone", "environment and result"):
            self.assertIn(binding, loop)

    def test_authored_ticket_executes_red_then_green_at_accepted_tst_seam(self) -> None:
        # This accepted TST is authored fixture input, not an actual user decision.
        ticket = {
            "id": "B4-example", "criterion": "AC-1: the subtotal of 10 and 5 is 15",
            "tst": {"id": "TST-example", "status": "accepted", "seams": ["cart.subtotal"]},
            "seam": "cart.subtotal", "oracle": "literal 15 from the ticket's worked example",
        }
        self.assertEqual(ticket["tst"]["status"], "accepted")
        self.assertIn(ticket["seam"], ticket["tst"]["seams"])
        test_source = (
            "import unittest\nfrom cart import subtotal\n\n"
            "class SubtotalTests(unittest.TestCase):\n"
            "    def test_ac1_subtotal_of_10_and_5_is_15(self):\n"
            "        self.assertEqual(subtotal([10, 5]), 15)\n"
        )
        runs = []
        with tempfile.TemporaryDirectory(prefix="acs-tdd-seams-") as temporary:
            work = Path(temporary)
            (work / "test_cart.py").write_text(test_source)
            for phase, implementation in (
                ("red", "def subtotal(prices):\n    return 0\n"),
                ("green", "def subtotal(prices):\n    return sum(prices)\n"),
            ):
                (work / "cart.py").write_text(implementation)
                inputs = {name: hashlib.sha256((work / name).read_bytes()).hexdigest()
                          for name in ("cart.py", "test_cart.py")}
                command = [sys.executable, "-B", "-m", "unittest", "-v", "test_cart.py"]
                result = subprocess.run(command, cwd=work, capture_output=True, text=True)
                timestamp = datetime.now(timezone.utc).isoformat()
                self.assertEqual(inputs, {name: hashlib.sha256((work / name).read_bytes()).hexdigest()
                                          for name in inputs})
                runs.append({"phase": phase, "criterion": ticket["criterion"],
                             "seam": ticket["seam"], "command": command, "cwd": str(work),
                             "revision": inputs, "timestamp": timestamp,
                             "exit_code": result.returncode, "output": result.stdout + result.stderr})
                if phase == "red":
                    self.assertEqual(result.returncode, 1, runs[-1]["output"])
                    self.assertIn("AssertionError: 0 != 15", runs[-1]["output"])
                else:
                    self.assertEqual(result.returncode, 0, runs[-1]["output"])
            self.assertEqual((work / "test_cart.py").read_text(), test_source)
        self.assertNotEqual(runs[0]["revision"]["cart.py"], runs[1]["revision"]["cart.py"])
        self.assertEqual(runs[0]["revision"]["test_cart.py"], runs[1]["revision"]["test_cart.py"])
        print(json.dumps({"evidence_kind": "authored fixture with actual subprocess runs; not a model transcript",
                          "ticket": ticket, "runs": runs}, indent=2))


if __name__ == "__main__":
    unittest.main()
