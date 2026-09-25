"""Behavioral checks for namespace/discovery/catalog integrity and materialization."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_suite import inventory_errors

REPOSITORY = Path(__file__).resolve().parents[3]


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.suite = self.root / "system"
        (self.suite / "skills").mkdir(parents=True)
        (self.root / "catalog").mkdir()
        for host in ("codex", "claude"):
            directory = self.suite / f".{host}-plugin"
            directory.mkdir()
            (directory / "plugin.json").write_text(json.dumps({
                "name": "agent-coding-skills", "skills": "./skills/",
            }))
        self.add_skill("acs-research")
        self.catalog(["acs-research"])

    def add_skill(self, name: str, category: str = "authoring") -> Path:
        directory = self.suite / "skills-src" / category / name
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: A bounded capability.\n---\n")
        discovery = self.suite / "skills" / name
        if not discovery.is_symlink():
            discovery.symlink_to(directory)
        return directory

    def catalog(self, names: list[str], category: str = "authoring") -> None:
        (self.root / "catalog/skill-set.json").write_text(json.dumps({
            "schemaVersion": 1,
            "id": "agent-coding-skills",
            "sourcePattern": "system/skills-src/{category}/{skill}/SKILL.md",
            "categories": [{"id": category, "skills": names}],
        }))

    def test_inventory_accepts_different_skill_counts(self) -> None:
        self.assertEqual(inventory_errors(self.suite), [])
        self.add_skill("acs-implement")
        self.catalog(["acs-research", "acs-implement"])
        self.assertEqual(inventory_errors(self.suite), [])

    def test_duplicate_source_is_rejected(self) -> None:
        self.add_skill("acs-research", "quality")
        self.assertTrue(any("duplicate source skill" in error for error in inventory_errors(self.suite)))

    def test_unprefixed_alias_is_rejected(self) -> None:
        (self.suite / "skills/research").symlink_to(self.suite / "skills/acs-research")
        self.assertIn("skills/research: unexpected discovery entry", inventory_errors(self.suite))

    def test_unprefixed_source_is_rejected(self) -> None:
        self.add_skill("tdd")
        self.catalog(["acs-research", "tdd"])
        self.assertTrue(any("acs- namespace" in error for error in inventory_errors(self.suite)))

    def test_wrong_frontmatter_name_is_rejected(self) -> None:
        path = self.suite / "skills-src/authoring/acs-research/SKILL.md"
        path.write_text(path.read_text().replace("name: acs-research", "name: research"))
        self.assertTrue(any("invalid name/description" in error for error in inventory_errors(self.suite)))

    def test_wrong_loader_target_is_rejected(self) -> None:
        discovery = self.suite / "skills/acs-research"
        discovery.unlink()
        discovery.symlink_to(self.root / "missing")
        self.assertTrue(any("discovery entry must symlink" in error for error in inventory_errors(self.suite)))

    def test_wrong_catalog_category_is_rejected(self) -> None:
        self.catalog(["acs-research"], "maintain")
        self.assertTrue(any("does not resolve to a canonical source" in error for error in inventory_errors(self.suite)))

    def test_fictional_or_missing_catalog_entries_are_rejected(self) -> None:
        self.catalog(["acs-plan"])
        errors = inventory_errors(self.suite)
        self.assertIn("catalog: missing skill acs-research", errors)
        self.assertTrue(any("acs-plan does not resolve" in error for error in errors))

    def test_duplicate_catalog_entry_is_rejected(self) -> None:
        self.catalog(["acs-research", "acs-research"])
        self.assertIn("catalog: duplicate skill acs-research", inventory_errors(self.suite))

    def test_plugin_cannot_point_at_another_skill_tree(self) -> None:
        path = self.suite / ".codex-plugin/plugin.json"
        path.write_text(json.dumps({"name": "agent-coding-skills", "skills": "./skills-src/"}))
        self.assertTrue(any("plugin identity or skill root differs" in error for error in inventory_errors(self.suite)))

    def test_current_context_builder_materializes_shared_directory_resources(self) -> None:
        output = self.root / "context-management"
        result = subprocess.run([
            sys.executable, str(REPOSITORY / "scripts/build-context-plugin.py"),
            "--output", str(output),
        ], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({path.name for path in (output / "skills").iterdir()}, {
            "acs-init-context", "acs-sync-context", "acs-translate-agent-context",
        })
        shared = Path("references/index-tools/external-tools.md")
        actual = output / "skills/acs-sync-context" / shared
        canonical = REPOSITORY / "system/skills-src/context/acs-init-context" / shared
        self.assertTrue(actual.is_file())
        self.assertEqual(actual.read_bytes(), canonical.read_bytes())
        self.assertFalse(any(path.is_symlink() for path in output.rglob("*")))


if __name__ == "__main__":
    unittest.main()
