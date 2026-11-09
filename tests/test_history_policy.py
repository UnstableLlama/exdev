# SPDX-License-Identifier: MIT
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from history_policy import ancestor_context, merge_policy, validate_entry_links


class HistoryPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        (self.repo/'a').write_text('root')
        self.git('add', '.'); self.git('commit', '-m', 'Root')
        self.root = self.git('rev-parse', 'HEAD')
        self.git('checkout', '-b', 'side')
        (self.repo/'b').write_text('branch')
        self.git('add', '.'); self.git('commit', '-m', 'Side')
        self.side = self.git('rev-parse', 'HEAD')
        self.git('checkout', 'main')
        (self.repo/'c').write_text('mainline')
        self.git('add', '.'); self.git('commit', '-m', 'Main')
        self.main = self.git('rev-parse', 'HEAD')

    def tearDown(self): self.tmp.cleanup()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode().strip()

    def test_branch_context_and_links_reject_unrelated_earlier_entry(self):
        entries = {1: {'sha': self.root}, 2: {'sha': self.main}, 3: {'sha': self.side}}
        self.assertEqual(ancestor_context(self.repo, self.side, entries), [1])
        validate_entry_links(self.repo, self.side, [1], entries)
        with self.assertRaisesRegex(ValueError, 'ancestor'):
            validate_entry_links(self.repo, self.side, [2], entries)

    def test_clean_merge_is_integration_and_preserves_branch_identity(self):
        self.git('merge', '--no-ff', 'side', '-m', 'Merge')
        merge = self.git('rev-parse', 'HEAD')
        policy = merge_policy(self.repo, merge)
        self.assertEqual(policy['introduced_shas'], [self.side])
        self.assertEqual(policy['analysis_policy'], 'integration_summary_only')
        self.assertFalse(policy['independent_training_example'])
        self.assertEqual(policy['parents'], [self.main, self.side])

    def test_tree_preserving_merge_requires_review_not_asserted_ours(self):
        self.git('merge', '--no-ff', '-s', 'ours', 'side', '-m', 'Keep main')
        policy = merge_policy(self.repo, self.git('rev-parse', 'HEAD'))
        self.assertTrue(policy['first_parent_tree_unchanged'])
        self.assertEqual(policy['analysis_policy'], 'merge_resolution_review_required')
        self.assertEqual(policy['strategy'], 'not_recoverable_from_commit_object')

    def test_entry_writer_rejects_nonancestor_and_identity_override(self):
        import encyclopedia
        from unittest.mock import patch
        entries = {1: {'sha': self.root}, 2: {'sha': self.main}}
        raw = {'sha': self.side}
        annotation = dict(problem='', reasoning='', impact='', source_notes='', confidence='',
                          links=[2], type='feature', status='draft')
        with patch.object(encyclopedia, 'REPO', self.repo), \
             patch.object(encyclopedia, 'ENTRIES', self.repo/'entries'), \
             patch.object(encyclopedia, 'record', return_value=(self.repo/'record.json', raw)), \
             patch.object(encyclopedia, 'entry_context', return_value=entries):
            with self.assertRaisesRegex(ValueError, 'ancestor'):
                encyclopedia.write(3, annotation)
            with self.assertRaisesRegex(ValueError, 'protected'):
                encyclopedia.write(3, dict(annotation, links=[1], sha=self.main))
