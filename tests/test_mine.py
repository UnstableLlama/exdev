# SPDX-License-Identifier: MIT
# Copyright (c) 2026 UnstableLlama and exdev contributors
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('mine', Path(__file__).parents[1] / 'scripts/mine.py')
mine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mine)

class MinerTests(unittest.TestCase):
    def test_references(self):
        refs = mine.references('Fix #12 and owner/repo#34 https://arxiv.org/abs/2401.12345v2 https://huggingface.co/org/model/blob/main/config.json')
        self.assertIn('org/model', refs['hf_repositories'])
        self.assertIn('12', refs['issue_pr_numbers'])
        self.assertIn('https://arxiv.org/abs/2401.12345v2', refs['papers'])

    def test_not_noise_from_message_alone(self):
        tag, noise, _ = mine.classify('Bump version', ['kernel.cu'], 'diff\n-old\n+new', False)
        self.assertFalse(noise)

    def test_collection_is_not_model_repository(self):
        refs = mine.references('https://huggingface.co/collections/turboderp/exl3 https://huggingface.co/org/model')
        self.assertEqual(refs['hf_repositories'], ['org/model'])

    def test_binary_and_calibration_references(self):
        diff = 'diff --git a/a.png b/a.png\nGIT binary patch\n+Qwen99 #12\ndiff --git a/standard_cal_data/a b/standard_cal_data/a\n+https://example.com/data\ndiff --git a/README.md b/README.md\n+https://github.com/org/repo/issues/42\n'
        refs = mine.diff_references('', diff)
        self.assertNotIn('12', refs['issue_pr_numbers'])
        self.assertIn('org/repo#42', refs['qualified_issues'])
        self.assertEqual(refs['embedded_data_urls'], ['https://example.com/data'])

    def test_document_formatting_noise(self):
        diff = 'diff --git a/README.md b/README.md\n--- a/README.md\n+++ b/README.md\n-### Title\n+## Title\n'
        self.assertTrue(mine.classify('Formatting', ['README.md'], diff, False)[1])
        self.assertFalse(mine.classify('Formatting', ['README.md'], diff + '+New explanation\n', False)[1])

    def test_python_indentation_not_automatic_noise(self):
        self.assertFalse(mine.classify('Formatting', ['a.py'], '-    return x\n+return x\n', True)[1])

    def test_history_resume_and_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); repo = root / 'repo'; repo.mkdir()
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL).decode().strip()
            git('init'); git('config', 'user.name', 'Test'); git('config', 'user.email', 'test@example.invalid')
            (repo / 'a.py').write_text('x=1\n'); git('add', '.'); git('commit', '-m', 'Initial commit')
            first = git('rev-parse', 'HEAD')
            (repo / 'a.py').write_text('x=2\n'); git('commit', '-am', 'Fix value #12')
            out = root / 'data'
            mine.mine(repo, out)
            records = sorted((out / 'records').glob('*.json'))
            self.assertEqual(len(records), 2)
            self.assertIsNone(json.loads(records[0].read_text())['parent_sha'])
            before = [p.read_bytes() for p in records]
            mine.mine(repo, out)
            self.assertEqual(before, [p.read_bytes() for p in records])
            dest = root / 'parent'
            mine.parent_checkout(repo, first, dest)
            self.assertEqual(list(dest.iterdir()), [])
            dest2 = root / 'parent2'
            mine.parent_checkout(repo, git('rev-parse','HEAD'), dest2)
            self.assertEqual((dest2 / 'a.py').read_text(), 'x=1\n')
            self.assertFalse((dest2 / '.git').exists())

class MergeTests(unittest.TestCase):
    def test_merge_and_corruption(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);repo=root/'repo';repo.mkdir()
            def git(*args):
                return subprocess.check_output(['git','-C',str(repo),*args],stderr=subprocess.DEVNULL).decode().strip()
            git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            (repo/'a').write_text('a');git('add','.');git('commit','-m','Initial')
            git('checkout','-b','side');(repo/'b').write_text('b');git('add','.');git('commit','-m','Side')
            side=git('rev-parse','HEAD');git('checkout','main')
            (repo/'c').write_text('c');git('add','.');git('commit','-m','Main');git('merge','--no-ff','side','-m','Merge')
            out=root/'out';mine.mine(repo,out)
            records=sorted((out/'records').glob('*.json'));values=[json.loads(p.read_text()) for p in records]
            self.assertEqual(len(records),4);self.assertEqual(len(values[-1]['parent_shas']),2)
            self.assertEqual(values[-1]['files_touched'],['b'])
            self.assertLess(next(v['position'] for v in values if v['sha']==side),values[-1]['position'])
            self.assertTrue((out/'LICENSES/exllamav3-MIT.txt').exists())
            records[0].write_text(records[0].read_text()+' ')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):mine.mine(repo,out)

if __name__ == '__main__': unittest.main()

class StdinTests(unittest.TestCase):
    def test_git_helper_does_not_inherit_open_stdin(self):
        from unittest.mock import patch
        with patch.object(mine.subprocess, 'check_output', return_value=b'empty') as run:
            mine.git(Path('/repo'), 'hash-object', '-t', 'tree', '--stdin')
            self.assertEqual(run.call_args.kwargs.get('stdin'), subprocess.DEVNULL)

    def test_empty_tree_hash_finishes_while_callers_stdin_stays_open(self):
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['git', 'init', '-q', tmp], check=True)
            script_dir = str(Path(__file__).parents[1] / 'scripts')
            program = ('import sys; sys.path.insert(0, sys.argv[1]); '
                       'from mine import git; '
                       'print(git(sys.argv[2], "hash-object", "-t", "tree", "--stdin").decode().strip())')
            child = subprocess.Popen([sys.executable, '-c', program, script_dir, tmp],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                self.assertEqual(child.wait(timeout=5), 0)
                self.assertEqual(child.stdout.read().strip(), b'4b825dc642cb6eb9a060e54bf8d69288fbee4904')
            finally:
                if child.poll() is None:
                    child.kill()
                    child.wait()
                child.stdin.close()
                child.stdout.close()
                child.stderr.close()
