#!/usr/bin/env python3
"""Validate standalone report references and basic visual-report structure."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

CONSUMERS = (
    Path("system/skills-src/design/technical/acs-technical-design"),
    Path("system/skills-src/design/technical/acs-design-architecture"),
    Path("system/skills-src/design/technical/acs-design-modules"),
    Path("system/skills-src/design/technical/acs-design-contracts"),
    Path("system/skills-src/design/technical/acs-design-test-strategy"),
    Path("system/skills-src/design/technical/acs-trace-requirements"),
    Path("system/skills-src/plan/acs-map-current-product"),
)

REPORT_VALIDATOR = Path("system/skills-src/authoring/scripts/validate-report-html.py")

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

def check_html(root: Path, path: Path) -> list[str]:
    """Delegate to the shipped per-card validator so there is one HTML checker."""
    spec = importlib.util.spec_from_file_location("validate_report_html", root / REPORT_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [f"{path}: {error}" for error in module.validate(path)]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("html", nargs="*", type=Path)
    args = parser.parse_args()
    errors = check_standalone_references(args.root)
    for path in args.html:
        errors.extend(check_html(args.root, path))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("visual report validation passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
