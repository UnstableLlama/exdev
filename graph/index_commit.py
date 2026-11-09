# SPDX-License-Identifier: MIT
"""Isolated, resumable chronological graph indexing. No source Git history reaches the backend."""
import argparse
import fcntl
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
from .bindings import supplement
from .timeline import Timeline
from .validate import ROOT, BIN, PIN, call

VERSION=1
WORK=ROOT/'.graph-work/production/exllamav3'
STORE=ROOT/'store'


def isolated_checkout(git_dir,sha,work):
    work=Path(work)
    marker=work.parent/(work.name+'.exdev-owned')
    if work.exists() and not marker.exists():
        raise ValueError('Refusing to replace a directory not owned by exdev')
    archive=subprocess.check_output(['git','--git-dir='+str(git_dir),'archive',sha])
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    marker.write_text('Generated isolated source tree; safe to rebuild.\n')
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(work,filter='data')
    # An empty local repository prevents discovery of the enclosing exdev repo.
    # No upstream objects, refs, configuration, remotes or history are copied.
    subprocess.run(['git','init','-q',str(work)],check=True,capture_output=True)


def export(query,cache,logs,label):
    rows=[]
    while True:
        offset=len(rows)
        r=call('query_graph',dict(project='exllamav3',query=query,format='json',max_rows=10000,
                                 offset=offset,max_output_tokens=100000),cache,logs/f'{label}-{offset}.log')
        rows.extend(r['rows'])
        if not r.get('has_more') and not r.get('truncated'): return rows
        if len(rows)==offset: raise RuntimeError('Truncated export without progress')


def build(rec):
    sha=rec['sha'];folder=STORE/'graphs';folder.mkdir(parents=True,exist_ok=True)
    result_path=folder/(sha+'.json.gz')
    if result_path.exists():
        with gzip.open(result_path,'rt') as f:s=json.load(f)
        if (s['sha']!=sha or s['parents']!=rec['parent_shas'] or s['position']!=rec['position']
                or s['provenance']['pipeline_version']!=VERSION or s['provenance']['backend_binary_sha256']!=PIN):
            raise ValueError('Incompatible existing snapshot; use a new store')
        db_path=folder/(sha+'.db.gz')
        if not db_path.exists(): raise ValueError('Snapshot database missing')
        if hashlib.sha256(db_path.read_bytes()).hexdigest()!=s['provenance']['backend_db_sha256']:
            raise ValueError('Snapshot database checksum mismatch')
        return s
    isolated_checkout(ROOT/'.sources/exllamav3.git',sha,WORK)
    logs=STORE/'logs'/sha;logs.mkdir(parents=True,exist_ok=True)
    cache=Path(tempfile.mkdtemp(prefix='cache-',dir=WORK.parent))
    index=call('index_repository',dict(repo_path=str(WORK),name='exllamav3',mode='full'),cache,logs/'index.log')
    nr=export('MATCH (n) RETURN n.qualified_name, n.name, n.label, n.file_path, n.start_line, n.end_line ORDER BY n.qualified_name',cache,logs,'nodes')
    er=export('MATCH (a)-[r]->(b) RETURN a.qualified_name, type(r), b.qualified_name ORDER BY a.qualified_name, b.qualified_name',cache,logs,'edges')
    nodes=[];source_lines={}
    for qn,name,kind,path,start,end in nr:
        n=dict(qn=qn,name=name,kind=kind,file=path,start=int(start or 0),end=int(end or 0))
        p=WORK/path
        if path and p.is_file() and n['start']>0 and n['end']>=n['start']:
            if path not in source_lines:source_lines[path]=p.read_bytes().splitlines(keepends=True)
            n['body_hash']=hashlib.sha256(b''.join(source_lines[path][n['start']-1:n['end']])).hexdigest()
        nodes.append(n)
    snapshot_db=logs/'snapshot.db'
    with sqlite3.connect(f'file:{cache}/exllamav3.db?mode=ro',uri=True) as src:
        src.execute('PRAGMA foreign_keys=ON')
        counts=[src.execute(f"SELECT count(*) FROM {t} WHERE project='exllamav3'").fetchone()[0] for t in ('nodes','edges')]
        if counts!=[len(nodes),len(er)]:raise RuntimeError('Graph export counts do not match database')
        with sqlite3.connect(snapshot_db) as dst:
            dst.execute('PRAGMA foreign_keys=ON');src.backup(dst)
    s=dict(sha=sha,position=rec['position'],parents=rec['parent_shas'],backend='0.12.1',nodes=nodes,edges=er,
           provenance=dict(pipeline_version=VERSION,backend_binary_sha256=PIN,source_isolation='archive-plus-empty-git',
                           teacher_ready=True,index_diagnostics=index,commit_date=rec['commit_date']))
    files={str(p.relative_to(WORK)):p.read_text(errors='replace') for p in sorted(WORK.rglob('*'))
           if p.is_file() and '.git' not in p.relative_to(WORK).parts and p.suffix in ('.py','.cpp','.cu','.cc')}
    bindings=supplement(s,files);s['supplemental_edges']=bindings['edges']
    (logs/'bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
    db_path=folder/(sha+'.db.gz')
    with snapshot_db.open('rb') as src,gzip.open(str(db_path)+'.tmp','wb') as dst:shutil.copyfileobj(src,dst)
    Path(str(db_path)+'.tmp').replace(db_path)
    s['provenance']['backend_db_sha256']=hashlib.sha256(db_path.read_bytes()).hexdigest()
    with gzip.open(str(result_path)+'.tmp','wt') as f:json.dump(s,f,sort_keys=True)
    Path(str(result_path)+'.tmp').replace(result_path)
    snapshot_db.unlink();shutil.rmtree(cache)
    return s


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stop-position',type=int,required=True,help='Inclusive miner position; resume skips verified snapshots')
    args=p.parse_args()
    if args.stop_position<1:p.error('stop-position must be positive')
    if hashlib.sha256(BIN.read_bytes()).hexdigest()!=PIN:raise ValueError('Backend checksum mismatch')
    STORE.mkdir(exist_ok=True)
    records=sorted((ROOT/'data/exllamav3-v5/records').glob('*.json'))
    if not records or args.stop_position>int(records[-1].name.split('_')[0]):
        raise ValueError('Requested position is outside the pinned mined history')
    with (STORE/'index.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        timeline=Timeline(STORE/'timeline.sqlite')
        try:
            for path in records:
                position=int(path.name.split('_')[0])
                if position>args.stop_position:break
                rec=json.loads(path.read_text())
                for parent in rec['parent_shas']:timeline.parents(parent)
                if shutil.disk_usage(STORE).free < 2 * 1024**3:
                    raise RuntimeError('Less than 2 GiB free; graph walk stopped at a resumable checkpoint')
                s=build(rec);created=timeline.ingest(s)
                print(f'{position} {s["sha"][:12]} {"indexed" if created else "verified"}: {len(s["nodes"])} nodes, {len(s["supplemental_edges"])} binding edges',flush=True)
            if timeline.db.execute('PRAGMA foreign_key_check').fetchall():raise RuntimeError('Foreign key violation')
        finally:timeline.close()

if __name__=='__main__':main()
