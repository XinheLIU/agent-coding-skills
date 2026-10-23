"""B12: real subprocess scans of authored Git fixture changes, not model transcripts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
GUARD = ROOT / "system/skills-src/test/acs-analyze-test-gaps/scripts/floor_guard.py"


class ConstraintFloorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="acs-constraint-floor-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write("CONSTRAINTS.md", "# Constraints\n\n## Enforced checks\n\n"
                   "| ID | Rule | Checked by | Stage |\n| --- | --- | --- | --- |\n"
                   "| coverage | >= 80% | tests | task |\n"
                   "| latency | <= 200 ms | benchmark | CI |\n\n"
                   "## Exceptions\n\n| ID | Rule | Reason | Owner | Expires |\n"
                   "| --- | --- | --- | --- | --- |\n")
        self.write("tests/test_total.py", "def test_total():\n    assert sum([2, 3]) == 5\n")
        self.write("handler.js", "try { work(); } catch (error) {\n  throw error;\n}\n")
        self.write("handler.py", "try:\n    work()\nexcept ValueError:\n    raise\n")
        self.write("src/value.py", "VALUE = 1\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture baseline")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True,
                                       stderr=subprocess.PIPE)

    def write(self, name: str, text: str) -> None:
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def replace(self, name: str, old: str, new: str) -> None:
        path = self.repo / name
        path.write_text(path.read_text().replace(old, new))

    def run_guard(self, expected: int, *, base: str | None = None,
                  cwd: Path | None = None) -> dict:
        result = subprocess.run([sys.executable, "-B", str(GUARD), "--base", base or self.base],
                                cwd=cwd or self.repo, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report["green_claim"])
        self.assertEqual(result.stderr, "")
        if expected != 2:
            self.assertEqual(report["merge_base"], self.base)
            self.assertRegex(report["diff_sha256"], r"^[0-9a-f]{64}$")
        return report

    def assert_move(self, report: dict, move: str, path: str, line: int, side: str = "new") -> None:
        self.assertIn({"file": path, "line": line, "side": side, "move": move}, report["findings"])

    def test_lowered_minimum_and_raised_maximum(self) -> None:
        self.replace("CONSTRAINTS.md", ">= 80%", ">= 70%")
        self.replace("CONSTRAINTS.md", "<= 200 ms", "<= 250 ms")
        report = self.run_guard(1)
        self.assert_move(report, "lowered-threshold", "CONSTRAINTS.md", 7)
        self.assert_move(report, "lowered-threshold", "CONSTRAINTS.md", 8)

    def test_skip_and_weakened_assertion(self) -> None:
        self.write("tests/test_total.py", "import pytest\n@pytest.mark.skip(reason='later')\n"
                   "def test_total():\n    assert True\n")
        report = self.run_guard(1)
        self.assert_move(report, "skipped-or-weakened-test", "tests/test_total.py", 2)
        self.assert_move(report, "skipped-or-weakened-test", "tests/test_total.py", 2, "old")

    def test_suppression_is_reported_without_matched_value(self) -> None:
        self.write("src/value.py", "VALUE = 'private-fixture-value'  # noqa\n")
        report = self.run_guard(1)
        self.assert_move(report, "suppression-comment", "src/value.py", 1)
        self.assertNotIn("private-fixture-value", json.dumps(report))

    def test_catch_emptied_by_deleting_body_is_detected(self) -> None:
        self.replace("handler.js", "  throw error;\n", "")
        report = self.run_guard(1)
        self.assert_move(report, "stubbed-catch", "handler.js", 1)

    def test_deletion_does_not_hide_behind_an_existing_identical_empty_catch(self) -> None:
        self.write("handler.js", "try { other(); } catch (error) {\n}\n"
                   "try { work(); } catch (error) {\n  throw error;\n}\n")
        self.git("add", ".")
        self.git("commit", "-qm", "existing empty catch fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.replace("handler.js", "  throw error;\n", "")
        self.assert_move(self.run_guard(1), "stubbed-catch", "handler.js", 3)

    def test_unchanged_empty_catch_does_not_flag_unrelated_edit(self) -> None:
        self.write("handler.js", "try { work(); } catch (error) {\n}\nconst value = 1;\n")
        self.git("add", ".")
        self.git("commit", "-qm", "existing empty catch fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.replace("handler.js", "value = 1", "value = 2")
        self.run_guard(0)

    def test_python_stubbed_catch(self) -> None:
        self.replace("handler.py", "    raise", "    pass")
        self.assert_move(self.run_guard(1), "stubbed-catch", "handler.py", 4)

    def test_arbitrary_exception_id_is_detected(self) -> None:
        with (self.repo / "CONSTRAINTS.md").open("a") as stream:
            stream.write("| legacy-waiver | coverage | migration | team | 2026-12-01 |\n")
        self.assert_move(self.run_guard(1), "new-exception-row", "CONSTRAINTS.md", 14)

    def test_clean_change_and_tightening_pass(self) -> None:
        self.replace("CONSTRAINTS.md", ">= 80%", ">= 85%")
        self.replace("CONSTRAINTS.md", "<= 200 ms", "<= 150 ms")
        self.write("src/value.py", "VALUE = 2\n")
        report = self.run_guard(0)
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["files_scanned"], 2)
        self.assertEqual(report["status"], "clean")

    def test_unchanged_tree_passes(self) -> None:
        self.assertEqual(self.run_guard(0)["files_scanned"], 0)

    def test_staged_unstaged_untracked_and_subdirectory_scope(self) -> None:
        self.write("src/value.py", "VALUE = 1  # noqa\n")
        self.git("add", "src/value.py")
        self.replace("handler.py", "    raise", "    pass")
        name = 'tests/a space "quoted"\nname.test.js'
        self.write(name, 'test.skip("unfinished", () => {});\n')
        report = self.run_guard(1, cwd=self.repo / "src")
        self.assertEqual(report["files_scanned"], 3)
        self.assert_move(report, "suppression-comment", "src/value.py", 1)
        self.assert_move(report, "stubbed-catch", "handler.py", 4)
        self.assert_move(report, "skipped-or-weakened-test", name, 1)

    def test_committed_branch_change_is_included(self) -> None:
        self.write("src/value.py", "VALUE = 1  # type: ignore\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture change")
        self.assert_move(self.run_guard(1), "suppression-comment", "src/value.py", 1)

    def test_deleted_test_file_is_reported_in_old_coordinates(self) -> None:
        (self.repo / "tests/test_total.py").unlink()
        self.assert_move(self.run_guard(1), "skipped-or-weakened-test", "tests/test_total.py", 1, "old")

    def test_removed_rule_and_stage_deferral_block(self) -> None:
        self.replace("CONSTRAINTS.md", "| coverage | >= 80% | tests | task |\n", "")
        self.replace("CONSTRAINTS.md", "| benchmark | CI |", "| benchmark | later |")
        report = self.run_guard(1)
        self.assert_move(report, "lowered-threshold", "CONSTRAINTS.md", 7, "old")
        self.assert_move(report, "lowered-threshold", "CONSTRAINTS.md", 7)

    def test_unknown_direction_change_blocks(self) -> None:
        self.replace("CONSTRAINTS.md", ">= 80%", "80%")
        self.run_guard(1)

    def test_removed_exception_tightens(self) -> None:
        original = (self.repo / "CONSTRAINTS.md").read_text()
        self.write("CONSTRAINTS.md", original + "| accepted | rule | reason | team | 2026-12-01 |\n")
        self.git("add", ".")
        self.git("commit", "-qm", "existing exception fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.write("CONSTRAINTS.md", original)
        self.run_guard(0)

    def test_changed_exception_is_still_a_finding(self) -> None:
        original = (self.repo / "CONSTRAINTS.md").read_text()
        self.write("CONSTRAINTS.md", original + "| accepted | rule | reason | team | 2026-12-01 |\n")
        self.git("add", ".")
        self.git("commit", "-qm", "existing exception fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.replace("CONSTRAINTS.md", "2026-12-01", "2027-01-01")
        self.run_guard(1)

    def test_existing_suppression_is_outside_changed_lines(self) -> None:
        self.write("src/value.py", "VALUE = 1  # noqa\nOTHER = 2\n")
        self.git("add", ".")
        self.git("commit", "-qm", "existing suppression fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.replace("src/value.py", "OTHER = 2", "OTHER = 3")
        self.run_guard(0)

    def test_ignored_and_markdown_examples_are_outside_code_scan(self) -> None:
        self.write(".gitignore", "ignored.py\n")
        self.write("ignored.py", "value = 1 # noqa\n")
        self.write("guide.md", "Document @ts-ignore and catch {} here.\n")
        self.run_guard(0)

    def test_missing_base_and_non_repository_fail_closed(self) -> None:
        self.assertEqual(self.run_guard(2, base="missing-ref")["status"], "unavailable")
        with tempfile.TemporaryDirectory() as outside:
            self.run_guard(2, cwd=Path(outside))

    def test_changed_binary_and_symlink_fail_closed(self) -> None:
        path = self.repo / "binary.bin"
        path.write_bytes(b"a\0b")
        self.run_guard(2)
        path.unlink()
        path.symlink_to("src/value.py")
        self.run_guard(2)

    def test_duplicate_constraint_rows_fail_closed(self) -> None:
        self.replace("CONSTRAINTS.md", "| latency |", "| coverage |")
        self.run_guard(2)

    def test_no_mutation_and_fingerprint_changes_with_input(self) -> None:
        self.write("src/value.py", "VALUE = 2\n")
        before_status = self.git("status", "--porcelain=v1")
        before_index = hashlib.sha256((self.repo / ".git/index").read_bytes()).hexdigest()
        before_content = (self.repo / "src/value.py").read_bytes()
        first = self.run_guard(0)
        self.assertEqual(before_status, self.git("status", "--porcelain=v1"))
        self.assertEqual(before_content, (self.repo / "src/value.py").read_bytes())
        self.assertEqual(before_index, hashlib.sha256((self.repo / ".git/index").read_bytes()).hexdigest())
        self.assertEqual(first["diff_sha256"], self.run_guard(0)["diff_sha256"])
        self.write("src/value.py", "VALUE = 3\n")
        self.assertNotEqual(first["diff_sha256"], self.run_guard(0)["diff_sha256"])


if __name__ == "__main__":
    unittest.main()
