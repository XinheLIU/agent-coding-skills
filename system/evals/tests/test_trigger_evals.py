"""B17 deterministic fixtures and router mechanics; no model observations."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import trigger_evals as runner


class TriggerEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.cases, cls.sources = runner.load_fixtures(runner.SUITE)
        cls.config = json.loads(runner.DEFAULT_CONFIG.read_text())
        cls.config.update(model="mock-router-v1", adapter_command=["local-mock"],
                          max_calls=len(cls.cases) * 3, evidence_kind="mock")

    def temporary_suite(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        suite = Path(temp.name) / "system"
        for source in self.sources.values():
            destination = suite / source.relative_to(runner.SUITE)
            destination.parent.mkdir(parents=True)
            shutil.copy2(source, destination)
            fixture = source.parent / "evals/trigger-fixtures.json"
            if fixture.exists():
                (destination.parent / "evals").mkdir()
                shutil.copy2(fixture, destination.parent / "evals/trigger-fixtures.json")
        return suite

    def mutate(self, suite, skill, change):
        source = next((suite / "skills-src").rglob(f"{skill}/SKILL.md"))
        fixture = source.parent / "evals/trigger-fixtures.json"
        data = json.loads(fixture.read_text())
        change(data)
        fixture.write_text(json.dumps(data))

    def mock_router(self, _command, *, input, **_kwargs):
        request = json.loads(input)
        self.assertEqual(set(request), {"schema", "model", "query", "catalog", "explicit_skill", "instruction"})
        self.assertNotIn("expect", input)
        # Authored test double, deliberately not evidence of model performance.
        selected = self.answers.get(request["query"], [])
        return subprocess.CompletedProcess(_command, 0, json.dumps({"model": request["model"], "selected": selected}), "")

    def correct_answers(self):
        self.answers = {c["q"]: [c["skill"]] for c in self.cases if c["expect"] == "trigger"}

    def test_all_invocable_skills_have_balanced_automatic_fixtures(self):
        self.assertEqual(runner.fixture_errors(), [])
        automatic = {s["name"] for s in self.catalog if s["automatic"]}
        self.assertEqual(len(automatic), 35)  # Includes the two release-tail skills.
        self.assertEqual({c["skill"] for c in self.cases}, automatic | {"acs-validate-demand"})
        for skill in automatic:
            for label in ("trigger", "no-trigger"):
                self.assertGreaterEqual(sum(c["skill"] == skill and c["invocation"] == "automatic" and c["expect"] == label for c in self.cases), 8)
        self.assertTrue(all(c["explicit_skill"] == "acs-validate-demand" for c in self.cases if c["skill"] == "acs-validate-demand" and c["expect"] == "trigger"))

    def test_missing_class_near_miss_duplicate_and_invalid_schema_fail(self):
        changes = [
            lambda d: d.update(queries=d["queries"][:8]),
            lambda d: [q.pop("near_miss_of", None) for q in d["queries"]],
            lambda d: d["queries"].append(d["queries"][0]),
            lambda d: d.update(schema=2),
            lambda d: d["queries"][8].update(near_miss_of="acs-does-not-exist"),
            lambda d: d["queries"][0].update(invocation="explicit", explicit_skill="acs-validate-demand"),
            lambda d: d["queries"][0].update(explicit_skill="acs-validate-demand"),
        ]
        for change in changes:
            with self.subTest(change=change):
                suite = self.temporary_suite()
                self.mutate(suite, "acs-research", change)
                self.assertTrue(runner.fixture_errors(suite))

    def test_missing_fixture_or_collision_link_fails(self):
        suite = self.temporary_suite()
        source = next((suite / "skills-src").rglob("acs-research/SKILL.md"))
        (source.parent / "evals/trigger-fixtures.json").unlink()
        self.assertTrue(runner.fixture_errors(suite))
        suite = self.temporary_suite()
        source = next((suite / "skills-src").rglob("acs-challenge-approach/SKILL.md"))
        source.write_text(source.read_text().replace("## When NOT to use", "## Lost boundary"))
        self.assertIn("When NOT to use", runner.fixture_errors(suite)[0])
        suite = self.temporary_suite()
        self.mutate(suite, "acs-review-code-quality", lambda d: [q.update(near_miss_of="acs-refactor-code") for q in d["queries"] if q.get("near_miss_of") == "acs-trace-requirements"])
        self.assertIn("reciprocal collision", runner.fixture_errors(suite)[0])

    def test_disabled_skill_cannot_have_automatic_positive(self):
        suite = self.temporary_suite()
        def change(data):
            data["queries"][0].update(invocation="automatic")
            data["queries"][0].pop("explicit_skill")
        self.mutate(suite, "acs-validate-demand", change)
        self.assertIn("disabled skill", runner.fixture_errors(suite)[0])

    def test_default_dry_run_never_executes_or_reports_metrics(self):
        with patch.object(runner.subprocess, "run") as adapter:
            report = runner.run(runner.SUITE, json.loads(runner.DEFAULT_CONFIG.read_text()))
        adapter.assert_not_called()
        self.assertEqual(report["status"], "dry-run")
        self.assertEqual(report["metrics"], {})
        self.assertEqual(report["completed_calls"], 0)
        self.assertEqual(report["planned_calls"], len(self.cases) * 3)

    def test_unset_model_budget_adapter_and_invalid_thresholds_block_before_calls(self):
        variants = [dict(model=None), dict(max_calls=None), dict(adapter_command=[]),
                    dict(max_calls=1), dict(min_recall=0), dict(min_precision=float("nan")),
                    dict(trigger_threshold=1.1), dict(runs_per_query=True)]
        with patch.object(runner.subprocess, "run") as adapter:
            for changed in variants:
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    runner.run(runner.SUITE, {**self.config, **changed}, execute=True)
        adapter.assert_not_called()

    def test_mock_success_separates_automatic_and_explicit_metrics(self):
        self.correct_answers()
        with patch.object(runner.subprocess, "run", side_effect=self.mock_router):
            report = runner.run(runner.SUITE, self.config, execute=True)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["evidence_kind"], "mock")
        self.assertEqual(report["completed_calls"], report["planned_calls"])
        demand = report["metrics"]["acs-validate-demand"]
        self.assertEqual(demand["explicit"]["recall"], 1)
        self.assertIsNone(demand["automatic"]["recall"])
        self.assertEqual(demand["automatic"]["fp"], 0)
        self.assertEqual(report["collision_failures"], [])
        for skill in report["metrics"]:
            if skill != "acs-validate-demand":
                self.assertEqual(report["metrics"][skill]["automatic"]["precision"], 1)

    def test_low_recall_and_missing_collision_destination_fail(self):
        self.answers = {}
        with patch.object(runner.subprocess, "run", side_effect=self.mock_router):
            report = runner.run(runner.SUITE, self.config, execute=True)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["metrics"]["acs-research"]["automatic"]["recall"], 0)
        self.assertTrue(report["collision_failures"])

    def test_false_positives_fail_precision_even_when_recall_is_perfect(self):
        self.correct_answers()
        for query, selected in self.answers.items():
            if "acs-research" not in selected and not query.startswith("/"):
                selected.append("acs-research")
        with patch.object(runner.subprocess, "run", side_effect=self.mock_router):
            report = runner.run(runner.SUITE, self.config, execute=True)
        metrics = report["metrics"]["acs-research"]["automatic"]
        self.assertEqual(metrics["recall"], 1)
        self.assertLess(metrics["precision"], self.config["min_precision"])
        self.assertEqual(report["status"], "failed")

    def test_majority_and_threshold_boundary_math(self):
        cases = [{"skill": "a", "expect": "trigger", "invocation": "automatic"},
                 {"skill": "a", "expect": "no-trigger", "invocation": "automatic"}]
        obs = [{"selections": [["a"], ["a"], []]}, {"selections": [["a"], [], []]}]
        metrics, _ = runner.summarize(cases, obs, self.config)
        self.assertEqual(metrics["a"]["automatic"]["tp"], 1)
        self.assertEqual(metrics["a"]["automatic"]["tn"], 1)
        config = {**self.config, "trigger_threshold": 1 / 3, "min_precision": .5}
        metrics, _ = runner.summarize(cases, obs, config)
        self.assertTrue(metrics["a"]["automatic"]["passed"])
        config["min_precision"] = .5001
        metrics, _ = runner.summarize(cases, obs, config)
        self.assertFalse(metrics["a"]["automatic"]["passed"])

    def test_invalid_adapter_partial_timeout_and_model_drift_are_void(self):
        invalid = ["not-json", "null", "[]",
                   json.dumps({"model": "different-model", "selected": []}),
                   json.dumps({"model": self.config["model"], "selected": ["unknown"]}),
                   json.dumps({"model": self.config["model"], "selected": ["acs-validate-demand"]}),
                   json.dumps({"model": self.config["model"], "selected": ["acs-research"] * 2})]
        for response in invalid:
            with self.subTest(response=response), patch.object(runner.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, response, "")):
                self.assertEqual(runner.run(runner.SUITE, self.config, execute=True)["status"], "void")
        good = subprocess.CompletedProcess([], 0, json.dumps({"model": self.config["model"], "selected": []}), "")
        for failure in [subprocess.TimeoutExpired("mock", 1), subprocess.CalledProcessError(1, "mock"), FileNotFoundError("mock")]:
            with patch.object(runner.subprocess, "run", side_effect=[good, failure]):
                report = runner.run(runner.SUITE, self.config, execute=True)
            self.assertEqual(report["status"], "void")
            self.assertEqual(report["completed_calls"], 1)
            self.assertEqual(report["metrics"], {})

    def test_casual_mention_never_authorizes_demand(self):
        self.correct_answers()
        casual = next(c for c in self.cases if "I saw acs-validate-demand" in c["q"])
        self.assertEqual(casual["invocation"], "automatic")
        self.answers[casual["q"]] = ["acs-validate-demand"]
        with patch.object(runner.subprocess, "run", side_effect=self.mock_router):
            report = runner.run(runner.SUITE, self.config, execute=True)
        self.assertEqual(report["status"], "void")
        self.assertIn("unauthorized", report["error"])

    def test_source_mutation_during_execution_voids_metrics(self):
        self.correct_answers()
        with patch.object(runner.subprocess, "run", side_effect=self.mock_router), patch.object(runner, "fingerprint", side_effect=["before", "after"]):
            report = runner.run(runner.SUITE, self.config, execute=True)
        self.assertEqual(report["status"], "void")
        self.assertEqual(report["metrics"], {})

    def test_added_skill_during_execution_voids_metrics(self):
        self.correct_answers()
        suite = self.temporary_suite()
        added = suite / "skills-src/new/acs-new/SKILL.md"
        def mutate_catalog(*args, **kwargs):
            if not added.exists():
                added.parent.mkdir(parents=True)
                added.write_text("---\nname: acs-new\ndescription: Use when testing catalog drift.\n---\n")
            return self.mock_router(*args, **kwargs)
        with patch.object(runner.subprocess, "run", side_effect=mutate_catalog):
            report = runner.run(suite, self.config, execute=True)
        self.assertEqual(report["status"], "void")
        self.assertEqual(report["metrics"], {})

    def test_real_json_adapter_transport_and_cli_metric_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            adapter = directory / "router.py"
            adapter.write_text('import json, sys\nr = json.load(sys.stdin)\nassert "expect" not in r\nprint(json.dumps({"model": r["model"], "selected": []}))\n')
            config = {**self.config, "adapter_command": [sys.executable, str(adapter)], "runs_per_query": 1}
            config_path = directory / "config.json"
            config_path.write_text(json.dumps(config))
            output = directory / "report.json"
            result = subprocess.run([sys.executable, str(Path(runner.__file__)), "--config", str(config_path), "--execute", "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(output.read_text())
            self.assertEqual(report["evidence_kind"], "mock")
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["completed_calls"], len(self.cases))
            adapter.write_text('print("not JSON")\n')
            result = subprocess.run([sys.executable, str(Path(runner.__file__)), "--config", str(config_path), "--execute", "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(output.read_text())["status"], "void")

    def test_cli_check_dry_plan_and_unconfigured_execution(self):
        for arguments, code in [(["--check"], 0), ([], 0), (["--execute"], 2)]:
            result = subprocess.run([sys.executable, str(Path(runner.__file__)), *arguments], capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        with tempfile.TemporaryDirectory() as temp:
            suite = self.temporary_suite()
            self.mutate(suite, "acs-research", lambda d: d.update(queries=[]))
            result = subprocess.run([sys.executable, str(Path(runner.__file__)), "--check", "--suite", str(suite)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
