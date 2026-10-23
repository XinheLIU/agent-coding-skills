"""Phase-boundary source contracts and authored transcript checks, not model runs."""
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
COORDINATION = SUITE / "protocols/context-coordination.md"
DECLARATIONS = SUITE / "protocols/skill-declarations.md"
IMPLEMENT = SUITE / "skills-src/build/acs-implement"
FIXTURE = SUITE / "evals/fixtures/phase-boundary-transcripts.json"
QUESTIONS = (
    "Does the next phase consume this one as a primary source?",
    "Is there enough context room left for the next phase?",
)


def transcript_errors(events: list[dict]) -> list[str]:
    """Check event ordering against B15; this is a fixture oracle, not a runtime."""
    boundary = events[0]
    errors = []
    kinds = [event["event"] for event in events]
    continuous = (boundary["primary_source"] is True
                  and boundary["context_room"] is True
                  and not boundary["transfer"] and not boundary["formal_review"])
    if "persist" not in kinds:
        return ["missing durable record"]
    persist = kinds.index("persist")
    next_phase = kinds.index("next_phase")
    if continuous and persist < next_phase:
        errors.append("unnecessary boundary persistence")
    if not continuous and persist > next_phase:
        errors.append("late persistence")
    if not events[persist].get("references"):
        errors.append("missing persisted references")
    if boundary["transfer"]:
        if "handoff" not in kinds:
            errors.append("missing handoff")
        else:
            handoff = kinds.index("handoff")
            if not persist < handoff < next_phase:
                errors.append("handoff order")
            envelope = events[handoff]
            required = {"identity", "scope", "references", "delta", "decisions", "rulings_made", "unresolved", "next_action"}
            if not required <= envelope.keys():
                errors.append("incomplete envelope")
            if envelope.get("references") != events[persist].get("references"):
                errors.append("unpersisted handoff references")
    elif continuous and "handoff" in kinds:
        errors.append("unnecessary handoff")
    return errors


class PhaseBoundaryTests(unittest.TestCase):
    def test_rule_has_one_owner_and_linked_consumers(self) -> None:
        text = COORDINATION.read_text()
        section = text.split("## Phase boundaries\n", 1)[1].split("\n## ", 1)[0]
        for question in QUESTIONS:
            self.assertIn(question, section)
            owners = [p for p in (SUITE / "protocols").glob("*.md") if question in p.read_text()]
            self.assertEqual(owners, [COORDINATION])
            self.assertEqual(text.count(question), 1)
            for skill in (SUITE / "skills-src").rglob("SKILL.md"):
                self.assertNotIn(question, skill.read_text(), str(skill))
        for clause in ("If both answers are yes", "persist the necessary proposals and evidence afterwards",
                       "If either answer is no or unknown", "across sessions, worktrees, and agents",
                       "Formal review", "49dd158", "does not adopt upstream host commands or token thresholds"):
            self.assertIn(clause, section)
        for consumer in (DECLARATIONS, IMPLEMENT / "SKILL.md"):
            self.assertIn("context-coordination.md#phase-boundaries", consumer.read_text())
        self.assertNotIn("Every cross-session or domain handoff contains:", DECLARATIONS.read_text())
        self.assertNotIn("for every domain or session transfer", text)

    def test_fixture_transcripts_cover_continuation_and_required_persistence(self) -> None:
        fixture = json.loads(FIXTURE.read_text())
        self.assertIn("not observed agent or model runs", fixture["evidence_kind"])
        cases = fixture["cases"]
        self.assertEqual({case["id"] for case in cases}, {
            "continuous-primary-source", "new-session", "new-worktree", "new-agent",
            "no-primary-source", "no-context-room", "unknown-context-room", "formal-review",
        })
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(transcript_errors(case["transcript"]), [])

    def test_mutations_reject_dropped_records_and_incorrect_boundary_order(self) -> None:
        cases = {c["id"]: c["transcript"] for c in json.loads(FIXTURE.read_text())["cases"]}
        events = copy.deepcopy(cases["continuous-primary-source"])
        events[1], events[2] = events[2], events[1]
        self.assertIn("unnecessary boundary persistence", transcript_errors(events))
        self.assertIn("missing durable record", transcript_errors(events[:1] + [events[2]]))
        for name in ("new-session", "new-worktree", "new-agent"):
            with self.subTest(case=name):
                events = copy.deepcopy(cases[name])
                events[1], events[3] = events[3], events[1]
                self.assertIn("late persistence", transcript_errors(events))
                self.assertIn("handoff order", transcript_errors(events))
                events = copy.deepcopy(cases[name])
                del events[2]["next_action"]
                self.assertIn("incomplete envelope", transcript_errors(events))
                events[2]["references"] = ["private-conversation"]
                self.assertIn("unpersisted handoff references", transcript_errors(events))
                del events[2]
                self.assertIn("missing handoff", transcript_errors(events))
        for name in ("no-primary-source", "no-context-room", "unknown-context-room", "formal-review"):
            events = copy.deepcopy(cases[name])
            events[1], events[2] = events[2], events[1]
            self.assertIn("late persistence", transcript_errors(events), name)

    def test_standalone_skill_preserves_phase_boundary_anchor_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "export"
            builder.build_standalone_skill(SUITE, output, IMPLEMENT)
            installed = root / "installed/acs-implement"
            installed.parent.mkdir()
            shutil.move(str(output), installed)
            self.assertEqual(validator.validate_package(installed), [])
            protocol = installed / "resources/protocols/context-coordination.md"
            self.assertIn("## Phase boundaries", protocol.read_text())
            self.assertIn("context-coordination.md#phase-boundaries", (installed / "SKILL.md").read_text())
            self.assertFalse(any(p.is_symlink() for p in installed.rglob("*")))


if __name__ == "__main__":
    unittest.main()
