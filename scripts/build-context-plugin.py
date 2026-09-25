#!/usr/bin/env python3
"""Materialize a portable context-only package using the suite resource builder."""
from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {name: ROOT / "system/skills-src/context" / name for name in (
    "acs-init-context", "acs-sync-context", "acs-translate-agent-context",
)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(tempfile.gettempdir()) / "context-management-built")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        try:
            marker = json.loads((output / "context-management.json").read_text())
        except (OSError, ValueError):
            raise SystemExit(f"Refusing to replace non-generated directory: {output}")
        if marker.get("name") != "context-management":
            raise SystemExit(f"Refusing to replace non-context package: {output}")
    spec = importlib.util.spec_from_file_location("build_plugins", ROOT / "scripts/build-plugins.py")
    assert spec and spec.loader
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.build_package(ROOT / "system", output, SKILLS, name="context-management",
                          description="ACS context initialization, synchronization, and translation.")
    (output / "context-management.json").write_text(json.dumps({
        "name": "context-management", "version": "0.4.0", "skills": list(SKILLS),
        "source": "system/skills-src/context",
    }, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
