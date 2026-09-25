#!/usr/bin/env python3
"""Materialize independently installable plugins and their local resource closure."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "system"
PLUGINS = ROOT / "plugins"
CATEGORY_TO_PLUGIN = {
    "plan": "acs-plan", "design/requirements": "acs-plan",
    "design/ux": "acs-design", "design/technical": "acs-design",
    "build": "acs-build", "test": "acs-build",
    "quality/review": "acs-quality", "test/review": "acs-quality",
    "quality/debugging": "acs-quality", "test/debugging": "acs-quality",
    "maintain": "acs-quality", "craft/context": "acs-craft",
    "craft/meta": "acs-craft", "context": "acs-craft", "authoring": "acs-craft",
}
PLUGIN_DESCRIPTIONS = {
    "acs-protocols": "Shared ACS contracts and workflows; optional legacy distribution.",
    "acs-plan": "Product discovery, ideation, and requirements skills for the ACS suite.",
    "acs-design": "UX and technical design skills for the ACS suite.",
    "acs-build": "Delivery planning, implementation, and test-gap analysis skills for the ACS suite.",
    "acs-quality": "Code review, refactoring, debugging, and incident diagnosis skills for the ACS suite.",
    "acs-craft": "Context lifecycle and authoring skills for the ACS suite.",
}
LINK = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
FENCE = re.compile(r"(^```[^\n]*\n.*?^```[ \t]*$)", re.MULTILINE | re.DOTALL)


def local_reference(raw: str) -> tuple[str, str] | None:
    """Return a concrete relative path and its optional anchor/title suffix."""
    raw = raw.strip()
    if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", raw) or raw.startswith(("/", "#")):
        return None
    if any(character in raw for character in "<>{}*"):
        return None  # A placeholder, not a package dependency.
    path, separator, title = raw.partition(' "')
    file_part, anchor, fragment = path.partition("#")
    suffix = (anchor + fragment if anchor else "") + (separator + title if separator else "")
    return unquote(file_part), suffix


class Materializer:
    """Copy selected skills, dereference shared files, and close resource links."""

    def __init__(self, suite: Path, output: Path, skills: dict[str, Path], *,
                 contracts_home: str = "resources/protocols") -> None:
        self.suite = suite.resolve()
        self.output = output.resolve()
        self.skills = skills
        self.destinations: dict[Path, Path] = {}
        self.pending: list[tuple[Path, Path]] = []
        self.copied: set[Path] = set()
        # Shared contracts keep one stable packaged home so link targets never
        # depend on which skill's dereferenced copy registered the file first.
        for contract in sorted((self.suite / "protocols").iterdir()):
            if contract.is_file():
                self.destinations[contract.resolve()] = self.output / contracts_home / contract.name

    def add_file(self, source: Path, destination: Path) -> None:
        canonical = source.resolve(strict=True)
        if not canonical.is_relative_to(self.suite):
            raise ValueError(f"Resource escapes source suite: {source}")
        if destination in self.copied:
            return
        self.copied.add(destination)
        self.destinations.setdefault(canonical, destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canonical, destination)
        if canonical.suffix == ".md":
            self.pending.append((canonical, destination))

    def add_tree(self, source: Path, destination: Path, *, include_skill: bool = True) -> None:
        for entry in sorted(source.iterdir()):
            if entry.name == "__pycache__" or entry.suffix == ".pyc":
                continue
            if entry.name == "SKILL.md" and not include_skill:
                continue
            target = destination / entry.name
            if entry.is_dir():
                self.add_tree(entry, target, include_skill=include_skill)
            else:
                self.add_file(entry, target)

    def resource(self, source: Path) -> Path:
        source = source.resolve(strict=True)
        existing = self.destinations.get(source)
        if existing:
            # A pre-seeded contract is copied on first use, not up front.
            if existing not in self.copied:
                self.add_file(source, existing)
            return existing
        if not source.is_relative_to(self.suite):
            raise ValueError(f"Linked resource escapes source suite: {source}")
        destination = self.output / "resources" / source.relative_to(self.suite)
        # Companion resource directories contain adjacent scripts/templates that
        # may be referenced by code or inline instructions instead of MD links.
        skill_root = next((parent for parent in source.parents if (parent / "SKILL.md").is_file()), None)
        if skill_root and skill_root.is_relative_to(self.suite / "skills-src"):
            self.add_tree(skill_root, self.output / "resources" / skill_root.relative_to(self.suite), include_skill=False)
            if source.name == "SKILL.md":
                self.add_file(source, destination)
        elif source.is_dir():
            self.add_tree(source, destination)
        else:
            self.add_file(source, destination)
        return self.destinations.get(source, destination)

    def rewrite(self, source: Path, destination: Path, text: str) -> str:
        def replace(match: re.Match[str]) -> str:
            reference = local_reference(match[2])
            if reference is None:
                return match[0]
            path, suffix = reference
            target = (source.parent / path).resolve()
            if not target.is_relative_to(self.suite):
                # A research corpus is source-checkout provenance, never shipped.
                if target.is_relative_to(self.suite.parent / "references"):
                    provenance = target.relative_to(self.suite.parent).as_posix()
                    return f"{match[1][1:-1]} (source-checkout provenance: `{provenance}{suffix}`)"
                if target.is_relative_to(self.suite.parent):
                    relative = target.relative_to(self.suite.parent).as_posix()
                    return f"{match[1]}(https://github.com/XinheLIU/agent-coding-skills/blob/main/{relative}{suffix})"
                raise ValueError(f"Linked resource escapes repository: {target}")
            companion = target.name == "SKILL.md" and target.parent.name not in self.skills
            copied = self.resource(target)
            relative = Path(os.path.relpath(copied, destination.parent)).as_posix()
            note = " (reference procedure; capability not installed)" if companion else ""
            return f"{match[1]}({relative}{suffix}){note}"

        # Examples are not dependencies and must retain their original spelling.
        return "".join(part if index % 2 else LINK.sub(replace, part)
                       for index, part in enumerate(FENCE.split(text)))

    def build(self, *, standalone: bool = False) -> None:
        notices = self.suite / "THIRD_PARTY_NOTICES.md"
        if notices.is_file():
            self.add_file(notices, self.output / "THIRD_PARTY_NOTICES.md")
        license_file = self.suite.parent / "LICENSE"
        if license_file.is_file():
            self.output.mkdir(parents=True, exist_ok=True)
            shutil.copy2(license_file, self.output / "LICENSE")
        for name, source in sorted(self.skills.items()):
            destination = self.output if standalone else self.output / "skills" / name
            self.add_tree(source, destination)
        index = 0
        while index < len(self.pending):
            source, destination = self.pending[index]
            index += 1
            destination.write_text(self.rewrite(source, destination, source.read_text()))


def build_standalone_skill(suite: Path, output: Path, source: Path) -> None:
    """Export one skill with all dependencies inside its own directory."""
    if output.exists():
        raise ValueError(f"Standalone output must be a new directory: {output}")
    Materializer(suite, output, {source.name: source}).build(standalone=True)


def write_manifest(output: Path, name: str, description: str, version: str) -> None:
    manifest = {
        "name": name, "version": version, "description": description,
        "author": {"name": "Xinhe LIU", "url": "https://github.com/XinheLIU"},
        "repository": "https://github.com/XinheLIU/agent-coding-skills",
        "license": "MIT", "skills": "./skills/",
    }
    for host in ("claude", "codex"):
        path = output / f".{host}-plugin/plugin.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2) + "\n")


def write_package_metadata(output: Path, name: str, description: str,
                           version: str, skills: dict[str, Path]) -> None:
    catalog = {"name": name, "version": version, "skills": [
        {"id": skill, "path": f"skills/{skill}/SKILL.md"} for skill in sorted(skills)
    ]}
    (output / "catalog").mkdir(exist_ok=True)
    (output / "catalog/skill-set.json").write_text(json.dumps(catalog, indent=2) + "\n")
    (output / "package.json").write_text(json.dumps({
        "name": name, "version": version, "description": description,
        "license": "MIT", "main": "catalog/skill-set.json",
    }, indent=2) + "\n")
    inventory = "\n".join(f"- [{skill}](skills/{skill}/SKILL.md)" for skill in sorted(skills))
    (output / "README.md").write_text(
        f"# {name}\n\nLast updated: 2026-09-26\n\n{description}\n\n"
        "Generated by `scripts/build-plugins.py`; edit canonical sources, then rebuild.\n\n"
        "Install or move this entire plugin directory. Keep `skills/` and `resources/` together; "
        "copying only `skills/` loses embedded contracts. No companion plugin is required. "
        "Additional procedures under `resources/` are readable references, not registered capabilities.\n\n"
        "The [catalog](catalog/skill-set.json) lists discovered skills. "
        "[Third-party notices](THIRD_PARTY_NOTICES.md) preserve source provenance.\n\n"
        + (f"## Skills\n\n{inventory}\n" if skills else
           "This legacy package distributes contracts and workflows; it registers no skills.\n")
    )


def build_package(suite: Path, output: Path, skills: dict[str, Path], *, name: str,
                  description: str, version: str = "0.4.0") -> None:
    for directory in ("skills", "resources", "shared", "protocols", "workflows"):
        target = output / directory
        if target.is_symlink():
            target.unlink()
        elif target.exists():
            shutil.rmtree(target)
    Materializer(suite, output, skills).build()
    write_manifest(output, name, description, version)
    write_package_metadata(output, name, description, version, skills)


def build_plugins(output: Path) -> list[dict[str, str]]:
    catalog = json.loads((ROOT / "catalog/skill-set.json").read_text())
    grouped: dict[str, dict[str, Path]] = {}
    for category in catalog["categories"]:
        plugin = CATEGORY_TO_PLUGIN[category["id"]]
        for name in category["skills"]:
            grouped.setdefault(plugin, {})[name] = SUITE / "skills-src" / category["id"] / name
    entries: list[dict[str, str]] = []
    for name, description in PLUGIN_DESCRIPTIONS.items():
        destination = output / name
        if name == "acs-protocols":
            for directory in ("protocols", "workflows", "resources", "shared"):
                target = destination / directory
                if target.exists():
                    shutil.rmtree(target)
            materializer = Materializer(SUITE, destination, {}, contracts_home="protocols")
            for directory in ("protocols", "workflows"):
                materializer.add_tree(SUITE / directory, destination / directory)
            materializer.build()
            write_manifest(destination, name, description, "1.0.0")
            write_package_metadata(destination, name, description, "1.0.0", {})
            for host in ("claude", "codex"):
                manifest_path = destination / f".{host}-plugin/plugin.json"
                manifest = json.loads(manifest_path.read_text())
                del manifest["skills"]
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            print("acs-protocols: materialized optional legacy contract package")
        else:
            skills = grouped[name]
            build_package(SUITE, destination, skills, name=name, description=description, version="1.0.0")
            print(f"{name}: {len(skills)} skills, embedded resources")
        entries.append({"name": name, "source": f"./plugins/{name}", "description": description})
    # Retain existing phase package IDs without changing the active marketplace.
    for plugin in catalog["plugins"]:
        if plugin["name"] not in {"acs-context", "acs-authoring", "acs-test", "acs-maintain"}:
            continue
        skills = {
            name: SUITE / "skills-src" / category["id"] / name
            for category in catalog["categories"]
            if category["id"].split("/")[0] == plugin["phase"]
            for name in category["skills"]
        }
        build_package(SUITE, output / plugin["name"], skills, name=plugin["name"],
                      description=plugin["description"], version=plugin["version"])
        print(f"{plugin['name']}: {len(skills)} skills, retained phase package")
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PLUGINS,
                        help="Build elsewhere without changing the repository marketplace")
    parser.add_argument("--standalone", action="store_true",
                        help="Export self-contained skill directories for individual-skill installers")
    args = parser.parse_args()
    output = args.output.resolve()
    if args.standalone:
        if output == PLUGINS.resolve():
            parser.error("--standalone requires a separate --output directory")
        for source in sorted((SUITE / "skills-src").rglob("SKILL.md")):
            build_standalone_skill(SUITE, output / source.parent.name, source.parent)
        return
    entries = build_plugins(output)
    if output == PLUGINS.resolve():
        path = ROOT / ".claude-plugin/marketplace.json"
        marketplace = json.loads(path.read_text())
        marketplace["plugins"] = entries + [{
            "name": "agent-coding-skills", "source": "./system",
            "description": "All ACS skills, shared memory contracts, and workflows.",
        }]
        path.write_text(json.dumps(marketplace, indent=2) + "\n")


if __name__ == "__main__":
    main()
