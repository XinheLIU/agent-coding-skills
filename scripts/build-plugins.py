#!/usr/bin/env python3
"""Build independently installable plugins from skills-src.

Reads catalog/skill-set.json for the suite -> skill-name mapping, copies each
suite's SKILL.md files into plugins/<suite>/skills/<name>/SKILL.md, rewrites
protocol:acs:* references into relative paths that reach the acs-protocols
plugin, and copies the protocol files themselves into plugins/acs-protocols/.

Idempotent: deletes and recreates each plugin's skills/ (or protocols/)
directory on every run rather than merging.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "system"
PLUGINS = ROOT / "plugins"

PROTOCOL_REF = re.compile(r'protocol:acs:([a-z][a-z0-9-]*)')
# Matches a skills-src-relative link into system/workflows/, e.g.
# "../../../workflows/feature-delivery.md". Only rewrites links that leave
# a skill's own directory to reach workflows/; links already inside
# workflows/*.md (workflow-to-workflow) are untouched by this pattern since
# those files are copied, not scanned, by build_protocols_plugin().
WORKFLOWS_REF = re.compile(r'(?:\.\./)+workflows/([a-zA-Z0-9_-]+\.md)')

# category id (from catalog/skill-set.json) -> plugin name
CATEGORY_TO_PLUGIN = {
    "plan": "acs-plan",
    "design/requirements": "acs-plan",
    "design/ux": "acs-design",
    "design/technical": "acs-design",
    "build": "acs-build",
    "test": "acs-build",
    "quality/review": "acs-quality",
    "quality/debugging": "acs-quality",
    "maintain": "acs-quality",
    "craft/context": "acs-craft",
    "craft/meta": "acs-craft",
}

PLUGIN_DESCRIPTIONS = {
    "acs-protocols": "Shared lifecycle, identity, and domain-memory contracts for the ACS suite. No skills; other acs-* plugins depend on it.",
    "acs-plan": "Product discovery, ideation, and requirements skills for the ACS suite.",
    "acs-design": "UX and technical design skills for the ACS suite.",
    "acs-build": "Delivery planning, implementation, and test-gap analysis skills for the ACS suite.",
    "acs-quality": "Code review, refactoring, debugging, and incident diagnosis skills for the ACS suite.",
    "acs-craft": "Context lifecycle and meta skills (research, skill authoring, portfolio mapping) for the ACS suite.",
}


def load_skill_to_dir() -> dict[str, Path]:
    """Map skill name -> its directory under system/skills-src."""
    mapping: dict[str, Path] = {}
    for skill_md in SUITE.glob("skills-src/**/SKILL.md"):
        mapping[skill_md.parent.name] = skill_md.parent
    return mapping


def load_skill_to_plugin() -> dict[str, str]:
    skillset = json.loads((ROOT / "catalog/skill-set.json").read_text())
    mapping: dict[str, str] = {}
    for category in skillset["categories"]:
        plugin = CATEGORY_TO_PLUGIN.get(category["id"])
        if plugin is None:
            raise SystemExit(f"category '{category['id']}' has no plugin mapping")
        for skill in category["skills"]:
            mapping[skill] = plugin
    return mapping


def rewrite_protocol_refs(content: str, depth_to_plugins_root: str) -> str:
    """Rewrite protocol:acs:X and workflows/X.md references to relative paths
    that reach the acs-protocols plugin.

    depth_to_plugins_root is the '../' prefix from a skill's directory
    (plugins/<suite>/skills/<name>/) up to plugins/.
    """

    def replace_protocol(match: re.Match[str]) -> str:
        name = match.group(1)
        return f"{depth_to_plugins_root}acs-protocols/protocols/{name}.md"

    def replace_workflow(match: re.Match[str]) -> str:
        filename = match.group(1)
        return f"{depth_to_plugins_root}acs-protocols/workflows/{filename}"

    content = PROTOCOL_REF.sub(replace_protocol, content)
    content = WORKFLOWS_REF.sub(replace_workflow, content)
    return content


PROTOCOLS_VERSION = "1.0.0"


def write_plugin_json(plugin_dir: Path, name: str, needs_protocols: bool) -> None:
    manifest = {
        "name": name,
        "version": "1.0.0",
        "description": PLUGIN_DESCRIPTIONS[name],
        "author": {"name": "Xinhe LIU", "url": "https://github.com/XinheLIU"},
        "repository": "https://github.com/XinheLIU/agent-coding-skills",
        "license": "MIT",
    }
    if needs_protocols:
        manifest["skills"] = "./skills/"
        manifest["peerDependencies"] = {"acs-protocols": f"^{PROTOCOLS_VERSION}"}
    plugin_json_dir = plugin_dir / ".claude-plugin"
    plugin_json_dir.mkdir(parents=True, exist_ok=True)
    (plugin_json_dir / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n")


def build_protocols_plugin() -> None:
    plugin_dir = PLUGINS / "acs-protocols"

    protocols_out = plugin_dir / "protocols"
    if protocols_out.exists():
        shutil.rmtree(protocols_out)
    shutil.copytree(SUITE / "protocols", protocols_out)

    # workflows/ is cross-domain orchestration narrative (build+plan+craft all
    # linked from it) — same "shared, not owned by one suite" status as
    # protocols/, so it ships in the same base package. Copied verbatim:
    # internal links inside these files are pre-existing and out of scope.
    workflows_out = plugin_dir / "workflows"
    if workflows_out.exists():
        shutil.rmtree(workflows_out)
    shutil.copytree(SUITE / "workflows", workflows_out)

    write_plugin_json(plugin_dir, "acs-protocols", needs_protocols=False)
    print(f"acs-protocols: copied {len(list(protocols_out.glob('*.md')))} protocol files, {len(list(workflows_out.glob('*.md')))} workflow files")


def build_skill_plugins() -> None:
    skill_to_dir = load_skill_to_dir()
    skill_to_plugin = load_skill_to_plugin()

    # depth from plugins/<suite>/skills/<name>/ to plugins/ is always ../../../
    depth_to_plugins_root = "../../../"

    per_plugin_count: dict[str, int] = {}

    for skill_name, plugin_name in sorted(skill_to_plugin.items()):
        src_dir = skill_to_dir.get(skill_name)
        if src_dir is None:
            raise SystemExit(f"skill '{skill_name}' listed in skill-set.json but missing under skills-src/")

        dest_dir = PLUGINS / plugin_name / "skills" / skill_name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(src_dir, dest_dir)

        skill_md = dest_dir / "SKILL.md"
        content = skill_md.read_text()
        rewritten = rewrite_protocol_refs(content, depth_to_plugins_root)
        skill_md.write_text(rewritten)

        per_plugin_count[plugin_name] = per_plugin_count.get(plugin_name, 0) + 1

    for plugin_name, count in sorted(per_plugin_count.items()):
        write_plugin_json(PLUGINS / plugin_name, plugin_name, needs_protocols=True)
        print(f"{plugin_name}: {count} skills")


def update_marketplace() -> None:
    marketplace_path = ROOT / ".claude-plugin/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    marketplace["plugins"] = [
        {
            "name": "acs-protocols",
            "source": "./plugins/acs-protocols",
            "description": PLUGIN_DESCRIPTIONS["acs-protocols"],
        },
        *[
            {
                "name": name,
                "source": f"./plugins/{name}",
                "description": PLUGIN_DESCRIPTIONS[name],
            }
            for name in ["acs-plan", "acs-design", "acs-build", "acs-quality", "acs-craft"]
        ],
        {
            "name": "agent-coding-skills",
            "source": "./system",
            "description": "ACS coding skills with shared memory, context management, product ideation, delivery, testing, and debugging workflows. Monolithic install; equivalent to installing all acs-* plugins together.",
        },
    ]
    marketplace_path.write_text(json.dumps(marketplace, indent=2) + "\n")
    print("marketplace.json: registered 6 plugins + monolithic install")


def main() -> None:
    PLUGINS.mkdir(exist_ok=True)
    build_protocols_plugin()
    build_skill_plugins()
    update_marketplace()


if __name__ == "__main__":
    main()
