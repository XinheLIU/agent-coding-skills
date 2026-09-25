"""Exercise source-free package relocation and real packaged renderer behavior."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

REPOSITORY = Path(__file__).resolve().parents[3]


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load("build_plugins", REPOSITORY / "scripts/build-plugins.py")
validator = load("validate_protocols", REPOSITORY / "scripts/validate-protocols.py")


class PackageTests(unittest.TestCase):
    def test_transitive_resources_survive_source_removal_and_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            suite = root / "source/system"
            skill = suite / "skills-src/build/acs-example"
            skill.mkdir(parents=True)
            (suite / "THIRD_PARTY_NOTICES.md").write_text("# Fixture provenance\n")
            (suite.parent / "LICENSE").write_text("Fixture license\n")
            protocols = suite / "protocols"
            protocols.mkdir()
            (protocols / "memory.md").write_text("# Memory\n[Review](review.md#review)\n")
            (protocols / "review.md").write_text("# Review\nKeep the reviewed revision.\n")
            (skill / "references").mkdir()
            (skill / "references/memory.md").symlink_to(protocols / "memory.md")
            companion = suite / "skills-src/context/acs-companion"
            (companion / "scripts").mkdir(parents=True)
            (companion / "SKILL.md").write_text("# Companion\n[Run](scripts/check.py)\n")
            (companion / "scripts/check.py").write_text("print('self-contained')\n")
            (skill / "SKILL.md").write_text(
                "# Example\n[Memory](references/memory.md)\n"
                "[Companion](../../context/acs-companion/SKILL.md)\n"
                "```md\n[Example](not-a-real-file.md)\n```\n"
            )
            output = root / "build/example"
            builder.build_package(suite, output, {"acs-example": skill}, name="example", description="Fixture")
            relocated = root / "isolated/example"
            relocated.parent.mkdir()
            shutil.move(str(output), relocated)
            shutil.rmtree(root / "source")
            self.assertEqual(validator.validate_package(relocated), [])
            self.assertEqual({path.name for path in (relocated / "skills").iterdir()}, {"acs-example"})
            text = (relocated / "skills/acs-example/SKILL.md").read_text()
            self.assertIn("reference procedure; capability not installed", text)
            self.assertIn("[Example](not-a-real-file.md)", text)
            script = relocated / "resources/skills-src/context/acs-companion/scripts/check.py"
            result = subprocess.run([sys.executable, str(script)], cwd=relocated,
                                    check=True, text=True, capture_output=True)
            self.assertEqual(result.stdout.strip(), "self-contained")

    def test_package_audit_rejects_link_escape_and_missing_transitive_resource(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "package"
            package.mkdir()
            (root / "outside.md").write_text("# Outside\n")
            (package / "SKILL.md").write_text("[Outside](../outside.md)\n[Missing](missing.md)\n")
            errors = validator.validate_package(package)
            self.assertTrue(any("reference escapes package" in error for error in errors))
            self.assertTrue(any("broken reference" in error for error in errors))

    def test_current_packages_are_deterministic_and_renderer_runs_after_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "packages"
            command = [sys.executable, str(REPOSITORY / "scripts/build-plugins.py"), "--output", str(output)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            # Default and --output builds use this same regeneration path.
            # Preserve unknown user material while removing only legacy generated trees.
            note = output / "acs-context/user-notes/keep.txt"
            note.parent.mkdir()
            note.write_text("User-owned notes survive regeneration.\n")
            before = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
            for directory in ("shared", "protocols", "workflows"):
                stale = output / "acs-context" / directory / "old-contract.md"
                stale.parent.mkdir(exist_ok=True)
                stale.write_text("[Obsolete link](missing.md)\n")
            self.assertTrue(validator.validate_package(output / "acs-context"))
            subprocess.run(command, check=True, capture_output=True, text=True)
            after = {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}
            self.assertEqual(before, after)
            self.assertEqual(validator.validate_built_plugins(output)[0], [])
            isolated = root / "isolated-craft"
            shutil.move(str(output / "acs-craft"), isolated)
            shutil.rmtree(output)
            self.assertEqual(validator.validate_package(isolated), [])
            result = subprocess.run([
                sys.executable, "-m", "unittest", "discover", "-s",
                str(isolated / "skills/acs-draw-portfolio-dag/tests"), "-p", "test_*.py", "-v",
            ], cwd=isolated, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("\nOK\n", result.stderr)


if __name__ == "__main__":
    unittest.main()
