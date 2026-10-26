from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'adaptive-codex-orchestrator'


class InstallTests(unittest.TestCase):
    def run_installer(self, dest, cwd):
        return subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/install.py'),
                               '--dest', str(dest)], cwd=cwd, capture_output=True,
                              text=True, timeout=10)

    def test_installs_complete_skill_from_another_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'repository' / '.agents' / 'skills'
            result = self.run_installer(dest, tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            actual = dest / SOURCE.name
            expected = {p.relative_to(SOURCE): p.read_bytes()
                        for p in SOURCE.rglob('*') if p.is_file()}
            copied = {p.relative_to(actual): p.read_bytes()
                      for p in actual.rglob('*') if p.is_file()}
            self.assertEqual(copied, expected)

    def test_existing_installation_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'skills'
            installed = dest / SOURCE.name
            installed.mkdir(parents=True)
            sentinel = installed / 'SKILL.md'
            sentinel.write_text('user customization')
            result = self.run_installer(dest, tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('destination already exists', result.stderr)
            self.assertEqual(sentinel.read_text(), 'user customization')
            self.assertEqual(list(installed.iterdir()), [sentinel])

    def test_existing_symlink_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'skills'
            dest.mkdir()
            installed = dest / SOURCE.name
            installed.symlink_to(Path(tmp) / 'missing', target_is_directory=True)
            result = self.run_installer(dest, tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(installed.is_symlink())
            self.assertFalse(installed.exists())


if __name__ == '__main__':
    unittest.main()
