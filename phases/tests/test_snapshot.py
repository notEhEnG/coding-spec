import unittest
import sys
import tempfile
import hashlib
from pathlib import Path

# Add src parent to sys.path to enable imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.init import run_init

class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_path = Path(self.temp_dir.name)
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def get_file_hash(self, path):
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
        
    def test_templates_stability(self):
        # Run init
        run_init(self.temp_dir.name)
        
        script_dir = Path(__file__).resolve().parent.parent
        source_templates_dir = script_dir / 'templates'
        
        templates = [
            'spec.template.md',
            'plan.template.md',
            'tasks.template.md',
            'review.template.md',
            'constitution.template.md'
        ]
        
        for t in templates:
            src_file = source_templates_dir / t
            dest_file = self.target_path / 'templates' / t
            if src_file.is_file():
                self.assertEqual(
                    self.get_file_hash(src_file),
                    self.get_file_hash(dest_file),
                    f"Snapshot mismatch for template: {t}. Generated file differs from source."
                )
