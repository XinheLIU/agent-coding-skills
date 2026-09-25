#!/usr/bin/env python3
"""Check protocol registry, concrete source links, and isolated package closure."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "system"
PLUGINS = ROOT / "plugins"
sys.path.insert(0, str(SUITE / "evals"))
from validate_suite import FENCE, LINK, anchors

PROTOCOL_REF = re.compile(r"protocol:acs:([a-z][a-z0-9-]*)")
BUILT_PLUGINS = {"acs-protocols", "acs-plan", "acs-design", "acs-build", "acs-quality", "acs-craft", "acs-context", "acs-authoring", "acs-test", "acs-maintain"}


def link_errors(path: Path, boundary: Path, *, isolated: bool = False) -> list[str]:
    errors: list[str] = []
    content = FENCE.sub("", path.read_text())
    for reference in LINK.findall(content):
        raw = reference.strip().split(' "', 1)[0]
        if raw.startswith("protocol:"):
            errors.append(f"unresolved logical reference: {reference}")
            continue
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", raw) or any(c in raw for c in "<>{}*"):
            continue
        file_part, _, fragment = raw.partition("#")
        target = (path.parent / unquote(file_part)).resolve() if file_part else path.resolve()
        if not target.is_relative_to(boundary.resolve()):
            if isolated:
                errors.append(f"reference escapes package: {reference}")
                continue
            if target.is_relative_to(boundary.resolve().parent / "references"):
                continue  # Optional source provenance may be absent.
        if not target.exists():
            errors.append(f"broken reference: {reference}")
        elif fragment and target.is_file() and target.suffix in {".md", ".html"}:
            if unquote(fragment) not in anchors(target):
                errors.append(f"missing anchor: {reference}")
    return errors


def validate_protocols(suite: Path = SUITE) -> list[str]:
    errors: list[str] = []
    try:
        registry = json.loads((suite / "protocols/registry.json").read_text())
    except (OSError, ValueError) as error:
        return [f"Cannot load registry: {error}"]
    if registry.get("schemaVersion") != 1 or registry.get("namespace") != "acs":
        errors.append("Invalid registry schema or namespace")
    protocols = registry.get("protocols", {})
    for name, spec in protocols.items():
        if spec.get("id") != f"protocol:acs:{name}":
            errors.append(f"{name}: registry ID mismatch")
        path = (suite / spec["canonical"]).resolve()
        if not path.is_relative_to((suite / "protocols").resolve()):
            errors.append(f"{name}: canonical protocol escapes protocol directory")
            continue
        if not path.is_file():
            errors.append(f"Protocol file missing: {spec['canonical']}")
            continue
        match = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.DOTALL)
        if not match:
            errors.append(f"{spec['canonical']}: missing frontmatter")
            continue
        for field, expected in (("protocol", f"acs:{name}"), ("version", spec.get("version")), ("status", spec.get("status"))):
            actual = re.search(rf"^{field}: (.+)$", match[1], re.MULTILINE)
            if not expected or not actual or actual[1] != expected:
                errors.append(f"{spec['canonical']}: {field} differs from registry")
        if spec.get("anchor", "").lstrip("#") and spec["anchor"].lstrip("#") not in anchors(path):
            errors.append(f"{spec['canonical']}: registry anchor missing: {spec['anchor']}")
    for directory in ("skills-src", "protocols", "workflows"):
        for path in sorted((suite / directory).rglob("*.md")):
            if not path.exists():
                errors.append(f"{path.relative_to(suite)}: broken resource symlink")
                continue
            for error in link_errors(path.resolve(), suite):
                errors.append(f"{path.relative_to(suite)}: {error}")
    return errors


def validate_package(package: Path) -> list[str]:
    """Audit every copied instruction, not just discovered SKILL entrypoints."""
    errors: list[str] = []
    for path in sorted(package.rglob("*")):
        if path.is_symlink():
            errors.append(f"{path.relative_to(package)}: package must materialize symlinks")
        elif path.suffix == ".md":
            errors.extend(f"{path.relative_to(package)}: {error}" for error in link_errors(path, package, isolated=True))
    for path in package.glob(".*-plugin/plugin.json"):
        manifest = json.loads(path.read_text())
        if manifest.get("peerDependencies") or manifest.get("dependencies"):
            errors.append(f"{path.relative_to(package)}: package still requires companion plugins")
        if "skills" in manifest:
            skills = (package / manifest["skills"]).resolve()
            if not skills.is_relative_to(package.resolve()) or not skills.is_dir():
                errors.append(f"{path.relative_to(package)}: invalid discovery root")
    package_json = package / "package.json"
    if package_json.is_file():
        manifest = json.loads(package_json.read_text())
        if manifest.get("dependencies") or manifest.get("peerDependencies"):
            errors.append("package.json: package still requires companion plugins")
        catalog_path = package / manifest.get("main", "catalog/skill-set.json")
        if not catalog_path.is_file():
            errors.append("package.json: catalog is missing")
        else:
            catalog = json.loads(catalog_path.read_text())
            identifiers = [skill["id"] for skill in catalog.get("skills", [])]
            discovered = {path.parent.name for path in (package / "skills").glob("*/SKILL.md")}
            if len(identifiers) != len(set(identifiers)) or set(identifiers) != discovered:
                errors.append("catalog/skill-set.json: skill inventory differs from discovery")
            if catalog.get("name") != manifest.get("name") or catalog.get("version") != manifest.get("version"):
                errors.append("catalog/skill-set.json: identity/version differs from package")
            for skill in catalog.get("skills", []):
                if skill.get("path") != f"skills/{skill['id']}/SKILL.md":
                    errors.append(f"catalog/skill-set.json: invalid entry path for {skill['id']}")
    return errors


def validate_built_plugins(plugins: Path = PLUGINS) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not plugins.exists():
        return errors, warnings
    for name in sorted(BUILT_PLUGINS):
        package = plugins / name
        if not package.is_dir():
            errors.append(f"Missing generated plugin: {name}")
            continue
        errors.extend(f"{name}/{error}" for error in validate_package(package))
    return errors, warnings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugins", type=Path, default=PLUGINS)
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    findings = validate_protocols()
    if not args.source_only:
        findings += validate_built_plugins(args.plugins)[0]
    for finding in findings:
        print(finding)
    print(f"Protocol registry, links and package closure: {'FAIL' if findings else 'PASS'}")
    sys.exit(bool(findings))
