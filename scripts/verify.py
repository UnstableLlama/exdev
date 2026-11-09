#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 UnstableLlama and exdev contributors
"""Check record integrity, DAG order and exact first-25 patch replay (no GPU claims)."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile
from mine import git, text, parent_checkout, atomic_json


def verify(repo, data, entry_dir):
    manifest=json.loads((data/'manifest.json').read_text())
    records=sorted((data/'records').glob('*.json'))
    expected=text(git(repo,'rev-list','--reverse','--topo-order',manifest['head'])).splitlines()
    assert len(records)==len(expected), 'Record count mismatch'
    seen=set(); counts=Counter(); noise=0
    db=sqlite3.connect(data/'index.sqlite3');db.execute('PRAGMA foreign_keys=ON')
    for position,(path,sha) in enumerate(zip(records,expected),1):
        r=json.loads(path.read_text())
        assert (r['position'],r['sha'])==(position,sha)
        assert set(r['parent_shas'])<=seen, 'Parent appears after child'
        assert hashlib.sha256(r['diff'].encode('utf-8','surrogateescape')).hexdigest()==r['diff_sha256']
        stored=db.execute('SELECT record_sha256 FROM commits WHERE sha=?',(sha,)).fetchone()
        assert stored and stored[0]==hashlib.sha256(path.read_bytes()).hexdigest()
        seen.add(sha);counts[r['type']]+=1;noise+=r['noise']
    assert db.execute('SELECT count(*) FROM commits').fetchone()[0]==len(records)
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    report=json.loads((data/'report.json').read_text())
    assert dict(counts)==report['counts_per_type'] and noise==report['noise_count']
    entries=sorted(entry_dir.glob('*.json'));replayed=[]
    for position,path in enumerate(entries,1):
        e=json.loads(path.read_text());r=json.loads(records[position-1].read_text())
        assert e['position']==position and e['sha']==r['sha']
        assert e['diff_sha256']==r['diff_sha256']
        assert all(0<i<position for i in e['links'])
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/'parent';parent_checkout(repo,r['sha'],dest)
            subprocess.run(['git','apply','--check','--binary','-'],input=r['diff'].encode('utf-8','surrogateescape'),cwd=dest,check=True,capture_output=True)
            subprocess.run(['git','apply','--binary','-'],input=r['diff'].encode('utf-8','surrogateescape'),cwd=dest,check=True,capture_output=True)
            # Compare every tracked path, including binary assets, without importing upstream code.
            expected_tree={}
            for item in git(repo,'ls-tree','-rz',r['sha']).split(b'\0'):
                if not item:continue
                meta,name=item.split(b'\t',1);mode,kind,blob=meta.split()
                if kind!=b'blob':raise AssertionError('Submodule verification not implemented')
                expected_tree[text(name)]=(mode.decode(),blob.decode())
            actual_paths={str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file() or p.is_symlink()}
            assert actual_paths==set(expected_tree), 'Tree paths differ'
            for name,(mode,blob) in expected_tree.items():
                p=dest/name
                raw=str(p.readlink()).encode() if p.is_symlink() else p.read_bytes()
                calculated=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
                assert calculated==blob, 'Blob mismatch: '+name
                assert (p.is_symlink())==(mode=='120000')
                if mode!='120000':assert bool(p.stat().st_mode & 0o111)==(mode=='100755')
            replayed.append(r['sha'])
    result={'records':len(records),'entries':len(entries),'replayed_trees':len(replayed),'head':manifest['head'],
            'checks':['unique sequence and parent-before-child order','raw diff SHA-256','SQLite record checksums and row counts','type/noise totals','entry identity and backward links','first-25 full patch replay, paths, blob hashes and executable modes'],
            'not_checked':['upstream imports','CUDA builds','model inference','quantization numerical equivalence','complete external-source research'],
            'entry_statuses':dict(Counter(json.loads(p.read_text())['status'] for p in entries))}
    db.close();return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.sources/exllamav3.git'));p.add_argument('--data',type=Path,default=Path('data/exllamav3-v5'));p.add_argument('--entries',type=Path,default=Path('encyclopedia/entries'));a=p.parse_args()
    result=verify(a.repo,a.data,a.entries);atomic_json(Path('reports/verification.json'),result);print(json.dumps(result,indent=2))
