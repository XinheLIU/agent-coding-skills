#!/usr/bin/env python3
"""Migrate relative protocol references to logical protocol IDs.

Replaces filesystem-dependent relative paths with stable logical IDs:
  ../../../craft/context/acs-init-context/references/PROTOCOL.md
    -> protocol:acs:skill-declarations

  ../../../../workflows/context-coordination.md
    -> protocol:acs:context-coordination
"""
from __future__ import annotations

import re
from pathlib import Path

SUITE = Path(__file__).resolve().parents[1] / "system"

# Mapping from old relative path patterns to new protocol IDs
PROTOCOL_MIGRATIONS = {
    # PROTOCOL.md -> skill-declarations
    r'\.\./\.\./\.\./craft/context/acs-init-context/references/PROTOCOL\.md': 'protocol:acs:skill-declarations',
    r'\.\./acs-init-context/references/PROTOCOL\.md': 'protocol:acs:skill-declarations',
    r'references/PROTOCOL\.md': 'protocol:acs:skill-declarations',

    # context-coordination.md
    r'\.\./\.\./\.\./\.\./workflows/context-coordination\.md': 'protocol:acs:context-coordination',
    r'\.\./\.\./\.\./workflows/context-coordination\.md': 'protocol:acs:context-coordination',

    # orchestration-protocol.md
    r'references/orchestration-protocol\.md': 'protocol:acs:orchestration',

    # domain memory contracts
    r'\.\./\.\./\.\./craft/context/acs-init-context/references/design-memory\.md': 'protocol:acs:design-memory',
    r'\.\./acs-init-context/references/design-memory\.md': 'protocol:acs:design-memory',
    r'references/design-memory\.md': 'protocol:acs:design-memory',

    r'\.\./\.\./\.\./craft/context/acs-init-context/references/engineering-memory\.md': 'protocol:acs:engineering-memory',
    r'\.\./acs-init-context/references/engineering-memory\.md': 'protocol:acs:engineering-memory',
    r'references/engineering-memory\.md': 'protocol:acs:engineering-memory',

    r'\.\./\.\./\.\./craft/context/acs-init-context/references/operations-memory\.md': 'protocol:acs:operations-memory',
    r'\.\./acs-init-context/references/operations-memory\.md': 'protocol:acs:operations-memory',
    r'references/operations-memory\.md': 'protocol:acs:operations-memory',

    r'\.\./\.\./\.\./craft/context/acs-init-context/references/product-memory\.md': 'protocol:acs:product-memory',
    r'\.\./acs-init-context/references/product-memory\.md': 'protocol:acs:product-memory',
    r'references/product-memory\.md': 'protocol:acs:product-memory',
}


def migrate_file(path: Path) -> tuple[bool, list[str]]:
    """Migrate protocol references in one file.

    Returns (changed, list_of_changes)
    """
    content = path.read_text(encoding='utf-8')
    original = content
    changes = []

    # Track which patterns we matched
    for pattern, protocol_id in PROTOCOL_MIGRATIONS.items():
        # Look for markdown links: [text](relative/path.md)
        # Match both with and without anchors
        link_pattern = rf'\[([^\]]+)\]\(({pattern})(#[^\)]+)?\)'
        matches = re.findall(link_pattern, content)

        if matches:
            # Replace with protocol ID, preserving anchor if present
            def replace_link(match):
                text = match.group(1)
                anchor = match.group(3) or ''
                # Remove the anchor part from protocol ID reference (protocols use their own section structure)
                return f'[{text}]({protocol_id})'

            content = re.sub(link_pattern, replace_link, content)
            for match in matches:
                old_path = match[1] + (match[2] if len(match) > 2 else '')
                changes.append(f"  {old_path} -> {protocol_id}")

    if content != original:
        path.write_text(content, encoding='utf-8')
        return True, changes

    return False, []


def main() -> None:
    skills = sorted((SUITE / "skills-src").rglob("SKILL.md"))
    workflows = sorted((SUITE / "workflows").glob("*.md"))

    total_files = 0
    total_changes = 0

    print("Migrating protocol references to logical IDs...\n")

    for path in skills + workflows:
        changed, changes = migrate_file(path)
        if changed:
            total_files += 1
            total_changes += len(changes)
            rel_path = path.relative_to(SUITE)
            print(f"✓ {rel_path}")
            for change in changes:
                print(change)
            print()

    print(f"\nMigration complete:")
    print(f"  {total_files} files modified")
    print(f"  {total_changes} references migrated")

    # Verify no remaining references
    print("\nVerifying migration...")
    remaining = []
    for path in skills:
        content = path.read_text(encoding='utf-8')
        for pattern in PROTOCOL_MIGRATIONS.keys():
            if re.search(pattern, content):
                remaining.append((path.relative_to(SUITE), pattern))

    if remaining:
        print("\n⚠ Warning: Some relative paths remain:")
        for path, pattern in remaining:
            print(f"  {path}: {pattern}")
    else:
        print("✓ All relative protocol paths migrated successfully")


if __name__ == "__main__":
    main()
