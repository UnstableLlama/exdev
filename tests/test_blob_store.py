# SPDX-License-Identifier: MIT
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from teacher.blob_store import put, migrate, store_root
from teacher.runner import command
import subprocess


class BlobStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packets = [self.root / '.teacher' / kind / 'one' for kind in ('retrieval', 'audits')]
        for p in self.packets:
            (p / 'blobs').mkdir(parents=True)
            (p / 'manifest.json').write_text('{}\n')

    def test_shared_readonly_idempotent_and_migration(self):
        a, b = self.packets
        raw = b'unchanged historical evidence'
        digest = hashlib.sha256(raw).hexdigest()
        for p in self.packets:
            (p / 'blobs' / digest).write_bytes(raw)
        result = migrate(self.packets)
        self.assertEqual(result['blobs_verified'], 2)
        self.assertTrue(os.path.samefile(a/'blobs'/digest, b/'blobs'/digest))
        self.assertEqual((a/'blobs'/digest).stat().st_mode & 0o222, 0)
        before = (a/'blobs'/digest).stat().st_ino
        put(a, raw)
        self.assertEqual((a/'blobs'/digest).stat().st_ino, before)
        self.assertEqual(migrate(self.packets), result)

    def test_corruption_and_symlinks_fail_without_replacing_original(self):
        a, b = self.packets
        digest = hashlib.sha256(b'right').hexdigest()
        target = a/'blobs'/digest
        target.write_bytes(b'wrong')
        with self.assertRaises(ValueError): migrate([a])
        self.assertEqual(target.read_bytes(), b'wrong')
        target.unlink()
        target.symlink_to(b/'manifest.json')
        with self.assertRaises(ValueError): put(a, b'right')
        target.unlink()
        put(a, b'right')
        source = store_root(a)/digest
        source.chmod(0o644)
        source.write_bytes(b'bad store')
        with self.assertRaises(ValueError): put(b, b'right')
        self.assertFalse((b/'blobs'/digest).exists())

    def test_failed_link_keeps_verified_old_copy(self):
        a, _ = self.packets
        raw = b'original copy'
        digest = hashlib.sha256(raw).hexdigest()
        target = a/'blobs'/digest
        target.write_bytes(raw)
        inode = target.stat().st_ino
        with patch('teacher.blob_store.os.link', side_effect=OSError('cross-device')):
            with self.assertRaises(OSError): put(a, raw)
        self.assertEqual(target.stat().st_ino, inode)
        self.assertEqual(target.read_bytes(), raw)
        self.assertEqual(list(target.parent.glob('.link-*')), [])
        put(a, raw)
        self.assertTrue(os.path.samefile(target, store_root(a)/digest))

    @unittest.skipUnless(os.environ.get('EXDEV_SANDBOX_TESTS') == '1', 'Host namespace test')
    def test_sandbox_cannot_write_chmod_or_reach_store(self):
        a, b = self.packets
        digest = put(a, b'sandbox immutable')
        put(b, b'sandbox immutable')
        code = f'''import os
p='/packet/blobs/{digest}'
for operation in [lambda:open(p,'wb'),lambda:os.chmod(p,0o644),lambda:os.unlink(p)]:
 try: operation()
 except OSError: pass
 else: raise AssertionError('packet mutation allowed')
assert not os.path.exists({str(store_root(a))!r})
print('readonly confirmed')
'''
        cmd = command(a)
        cmd[-1:] = ['-c', code]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((b/'blobs'/digest).read_bytes(), b'sandbox immutable')
