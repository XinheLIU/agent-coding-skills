import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


SKILL_DIR = Path(__file__).resolve().parents[1]
SCAN_SCRIPT = SKILL_DIR / "scripts" / "scan_specs.py"
RENDER_SCRIPT = SKILL_DIR / "scripts" / "render_dag.py"
TASK_SCAN_SCRIPT = SKILL_DIR / "scripts" / "scan_tasks.py"


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.section_links: dict[str, list[str]] = {}
        self.ticket_states: dict[str, str] = {}
        self.section = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id", "") or ""
        if element_id:
            self.ids.add(element_id)
        if tag == "section":
            self.section = element_id
        if tag == "a":
            href = attributes.get("href", "") or ""
            self.links.append(href)
            self.section_links.setdefault(self.section, []).append(href)
        if tag == "article":
            self.ticket_states[element_id.removeprefix("ticket-")] = (attributes.get("class", "") or "").split()[-1]

    def handle_endtag(self, tag: str) -> None:
        if tag == "section":
            self.section = ""


class RoadmapTest(unittest.TestCase):
    def test_delivery_plan_refresh_matches_graph_and_preserves_canonical_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            change = root / "profile"
            tasks = change / "tasks"
            tasks.mkdir(parents=True)
            spec = change / "spec.md"
            spec.write_text("# Profile scope\n\nLast updated: 2026-09-17\n", encoding="utf-8")
            tickets = [
                ("D1", "design", "pending", "ready", "none"),
                ("T1", "implementation", "pending", "ready", "none"),
                ("T2", "implementation", "pending", "ready", "D1"),
                ("T3", "implementation", "failed", "ready", "none"),
                ("T4", "implementation", "done", "needs-review", "none"),
                ("T5", "implementation", "superseded", "ready", "none"),
            ]
            for ticket_id, kind, status, readiness, deps in tickets:
                (tasks / f"{ticket_id}.md").write_text(
                    f'# {ticket_id}: Profile <script>alert("x")</script>\n\n'
                    "Last updated: 2026-09-17\n\n"
                    f"Type: {kind}\nStatus: {status}\nReadiness: {readiness}\ndepends_on: {deps}\n\n"
                    "## Scope\nEdit profile\n\n## Inputs\nspec.md criterion AC1\n\n"
                    "## Verification\nacs-design-architecture resolves avatar storage\n\n"
                    "## Blockers\nStorage retention policy\n\n## Evidence\nDecision reference ADR-1\n",
                    encoding="utf-8",
                )
            plan_path = root / "plan.json"
            plan = {
                "scope": "Edit profiles; deletion is excluded < & >.",
                "outcomes": ["Members can update their display names", "Members can replace avatars"],
                "next_action": "Resolve avatar storage.",
                "sources": [{"label": "Accepted scope", "href": "spec.md", "revision": "revision-1"}],
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            manifest_path = root / "manifest.json"
            report = change / "delivery-plan.html"
            render = [sys.executable, str(RENDER_SCRIPT), str(manifest_path), "--plan", str(plan_path),
                      "--storage-key", "delivery-profile", "-o", str(report)]
            for design_done in (False, True):
                before = {path: path.read_bytes() for path in [spec, *tasks.glob("*.md")]}
                subprocess.run([sys.executable, str(TASK_SCAN_SCRIPT), str(change), "-o", str(manifest_path)],
                               check=True, capture_output=True, text=True)
                subprocess.run(render, check=True, capture_output=True, text=True)
                html = report.read_text(encoding="utf-8")
                parsed = ReportParser()
                parsed.feed(html)
                expected_ready = {"#ticket-profile%2FT1"}
                if design_done:
                    expected_ready.add("#ticket-profile%2FT2")
                self.assertEqual(set(parsed.section_links["frontier"]), expected_ready)
                self.assertEqual(parsed.section_links.get("design-blockers", []),
                                 [] if design_done else ["#ticket-profile%2FD1"])
                self.assertEqual(len(parsed.ticket_states), len(tickets))
                for href in parsed.links:
                    if href.startswith("#"):
                        self.assertIn(unquote(href[1:]), parsed.ids)
                    else:
                        self.assertTrue((report.parent / unquote(href)).is_file(), href)
                nodes = re.search(r"const NODES = (.+);", html)
                assert nodes
                status_logic = html[html.index("function computeStatus"):html.index("const NODE_W")]
                result = subprocess.run(
                    ["node", "-e", f"const NODES = {nodes[1]};\n{status_logic}\nconsole.log(JSON.stringify(computeStatus()));"],
                    check=True, capture_output=True, text=True,
                )
                self.assertEqual(json.loads(result.stdout), parsed.ticket_states)
                self.assertIn("Edit profiles; deletion is excluded &lt; &amp; &gt;.", html)
                self.assertIn("acs-design-architecture resolves avatar storage", html)
                self.assertIn("Decision reference ADR-1", html)
                self.assertIn(plan["next_action"], html)
                self.assertIn('const STORAGE_KEY = "delivery-profile";', html)
                self.assertNotIn('<script>alert("x")</script>', html)
                self.assertEqual(html.count("</script>"), 1)
                self.assertEqual(before, {path: path.read_bytes() for path in before})
                # Re-render the same report after a canonical decision is settled.
                decision = tasks / "D1.md"
                decision.write_text(decision.read_text().replace("Status: pending", "Status: done"))
                plan["next_action"] = "Implement profile editing when authorized."
                plan_path.write_text(json.dumps(plan), encoding="utf-8")
            rejected = subprocess.run(render + ["--format", "mermaid"], capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("--plan requires --format html", rejected.stderr)

    def test_incomplete_metadata_and_prose_blockers_are_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tasks = root / "change" / "tasks"
            tasks.mkdir(parents=True)
            (tasks / "T1.md").write_text(
                "# T1: Incomplete metadata\nStatus: done\ndepends_on: none\n",
                encoding="utf-8",
            )
            (tasks / "T2.md").write_text(
                "# T2: External blocker\nType: implementation\nStatus: pending\n"
                "Readiness: ready\ndepends_on: obtain storage access\n",
                encoding="utf-8",
            )
            manifest_path = root / "manifest.json"
            subprocess.run(
                [sys.executable, str(TASK_SCAN_SCRIPT), str(root), "-o", str(manifest_path)],
                check=True, capture_output=True, text=True,
            )
            manifest = json.loads(manifest_path.read_text())
            self.assertEqual(len(manifest["warnings"]), 3)
            self.assertEqual(manifest["unresolved_dep_count"], 1)
            self.assertTrue(all(not node["done"] and not node["execution_ready"] for node in manifest["nodes"]))

    def test_canonical_tickets_preserve_sources_and_gate_the_frontier(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tasks = root / "profile" / "tasks"
            tasks.mkdir(parents=True)
            # Design is complete, but its evidence is stale. Name editing is independent.
            tickets = [
                ("D1", "design", "done", "needs-review", "none"),
                ("T1", "implementation", "pending", "ready", "none"),
                ("T2", "implementation", "pending", "ready", "D1"),
                ("T3", "implementation", "pending", "needs-criteria", "none"),
                ("T4", "implementation", "failed", "ready", "none"),
                ("D2", "design", "pending", "ready", "none"),
                ("T5", "implementation", "in_progress", "ready", "none"),
            ]
            for ticket_id, kind, status, readiness, deps in tickets:
                (tasks / f"{ticket_id}.md").write_text(
                    f"# {ticket_id}: Outcome {ticket_id}\n\n"
                    f"Type: {kind}\nStatus: {status}\nReadiness: {readiness}\n"
                    f"depends_on: {deps}\n", encoding="utf-8",
                )
            before = {path: path.read_bytes() for path in tasks.glob("*.md")}
            manifest_path = root / "manifest.json"
            html_path = root / "roadmap.html"
            for expected_avatar_status in ("todo", "frontier"):
                subprocess.run(
                    [sys.executable, str(TASK_SCAN_SCRIPT), str(tasks.parent), "-o", str(manifest_path)],
                    check=True, capture_output=True, text=True,
                )
                manifest = json.loads(manifest_path.read_text())
                self.assertEqual(manifest["warnings"], [])
                self.assertEqual(len(manifest["nodes"]), 7)
                avatar = next(node for node in manifest["nodes"] if node["id"] == "profile/T2")
                self.assertEqual(avatar["deps"], ["profile/D1"])
                self.assertTrue(avatar["source_revision"].startswith("sha256:"))
                self.assertEqual(Path(avatar["source_file"]), (tasks / "T2.md").resolve())
                subprocess.run(
                    [sys.executable, str(RENDER_SCRIPT), str(manifest_path), "-o", str(html_path)],
                    check=True, capture_output=True, text=True,
                )
                html = html_path.read_text()
                nodes = re.search(r"const NODES = (.+);", html)
                self.assertIsNotNone(nodes)
                assert nodes
                status_logic = html[html.index("function computeStatus"):html.index("const NODE_W")]
                result = subprocess.run(
                    ["node", "-e", f"const NODES = {nodes[1]};\n{status_logic}\nconsole.log(JSON.stringify(computeStatus()));"],
                    check=True, capture_output=True, text=True,
                )
                statuses = json.loads(result.stdout)
                self.assertEqual(statuses["profile/T1"], "frontier")
                self.assertEqual(statuses["profile/T2"], expected_avatar_status)
                for ticket_id in ("T3", "T4", "D2"):
                    self.assertEqual(statuses[f"profile/{ticket_id}"], "todo")
                self.assertEqual(statuses["profile/T5"], "inprogress")
                if expected_avatar_status == "todo":
                    self.assertEqual(before, {path: path.read_bytes() for path in tasks.glob("*.md")})
                    decision = tasks / "D1.md"
                    decision.write_text(decision.read_text().replace("needs-review", "ready"))

    def test_cross_change_edges_and_invalid_graphs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for change, deps in (("alpha", "none"), ("beta", "alpha/T1")):
                tasks = root / change / "tasks"
                tasks.mkdir(parents=True)
                (tasks / "T1.md").write_text(
                    "# T1: Deliver a slice\nType: implementation\nStatus: pending\n"
                    f"Readiness: ready\ndepends_on: {deps}\n", encoding="utf-8",
                )
            manifest = root / "manifest.json"
            command = [sys.executable, str(TASK_SCAN_SCRIPT), str(root), "-o", str(manifest)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            data = json.loads(manifest.read_text())
            self.assertEqual(data["nodes"][1]["deps"], ["alpha/T1"])
            mermaid = root / "roadmap.md"
            render = [sys.executable, str(RENDER_SCRIPT), str(manifest), "--format", "mermaid", "-o", str(mermaid)]
            subprocess.run(render, check=True, capture_output=True, text=True)
            self.assertIn('n1["beta/T1', mermaid.read_text())
            self.assertIn("n0 --> n1", mermaid.read_text())
            overlay = root / "overlay.json"
            overlay.write_text(json.dumps({"extra_deps": {"alpha/T1": ["beta/T1"]}}))
            result = subprocess.run(render + ["--overlay", str(overlay)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Dependency cycle", result.stderr)
            first = root / "alpha/tasks/T1.md"
            original = first.read_text()
            for deps, error in (("missing", "missing prerequisite"), ("beta/T1", "Dependency cycle"), ("T1", "Dependency cycle")):
                with self.subTest(deps=deps):
                    first.write_text(original.replace("depends_on: none", f"depends_on: {deps}"))
                    result = subprocess.run(command, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(error, result.stderr)

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
            self.assertNotIn('STORAGE_KEY + "_status"', html)
            self.assertIn("flowchart TB", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
