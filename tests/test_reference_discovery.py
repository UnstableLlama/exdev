# SPDX-License-Identifier: MIT
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from teacher.reference_discovery import discover


class ReferenceDiscoveryTests(unittest.TestCase):
    def test_all_pages_unrelated_names_and_pinned_architecture(self):
        seen=[]
        def pages(url):
            seen.append(url)
            if '/api/models?' in url:
                return iter([[{'id':'org/named-family'}],[{'id':'org/unrelated-name'},{'id':'org/future'}]])
            if '/future/' in url:return iter([[{'id':'f'*40,'date':'2026-01-01T00:00:00Z'}]])
            return iter([[{'id':'b'*40,'date':'2026-01-01T00:00:00Z'}],[{'id':'a'*40,'date':'2020-01-01T00:00:00Z'}]])
        def fetch(url):
            self.assertIn('/'+'a'*40+'/config.json',url)
            return json.dumps({'architectures':['Target' if 'unrelated-name' in url else 'Other']}).encode(),{}
        with patch('teacher.reference_discovery.pages',side_effect=pages),patch('teacher.reference_discovery.fetch',side_effect=fetch):
            report,selection=discover('org','Target','2021-01-01T00:00:00Z')
        self.assertEqual([s['repo'] for s in selection],['org/unrelated-name'])
        self.assertEqual(len(report['enumerated_repositories']),3)
        self.assertNotIn('search=',seen[0]);self.assertNotIn('org/future',selection[0]['candidates_considered'])
        self.assertTrue(report['complete'])

    def test_unavailable_is_reported_not_silently_excluded(self):
        with patch('teacher.reference_discovery.pages',side_effect=[iter([[{'id':'org/gated'}]]),iter([[{'id':'a'*40,'date':'2020-01-01T00:00:00Z'}]])]),patch('teacher.reference_discovery.fetch',side_effect=HTTPError('url',401,'Unauthorized',{},None)):
            report,selection=discover('org','Target','2021-01-01T00:00:00Z',workers=1)
        self.assertFalse(report['complete']);self.assertEqual(report['unavailable'],['org/gated']);self.assertEqual(selection,[])
