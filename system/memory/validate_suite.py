#!/usr/bin/env python3
"""Dependency-free structural checks for this suite; not a runtime Harness.

Validates the deliberately constrained six-field YAML declaration syntax, source
skill discovery, and suite-local Markdown references. Behavioral scenarios in
memory/evals require an isolated agent run; this script does not execute them.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

SUITE = Path(__file__).resolve().parents[1]
FIELDS = {"requires", "retrieves", "produces", "updates", "invalidates", "handoff_to"}
FENCE = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.MULTILINE | re.DOTALL)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SELECTOR = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*\Z")


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
        if not target.is_relative_to(boundary.resolve()):
            continue  # External provenance is outside this suite's reference audit.
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
        if len(selectors) != len(set(selectors)) or any(not SELECTOR.fullmatch(v) for v in selectors):
            errors.append(f"invalid or duplicate selectors: {field}")
    if seen != FIELDS:
        errors.append(f"context fields: missing={sorted(FIELDS - seen)}, unknown={sorted(seen - FIELDS)}")
    return errors


def validate(suite: Path = SUITE) -> list[str]:
    errors: list[str] = []
    skills = sorted((suite / "skills-src").rglob("SKILL.md"))
    if len(skills) != 45:
        errors.append(f"expected 45 source skills, found {len(skills)}")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(suite)
        for error in declaration_errors(text):
            errors.append(f"{relative}: {error}")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not frontmatter:
            errors.append(f"{relative}: missing frontmatter")
        elif not re.search(rf"^name: {re.escape(path.parent.name)}$", frontmatter[1], re.MULTILINE) or not re.search(r"^description: .+", frontmatter[1], re.MULTILINE):
            errors.append(f"{relative}: invalid name/description")
        discovery = suite / "skills" / path.parent.name
        if not discovery.is_symlink() or discovery.resolve() != path.parent.resolve():
            errors.append(f"{relative}: discovery entry must symlink to this source")
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
    findings = validate()
    for finding in findings:
        print(finding)
    print(f"45 source skills, discovery symlinks, declarations, local links/anchors: {'FAIL' if findings else 'PASS'}")
    sys.exit(bool(findings))
