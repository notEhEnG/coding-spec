import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.init import run_init
from src.commands.plan import run_plan
from src.commands.spec import run_spec


class TestCLICommands(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_command(self):
        exit_code = run_init(self.temp_dir.name)
        self.assertEqual(exit_code, 0)

        for subdir in (
            "docs/specs",
            "docs/plans",
            "templates",
            "examples",
            "prompts",
            "src",
            "tests",
        ):
            self.assertTrue((self.target_path / subdir).is_dir())

        self.assertTrue((self.target_path / "templates" / "spec.template.md").is_file())

    def test_spec_and_plan_commands(self):
        run_init(self.temp_dir.name)

        self.assertEqual(run_spec("Test Feature", self.temp_dir.name), 0)
        spec_file = self.target_path / "docs" / "specs" / "test-feature.md"
        self.assertTrue(spec_file.is_file())
        self.assertIn("Test Feature", spec_file.read_text(encoding="utf-8"))

        self.assertEqual(run_plan(str(spec_file), self.temp_dir.name), 0)
        plan_file = self.target_path / "docs" / "plans" / "test-feature-plan.md"
        self.assertTrue(plan_file.is_file())
        self.assertIn("Test Feature", plan_file.read_text(encoding="utf-8"))