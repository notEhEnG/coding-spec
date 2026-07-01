import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.init import run_init
from src.paths import package_root


class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def file_hash(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_templates_stability(self):
        run_init(self.temp_dir.name)

        source_templates_dir = package_root() / "templates"
        for name in (
            "spec.template.md",
            "plan.template.md",
            "tasks.template.md",
            "review.template.md",
            "constitution.template.md",
        ):
            src_file = source_templates_dir / name
            dest_file = self.target_path / "templates" / name
            self.assertTrue(src_file.is_file())
            self.assertEqual(
                self.file_hash(src_file),
                self.file_hash(dest_file),
                f"Snapshot mismatch for template: {name}",
            )