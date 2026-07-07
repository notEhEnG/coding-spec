import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.init import run_init
from src.commands.plan import run_plan
from src.commands.review import run_review
from src.commands.spec import run_spec
from src.commands.validate import run_validate


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

    def test_validate_passes_on_generated_spec(self):
        run_init(self.temp_dir.name)
        run_spec("Test Feature", self.temp_dir.name)
        spec_file = self.target_path / "docs" / "specs" / "test-feature.md"

        # A spec straight from the toolkit template has all required sections.
        self.assertEqual(run_validate(str(spec_file)), 0)

    def test_validate_fails_on_incomplete_spec(self):
        spec_file = self.target_path / "incomplete.md"
        spec_file.write_text("# Feature Spec\n\n## Summary\nJust a summary.\n", encoding="utf-8")

        # Missing acceptance criteria and test considerations -> non-zero exit.
        self.assertEqual(run_validate(str(spec_file)), 1)

    def test_validate_missing_file(self):
        missing = self.target_path / "nope.md"
        self.assertEqual(run_validate(str(missing)), 1)

    def test_review_extracts_numbered_criteria(self):
        run_init(self.temp_dir.name)
        run_spec("Test Feature", self.temp_dir.name)
        spec_file = self.target_path / "docs" / "specs" / "test-feature.md"

        self.assertEqual(run_review(str(spec_file), self.temp_dir.name), 0)
        review_file = self.target_path / "docs" / "plans" / "test-feature-review.md"
        self.assertTrue(review_file.is_file())

        review_text = review_file.read_text(encoding="utf-8")
        # The template's "## 3. Acceptance Criteria" items must be extracted, not
        # reported as "no criteria found" (the regression fixed on port).
        self.assertIn("Criteria 1", review_text)
        self.assertNotIn("No explicit acceptance criteria", review_text)