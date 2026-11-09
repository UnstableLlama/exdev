# SPDX-License-Identifier: MIT
"""Read-only source/database audit of a fixed prefix while indexing continues."""
import argparse
from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
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
from .timeline import symbol_diff, symbols, read_snapshot
from .validate import ROOT


def readonly(path):
    db=sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True,timeout=30)
    db.execute('PRAGMA foreign_keys=ON');db.execute('PRAGMA query_only=ON')
    return db


def verify_export(snapshot,path):
    with closing(readonly(path)) as db:
        if db.execute('PRAGMA quick_check').fetchall()!=[('ok',)]:raise ValueError('Backend database integrity failure')
        actual=Counter(db.execute("SELECT qualified_name,name,label,file_path,start_line,end_line FROM nodes WHERE project='exllamav3'"))
        expected=Counter((n['qn'],n['name'],n['kind'],n['file'],n['start'],n['end']) for n in snapshot['nodes'])
        if actual!=expected:raise ValueError('Exported nodes differ from backend database')
        actual=Counter(db.execute("SELECT a.qualified_name,e.type,b.qualified_name FROM edges e JOIN nodes a ON a.id=e.source_id JOIN nodes b ON b.id=e.target_id WHERE e.project='exllamav3'"))
        if actual!=Counter(tuple(e) for e in snapshot['edges']):raise ValueError('Exported edges differ from backend database')


def verify_source(snapshot,files):
    checked=0
    for n in snapshot['nodes']:
        if 'body_hash' not in n:continue
        if n['file'] not in files:raise ValueError('Indexed source missing: '+n['file'])
        lines=files[n['file']].splitlines(keepends=True)
        body=b''.join(lines[n['start']-1:n['end']])
        if hashlib.sha256(body).hexdigest()!=n['body_hash']:raise ValueError('Indexed source hash differs: '+n['qn'])
        checked+=1
    return checked


def verify_events(before,after,stored):
    if sorted(stored,key=lambda e:(e['qn'],e['event']))!=symbol_diff(before,after):
        raise ValueError('Stored symbol events differ from first-parent diff')


def source_archive(sha):
    data=subprocess.check_output(['git','--git-dir='+str(ROOT/'.sources/exllamav3.git'),'archive',sha])
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        return {m.name:tar.extractfile(m).read() for m in tar if m.isfile()}


def audit(store,limit=None):
    store=Path(store)
    with closing(readonly(store/'timeline.sqlite')) as db:
        # Capture immutable commit identities only; release read locks between queries
        # so the indexer can keep committing newer snapshots.
        rows=db.execute('SELECT sha,position,parents,fingerprint FROM commits WHERE position<=? ORDER BY position',
                        (limit if limit is not None else 2**63-1,)).fetchall()
        if not rows:raise ValueError('No completed snapshots to audit')
        if [r[1] for r in rows]!=list(range(1,rows[-1][1]+1)):raise ValueError('Indexed prefix has gaps')
        seen=set();counts=Counter();last=None
        for sha,position,parents_json,fingerprint in rows:
            parents=json.loads(parents_json)
            if not set(parents)<=seen:raise ValueError('Parent absent from earlier verified prefix')
            with gzip.open(store/'graphs'/(sha+'.json.gz'),'rt') as f:s=json.load(f)
            if (s['sha'],s['position'],s['parents'])!=(sha,position,parents):raise ValueError('Snapshot identity mismatch')
            rec=json.loads((ROOT/f'data/exllamav3-v5/records/{position:06d}_{sha}.json').read_text())
            if rec['parent_shas']!=parents:raise ValueError('Mined parent mismatch')
            upstream=subprocess.check_output(['git','--git-dir='+str(ROOT/'.sources/exllamav3.git'),'show','-s','--format=%P',sha],text=True).split()
            if upstream!=parents:raise ValueError('Upstream parent mismatch')
            serialized=json.dumps(s,sort_keys=True,separators=(',',':'))
            if hashlib.sha256(serialized.encode()).hexdigest()!=fingerprint:raise ValueError('Snapshot fingerprint mismatch')
            stored=db.execute('SELECT snapshot_path,parent_sha FROM commits WHERE sha=?',(sha,)).fetchone()
            if read_snapshot(store,stored[0],fingerprint)!=s or stored[1]!=(parents[0] if parents else None):raise ValueError('Timeline snapshot mismatch')
            archive=store/'graphs'/(sha+'.db.gz')
            if hashlib.sha256(archive.read_bytes()).hexdigest()!=s['provenance']['backend_db_sha256']:raise ValueError('Database archive checksum mismatch')
            with tempfile.TemporaryDirectory(prefix='exdev-audit-') as tmp:
                path=Path(tmp)/'snapshot.db'
                with gzip.open(archive,'rb') as src,path.open('wb') as dst:shutil.copyfileobj(src,dst)
                verify_export(s,path)
            files=source_archive(sha)
            counts['source_ranges']+=verify_source(s,files)
            textfiles={p:b.decode('utf-8',errors='replace').replace('\r\n','\n').replace('\r','\n') for p,b in files.items()
                       if p.endswith(('.py','.cpp','.cc','.cu'))}
            if supplement(s,textfiles)['edges']!=s['supplemental_edges']:raise ValueError('Binding edges do not reproduce from source')
            if parents:
                previous=last if last and last['sha']==parents[0] else read_snapshot(store,*db.execute('SELECT snapshot_path,fingerprint FROM commits WHERE sha=?',(parents[0],)).fetchone())
                before=previous['nodes']
            else:before=[]
            events=[dict(zip(('qn','event','previous_qn','file','start','end'),r)) for r in db.execute('SELECT qn,event,previous_qn,file,start,end FROM symbol_events WHERE sha=?',(sha,))]
            verify_events(before,s['nodes'],events)
            occurrences={q:json.loads(data) for q,data in db.execute('SELECT qn,data FROM occurrences WHERE sha=?',(sha,))}
            if occurrences!=symbols(s['nodes']):raise ValueError('Symbol occurrence mismatch')
            counts.update(commits=1,nodes=len(s['nodes']),edges=len(s['edges']),supplemental_edges=len(s['supplemental_edges']),symbol_events=len(events))
            seen.add(sha);last=s
            if position%10==0:print(f'Audited through {position}: {sha[:12]}',flush=True)
        if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Timeline foreign-key failure')
    return dict(status='passed',audited_at=datetime.now(timezone.utc).isoformat(),through_position=rows[-1][1],
                through_sha=rows[-1][0],counts=dict(counts),scope='Completed prefix captured at audit start; not a full-history completion claim',
                checks=['commit_and_parent_identity','archive_checksum','exact_node_and_edge_multisets','source_range_hashes',
                        'reproduced_binding_edges','first_parent_events','symbol_occurrences','timeline_fingerprint','foreign_keys'])


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stop-position',type=int)
    p.add_argument('--store',type=Path,default=ROOT/'store');p.add_argument('--out',type=Path,default=ROOT/'reports/graph-audit.json')
    a=p.parse_args()
    try:result=audit(a.store,a.stop_position)
    except Exception as e:
        result=dict(status='failed',audited_at=datetime.now(timezone.utc).isoformat(),error=str(e))
        a.out.write_text(json.dumps(result,indent=2)+'\n');raise
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
