"""Check source-derived dates, preserved paragraph variants, and read-only drift CLI."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_packages import REPOSITORY, builder, validator


class GeneratedBoilerplateTests(unittest.TestCase):
    def test_readme_date_tracks_transitive_source_not_mtime(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            suite = root / "source/system"
            skill = suite / "skills-src/build/acs-example"
            skill.mkdir(parents=True)
            protocols = suite / "protocols"
            protocols.mkdir()
            dependency = protocols / "memory.md"
            dependency.write_text("# Memory\n\nLast updated: 2031-03-04\n")
            (skill / "SKILL.md").write_text(
                "# Example\n\nLast updated: 2030-01-02\n\n[Memory](../../../protocols/memory.md)\n"
            )
            output = root / "package"
            for expected_date in ("2031-03-04", "2032-05-06"):
                dependency.write_text(f"# Memory\n\nLast updated: {expected_date}\n")
                builder.build_package(suite, output, {"acs-example": skill},
                                      name="example", description="Fixture")
                self.assertIn(f"Last updated: {expected_date}\n", (output / "README.md").read_text())
            dependency.write_text("# Memory\n\nLast updated: 2032-99-99\n")
            with self.assertRaises(ValueError):
                builder.build_package(suite, output, {"acs-example": skill},
                                      name="example", description="Fixture")

    def test_all_sources_route_to_preserved_variants_and_expand_once(self) -> None:
        suite = REPOSITORY / "system"
        sources = sorted((suite / "skills-src").rglob("SKILL.md"))
        self.assertEqual(len(sources), 45)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "package"
            builder.build_package(suite, output, {source.parent.name: source.parent for source in sources},
                                  name="all", description="Fixture")
            self.assertEqual(validator.validate_package(output), [])
            for source in sources:
                original = source.read_text()
                self.assertNotIn("Shared semantics:", original)
                self.assertEqual(original.count("[Shared semantics]("), 1)
                packaged = (output / "skills" / source.parent.name / "SKILL.md").read_text()
                self.assertEqual(packaged.count("Shared semantics:"), 1, source.parent.name)
                self.assertNotIn("[Shared semantics](", packaged)
                self.assertEqual(original.split("---", 2)[1], packaged.split("---", 2)[1])
                self.assertEqual(validator.link_errors(source, suite), [])
            cases = {
                "acs-tdd": "Apply their memory ownership and save-before-handoff rules; existing authorization persists.",
                "acs-plan-delivery": "A planning request authorizes the plan, not implementation.",
                "acs-sync-context": "Domain results and proposed transitions use those contracts; existing authorization persists.",
                "acs-create-readme": "owns repository-wide document classification and reorganization.",
                "acs-technical-design": "Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff.",
            }
            for name, semantic_rule in cases.items():
                self.assertIn(semantic_rule, (output / "skills" / name / "SKILL.md").read_text())

    def test_standalone_expansion_relocates_links_and_fails_on_bad_include(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_suite = REPOSITORY / "system"
            source = source_suite / "skills-src/build/acs-plan-delivery"
            exported = root / "export"
            builder.build_standalone_skill(source_suite, exported, source)
            installed = root / "installed"
            shutil.move(exported, installed)
            self.assertEqual(validator.validate_package(installed), [])
            self.assertIn("A planning request authorizes the plan, not implementation.",
                          (installed / "SKILL.md").read_text())
            materializer = builder.Materializer(source_suite, root / "invalid", {})
            marker = "[Shared semantics](../../../docs/shared-semantics.md#missing)"
            with self.assertRaisesRegex(ValueError, "Missing shared semantics section"):
                materializer.shared_semantics(source / "SKILL.md", installed / "SKILL.md", marker)
            with self.assertRaisesRegex(ValueError, "Duplicate shared semantics link"):
                materializer.shared_semantics(source / "SKILL.md", installed / "SKILL.md", marker + "\n" + marker)

    def test_check_detects_drift_without_repairing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "plugins"
            command = [sys.executable, str(REPOSITORY / "scripts/build-plugins.py"), "--output", str(output)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            pristine = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertEqual(pristine, {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()})
            result = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            changes = {
                "acs-build/README.md": lambda text: re.sub(r"Last updated: \S+", "Last updated: 1900-01-01", text),
                "acs-build/skills/acs-tdd/SKILL.md": lambda text: text.replace("Shared semantics:", "Stale semantics:"),
                "acs-build/catalog/skill-set.json": lambda text: text.replace('"acs-tdd"', '"stale-skill"'),
                "acs-build/.claude-plugin/plugin.json": lambda text: text.replace("Delivery planning", "Stale description"),
            }
            for relative, mutate in changes.items():
                with self.subTest(relative=relative):
                    path = output / relative
                    stale = mutate(path.read_text())
                    self.assertNotEqual(stale.encode(), pristine[Path(relative)])
                    path.write_text(stale)
                    result = subprocess.run(command + ["--check"], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(f"STALE {relative}", result.stdout)
                    self.assertEqual(path.read_text(), stale)
                    path.write_bytes(pristine[Path(relative)])
            missing = output / "acs-build/README.md"
            missing.unlink()
            result = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("STALE acs-build/README.md", result.stdout)
            self.assertFalse(missing.exists())
            missing.write_bytes(pristine[Path("acs-build/README.md")])
            extra = output / "acs-build/resources/stale.md"
            extra.write_text("Stale generated resource\n")
            result = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unexpected generated file", result.stdout)
            extra.unlink()
            note = output / "acs-build/user-notes.txt"
            note.write_text("Preserved user material\n")
            result = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(note.read_text(), "Preserved user material\n")
            missing_output = Path(temporary) / "absent"
            result = subprocess.run(command[:-1] + [str(missing_output), "--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(missing_output.exists())

    def test_standalone_check_and_marketplace_drift(self) -> None:
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "standalone"
            command = [sys.executable, str(REPOSITORY / "scripts/build-plugins.py"),
                       "--standalone", "--output", str(output)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            result = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            skill = output / "acs-plan-delivery/SKILL.md"
            skill.write_text(skill.read_text().replace("Shared semantics:", "Stale semantics:"))
            result = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("STALE acs-plan-delivery/SKILL.md", result.stdout)
            self.assertIn("Stale semantics:", skill.read_text())

            # Isolate the default-output marketplace branch from the real checkout.
            (root / ".claude-plugin").mkdir()
            marketplace = root / ".claude-plugin/marketplace.json"
            marketplace.write_text('{"name": "fixture", "plugins": []}\n')
            plugins = root / "plugins"
            with patch.object(builder, "ROOT", root), patch.object(builder, "PLUGINS", plugins), \
                    patch.object(builder, "build_output", return_value=[]):
                self.assertEqual(builder.check_output(plugins, standalone=False),
                                 ["STALE .claude-plugin/marketplace.json"])
                self.assertEqual(marketplace.read_text(), '{"name": "fixture", "plugins": []}\n')
                marketplace.write_text(builder.marketplace_text([]))
                self.assertEqual(builder.check_output(plugins, standalone=False), [])


if __name__ == "__main__":
    unittest.main()
