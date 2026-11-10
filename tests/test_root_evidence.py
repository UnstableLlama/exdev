# SPDX-License-Identifier: MIT
import unittest
from teacher.root_evidence import choose_revision, paper_text, validate_range


class RootEvidenceTests(unittest.TestCase):
    def test_latest_revision_uses_timestamps_and_excludes_future(self):
        rows=[{'id':'future','date':'2025-04-07T00:00:00Z'}, {'id':'old','date':'2025-01-01T00:00:00Z'}, {'id':'chosen','date':'2025-04-06T12:42:49.000Z'}]
        self.assertEqual(choose_revision(rows)['id'],'chosen')
        with self.assertRaises(ValueError):choose_revision(rows[:1])

    def test_range_must_exactly_match_header_request(self):
        validate_range(206,'bytes 8-99/1000',8,99)
        for status,value in [(200,None),(206,'bytes 0-7/1000'),(206,'bytes 8-100/1000')]:
            with self.assertRaises(ValueError):validate_range(status,value,8,99)

    def test_paper_extraction_excludes_site_chrome_and_preserves_math(self):
        html='<header>FUTURE SITE NOTICE</header><article>Paper <math alttext="x^2">x squared</math></article><footer>OTHER</footer>'
        text=paper_text(html)
        self.assertIn('x^2',text)
        self.assertNotIn('FUTURE',text)
        self.assertNotIn('OTHER',text)
