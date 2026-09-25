#!/usr/bin/env python3
"""Dependency-free structural checks for this suite; not a runtime Harness.

Validates the deliberately constrained six-field YAML declaration syntax, source
skill discovery, and suite-local Markdown references. Behavioral scenarios in
evals/evals require an isolated agent run; this script does not execute them.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import TypedDict
from urllib.parse import unquote

SUITE = Path(__file__).resolve().parents[1]
FIELDS = {"requires", "retrieves", "produces", "updates", "invalidates", "handoff_to"}
FENCE = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.MULTILINE | re.DOTALL)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SELECTOR = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*\Z")


class Category(TypedDict):
    id: str
    skills: list[str]


class Catalog(TypedDict):
    schemaVersion: int
    id: str
    sourcePattern: str
    categories: list[Category]


class Plugin(TypedDict):
    name: str
    skills: str


def inventory_errors(suite: Path = SUITE) -> list[str]:
    """Compare public identities with actual source, discovery and catalog paths."""
    errors: list[str] = []
    sources = sorted((suite / "skills-src").rglob("SKILL.md"))
    names = [path.parent.name for path in sources]
    if not names:
        errors.append("no source skills discovered")
    for name, count in Counter(names).items():
        if count > 1:
            errors.append(f"duplicate source skill: {name}")
    for source in sources:
        name = source.parent.name
        relative = source.relative_to(suite)
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", source.read_text(), re.DOTALL)
        if not re.fullmatch(r"acs-[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{relative}: skill ID must use the acs- namespace (max 64 characters)")
        if not frontmatter or not re.search(rf"^name: {re.escape(name)}$", frontmatter[1], re.MULTILINE) or not re.search(r"^description: .+", frontmatter[1], re.MULTILINE):
            errors.append(f"{relative}: invalid name/description")
        discovery = suite / "skills" / name
        if not discovery.is_symlink() or discovery.resolve() != source.parent.resolve():
            errors.append(f"{relative}: discovery entry must symlink to this source")
    discovery_root = suite / "skills"
    entries = list(discovery_root.iterdir()) if discovery_root.is_dir() else []
    for entry in entries:
        if entry.name not in names:
            errors.append(f"skills/{entry.name}: unexpected discovery entry")

    catalog_path = suite.parent / "catalog/skill-set.json"
    try:
        catalog: Catalog = json.loads(catalog_path.read_text())
        if catalog["schemaVersion"] != 1 or catalog["id"] != "agent-coding-skills":
            errors.append("catalog: unsupported schema or product identity")
        catalog_names: list[str] = []
        for category in catalog["categories"]:
            for name in category["skills"]:
                catalog_names.append(name)
                target = suite.parent / catalog["sourcePattern"].replace("{category}", category["id"]).replace("{skill}", name)
                if target not in sources:
                    errors.append(f"catalog: {name} does not resolve to a canonical source")
        for name, count in Counter(catalog_names).items():
            if count > 1:
                errors.append(f"catalog: duplicate skill {name}")
        for name in sorted(set(names) - set(catalog_names)):
            errors.append(f"catalog: missing skill {name}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f"catalog: cannot read inventory: {error}")

    for host in ("codex", "claude"):
        path = suite / f".{host}-plugin/plugin.json"
        try:
            plugin: Plugin = json.loads(path.read_text())
            if plugin["name"] != "agent-coding-skills" or (suite / plugin["skills"]).resolve() != discovery_root.resolve():
                errors.append(f"{path.relative_to(suite)}: plugin identity or skill root differs")
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f"{path.relative_to(suite)}: invalid manifest: {error}")

    context_root = suite.parent / "plugins/context-management/skills"
    if context_root.is_dir():
        expected = {"acs-init-context", "acs-sync-context", "acs-translate-agent-context"}
        if {entry.name for entry in context_root.iterdir()} != expected:
            errors.append("context subpackage: unexpected skill inventory")
        # Content is rewritten during portable materialization; byte equality
        # with sources would reject correctly relocated links. Package closure
        # is exercised by build-context-plugin and isolated package tests.
        for name in sorted(expected):
            if not (context_root / name / "SKILL.md").is_file():
                errors.append(f"context subpackage: missing entrypoint {name}")
    return errors


class HtmlAnchors(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key == "id" and value:
                self.anchors.add(value)


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    parser = HtmlAnchors()
    parser.feed(text)
    result = parser.anchors
    seen: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", FENCE.sub("", text), re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def reference_errors(path: Path, boundary: Path) -> list[str]:
    """Check concrete relative links only; templates/URLs are not local inputs."""
    errors: list[str] = []
    text = FENCE.sub("", path.read_text(encoding="utf-8"))
    for reference in LINK.findall(text):
        raw = reference.strip().split(' "', 1)[0]
        if "://" in raw or raw.startswith(("/", "mailto:")) or any(c in raw for c in "<>{}*"):
            continue
        file_part, _, fragment = raw.partition("#")
        target = (path.parent / unquote(file_part)).resolve() if file_part else path.resolve()
        if target.is_relative_to(boundary.resolve().parent / "references"):
            continue  # Optional read-only provenance may be absent from a clone.
        if not target.exists():
            errors.append(f"broken reference: {reference}")
        elif fragment and target.is_file() and target.suffix in {".md", ".html"}:
            if unquote(fragment) not in anchors(target):
                errors.append(f"missing anchor: {reference}")
    return errors


def declaration_errors(text: str) -> list[str]:
    blocks = re.findall(r"^```yaml\n(context:\n.*?)^```[ \t]*$", text, re.MULTILINE | re.DOTALL)
    if len(blocks) != 1:
        return [f"expected one context declaration, found {len(blocks)}"]
    errors: list[str] = []
    seen: set[str] = set()
    protocol = (SUITE / "protocols/skill-declarations.md").read_text()
    consumers = protocol.split("## Handoff consumers\n", 1)[1].split("\n## ", 1)[0]
    handoff_consumers = set(re.findall(r"^\| `([^`]+)` \|", consumers, re.MULTILINE))
    for line in blocks[0].splitlines()[1:]:
        match = re.fullmatch(r"  ([a-z_]+): \[([^\[\]]*)\]", line)
        if not match:
            errors.append(f"invalid declaration line: {line}")
            continue
        field, values = match.groups()
        if field in seen:
            errors.append(f"duplicate context field: {field}")
        seen.add(field)
        selectors = [value.strip() for value in values.split(",")] if values.strip() else []
        if field == "handoff_to":
            unknown = sorted(set(selectors) - handoff_consumers)
            if unknown:
                errors.append(f"undefined handoff consumers: {unknown}")
        if len(selectors) != len(set(selectors)) or any(not SELECTOR.fullmatch(v) for v in selectors):
            errors.append(f"invalid or duplicate selectors: {field}")
    if seen != FIELDS:
        errors.append(f"context fields: missing={sorted(FIELDS - seen)}, unknown={sorted(seen - FIELDS)}")
    return errors


def validate(suite: Path = SUITE, *, inventory_only: bool = False) -> list[str]:
    errors = inventory_errors(suite)
    if inventory_only:
        return errors
    skills = sorted((suite / "skills-src").rglob("SKILL.md"))
    for path in skills:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(suite)
        for error in declaration_errors(text):
            errors.append(f"{relative}: {error}")
    excluded = {"IMPLEMENTATION-SUMMARY.md", "MEMORY-ENHANCEMENT-ANALYSIS.md"}
    for path in suite.rglob("*"):
        if path.is_symlink():
            if not path.exists():
                errors.append(f"{path.relative_to(suite)}: broken symlink")
            continue
        if path.suffix != ".md" or path.name in excluded:
            continue
        for error in reference_errors(path, suite):
            errors.append(f"{path.relative_to(suite)}: {error}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory-only", action="store_true", help="Check source, discovery, catalog, manifests and context package identity only")
    args = parser.parse_args()
    findings = validate(inventory_only=args.inventory_only)
    for finding in findings:
        print(finding)
    count = sum(1 for _ in (SUITE / "skills-src").rglob("SKILL.md"))
    checks = "inventory" if args.inventory_only else "inventory, declarations, local links/anchors"
    print(f"{count} source skills; {checks}: {'FAIL' if findings else 'PASS'}")
    sys.exit(bool(findings))
