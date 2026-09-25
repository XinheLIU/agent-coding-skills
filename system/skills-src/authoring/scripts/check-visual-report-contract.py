#!/usr/bin/env python3
"""Check that report-producing skills carry the portable visual contract."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    "current/target",
    "inline SVG",
    "Mermaid",
    "320",
    "top recommendation",
)
CONSUMERS = (
    ROOT / "design/technical/acs-audit-architecture",
    ROOT / "design/technical/acs-design-architecture",
    ROOT / "design/technical/acs-design-modules",
    ROOT / "test/review/acs-review-architecture",
    ROOT / "test/review/acs-refactor-code",
    ROOT / "plan/acs-map-current-product",
)


def main() -> int:
    errors: list[str] = []
    canonical = ROOT / "authoring/references/visual-report.md"
    if not canonical.exists():
        errors.append(f"missing canonical contract: {canonical}")
    for skill_dir in CONSUMERS:
        report_reference = "references/html-report.md" if skill_dir.name == "acs-map-current-product" else "references/HTML-REPORT.md"
        for relative in ("SKILL.md", "references/visual-report.md", report_reference):
            path = skill_dir / relative
            if not path.exists():
                errors.append(f"{skill_dir.name}: missing {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            if relative == "references/visual-report.md" and path.resolve() != canonical.resolve():
                errors.append(f"{path}: must resolve to the shared display template")
            if "Last updated:" not in text:
                errors.append(f"{path}: missing Last updated date")
            if relative.startswith("references/") and relative.endswith("visual-report.md"):
                for phrase in REQUIRED:
                    if phrase.lower() not in text.lower():
                        errors.append(f"{path}: missing contract phrase {phrase!r}")
            if "/meta/" in text or "/Users/" in text:
                errors.append(f"{path}: contains non-portable absolute reference")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"visual report contract OK ({len(CONSUMERS)} consumers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
