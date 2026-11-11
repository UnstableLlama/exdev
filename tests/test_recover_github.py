# SPDX-License-Identifier: MIT
import hashlib
import json
import unittest
from teacher.recover_github import bounded_discussions, repo_path_hints, retrospective_path
from teacher.evidence import discussion_snapshot


class DiscussionRecoveryTests(unittest.TestCase):
    def test_bound_keeps_newest_items_and_reports_truncation(self):
        items=[{'created_at':f'2025-01-{day:02d}T00:00:00Z','kind':'issue','number':day} for day in range(1,6)]
        selected,truncated=bounded_discussions(items,3)
        self.assertTrue(truncated)
        self.assertEqual([item['number'] for item in selected],[3,4,5])
        selected,truncated=bounded_discussions(items,10)
        self.assertFalse(truncated);self.assertEqual(len(selected),5)

    def test_retrospective_name_is_derived_from_range(self):
        self.assertEqual(retrospective_path(17).name,'unreferenced-discussion-retrospective-002-016.json')
        self.assertEqual(retrospective_path(18).name,'unreferenced-discussion-retrospective-002-017.json')

    def test_path_hints_strip_install_prefix_filter_parent_tree_and_cap(self):
        text=('Traceback: File "/venv/lib/site-packages/exllamav3/ext.py", line 4\n'
              'then exllamav3/modules/linear.py and missing/not_in_tree.py')
        payload={'objects':[{'content':text}]};content=json.dumps(payload)
        item={'available':True,'content':content,'content_sha256':hashlib.sha256(content.encode()).hexdigest()}
        paths=['exllamav3/ext.py','exllamav3/modules/linear.py','exllamav3/z.py']
        self.assertEqual(repo_path_hints(item,paths),{
            'repo_paths_mentioned':['exllamav3/ext.py','exllamav3/modules/linear.py'],
            'repo_paths_mentioned_truncated':False})
        self.assertEqual(repo_path_hints(item,paths,1),{
            'repo_paths_mentioned':['exllamav3/ext.py'],
            'repo_paths_mentioned_truncated':True})

    def test_unavailable_discussion_has_no_path_hint(self):
        self.assertIsNone(repo_path_hints({'available':False},['exllamav3/ext.py']))

    def test_path_hints_use_only_cutoff_snapshot_content(self):
        def obj(identity,created,body):
            return {'id':identity,'url':'https://example.test/'+identity,'createdAt':created,
                    'lastEditedAt':None,'body':body,'author':{'login':'u'},'edits':[]}
        bundle={'createdAt':'2025-01-01T00:00:00Z','timeline_complete':True,
                'state_events':[],'title_events':[],'title':'Failure','number':1,'kind':'issue',
                'author':{'login':'u'},'url':'https://example.test/issues/1','retrieved_at':'2025-01-04T00:00:00Z',
                'objects':[obj('root','2025-01-01T00:00:00Z','exllamav3/ext.py'),
                           obj('future','2025-01-03T00:00:00Z','exllamav3/modules/linear.py')]}
        row=discussion_snapshot(bundle,'2025-01-02T00:00:00Z')
        self.assertEqual(repo_path_hints(row,['exllamav3/ext.py','exllamav3/modules/linear.py']),{
            'repo_paths_mentioned':['exllamav3/ext.py'],
            'repo_paths_mentioned_truncated':False})


if __name__ == '__main__':
    unittest.main()
