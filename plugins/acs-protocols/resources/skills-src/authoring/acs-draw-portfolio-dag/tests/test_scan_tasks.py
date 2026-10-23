"""CLI contract fixtures; no model behavior is exercised here."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scan_tasks.py"
SCHEMA = json.loads(Path(__file__).with_name("status.schema.json").read_text())


def validate_schema(value, schema):
    """Validate the type/required/enum/items/properties subset used by this fixture."""
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
    expected = schema["type"]
    assert type(value) in [types[name] for name in (expected if isinstance(expected, list) else [expected])]
    if "enum" in schema:
        assert value in schema["enum"]
    if isinstance(value, dict):
        assert set(schema.get("required", [])) <= value.keys()
        if schema.get("additionalProperties") is False:
            assert value.keys() <= schema["properties"].keys()
        for key, item in value.items():
            validate_schema(item, schema["properties"][key])
    if isinstance(value, list):
        for item in value:
            validate_schema(item, schema["items"])


class ScanTasksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tasks = self.root / "change" / "tasks"
        self.tasks.mkdir(parents=True)

    def ticket(self, name, *, status="pending", readiness="ready", kind="implementation", deps="none", change="change"):
        tasks = self.root / change / "tasks"
        tasks.mkdir(exist_ok=True, parents=True)
        (tasks / f"{name}.md").write_text(
            f"# {name}: Outcome {name}\nType: {kind}\nStatus: {status}\n"
            f"Readiness: {readiness}\ndepends_on: {deps}\n", encoding="utf-8")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), *map(str, args)],
                              capture_output=True, text=True)

    def status(self):
        before = {p: p.read_bytes() for p in self.root.glob("*/tasks/*.md")}
        result = self.run_cli("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        data = json.loads(result.stdout)
        validate_schema(data, SCHEMA)
        self.assertEqual(before, {p: p.read_bytes() for p in before})
        self.assertTrue(any("prerequisites" in warning and "state" in warning for warning in data["warnings"]))
        return data

    def test_schema_frontier_and_one_deterministic_next(self):
        self.ticket("B")
        self.ticket("A")
        self.ticket("C", deps="A")
        data = self.status()
        self.assertEqual(data["frontier"], ["change/A", "change/B"])
        self.assertEqual(data["next"], {"action": "implement", "ticket_id": "change/A"})
        self.assertEqual(data, self.status())
        for node in data["tickets"]:
            self.assertRegex(node["source_revision"], r"^sha256:[0-9a-f]{64}$")
        broken = dict(data, next=[data["next"], data["next"]])
        with self.assertRaises(AssertionError):
            validate_schema(broken, SCHEMA)

    def test_missing_dependencies_reported_but_manifest_still_rejects(self):
        self.ticket("A", deps="absent, other/missing")
        data = self.status()
        self.assertEqual(data["tickets"][0]["missing_dependencies"], ["change/absent", "other/missing"])
        self.assertFalse(data["tickets"][0]["execution_ready"])
        self.assertEqual(data["frontier"], [])
        self.assertEqual(data["next"], {"action": "resolve_blockers", "ticket_id": "change/A"})
        result = self.run_cli("-o", self.root / "manifest.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing prerequisite", result.stderr)
        self.assertFalse((self.root / "manifest.json").exists())

    def test_readiness_status_and_dependency_gates(self):
        self.ticket("D", kind="design", status="done", readiness="needs-review")
        self.ticket("T", deps="D")
        self.ticket("Design", kind="design")
        self.ticket("Failed", status="failed")
        self.ticket("Unknown", status="unknown")
        self.ticket("Prose", deps="ask owner")
        self.ticket("Unready", readiness="needs-criteria")
        self.ticket("Superseded", status="superseded")
        data = self.status()
        self.assertEqual(data["frontier"], [])
        self.assertEqual(data["next"]["action"], "resolve_blockers")
        nodes = {node["id"]: node for node in data["tickets"]}
        self.assertEqual(nodes["change/T"]["blocked_dependencies"], ["change/D"])
        self.assertEqual(nodes["change/Prose"]["unresolved_dep_text"], "ask owner")
        self.ticket("D", kind="design", status="done")
        self.assertEqual(self.status()["frontier"], ["change/T"])

    def test_cross_change_completed_prerequisite(self):
        self.ticket("A", status="done", kind="design")
        self.ticket("B", deps="change/A", change="other")
        self.assertEqual(self.status()["frontier"], ["other/B"])

    def test_wait_resolve_and_complete_actions(self):
        self.ticket("A", status="in_progress")
        self.assertEqual(self.status()["next"], {"action": "wait", "ticket_id": "change/A"})
        self.ticket("A", status="done")
        self.ticket("B", status="superseded")
        self.assertEqual(self.status()["next"], {"action": "complete", "ticket_id": None})
        self.ticket("A", status="done", readiness="needs-review")
        self.assertEqual(self.status()["next"]["action"], "resolve_blockers")

    def test_done_record_does_not_hide_missing_prerequisites(self):
        self.ticket("A", status="done", deps="missing")
        data = self.status()
        self.assertEqual(data["tickets"][0]["status"], "done")
        self.assertEqual(data["tickets"][0]["missing_dependencies"], ["change/missing"])
        self.assertEqual(data["next"]["action"], "resolve_blockers")

    def test_json_rejects_cycles_even_with_missing_ids(self):
        self.ticket("A", deps="B, missing")
        self.ticket("B", deps="A")
        result = self.run_cli("--json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Dependency cycle", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_manifest_bytes_unchanged_when_json_also_requested(self):
        self.ticket("A")
        manifest = self.root / "manifest.json"
        result = self.run_cli("-o", manifest)
        self.assertEqual(result.returncode, 0, result.stderr)
        before = manifest.read_bytes()
        self.assertIn("Scanned 1 tickets", result.stdout)
        result = self.run_cli("--json", "-o", manifest)
        self.assertEqual(result.returncode, 0, result.stderr)
        validate_schema(json.loads(result.stdout), SCHEMA)
        self.assertEqual(before, manifest.read_bytes())

    def test_output_mode_required(self):
        self.ticket("A")
        self.assertNotEqual(self.run_cli().returncode, 0)


if __name__ == "__main__":
    unittest.main()
