"""B5 source/package checks and authored simulation; no model behavior claimed."""
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
SKILL = SUITE / "skills-src/maintain/acs-diagnose-incident"
FIXTURE = SUITE / "evals/fixtures/acs-diagnose-incident-stops.json"


def stop_errors(transcript: list[dict]) -> list[str]:
    """Check an authored trace's stop boundary, not an agent's compliance."""
    falsified = set()
    for index, event in enumerate(transcript):
        if event["action"] == "probe" and event.get("verdict") == "falsified":
            falsified.add(event["hypothesis"])
        if len(falsified) == 3:
            remaining = transcript[index + 1:]
            if len(remaining) != 1 or remaining[0]["action"] != "stop_and_offer_options":
                return ["three strikes must end in options without another probe"]
            stop = remaining[0]
            if not stop.get("awaiting_user_choice"):
                return ["must await user choice"]
            if {option["choice"] for option in stop.get("options", [])} != {
                "continue", "escalate", "instrument_and_wait"
            }:
                return ["missing stop options"]
            return []
    return ["scenario must falsify three distinct hypotheses"]


class DiagnoseIncidentTests(unittest.TestCase):
    def test_source_has_numbered_rules_and_preserves_catalog_description(self) -> None:
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("description: Use when behavior is broken, intermittent, slow, or resistant to an obvious fix.", text)
        rules = re.findall(r"^([1-4])\. \*\*(.*?)\*\* (.+)$", text, re.MULTILINE)
        self.assertEqual([number for number, _, _ in rules], ["1", "2", "3", "4"])
        for rule, phrase in zip(rules, (
            "After three falsified hypotheses", "narrowest directory",
            "more than five distinct files in total", "[DEBUG-xxxx]",
        )):
            self.assertIn(phrase, rule[2])
        self.assertIn("Wait for the user's choice before a fourth probe", rules[0][2])
        self.assertIn("including a regression test", rules[1][2])
        self.assertIn("wait before editing a sixth file", rules[2][2])
        self.assertNotIn("three to five", text)
        self.assertIn("rg -n -F '[DEBUG-a4f2]'", text)

    def test_authored_three_strike_transcript(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not a model transcript", fixture["evidence_kind"])
        self.assertEqual(fixture["skill"], "acs-diagnose-incident")
        self.assertEqual(stop_errors(fixture["transcript"]), [])

    def test_simulation_checker_rejects_fourth_probe_and_unapproved_continuation(self) -> None:
        original = json.loads(FIXTURE.read_text())["transcript"]
        fourth_probe = {"role": "assistant", "action": "probe", "hypothesis": "H4", "verdict": "falsified"}
        for position in (-1, len(original)):
            transcript = copy.deepcopy(original)
            transcript.insert(position, fourth_probe)
            self.assertIn("three strikes must end in options without another probe", stop_errors(transcript))
        transcript = copy.deepcopy(original)
        transcript[-1]["awaiting_user_choice"] = False
        self.assertIn("must await user choice", stop_errors(transcript))
        transcript = copy.deepcopy(original)
        transcript[-1]["options"].pop()
        self.assertIn("missing stop options", stop_errors(transcript))

    def test_runtime_recipes_survive_standalone_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, SKILL)
            installed = root / "installed/acs-diagnose-incident"
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            recipe = installed / "references/runtime-debuggers.md"
            self.assertEqual(recipe.read_bytes(), (SKILL / "references/runtime-debuggers.md").read_bytes())
            self.assertIn("node inspect path/to/repro.js", recipe.read_text())
            self.assertIn("python -m debugpy --listen 127.0.0.1:5678 --wait-for-client", recipe.read_text())
            self.assertFalse(any(path.is_symlink() for path in installed.rglob("*")))


if __name__ == "__main__":
    unittest.main()
