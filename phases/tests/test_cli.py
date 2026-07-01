import unittest
import sys
import tempfile
from pathlib import Path

# Add src parent to sys.path to enable imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.validate import run_validate
from src.commands.init import run_init
from src.commands.spec import run_spec
from src.commands.plan import run_plan

class TestCLICommands(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_path = Path(self.temp_dir.name)
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def test_init_command(self):
        exit_code = run_init(self.temp_dir.name)
        self.assertEqual(exit_code, 0)
        
        # Verify subdirectories
        subdirs = ['docs/specs', 'docs/plans', 'templates', 'examples', 'prompts', 'src', 'tests']
        for d in subdirs:
            self.assertTrue((self.target_path / d).is_dir())
            
        # Verify templates copied
        self.assertTrue((self.target_path / 'templates' / 'spec.template.md').is_file())
        
    def test_spec_and_plan_commands(self):
        # Run init first to populate templates
        run_init(self.temp_dir.name)
        
        # Run spec
        exit_code_spec = run_spec("Test Feature", self.temp_dir.name)
        self.assertEqual(exit_code_spec, 0)
        
        spec_file = self.target_path / 'docs' / 'specs' / 'test-feature.md'
        self.assertTrue(spec_file.is_file())
        self.assertIn("Test Feature", spec_file.read_text(encoding='utf-8'))
        
        # Run plan
        exit_code_plan = run_plan(str(spec_file), self.temp_dir.name)
        self.assertEqual(exit_code_plan, 0)
        
        plan_file = self.target_path / 'docs' / 'plans' / 'test-feature-plan.md'
        self.assertTrue(plan_file.is_file())
        
    def test_validate_rules(self):
        # Create a spec file without testing section
        run_init(self.temp_dir.name)
        run_spec("Dummy Feature", self.temp_dir.name)
        spec_file = self.target_path / 'docs' / 'specs' / 'dummy-feature.md'
        
        # Validation should fail due to missing Test Considerations section in default template
        exit_code = run_validate(str(spec_file))
        self.assertEqual(exit_code, 1)
        
        # Append Test Considerations
        with open(spec_file, 'a', encoding='utf-8') as f:
            f.write("\n## Test Considerations\n- Write unit tests\n")
            
        # Now validation should pass
        exit_code_after = run_validate(str(spec_file))
        self.assertEqual(exit_code_after, 0)
