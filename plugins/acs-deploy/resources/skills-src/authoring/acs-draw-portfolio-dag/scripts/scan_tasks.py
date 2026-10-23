#!/usr/bin/env python3
"""Project canonical docs/changes/<change>/tasks/*.md tickets into a DAG manifest.

Accepts one change directory or a directory containing changes. Dependencies are
comma-separated local task IDs or change/task IDs. Other tracker formats use a
separate derived manifest; this adapter never rewrites source tickets.
Use --json for status on stdout, -o for the original renderer manifest, or both.
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


class TicketStatus(TypedDict):
    id: str
    status: str
    readiness: str
    ticket_type: str
    deps: list[str]
    execution_ready: bool
    missing_dependencies: list[str]
    blocked_dependencies: list[str]
    unresolved_dep_text: str
    source_file: str
    source_revision: str


class NextAction(TypedDict):
    action: str
    ticket_id: str | None


class StatusReport(TypedDict):
    root: str
    tickets: list[TicketStatus]
    frontier: list[str]
    next: NextAction
    warnings: list[str]


# Adapted from OpenSpec openspec-propose:107-137 (bae58cf).
STATUS_CAVEAT = (
    "Status shows a record's state, not whether its prerequisites were satisfied; "
    "dependency checks use recorded completion and do not verify execution evidence."
)


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


def status_report(manifest: Manifest) -> StatusReport:
    """Project record state and direct dependency readiness without changing it.

    Missing IDs are reportable here; the renderer manifest remains strict.
    Existing done semantics include type/readiness checks, not evidence auditing.
    Next chooses the first stable ID in frontier, active work, then unresolved
    work. Superseded records need no next action but cannot satisfy dependencies.
    """
    nodes = sorted(manifest["nodes"], key=lambda node: node["id"])
    by_id = {node["id"]: node for node in nodes}
    # Keep cycle and duplicate-ID checks, ignoring only absent prerequisite IDs.
    validate_graph([
        {**node, "deps": [dep for dep in node["deps"] if dep in by_id]}
        for node in nodes
    ])
    tickets: list[TicketStatus] = []
    frontier: list[str] = []
    active: list[str] = []
    unresolved: list[str] = []
    for node in nodes:
        missing = [dep for dep in node["deps"] if dep not in by_id]
        blocked = [dep for dep in node["deps"] if dep in by_id and not by_id[dep]["done"]]
        ready = node["execution_ready"] and not missing and not blocked
        tickets.append({
            "id": node["id"],
            "status": node["status_raw"],
            "readiness": node["readiness"],
            "ticket_type": node["ticket_type"],
            "deps": node["deps"],
            "execution_ready": ready,
            "missing_dependencies": missing,
            "blocked_dependencies": blocked,
            "unresolved_dep_text": node["unresolved_dep_text"],
            "source_file": node["source_file"],
            "source_revision": node["source_revision"],
        })
        if ready:
            frontier.append(node["id"])
        if node["in_progress"]:
            active.append(node["id"])
        if node["status_raw"] != "superseded" and (not node["done"] or missing or blocked):
            unresolved.append(node["id"])
    next_action: NextAction
    if frontier:
        next_action = {"action": "implement", "ticket_id": frontier[0]}
    elif active:
        next_action = {"action": "wait", "ticket_id": active[0]}
    elif unresolved:
        next_action = {"action": "resolve_blockers", "ticket_id": unresolved[0]}
    else:
        next_action = {"action": "complete", "ticket_id": None}
    return {
        "root": manifest["root"],
        "tickets": tickets,
        "frontier": frontier,
        "next": next_action,
        "warnings": [STATUS_CAVEAT, *manifest["warnings"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("-o", "--out", type=Path, help="write the renderer manifest")
    parser.add_argument("--json", action="store_true", help="print machine-readable status to stdout")
    args = parser.parse_args()
    if not args.out and not args.json:
        parser.error("at least one of -o/--out or --json is required")
    manifest = scan(args.root)
    if args.out:
        validate_graph(manifest["nodes"])
        args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.json:
        print(json.dumps(status_report(manifest), indent=2, ensure_ascii=False))
    else:
        for warning in manifest["warnings"]:
            print(f"warning: {warning}")
        print(f"Scanned {len(manifest['nodes'])} tickets -> {args.out}")


if __name__ == "__main__":
    main()
