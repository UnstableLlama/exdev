# SPDX-License-Identifier: MIT
"""Trusted immutable packet storage; never mounted into the teacher sandbox."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


def store_root(packet):
    packet = Path(packet).absolute()
    for parent in packet.parents:
        if parent.name == '.teacher':
            return parent / 'blob-store'
    # Isolated fixtures/standalone packets share only their containing directory.
    return packet.parent / '.packet-blob-store'


def verify(path, digest):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or not re.fullmatch('[a-f0-9]{64}', digest):
        raise ValueError(f'Not a regular content-addressed blob: {path}')
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != digest:
        raise ValueError(f'Blob checksum mismatch: {path}')


def put(packet, data):
    """Publish bytes by atomic hard link; never write into an existing inode."""
    packet = Path(packet)
    digest = hashlib.sha256(data).hexdigest()
    root = store_root(packet)
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink():
        raise ValueError('Blob store must not be a symlink')
    target = packet / 'blobs' / digest
    source = root / digest
    with (root / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if source.exists() or source.is_symlink():
            verify(source, digest)
            source.chmod(0o444)
        else:
            fd, name = tempfile.mkstemp(prefix='.new-', dir=root)
            try:
                with os.fdopen(fd, 'wb') as out:
                    out.write(data)
                    out.flush()
                    os.fsync(out.fileno())
                    os.fchmod(out.fileno(), 0o444)
                os.replace(name, source)
            finally:
                Path(name).unlink(missing_ok=True)
        if target.exists() or target.is_symlink():
            verify(target, digest)
            if os.path.samefile(source, target):
                return digest
        # Same-filesystem hard links are required; fail instead of silently copying.
        fd, name = tempfile.mkstemp(prefix='.link-', dir=target.parent)
        os.close(fd)
        Path(name).unlink()
        try:
            os.link(source, name)
            os.replace(name, target)
        finally:
            Path(name).unlink(missing_ok=True)
    return digest


def migrate(packets):
    """Verify every old copy before replacing it, then fully verify all links."""
    manifests = {str(p / 'manifest.json'): hashlib.sha256((p / 'manifest.json').read_bytes()).hexdigest()
                 for p in packets}
    count = 0
    for packet in packets:
        for blob in sorted((packet / 'blobs').iterdir()):
            verify(blob, blob.name)
            data = blob.read_bytes()
            if hashlib.sha256(data).hexdigest() != blob.name:
                raise ValueError('Blob changed during migration')
            put(packet, data)
            count += 1
    for packet in packets:
        for blob in (packet / 'blobs').iterdir():
            verify(blob, blob.name)
            assert os.path.samefile(blob, store_root(packet) / blob.name)
            assert blob.stat().st_mode & 0o222 == 0
    for path, digest in manifests.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
    return {'packets': len(packets), 'blobs_verified': count, 'manifest_hashes_unchanged': manifests}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    packets = sorted(p.parent for p in args.root.rglob('manifest.json') if (p.parent / 'blobs').is_dir())
    result = migrate(packets)
    args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'manifest_hashes_unchanged'}))


if __name__ == '__main__':
    main()
