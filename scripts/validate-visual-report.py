#!/usr/bin/env python3
"""Validate standalone report references and basic visual-report structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CONSUMERS = (
    Path("system/skills-src/design/technical/acs-audit-architecture"),
    Path("system/skills-src/test/review/acs-review-architecture"),
    Path("system/skills-src/plan/acs-map-current-product"),
)

def check_standalone_references(root: Path) -> list[str]:
    errors: list[str] = []
    for consumer in CONSUMERS:
        skill = root / consumer / "SKILL.md"
        local_reference = root / consumer / "references/visual-report.md"
        if not skill.is_file():
            errors.append(f"missing skill: {skill}")
            continue
        if not local_reference.is_file():
            errors.append(f"missing local visual reference: {local_reference}")
        text = skill.read_text(encoding="utf-8")
        if "references/visual-report.md" not in text:
            errors.append(f"skill does not declare visual reference: {skill}")
    return errors

def check_html(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not any(marker in text for marker in ("top-recommendation", "Top recommendation", "Recommended order")):
        errors.append(f"missing top recommendation marker: {path}")
    if text.lower().count("before") and not text.lower().count("after"):
        errors.append(f"before visual has no after counterpart: {path}")
    anchors = set(re.findall(r'id=["\']([^"\']+)', text))
    for target in re.findall(r'href=["\']#([^"\']+)', text):
        if target not in anchors:
            errors.append(f"broken internal link #{target} in {path}")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("html", nargs="*", type=Path)
    args = parser.parse_args()
    errors = check_standalone_references(args.root)
    for path in args.html:
        errors.extend(check_html(path))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("visual report validation passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
