# SPDX-License-Identifier: MIT
import subprocess
import tempfile
import unittest
from pathlib import Path
from graph.index_commit import isolated_checkout

class IsolatedCheckoutTests(unittest.TestCase):
    def test_export_contains_no_future_objects_or_remotes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);repo=base/'source';repo.mkdir()
            def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
            git('init','-q');git('config','user.email','test@example.test');git('config','user.name','Test')
            (repo/'x.py').write_text('old\n');git('add','.');git('commit','-qm','old');old=git('rev-parse','HEAD')
            (repo/'x.py').write_text('future\n');git('commit','-qam','future');future=git('rev-parse','HEAD')
            work=base/'work'
            isolated_checkout(repo/'.git',old,work)
            self.assertEqual((work/'x.py').read_text(),'old\n')
            self.assertEqual(subprocess.check_output(['git','-C',str(work),'remote'],text=True),'')
            result=subprocess.run(['git','-C',str(work),'cat-file','-e',future],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            (work/'future-only.py').write_text('stale')
            isolated_checkout(repo/'.git',old,work)
            self.assertFalse((work/'future-only.py').exists())

    def test_refuses_to_replace_unowned_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)/'work';work.mkdir();(work/'user.txt').write_text('keep')
            with self.assertRaisesRegex(ValueError,'owned'):
                isolated_checkout(Path('/missing'), 'missing',work)
            self.assertTrue((work/'user.txt').exists())
