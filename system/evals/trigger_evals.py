#!/usr/bin/env python3
"""Validate trigger fixtures, plan calls, or evaluate a configured JSON router adapter.

Default is a read-only dry plan. No model/provider dependency or implicit execution.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

SUITE = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = SUITE / "evals/fixtures/trigger-router.json"
QUESTIONING = ("acs-challenge-approach", "acs-review-code-quality",
               "acs-design-interaction-flow", "acs-validate-demand")
COLLISIONS = [("acs-trace-requirements", "acs-review-code-quality")]
COLLISIONS += [(a, b) for i, a in enumerate(QUESTIONING) for b in QUESTIONING[i + 1:]]


def read_catalog(suite: Path) -> tuple[list[dict], dict[str, Path]]:
    catalog, sources = [], {}
    for path in sorted((suite / "skills-src").rglob("SKILL.md")):
        text = path.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not front:
            raise ValueError(f"{path}: missing frontmatter")
        fields = front[1]
        name = re.findall(r"^name: (.+)$", fields, re.M)
        descriptions = re.findall(r"^description: *([^\n]*(?:\n[ \t]+[^\n]*)*)", fields, re.M)
        flags = re.findall(r"^disable-model-invocation: *(.*)$", fields, re.M)
        if name != [path.parent.name] or len(descriptions) != 1 or flags not in ([], ["true"], ["false"]):
            raise ValueError(f"{path}: invalid catalog declaration")
        raw = descriptions[0].strip()
        if raw.startswith('"'):
            description = json.loads(raw)
        elif raw.startswith("'") and raw.endswith("'"):
            description = raw[1:-1].replace("''", "'")
        elif raw.split("\n", 1)[0] in {">", ">-", ">+", "|", "|-", "|+"}:
            description = " ".join(line.strip() for line in raw.splitlines()[1:])
        else:
            description = raw
        if not isinstance(description, str) or not description:
            raise ValueError(f"{path}: invalid description")
        if name[0] in sources:
            raise ValueError(f"duplicate skill {name[0]}")
        sources[name[0]] = path
        catalog.append({"name": name[0], "description": description,
                        "automatic": flags != ["true"]})
    if not sources:
        raise ValueError("no source skills")
    return catalog, sources


def load_fixtures(suite: Path) -> tuple[list[dict], list[dict], dict[str, Path]]:
    catalog, sources = read_catalog(suite)
    required = {s["name"] for s in catalog if s["automatic"]} | {"acs-validate-demand"}
    cases = []
    for skill in sorted(required):
        if skill not in sources:
            raise ValueError(f"missing skill {skill}")
        path = sources[skill].parent / "evals/trigger-fixtures.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema") != 1 or data.get("skill") != skill:
            raise ValueError(f"{skill}: invalid fixture schema/identity")
        queries = data.get("queries")
        if not isinstance(queries, list):
            raise ValueError(f"{skill}: queries must be an array")
        ids, prompts, counts, near = set(), set(), {"trigger": 0, "no-trigger": 0}, set()
        for q in queries:
            if not isinstance(q, dict) or not isinstance(q.get("id"), str) or not q["id"] or q["id"] in ids:
                raise ValueError(f"{skill}: duplicate/missing query id")
            if not isinstance(q.get("q"), str) or not q["q"].strip() or q["q"].strip() in prompts:
                raise ValueError(f"{skill}: empty/duplicate query")
            if q.get("expect") not in counts or q.get("invocation") not in {"automatic", "explicit"}:
                raise ValueError(f"{skill}: invalid expectation/invocation")
            explicit = q.get("explicit_skill")
            if q["invocation"] == "explicit":
                if explicit not in sources or not q["q"].startswith(f"/{explicit} "):
                    raise ValueError(f"{skill}: explicit case must start with its slash invocation")
            elif explicit is not None:
                raise ValueError(f"{skill}: automatic case cannot authorize an explicit skill")
            automatic = next(s["automatic"] for s in catalog if s["name"] == skill)
            if q["expect"] == "trigger" and not automatic and explicit != skill:
                raise ValueError(f"{skill}: disabled skill needs explicit invocation")
            neighbor = q.get("near_miss_of")
            if neighbor is not None:
                if neighbor not in sources or neighbor == skill or q["expect"] != "no-trigger":
                    raise ValueError(f"{skill}: invalid near-miss neighbor")
                near.add(neighbor)
            ids.add(q["id"])
            prompts.add(q["q"].strip())
            counts[q["expect"]] += 1
            cases.append({**q, "skill": skill})
        if min(counts.values()) < 8 or not near:
            raise ValueError(f"{skill}: need >=8 queries per class and a named near-miss")
        if automatic and any(sum(q["invocation"] == "automatic" and q["expect"] == label
                                 for q in queries) < 8 for label in counts):
            raise ValueError(f"{skill}: need >=8 automatic queries per class")
        for a, b in COLLISIONS:
            other = b if a == skill else a if b == skill else None
            if other and other not in near:
                raise ValueError(f"{skill}: missing reciprocal collision fixture for {other}")
    for a, b in COLLISIONS:
        for skill, other in ((a, b), (b, a)):
            text = sources[skill].read_text(encoding="utf-8")
            section = text.split("## When NOT to use\n", 1)[-1].split("\n## ", 1)[0]
            links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", section)
            if "## When NOT to use\n" not in text or not any(
                    (sources[skill].parent / link).resolve() == sources[other].resolve() for link in links):
                raise ValueError(f"{skill}: missing reciprocal When NOT to use link to {other}")
    return catalog, cases, sources


def fixture_errors(suite: Path = SUITE) -> list[str]:
    try:
        load_fixtures(suite)
        return []
    except (OSError, ValueError, TypeError, KeyError) as error:
        return [f"trigger fixtures: {error}"]


def fingerprint(suite: Path, sources: dict[str, Path]) -> str:
    paths = list((suite / "skills-src").rglob("SKILL.md")) + list((suite / "skills-src").rglob("evals/trigger-fixtures.json"))
    inputs = {str(path.relative_to(suite)): path for path in paths}
    inputs["evals/trigger_evals.py"] = Path(__file__).resolve()
    digest = hashlib.sha256()
    for name, path in sorted(inputs.items()):
        digest.update(name.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def validate_config(config: dict, *, execute: bool) -> None:
    if not isinstance(config, dict) or config.get("schema") != 1:
        raise ValueError("unsupported router config")
    for key in ("runs_per_query", "timeout_seconds"):
        if type(config.get(key)) is not int or config[key] < 1:
            raise ValueError(f"{key} must be a positive integer")
    for key in ("trigger_threshold", "min_precision", "min_recall"):
        value = config.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 < value <= 1:
            raise ValueError(f"{key} must be in (0, 1]")
    if config.get("evidence_kind") not in {"mock", "measured"}:
        raise ValueError("evidence_kind must be mock or measured")
    if execute:
        if not isinstance(config.get("model"), str) or not config["model"].strip():
            raise ValueError("execution requires an explicitly pinned model")
        command = config.get("adapter_command")
        if not isinstance(command, list) or not command or any(not isinstance(s, str) or not s for s in command):
            raise ValueError("execution requires adapter_command as an argv array")
        if type(config.get("max_calls")) is not int or config["max_calls"] < 1:
            raise ValueError("execution requires an explicit max_calls budget")


def summarize(cases: list[dict], observations: list[dict], config: dict) -> tuple[dict, list[str]]:
    metrics, collisions = {}, []
    for case, observed in zip(cases, observations, strict=True):
        counts = {}
        for selected in observed["selections"]:
            for name in selected:
                counts[name] = counts.get(name, 0) + 1
        selected = {name for name, count in counts.items()
                    if count / config["runs_per_query"] >= config["trigger_threshold"]}
        expected, predicted = case["expect"] == "trigger", case["skill"] in selected
        group = metrics.setdefault(case["skill"], {}).setdefault(case["invocation"],
                    {"tp": 0, "fp": 0, "tn": 0, "fn": 0})
        group[("tp" if expected else "fp") if predicted else ("fn" if expected else "tn")] += 1
        if case.get("near_miss_of") and (predicted or case["near_miss_of"] not in selected):
            collisions.append(f'{case["skill"]}/{case["id"]}')
    for groups in metrics.values():
        for group in groups.values():
            group["precision"] = group["tp"] / (group["tp"] + group["fp"]) if group["tp"] + group["fp"] else None
            group["recall"] = group["tp"] / (group["tp"] + group["fn"]) if group["tp"] + group["fn"] else None
            group["passed"] = (not group["fp"] if group["precision"] is None else group["precision"] >= config["min_precision"]) and (
                group["recall"] is None or group["recall"] >= config["min_recall"])
    return metrics, collisions


def run(suite: Path, config: dict, *, execute: bool = False) -> dict:
    validate_config(config, execute=execute)
    catalog, cases, sources = load_fixtures(suite)
    source_hash = fingerprint(suite, sources)
    calls = len(cases) * config["runs_per_query"]
    report = {"schema": 1, "status": "dry-run", "evidence_kind": config["evidence_kind"],
              "model": config.get("model"), "timestamp": datetime.now(timezone.utc).isoformat(),
              "source_sha256": source_hash,
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "config_sha256": hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest(),
              "settings": config, "queries": len(cases), "planned_calls": calls,
              "completed_calls": 0, "metrics": {}, "observations": []}
    if not execute:
        return report
    if calls > config["max_calls"]:
        raise ValueError(f'planned {calls} calls exceeds max_calls={config["max_calls"]}')
    automatic = {s["name"] for s in catalog if s["automatic"]}
    try:
        for case in cases:
            record = {"skill": case["skill"], "id": case["id"], "invocation": case["invocation"], "selections": []}
            report["observations"].append(record)
            # Do not send expectation, target skill, fixture ID, or neighbor to the router.
            request = {"schema": 1, "model": config["model"], "query": case["q"],
                       "catalog": catalog, "explicit_skill": case.get("explicit_skill"),
                       "instruction": "Select relevant skills by their descriptions. Automatic selection excludes automatic=false. Only explicit_skill authorizes an explicit-only skill; mere mentions do not. Return JSON with model and selected (an array of exact skill IDs); do not execute skills."}
            for _ in range(config["runs_per_query"]):
                result = subprocess.run(config["adapter_command"], input=json.dumps(request),
                                        capture_output=True, text=True, timeout=config["timeout_seconds"], check=True)
                response = json.loads(result.stdout)
                selected = response.get("selected") if isinstance(response, dict) else None
                if not isinstance(response, dict) or response.get("model") != config["model"] or not isinstance(selected, list) or any(
                        not isinstance(s, str) for s in selected) or len(set(selected)) != len(selected):
                    raise ValueError("invalid adapter response or model mismatch")
                if set(selected) - (automatic | {case.get("explicit_skill")}):
                    raise ValueError("adapter selected unknown or unauthorized explicit-only skill")
                record["selections"].append(selected)
                report["completed_calls"] += 1
        if source_hash != fingerprint(suite, sources):
            raise ValueError("source changed during run; rerun against a stable source")
        metrics, collisions = summarize(cases, report["observations"], config)
        report.update(metrics=metrics, collision_failures=collisions)
        report["status"] = "passed" if not collisions and all(
            m["passed"] for groups in metrics.values() for m in groups.values()) else "failed"
    except (OSError, ValueError, AttributeError, subprocess.SubprocessError) as error:
        report.update(status="void", error=str(error), metrics={})
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=SUITE)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true", help="Execute configured adapter within explicit call budget")
    mode.add_argument("--check", action="store_true", help="Validate fixture coverage and reciprocal links only")
    parser.add_argument("--output", type=Path, help="Write JSON report to a scratch path; stdout otherwise")
    args = parser.parse_args()
    try:
        if args.check:
            errors = fixture_errors(args.suite)
            print("\n".join(errors) if errors else "Trigger fixture coverage and collision pointers: PASS")
            return int(bool(errors))
        config = json.loads(args.config.read_text(encoding="utf-8"))
        report = run(args.suite, config, execute=args.execute)
        text = json.dumps(report, indent=2) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return {"dry-run": 0, "passed": 0, "failed": 1, "void": 2}[report["status"]]
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Trigger eval blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
