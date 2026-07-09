import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.catalog import run_catalog
from src.commands.init import run_init
from src.commands.plan import run_plan
from src.commands.review import run_review
from src.commands.score import compute_score, run_score
from src.commands.spec import run_spec


class TestPhase4(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target = Path(self.temp_dir.name)
        # A full workspace with one generated spec.
        run_init(self.temp_dir.name)
        run_spec("Test Feature", self.temp_dir.name)
        self.spec_file = self.target / "docs" / "specs" / "test-feature.md"

    def tearDown(self):
        self.temp_dir.cleanup()

    # ---- Phase 4: score ----
    def test_score_generates_scorecard(self):
        self.assertEqual(run_score(str(self.spec_file), self.temp_dir.name), 0)
        card = self.target / "docs" / "plans" / "test-feature-scorecard.md"
        self.assertTrue(card.is_file())
        text = card.read_text(encoding="utf-8")
        self.assertIn("Grade:", text)

    def test_score_rewards_plan_and_review(self):
        before = compute_score(self.spec_file, self.target)["total"]
        run_plan(str(self.spec_file), self.temp_dir.name)
        run_review(str(self.spec_file), self.temp_dir.name)
        after = compute_score(self.spec_file, self.target)["total"]
        # Adding a plan and a review checklist raises the artifacts score.
        self.assertGreater(after, before)

    def test_score_missing_spec_fails(self):
        missing = self.target / "docs" / "specs" / "nope.md"
        self.assertEqual(run_score(str(missing), self.temp_dir.name), 1)

    # ---- Phase 4: catalog ----
    def test_catalog_indexes_specs(self):
        run_spec("Second Feature", self.temp_dir.name)
        self.assertEqual(run_catalog(self.temp_dir.name), 0)
        catalog = self.target / "docs" / "catalog.md"
        self.assertTrue(catalog.is_file())
        text = catalog.read_text(encoding="utf-8")
        self.assertIn("test-feature", text)
        self.assertIn("second-feature", text)
        self.assertIn("Portfolio average", text)

    # ---- Skill packaging contract ----
    def test_skill_routes_phase4_commands(self):
        # Guard that the new Phase 4 commands stay documented in the root
        # SKILL.md dispatch table so they can't ship without agent routing.
        repo_root = Path(__file__).resolve().parent.parent
        skill = (repo_root / "SKILL.md").read_text(encoding="utf-8")
        for command in ("score", "catalog"):
            self.assertIn(f"coding-spec {command}", skill, f"SKILL.md does not route '{command}'")


if __name__ == "__main__":
    unittest.main()
