#!/usr/bin/env python3
"""Read-only coordination mechanics for ACS source checkouts (stdlib only).

Run --help or <command> --help for the local Markdown adapter contract. Hosts
resolve explicit/configured tracker references before calling this adapter; it
never guesses branch identity, claims work, changes status, or grants authority.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

# Importing reused checkers must not write bytecode into the source checkout.
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py"
EVIDENCE = ROOT / "system/skills-src/build/acs-implement/scripts/check-evidence.py"
CONSUMED = re.compile(r"^```acs-consumed-revisions[ \t]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)
DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def status(root: Path) -> dict:
    scanner = load_module("acs_task_scanner", SCANNER)
    return scanner.status_report(scanner.scan(root))


def resolve(root: Path, ticket: str | None) -> dict:
    """Resolve existing canonical IDs only; local IDs must be unambiguous."""
    report = status(root)
    if ticket is None:
        return {"root": report["root"], "tickets": [
            {key: row[key] for key in ("id", "source_file", "source_revision")}
            for row in report["tickets"]
        ]}
    matches = [row for row in report["tickets"]
               if ticket in (row["id"], row["id"].split("/", 1)[1])]
    if len(matches) != 1:
        raise ValueError(f"IDENTITY-UNRESOLVED: {ticket!r} matches {len(matches)} tickets; supply change/task ID")
    return {key: matches[0][key] for key in ("id", "source_file", "source_revision")}


def freshness(root: Path) -> dict:
    """Scan in-record JSON bindings; revisions hash exact source file bytes.

    Each acs-consumed-revisions fence contains a nonempty JSON array of objects:
    source (path relative to the owning record), revision (sha256:<hex>), scope
    (the conclusion affected). Unsupported identities remain review candidates.
    No fence means unassessed, never evidence of current premises. This adapter
    does not interpret HTML, remote trackers, Git revisions, or material impact.
    """
    root = root.resolve()
    paths = [root] if root.is_file() else sorted(root.rglob("*.md"))
    if not paths:
        raise ValueError(f"NO-RECORDS: {root}")
    report = {"root": str(root), "bindings": [], "needs_review": [], "unassessed": [], "errors": []}
    for record in paths:
        text = record.read_text(encoding="utf-8")
        blocks = CONSUMED.findall(text)
        if text.count("```acs-consumed-revisions") != len(blocks):
            report["errors"].append(f"{record}: INVALID-BINDINGS: malformed fence")
        if not blocks:
            report["unassessed"].append(str(record))
        for block in blocks:
            try:
                rows = json.loads(block)
                if not isinstance(rows, list) or not rows:
                    raise ValueError("expected nonempty array")
                for row in rows:
                    if not isinstance(row, dict) or any(
                        not isinstance(row.get(key), str) or not row[key].strip()
                        for key in ("source", "revision", "scope")
                    ):
                        raise ValueError("each binding needs nonempty source, revision and scope")
            except ValueError as error:
                report["errors"].append(f"{record}: INVALID-BINDINGS: {error}")
                continue
            for row in rows:
                source = (record.parent / row["source"]).resolve()
                current = None
                reason = None
                if not DIGEST.fullmatch(row["revision"]):
                    reason = "UNSUPPORTED-REVISION"
                else:
                    try:
                        current = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
                    except OSError:
                        reason = "SOURCE-UNAVAILABLE"
                    else:
                        if current != row["revision"]:
                            reason = "CHANGED-PREMISE"
                binding = {"record": str(record), "source": str(source), "scope": row["scope"],
                           "consumed_revision": row["revision"], "current_revision": current,
                           "freshness": "needs review" if reason else "current", "reason": reason}
                report["bindings"].append(binding)
                if reason:
                    report["needs_review"].append(binding)
    report["warnings"] = ["Only explicit file-hash bindings are assessed; the domain owner judges material impact and propagation."]
    return report


def checks(plugins: Path, only: str) -> dict:
    """Run fixed repository checks, never commands supplied by evidence or tickets."""
    commands = {
        "catalog": [sys.executable, "-B", "system/evals/validate_suite.py"],
        "protocols": [sys.executable, "-B", "scripts/validate-protocols.py", "--plugins", str(plugins.resolve())],
        "derived": [sys.executable, "-B", "scripts/build-plugins.py", "--check", "--output", str(plugins.resolve())],
    }
    results = []
    for name, command in commands.items():
        if only != "all" and name != only:
            continue
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        results.append({"check": name, "command": command, "exit_code": process.returncode,
                        "stdout": process.stdout, "stderr": process.stderr})
    return {"checks": results, "passed": all(row["exit_code"] == 0 for row in results)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, description in (
        ("resolve", "Resolve canonical task IDs, paths and record hashes; ambiguous local IDs fail."),
        ("status", "Report B14 status, frontier and one next action; does not verify execution."),
        ("freshness", freshness.__doc__),
    ):
        command = commands.add_parser(name, description=description)
        command.add_argument("root", type=Path, help="Explicit local change/changes directory; freshness also accepts a Markdown file")
        if name == "resolve":
            command.add_argument("--ticket", help="Canonical change/task ID or unambiguous local task ID")
    command = commands.add_parser("verify", description="Check recorded evidence via B19, without executing its commands.")
    command.add_argument("evidence", type=Path)
    command.add_argument("--base", required=True, help="Immutable dispatch identity")
    command.add_argument("--revision", required=True, help="Independently resolved completion identity")
    command = commands.add_parser("checks", description=checks.__doc__)
    command.add_argument("--plugins", type=Path, default=ROOT / "plugins")
    command.add_argument("--only", choices=("all", "catalog", "protocols", "derived"), default="all")
    args = parser.parse_args()
    try:
        if args.command == "resolve":
            report = resolve(args.root, args.ticket)
        elif args.command == "status":
            report = status(args.root)
        elif args.command == "freshness":
            report = freshness(args.root)
        elif args.command == "verify":
            if not args.base.strip() or not args.revision.strip():
                raise ValueError("INVALID-IDENTITY: base and revision must be nonempty")
            checker = load_module("acs_evidence_checker", EVIDENCE)
            errors = checker.evidence_errors(json.loads(args.evidence.read_text(encoding="utf-8")),
                                             base=args.base, revision=args.revision)
            report = {"base": args.base, "revision": args.revision, "errors": errors, "passed": not errors}
        else:
            report = checks(args.plugins, args.only)
    except (OSError, ValueError) as error:
        report = {"errors": [str(error)]}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return int(bool(report.get("errors") or report.get("needs_review") or report.get("passed") is False))


if __name__ == "__main__":
    raise SystemExit(main())
