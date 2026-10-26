import json
from pathlib import Path
import tempfile
import unittest
import eval_suite as e

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def test_all_baselines_fail_and_reference_passes(self):
        for name in e.fixtures():
            with self.subTest(fixture=name):
                case = self.root / name
                e.prepare(name, case)
                self.assertEqual(e.grade(case)['status'], 'fail')
                e.apply_reference(case)
                self.assertEqual(e.grade(case)['status'], 'pass')
    def test_refuses_nonempty_output(self):
        (self.root / 'keep').write_text('untouched')
        with self.assertRaises(ValueError): e.prepare('tiny', self.root)
        self.assertEqual((self.root / 'keep').read_text(), 'untouched')
    def test_public_test_only_patch_is_rejected(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        (case / 'workspace' / 'range_sum.py').write_text('def range_sum(start, end):\n    return 6\n')
        self.assertEqual(e.grade(case)['functional'], 'fail')
    def test_modified_sentinel_or_manifest_is_rejected(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        e.apply_reference(case)
        (case / 'workspace' / 'SENTINEL.txt').write_text('lost')
        self.assertEqual(e.grade(case)['integrity'], 'fail')
        (case / 'manifest.json').write_text('{}')
        self.assertEqual(e.grade(case)['integrity'], 'fail')
    def test_successful_premature_exit_does_not_pass(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        (case / 'workspace' / 'range_sum.py').write_text('import sys\nsys.exit(0)\n')
        result = e.grade(case)
        self.assertEqual(result['returncode'], 0)
        self.assertFalse(result['checks_completed'])
        self.assertEqual(result['status'], 'fail')

    def test_timeout(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        (case / 'workspace' / 'range_sum.py').write_text('while True: pass\n')
        self.assertEqual(e.grade(case, .2)['functional'], 'timeout')
    def test_summarize_missing_and_validation(self):
        record = {'trial_id':'a', 'fixture':'tiny', 'arm':'A', 'model':'m', 'runtime':'r',
                  'fixture_hash':'h', 'prompt_hash':'p', 'skill_hash':'none', 'outcome':'pass'}
        p = self.root / 'records.jsonl'
        p.write_text(json.dumps(record) + '\n')
        report = e.summarize(p)
        self.assertIsNone(report['arms']['A']['metrics']['tokens']['sum'])
        self.assertEqual(report['arms']['A']['metrics']['tokens']['observed'], 0)
        record['arm'] = 'D'
        p.write_text(json.dumps(record) + '\n')
        with self.assertRaises(ValueError): e.summarize(p)
    def test_interpreter_cache_allowed_and_not_executed(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        e.apply_reference(case)
        cache = case / 'workspace' / '__pycache__'
        cache.mkdir()
        (cache / 'range_sum.cpython-312.pyc').write_bytes(b'not valid bytecode')
        self.assertEqual(e.grade(case)['status'], 'pass')
    def test_post_execution_protected_mutation_rejected(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        (case / 'workspace' / 'range_sum.py').write_text(
            'from pathlib import Path\nPath("SENTINEL.txt").write_text("corrupt")\ndef range_sum(start, end):\n    return sum(range(start, end+1))\n')
        self.assertEqual(e.grade(case)['integrity'], 'fail')
        self.assertNotEqual((case / 'workspace' / 'SENTINEL.txt').read_text(), 'corrupt')
    def test_nonfinite_metrics_rejected(self):
        row = {'trial_id':'a', 'fixture':'tiny', 'arm':'A', 'model':'m', 'runtime':'r',
               'fixture_hash':'h', 'prompt_hash':'p', 'skill_hash':'disabled', 'outcome':'pass'}
        p = self.root / 'records.jsonl'
        for v in (float('nan'), float('inf'), float('-inf')):
            row['tokens'] = v
            p.write_text(json.dumps(row))
            with self.assertRaises(ValueError): e.summarize(p)
    def test_parallel_separate_modules_and_writable_paths_documented(self):
        case = self.root / 'case'
        meta = e.prepare('parallel', case)
        self.assertEqual(meta['allowed_changes'], ['binary_adapter.py', 'decimal_adapter.py', 'hex_adapter.py'])
        task = (case / 'workspace' / 'TASK.md').read_text()
        for name in meta['allowed_changes'] + ['test_public.py', 'SENTINEL.txt']:
            self.assertIn(name, task)

    def test_extra_file_rejected(self):
        case = self.root / 'case'
        e.prepare('tiny', case)
        (case / 'workspace' / 'extra.py').write_text('')
        self.assertEqual(e.grade(case)['integrity'], 'fail')

if __name__ == '__main__': unittest.main()
