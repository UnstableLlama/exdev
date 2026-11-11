# SPDX-License-Identifier: MIT
import unittest
from teacher.evidence import eligible_content, discussion_snapshot

class EvidenceTests(unittest.TestCase):
    def obj(self, **kwargs):
        return dict(id='x',url='https://github.com/a/b/issues/1',createdAt='2025-01-01T00:00:00Z',
                    updatedAt='2026-01-01T00:00:00Z',lastEditedAt=None,body='original',edits=[],**kwargs)

    def test_general_update_does_not_exclude_unedited_body(self):
        r=eligible_content(self.obj(),'2025-01-02T00:00:00Z')
        self.assertEqual(r['content'],'original')
        self.assertNotIn('updatedAt',r)

    def test_future_object_is_not_visible(self):
        self.assertIsNone(eligible_content(self.obj(),'2024-12-31T23:59:59Z'))

    def test_after_cutoff_edit_uses_only_dated_edit_evidence(self):
        o=self.obj();o.update(body='FUTURE',lastEditedAt='2025-01-03T00:00:00Z',
                             edits=[dict(id='old',editedAt='2025-01-01T12:00:00Z',diff='past edit text',deletedAt=None),
                                    dict(id='future',editedAt='2025-01-03T00:00:00Z',diff='FUTURE',deletedAt=None)])
        r=eligible_content(o,'2025-01-02T00:00:00Z')
        self.assertEqual(r['representation'],'edit_event_text')
        self.assertEqual(r['content'],'past edit text')
        self.assertNotIn('FUTURE',str(r))

    def test_deleted_edit_and_unknown_edit_metadata_fail_closed(self):
        o=self.obj();o.pop('lastEditedAt')
        self.assertIsNone(eligible_content(o,'2025-01-02T00:00:00Z'))
        o=self.obj();o.update(lastEditedAt='2025-01-03T00:00:00Z',edits=[dict(id='e',editedAt='2025-01-01T00:00:00Z',diff='removed',deletedAt='2025-01-04T00:00:00Z')])
        self.assertIsNone(eligible_content(o,'2025-01-02T00:00:00Z'))

    def test_unpublished_review_is_excluded(self):
        o=self.obj();o['publishedAt']=None
        self.assertIsNone(eligible_content(o,'2025-01-02T00:00:00Z'))

    def test_author_attribution_and_unknown_author(self):
        self.assertEqual(eligible_content(self.obj(author={'login':'reporter'}),'2025-01-02T00:00:00Z')['author_login'],'reporter')
        self.assertIsNone(eligible_content(self.obj(author=None),'2025-01-02T00:00:00Z')['author_login'])

    def discussion(self, **kwargs):
        root=self.obj(author={'login':'reporter'})
        result=dict(retrieved_at='2025-02-01T00:00:00Z',kind='issue',number=7,title='Current title',
                    state='OPEN',createdAt=root['createdAt'],closedAt=None,author=root['author'],url=root['url'],
                    timeline_complete=True,title_events=[],state_events=[],objects=[root])
        result.update(kwargs);return result

    def test_discussion_snapshot_filters_cutoff_state_and_recovers_title(self):
        cutoff='2025-01-02T00:00:00Z'
        self.assertIsNone(discussion_snapshot(self.discussion(createdAt='2025-01-03T00:00:00Z'),cutoff))
        closed=self.discussion(state_events=[{'kind':'closed','createdAt':'2025-01-01T12:00:00Z'}])
        self.assertIsNone(discussion_snapshot(closed,cutoff))
        reopened=self.discussion(state_events=[{'kind':'closed','createdAt':'2025-01-01T12:00:00Z'},
                                                {'kind':'reopened','createdAt':'2025-01-01T13:00:00Z'}],
                                  title_events=[{'createdAt':'2025-01-03T00:00:00Z','previousTitle':'Cutoff title','currentTitle':'Current title'}])
        row=discussion_snapshot(reopened,cutoff)
        self.assertEqual(row['title'],'Cutoff title');self.assertEqual(row['state'],'OPEN');self.assertTrue(row['available'])

    def test_discussion_snapshot_fails_closed_on_unknown_historical_content(self):
        root=self.obj();root.update(lastEditedAt='2025-01-03T00:00:00Z',body='FUTURE')
        row=discussion_snapshot(self.discussion(objects=[root]),'2025-01-02T00:00:00Z')
        self.assertFalse(row['available']);self.assertNotIn('content',row)
        with self.assertRaisesRegex(ValueError,'timeline'):
            discussion_snapshot(self.discussion(timeline_complete=False),'2025-01-02T00:00:00Z')
