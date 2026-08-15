import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCAN_SCRIPT = SKILL_DIR / "scripts" / "scan_specs.py"
RENDER_SCRIPT = SKILL_DIR / "scripts" / "render_dag.py"


class RoadmapTest(unittest.TestCase):
    def test_map_input_statuses_and_read_only_html(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "work"
            effort = root / "alpha"
            issues = effort / "issues"
            issues.mkdir(parents=True)
            (effort / "map.md").write_text("# Alpha map\n", encoding="utf-8")
            statuses = ["done", "merged", "abcdef1", "in progress"]
            for index, status in enumerate(statuses, start=1):
                blocker = "None" if index == 1 else "01 — First"
                (issues / f"{index:02d}-ticket.md").write_text(
                    f"# {index:02d} — Ticket {index}\n\n"
                    f"**Status:** {status}\n\n"
                    f"**Blocked by:** {blocker}\n",
                    encoding="utf-8",
                )

            manifest_path = Path(temp_dir) / "manifest.json"
            subprocess.run(
                [sys.executable, str(SCAN_SCRIPT), str(root), "-o", str(manifest_path)],
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertTrue(manifest["workstreams"][0]["source_file"].endswith("map.md"))
            self.assertEqual([node["done"] for node in manifest["nodes"]], [True, True, True, False])
            self.assertEqual(manifest["nodes"][1]["deps"], ["A01"])

            html_path = Path(temp_dir) / "roadmap.html"
            markdown_path = Path(temp_dir) / "roadmap.md"
            for output_format, output_path in (
                ("html", html_path),
                ("mermaid", markdown_path),
            ):
                subprocess.run(
                    [
                        sys.executable,
                        str(RENDER_SCRIPT),
                        str(manifest_path),
                        "--format",
                        output_format,
                        "-o",
                        str(output_path),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

            html = html_path.read_text(encoding="utf-8")
            self.assertIn("status from Markdown", html)
            self.assertNotIn("toggle finished", html)
            self.assertNotIn("_status", html)
            self.assertIn("flowchart TB", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
