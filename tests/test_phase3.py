import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.ci import run_ci
from src.commands.export import FORMATS, run_export
from src.commands.init import run_init
from src.commands.plan import run_plan
from src.commands.spec import run_spec
from src.commands.validate import run_validate_all


class TestPhase3(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target = Path(self.temp_dir.name)
        # A full workspace with one generated spec.
        run_init(self.temp_dir.name)
        run_spec("Test Feature", self.temp_dir.name)
        self.spec_file = self.target / "docs" / "specs" / "test-feature.md"

    def tearDown(self):
        self.temp_dir.cleanup()

    # ---- Phase 3: export ----
    def test_export_default_markdown(self):
        self.assertEqual(run_export(str(self.spec_file), None, self.temp_dir.name), 0)
        out = self.target / "docs" / "exports" / "test-feature.md"
        self.assertTrue(out.is_file())
        text = out.read_text(encoding="utf-8")
        self.assertIn("Specification", text)
        self.assertIn("Test Feature", text)

    def test_export_all_formats_write_distinct_files(self):
        produced = set()
        for fmt in FORMATS:
            self.assertEqual(run_export(str(self.spec_file), fmt, self.temp_dir.name), 0)
        exports_dir = self.target / "docs" / "exports"
        for name in ("test-feature.md", "test-feature.claude.md", "test-feature.mdc", "test-feature.agents.md"):
            path = exports_dir / name
            self.assertTrue(path.is_file(), f"missing export: {name}")
            produced.add(path.read_text(encoding="utf-8"))
        # Each wrapper differs, so the file contents are distinct.
        self.assertEqual(len(produced), 4)

    def test_export_bundles_plan_when_present(self):
        run_plan(str(self.spec_file), self.temp_dir.name)
        self.assertEqual(run_export(str(self.spec_file), "markdown", self.temp_dir.name), 0)
        text = (self.target / "docs" / "exports" / "test-feature.md").read_text(encoding="utf-8")
        self.assertIn("Technical Plan", text)

    def test_export_unknown_format_fails(self):
        self.assertEqual(run_export(str(self.spec_file), "nonsense", self.temp_dir.name), 1)

    # ---- Phase 3: validate --all ----
    def test_validate_all_passes_on_generated_spec(self):
        self.assertEqual(run_validate_all(self.temp_dir.name), 0)

    def test_validate_all_fails_when_any_spec_incomplete(self):
        bad = self.target / "docs" / "specs" / "bad.md"
        bad.write_text("# Bad\n\n## Summary\nNo criteria here.\n", encoding="utf-8")
        self.assertEqual(run_validate_all(self.temp_dir.name), 1)

    # ---- Phase 3: ci ----
    def test_ci_generates_workflow(self):
        self.assertEqual(run_ci(self.temp_dir.name), 0)
        wf = self.target / ".github" / "workflows" / "coding-spec.yml"
        self.assertTrue(wf.is_file())
        self.assertIn("validate --all", wf.read_text(encoding="utf-8"))

    def test_ci_refuses_to_overwrite(self):
        self.assertEqual(run_ci(self.temp_dir.name), 0)
        self.assertEqual(run_ci(self.temp_dir.name), 1)

    # ---- Skill packaging contract ----
    def test_skill_routes_every_toolkit_command(self):
        # The root SKILL.md is what makes /coding-spec work; guard that every
        # shipped toolkit subcommand stays documented in its dispatch table so a
        # new command can't ship without agent routing.
        repo_root = Path(__file__).resolve().parent.parent
        skill = (repo_root / "SKILL.md").read_text(encoding="utf-8")
        for command in ("init", "spec", "plan", "validate", "review", "export", "ci"):
            self.assertIn(f"coding-spec {command}", skill, f"SKILL.md does not route '{command}'")

    def test_installer_is_executable_and_present(self):
        repo_root = Path(__file__).resolve().parent.parent
        installer = repo_root / "install.sh"
        self.assertTrue(installer.is_file(), "install.sh missing")
        import os

        self.assertTrue(os.access(installer, os.X_OK), "install.sh is not executable")


if __name__ == "__main__":
    unittest.main()
