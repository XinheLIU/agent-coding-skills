#!/usr/bin/env python3
"""Scan a shared-memory work tree into a portfolio DAG manifest.

Expects, under a root directory, one subdirectory per workstream, each
containing a map.md or spec.md and an issues/ folder of NN-slug.md ticket
files. Extracts titles,
status lines, and same-workstream "Blocked by: NN — ..." references
mechanically. Cross-workstream references are usually prose ("the
metric-honesty workstream must land first") without a stable ticket
number, so this script only *flags* them under unresolved_deps for a
human or agent to read and turn into an explicit edge in an overlay
file — it does not guess.

Usage:
    python3 scan_specs.py <specs_root> -o manifest.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ISSUE_RE = re.compile(r"^(\d+)-.+\.md$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
ISSUE_TITLE_RE = re.compile(r"^\d+\s*[—\-–]\s*(.+)$")
FIELD_RE = re.compile(
    r"^\*\*({name})\*\*:?\s*(.*)$".format(name="Blocked by|Status|Depends on"),
    re.MULTILINE,
)
SPEC_STATUS_RE = re.compile(r"^Status:\s*(.+)$", re.MULTILINE)
SPEC_DEPENDS_RE = re.compile(r"^Depends on:\s*(.+)$", re.MULTILINE)
SPEC_PORTFOLIO_RE = re.compile(r"^Portfolio:\s*(.+)$", re.MULTILINE)
LOCAL_REF_RE = re.compile(r"\b(\d{2})\s*[—\-–]")

STOPWORDS = {"and", "the", "of", "to", "for", "a", "an"}


def slug_prefix(name: str, taken: set) -> str:
    parts = [p for p in re.split(r"[-_]", name) if p and p.lower() not in STOPWORDS]
    base = "".join(p[0] for p in parts[:3]).upper() or "WS"
    prefix = base
    n = 1
    while prefix in taken:
        n += 1
        prefix = f"{base}{n}"
    taken.add(prefix)
    return prefix


def parse_field_block(text: str, field: str) -> str:
    """Grab the text after '**field:**' (colon inside or outside the bold) up to
    the next blank line or next bold field."""
    m = re.search(r"\*\*" + re.escape(field) + r":?\*\*:?\s*(.*)", text)
    if not m:
        return ""
    start = m.end()
    rest = text[start:]
    stop = re.search(r"\n\s*\n|\n\*\*\w", rest)
    tail = rest[: stop.start()] if stop else rest
    return (m.group(1) + tail).strip().replace("\n", " ")


def is_done(status_text: str) -> bool:
    normalized = status_text.strip().lower()
    if re.search(r"\b(not done|not completed|incomplete|unmerged)\b", normalized):
        return False
    if re.search(r"\b(done|completed|merged)\b", normalized):
        return True
    return bool(re.fullmatch(r"(?:commit\s+)?[0-9a-f]{7,40}", normalized))


def scan_workstream(dir_path: Path, prefix: str, warnings: list) -> dict:
    source_path = dir_path / "map.md"
    if not source_path.exists():
        source_path = dir_path / "spec.md"
    source_text = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
    h1 = H1_RE.search(source_text)
    label = h1.group(1) if h1 else dir_path.name
    status_m = SPEC_STATUS_RE.search(source_text)
    depends_m = SPEC_DEPENDS_RE.search(source_text)
    portfolio_m = SPEC_PORTFOLIO_RE.search(source_text)
    ws = {
        "key": prefix,
        "dir": dir_path.name,
        "label": label,
        "status": status_m.group(1).strip() if status_m else "",
        "note": portfolio_m.group(1).strip() if portfolio_m else "",
        "spec_depends_on": depends_m.group(1).strip() if depends_m else "",
        "source_file": (
            str(source_path.relative_to(dir_path.parent.parent))
            if source_path.exists()
            else None
        ),
    }
    if not source_path.exists():
        warnings.append(f"{dir_path.name}: no map.md or spec.md found")
    return ws


def scan_issues(dir_path: Path, prefix: str, warnings: list) -> list:
    issues_dir = dir_path / "issues"
    nodes = []
    if not issues_dir.exists():
        warnings.append(f"{dir_path.name}: no issues/ folder found")
        return nodes
    for f in sorted(issues_dir.glob("*.md")):
        m = ISSUE_RE.match(f.name)
        if not m:
            warnings.append(f"{f}: filename does not match NN-slug.md, skipped")
            continue
        num = m.group(1)
        node_id = f"{prefix}{num}"
        text = f.read_text(encoding="utf-8")
        h1 = H1_RE.search(text)
        raw_title = h1.group(1) if h1 else f.stem
        tm = ISSUE_TITLE_RE.match(raw_title)
        title = f"{num} {tm.group(1)}" if tm else raw_title
        blocked_by = parse_field_block(text, "Blocked by")
        status = parse_field_block(text, "Status")
        deps, unresolved_clauses = [], []
        for clause in blocked_by.split(";"):
            clause = clause.strip(" .")
            if not clause or clause.lower().startswith("none"):
                continue
            cm = LOCAL_REF_RE.match(clause)
            if cm:
                dep_num = cm.group(1)
                if dep_num != num:
                    deps.append(f"{prefix}{dep_num}")
            else:
                # No leading "NN —" in this clause: either a cross-workstream
                # reference (its own ticket lives in another workstream's
                # prefix, which this scan cannot know) or free-text context
                # ("explicit approval to add the MySQL driver"). Flag for a
                # human/agent to resolve into an overlay edge; do not guess.
                unresolved_clauses.append(clause)
        unresolved = "; ".join(unresolved_clauses)
        nodes.append(
            {
                "id": node_id,
                "row": prefix,
                "title": title,
                "status_raw": status,
                "done": is_done(status),
                "deps": deps,
                "blocked_by_raw": blocked_by,
                "unresolved_dep_text": unresolved if unresolved and unresolved.lower() not in (
                    "", "none", "none.",
                ) else "",
                "source_file": str(f),
            }
        )
    return nodes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path, help="Directory containing one subfolder per workstream")
    ap.add_argument("-o", "--out", type=Path, default=Path("manifest.json"))
    args = ap.parse_args()

    root = args.root.resolve()
    warnings = []
    taken_prefixes = set()
    workstreams = []
    all_nodes = []

    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if (
            not (d / "map.md").exists()
            and not (d / "spec.md").exists()
            and not (d / "issues").exists()
        ):
            continue
        prefix = slug_prefix(d.name, taken_prefixes)
        workstreams.append(scan_workstream(d, prefix, warnings))
        all_nodes.extend(scan_issues(d, prefix, warnings))

    unresolved_count = sum(1 for n in all_nodes if n["unresolved_dep_text"])
    manifest = {
        "root": str(root),
        "workstreams": workstreams,
        "nodes": all_nodes,
        "warnings": warnings,
        "unresolved_dep_count": unresolved_count,
    }
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Scanned {len(workstreams)} workstreams, {len(all_nodes)} tickets -> {args.out}", file=sys.stderr)
    if unresolved_count:
        print(
            f"{unresolved_count} ticket(s) have prose 'Blocked by' text with no auto-resolved "
            f"ticket number (likely cross-workstream refs). Read manifest['nodes'][*]"
            f"['unresolved_dep_text'] and add explicit deps via an overlay file before rendering.",
            file=sys.stderr,
        )
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
