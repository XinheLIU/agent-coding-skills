#!/usr/bin/env python3
"""Materialize the portable context-management plugin from canonical sources."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path


SKILLS = {
    "init-context": Path("system/skills-src/craft/context/init-context"),
    "sync-context": Path("system/skills-src/craft/context/sync-context"),
    "translate-agent-context": Path("system/skills-src/craft/context/translate-agent-context"),
}


def copy_tree(source_root: Path, destination_root: Path) -> None:
    for source in source_root.rglob("*"):
        relative = source.relative_to(source_root)
        destination = destination_root / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    default_output = Path(tempfile.gettempdir()) / "context-management-built"
    parser.add_argument("--output", type=Path, default=default_output)
    args = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    output_root = (repository_root / args.output).resolve()
    if output_root.exists():
        marker = output_root / "context-management.json"
        try:
            marker_payload = json.loads(marker.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            raise SystemExit(f"Refusing to replace non-generated directory: {output_root}")
        if marker_payload.get("name") != "context-management":
            raise SystemExit(f"Refusing to replace non-context plugin directory: {output_root}")
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    for skill_name, source in SKILLS.items():
        copy_tree(repository_root / source, output_root / "skills" / skill_name)

    for directory in (".claude-plugin", ".codex-plugin", "commands"):
        source_directory = repository_root / "plugins/context-management" / directory
        copy_tree(source_directory, output_root / directory)
    shutil.copy2(repository_root / "plugins/context-management/package.json", output_root / "package.json")

    manifest = {
        "name": "context-management",
        "version": "0.1.0",
        "skills": list(SKILLS),
        "source": "system/skills-src/craft/context",
    }
    (output_root / "context-management.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(output_root)


if __name__ == "__main__":
    main()
