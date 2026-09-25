#!/usr/bin/env python3
"""Project canonical docs/changes/<change>/tasks/*.md tickets into a DAG manifest.

Accepts one change directory or a directory containing changes. Dependencies are
comma-separated local task IDs or change/task IDs. Other tracker formats use a
separate derived manifest; this adapter never rewrites source tickets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import TypedDict


class TicketNode(TypedDict, total=False):
    id: str
    row: str
    title: str
    status_raw: str
    done: bool
    in_progress: bool
    execution_ready: bool
    deps: list[str]
    tags: list[str]
    unresolved_dep_text: str
    source_file: str
    source_revision: str
    ticket_type: str
    readiness: str
    scope: str
    inputs: str
    verification: str
    blockers: str
    evidence: str


class Workstream(TypedDict):
    key: str
    label: str


class Manifest(TypedDict):
    root: str
    workstreams: list[Workstream]
    nodes: list[TicketNode]
    warnings: list[str]
    unresolved_dep_count: int


def field(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(.*)$", text, re.MULTILINE)
    return match[1].strip() if match else ""


def section(text: str, name: str) -> str:
    match = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match[1].strip() if match else ""


def scan(root: Path) -> Manifest:
    root = root.resolve()
    changes = [root] if (root / "tasks").is_dir() else sorted(
        path for path in root.iterdir() if (path / "tasks").is_dir()
    )
    nodes: list[TicketNode] = []
    warnings: list[str] = []
    for change in changes:
        for path in sorted((change / "tasks").glob("*.md")):
            source = path.read_bytes()
            text = source.decode("utf-8")
            heading = re.search(r"^# ([^:\n]+): (.+)$", text, re.MULTILINE)
            if not heading or heading[1] != path.stem:
                raise ValueError(f"{path}: expected '# {path.stem}: <title>'")
            node_id = f"{change.name}/{path.stem}"
            status = field(text, "Status")
            kind = field(text, "Type")
            readiness = field(text, "Readiness")
            if status not in {"pending", "in_progress", "done", "failed", "superseded"}:
                warnings.append(f"{node_id}: unknown/missing Status; not execution-ready")
            if kind not in {"implementation", "design"}:
                warnings.append(f"{node_id}: unknown/missing Type; not execution-ready")
            if readiness not in {"ready", "needs-design", "needs-criteria", "needs-review"}:
                warnings.append(f"{node_id}: unknown/missing Readiness; not execution-ready")
            raw_deps = field(text, "depends_on")
            deps: list[str] = []
            unresolved: list[str] = []
            if not raw_deps:
                warnings.append(f"{node_id}: missing depends_on; use 'none' for no dependencies")
            elif raw_deps != "none":
                for dependency in raw_deps.split(","):
                    dependency = dependency.strip()
                    if not re.fullmatch(r"[\w.-]+(?:/[\w.-]+)?", dependency):
                        unresolved.append(dependency)
                        continue
                    deps.append(dependency if "/" in dependency else f"{change.name}/{dependency}")
            if unresolved:
                warnings.append(f"{node_id}: unresolved dependencies: {', '.join(unresolved)}")
            nodes.append({
                "id": node_id,
                "row": change.name,
                "title": heading[2],
                "status_raw": status,
                "done": status == "done" and kind in {"implementation", "design"}
                    and readiness == "ready" and bool(raw_deps) and not unresolved,
                "in_progress": status == "in_progress",
                "execution_ready": kind == "implementation" and readiness == "ready"
                    and status == "pending" and bool(raw_deps) and not unresolved,
                "deps": list(dict.fromkeys(deps)),
                "tags": [kind or "unknown-type", readiness or "needs-review", status or "unknown-status"],
                "unresolved_dep_text": ", ".join(unresolved),
                "source_file": str(path),
                "source_revision": "sha256:" + hashlib.sha256(source).hexdigest(),
                "ticket_type": kind,
                "readiness": readiness,
                "scope": section(text, "Scope"),
                "inputs": section(text, "Inputs"),
                "verification": section(text, "Verification"),
                "blockers": section(text, "Blockers"),
                "evidence": section(text, "Evidence"),
            })
    if not nodes:
        raise ValueError(f"{root}: no canonical tasks found")
    return {
        "root": str(root),
        "workstreams": [{"key": path.name, "label": path.name} for path in changes],
        "nodes": nodes,
        "warnings": warnings,
        "unresolved_dep_count": sum(bool(node["unresolved_dep_text"]) for node in nodes),
    }


def validate_graph(nodes: list[TicketNode]) -> None:
    """Validate the final graph, including edges supplied through an overlay."""
    dependencies = {node["id"]: node["deps"] for node in nodes}
    if len(dependencies) != len(nodes):
        raise ValueError("Duplicate ticket IDs")
    for node_id, deps in dependencies.items():
        missing = set(deps) - dependencies.keys()
        if missing:
            raise ValueError(f"{node_id}: missing prerequisite IDs: {sorted(missing)}")
    remaining = {node_id: set(deps) for node_id, deps in dependencies.items()}
    while remaining:
        frontier = {node_id for node_id, deps in remaining.items() if not deps}
        if not frontier:
            raise ValueError(f"Dependency cycle among: {sorted(remaining)}")
        remaining = {node_id: deps - frontier for node_id, deps in remaining.items() if node_id not in frontier}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("-o", "--out", type=Path, required=True)
    args = parser.parse_args()
    manifest = scan(args.root)
    validate_graph(manifest["nodes"])
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    for warning in manifest["warnings"]:
        print(f"warning: {warning}")
    print(f"Scanned {len(manifest['nodes'])} tickets -> {args.out}")


if __name__ == "__main__":
    main()
