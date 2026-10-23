"""B11 authored contract and executed local mock, not live agent/production proof."""
from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from test_packages import builder, validator

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
SKILL = SUITE / "skills-src/design/technical/acs-design-contracts"
FIXTURE = SUITE / "evals/fixtures/acs-design-contracts-observability.json"


def design_errors(design: dict) -> list[str]:
    errors = []
    questions = {item["id"] for item in design["questions"]}
    if not 2 <= len(design["questions"]) <= 4 or len(questions) != len(design["questions"]):
        errors.append("need 2–4 distinct questions")
    if list(design).index("questions") > list(design).index("signals"):
        errors.append("questions must precede signals")
    covered = set()
    for signal in design["signals"]:
        answers = signal["answers"]
        if not answers or not set(answers) <= questions or not all(answers.values()):
            errors.append("signal needs valid question IDs and queries")
        covered.update(answers)
    if covered != questions:
        errors.append("questions must all have signals")
    for alert in design["alerts"]:
        if alert["signal"] not in {signal["name"] for signal in design["signals"]} or alert["question"] not in questions:
            errors.append("alert must map to signal and question")
        if not all(alert.get(key) for key in ("symptom", "threshold", "duration", "rationale", "destination", "query")):
            errors.append("alert needs symptom, threshold, duration, rationale, destination and query")
        runbook = design["runbooks"].get(alert["runbook"].removeprefix("#/runbooks/"), [])
        if len(runbook) != 3 or any(not line.startswith(prefix) or not line[len(prefix):].strip()
                                    for line, prefix in zip(runbook, ("Means:", "First query:", "Escalate to:"))):
            errors.append("alert needs a linked three-line runbook")
    if not all(design["verification"].get(key) for key in ("command", "environment")):
        errors.append("execution blocked: declare command and environment")
    return errors


def checkout(provider, connection: sqlite3.Connection, request_id: str) -> None:
    """Execute a mock boundary and emit its observed result, without injection metadata."""
    outcome, dependency, cause = "succeeded", "provider", "none"
    try:
        provider()
    except TimeoutError:
        outcome, cause = "failed", "timeout"
    connection.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)",
                       ("checkout_result", request_id, "checkout -> provider", outcome, dependency, cause))


def diagnose(connection: sqlite3.Connection, query: str) -> dict:
    """Only the telemetry connection and runbook query enter the diagnostic pass."""
    rows = connection.execute(query).fetchall()
    if len(rows) != 1 or any(value is None or value == "unknown" for value in rows[0]):
        raise ValueError("missing or ambiguous telemetry")
    return dict(zip(("request_id", "path", "dependency", "cause"), rows[0]))


class DesignContractsObservabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = json.loads(FIXTURE.read_text())
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.execute("CREATE TABLE telemetry(event, request_id, path, outcome, dependency, cause)")

    def test_authored_design_and_negative_contract_cases(self) -> None:
        self.assertEqual(design_errors(self.design), [])
        for count in (1, 5):
            mutated = copy.deepcopy(self.design)
            mutated["questions"] = [{"id": f"Q{i}"} for i in range(count)]
            self.assertIn("need 2–4 distinct questions", design_errors(mutated))
        mutated = copy.deepcopy(self.design)
        mutated["questions"] = mutated.pop("questions")
        self.assertIn("questions must precede signals", design_errors(mutated))
        mutated = copy.deepcopy(self.design)
        mutated["signals"][0]["answers"] = {"Q9": "SELECT 1"}
        self.assertIn("signal needs valid question IDs and queries", design_errors(mutated))
        self.assertIn("questions must all have signals", design_errors(mutated))
        for runbook in ([], ["Means: impact", "First query: SELECT 1"], ["Means:", "First query:", "Escalate to:"]):
            mutated = copy.deepcopy(self.design)
            mutated["runbooks"]["checkout_unavailable"] = runbook
            self.assertIn("alert needs a linked three-line runbook", design_errors(mutated))
        for key in ("command", "environment"):
            mutated = copy.deepcopy(self.design)
            mutated["verification"][key] = ""
            self.assertIn("execution blocked: declare command and environment", design_errors(mutated))

    def test_induced_failure_and_every_alert_test_fire(self) -> None:
        self.assertEqual(design_errors(self.design), [])  # execution precondition
        checkout(lambda: None, self.connection, "healthy-1")
        for alert in self.design["alerts"]:
            self.assertLess(self.connection.execute(alert["query"]).fetchone()[0], alert["threshold"])

        def timed_out_provider() -> None:
            raise TimeoutError("injection detail withheld from telemetry")

        checkout(timed_out_provider, self.connection, "request-2")
        for signal in self.design["signals"]:
            for query in signal["answers"].values():
                self.assertTrue(self.connection.execute(query).fetchall())
        with tempfile.TemporaryDirectory() as temporary:
            inbox = Path(temporary) / "scratch-inbox"
            inbox.mkdir()
            receipts = []
            for alert in self.design["alerts"]:
                if self.connection.execute(alert["query"]).fetchone()[0] >= alert["threshold"]:
                    destination = Path(temporary) / alert["destination"] / (alert["name"] + ".json")
                    destination.write_text(json.dumps({"alert": alert["name"], "runbook": alert["runbook"]}))
                receipt = json.loads((inbox / (alert["name"] + ".json")).read_text())
                runbook = self.design["runbooks"][receipt["runbook"].removeprefix("#/runbooks/")]
                diagnosis = diagnose(self.connection, runbook[1].removeprefix("First query: "))
                self.assertEqual(diagnosis, {"request_id": "request-2", "path": "checkout -> provider",
                                             "dependency": "provider", "cause": "timeout"})
                receipts.append({**receipt, "diagnosis": diagnosis})
            self.assertEqual(len(receipts), len(self.design["alerts"]))
            print("B11 local mock evidence: " + json.dumps({
                "source_sha256": hashlib.sha256((SKILL / "SKILL.md").read_bytes()).hexdigest(),
                "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
                "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "environment": self.design["verification"]["environment"],
                "telemetry": self.connection.execute("SELECT * FROM telemetry").fetchall(),
                "receipts": receipts,
            }, sort_keys=True))

    def test_diagnosis_rejects_missing_and_ambiguous_telemetry(self) -> None:
        query = self.design["runbooks"]["checkout_unavailable"][1].removeprefix("First query: ")
        with self.assertRaisesRegex(ValueError, "missing or ambiguous"):
            diagnose(self.connection, query)
        self.connection.execute("INSERT INTO telemetry VALUES ('checkout_result', 'r1', 'checkout', 'failed', 'provider', NULL)")
        with self.assertRaisesRegex(ValueError, "missing or ambiguous"):
            diagnose(self.connection, query)
        self.connection.execute("UPDATE telemetry SET cause = 'timeout'")
        self.connection.execute("INSERT INTO telemetry SELECT * FROM telemetry")
        with self.assertRaisesRegex(ValueError, "missing or ambiguous"):
            diagnose(self.connection, query)

    def test_source_requirements_survive_standalone_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            exported = Path(temporary) / "export"
            builder.build_standalone_skill(SUITE, exported, SKILL)
            installed = Path(temporary) / "installed"
            exported.rename(installed)
            self.assertEqual(validator.validate_package(installed), [])
            for path in (SKILL / "SKILL.md", installed / "SKILL.md"):
                text = path.read_text()
                for phrase in ("Before naming signals", "2–4 on-call questions", "every proposed signal",
                               "three-line runbook", "one test-fire per alert", "from telemetry alone",
                               "unset commands or environments block execution", "relevant changes invalidate them",
                               "Preserve existing authorization", "unexecuted checks remain explicit open items"):
                    self.assertIn(phrase, text)
                self.assertIn("acs-design-test-strategy", text)


if __name__ == "__main__":
    unittest.main()
