#!/usr/bin/env python3
"""Validate protocol registry and references in skills.

Checks:
1. All protocol:* references in SKILL.md files exist in registry
2. All protocol files referenced in registry exist on disk
3. All protocols have valid frontmatter (protocol, version, status)
4. No remaining relative paths to shared contracts (../../PROTOCOL.md style)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "system"
PLUGINS = ROOT / "plugins"
PROTOCOL_REF = re.compile(r'protocol:acs:([a-z][a-z0-9-]*)')
MD_LINK = re.compile(r'\[[^\]]*\]\(([^)#]+)(#[^)]*)?\)')


def validate_protocols() -> list[str]:
    """Validate protocol system integrity."""
    errors: list[str] = []

    # Load registry
    registry_path = SUITE / "protocols/registry.json"
    try:
        registry = json.loads(registry_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"Cannot load registry: {e}")
        return errors

    if registry.get("schemaVersion") != 1 or registry.get("namespace") != "acs":
        errors.append("Invalid registry schema or namespace")

    protocols = registry.get("protocols", {})

    # Check all protocol files exist and have valid frontmatter
    for name, spec in protocols.items():
        protocol_file = SUITE / spec["canonical"]
        if not protocol_file.exists():
            errors.append(f"Protocol file missing: {spec['canonical']}")
            continue

        content = protocol_file.read_text()
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not frontmatter_match:
            errors.append(f"{spec['canonical']}: missing frontmatter")
            continue

        frontmatter = frontmatter_match.group(1)
        if f"protocol: acs:{name}" not in frontmatter:
            errors.append(f"{spec['canonical']}: protocol ID mismatch (expected acs:{name})")
        if "version:" not in frontmatter:
            errors.append(f"{spec['canonical']}: missing version")
        if "status:" not in frontmatter:
            errors.append(f"{spec['canonical']}: missing status")

    # Check all protocol references in skills resolve
    skills = sorted((SUITE / "skills-src").rglob("SKILL.md"))
    for skill_path in skills:
        content = skill_path.read_text()
        for match in PROTOCOL_REF.finditer(content):
            protocol_name = match.group(1)
            if protocol_name not in protocols:
                rel_path = skill_path.relative_to(SUITE)
                errors.append(f"{rel_path}: references unknown protocol:acs:{protocol_name}")

    # Check for remaining old-style relative references
    OLD_PATTERNS = [
        (r'\.\./\.\./.*?/references/PROTOCOL\.md', 'references/PROTOCOL.md'),
        (r'\.\./\.\./.*?/workflows/context-coordination\.md', 'workflows/context-coordination.md'),
        (r'references/product-memory\.md(?!\s*\))', 'references/product-memory.md (should use protocol)'),
        (r'references/design-memory\.md(?!\s*\))', 'references/design-memory.md (should use protocol)'),
        (r'references/engineering-memory\.md(?!\s*\))', 'references/engineering-memory.md (should use protocol)'),
    ]

    for skill_path in skills:
        content = skill_path.read_text()
        for pattern, description in OLD_PATTERNS:
            if re.search(pattern, content):
                rel_path = skill_path.relative_to(SUITE)
                errors.append(f"{rel_path}: still contains old reference pattern: {description}")

    return errors


# Plugins built by scripts/build-plugins.py from skills-src. Other
# directories under plugins/ (e.g. a hand-maintained snapshot) are not this
# script's responsibility — their links are reported as warnings, not
# failures, so pre-existing issues there don't block this suite's validation.
BUILT_PLUGINS = {"acs-protocols", "acs-plan", "acs-design", "acs-build", "acs-quality", "acs-craft"}


def validate_built_plugins() -> tuple[list[str], list[str]]:
    """End-to-end check: every relative link in a built plugin's SKILL.md
    must resolve to a real file on disk. Catches broken rewrites that
    validate_protocols() cannot see, since it only checks skills-src (which
    still uses protocol:acs:* logical IDs, not resolved relative paths).

    Returns (errors, warnings): errors are for BUILT_PLUGINS, warnings are
    for any other plugin directory the same scan happens to pass over.
    """
    errors: list[str] = []
    warnings: list[str] = []
    if not PLUGINS.exists():
        return errors, warnings

    for skill_md in sorted(PLUGINS.glob("*/skills/*/SKILL.md")):
        plugin_name = skill_md.relative_to(PLUGINS).parts[0]
        sink = errors if plugin_name in BUILT_PLUGINS else warnings
        content = skill_md.read_text()

        remaining = PROTOCOL_REF.findall(content)
        if remaining:
            rel_path = skill_md.relative_to(ROOT)
            sink.append(f"{rel_path}: unresolved protocol:acs:{remaining[0]} in built plugin")

        for link_target, _anchor in MD_LINK.findall(content):
            if link_target.startswith(("http://", "https://", "protocol:")):
                continue
            resolved = (skill_md.parent / link_target).resolve()
            if not resolved.exists():
                rel_path = skill_md.relative_to(ROOT)
                sink.append(f"{rel_path}: broken link to '{link_target}' (resolved: {resolved})")

    for plugin_json in sorted(PLUGINS.glob("*/.claude-plugin/plugin.json")):
        plugin_dir = plugin_json.parent.parent
        plugin_name = plugin_dir.name
        sink = errors if plugin_name in BUILT_PLUGINS else warnings
        manifest = json.loads(plugin_json.read_text())
        for dep_name in manifest.get("peerDependencies", {}):
            if not (PLUGINS / dep_name).is_dir():
                rel_path = plugin_json.relative_to(ROOT)
                sink.append(f"{rel_path}: peerDependency '{dep_name}' has no plugins/{dep_name}/ directory")

    return errors, warnings


if __name__ == "__main__":
    findings = validate_protocols()
    plugin_errors, plugin_warnings = validate_built_plugins()
    findings += plugin_errors

    for finding in findings:
        print(finding)
    for warning in plugin_warnings:
        print(f"WARNING (pre-existing, outside build-plugins.py's scope): {warning}")

    count = len(list((SUITE / "protocols").glob("*.md")))
    plugin_count = len(BUILT_PLUGINS & {p.name for p in PLUGINS.iterdir()}) if PLUGINS.exists() else 0
    print(f"{count} protocols, {plugin_count} built plugins; registry and references: {'FAIL' if findings else 'PASS'}")
    sys.exit(bool(findings))
