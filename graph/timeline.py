# SPDX-License-Identifier: MIT
"""Transactional commit snapshots and first-parent symbol events with ancestry guards."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sqlite3

KINDS = {'Function', 'Method', 'Class', 'Struct', 'Enum'}


def symbols(nodes):
    return {n['qn']: n for n in nodes if n['kind'] in KINDS and n.get('body_hash')}


def symbol_diff(before, after):
    a,b = symbols(before),symbols(after)
    events = []
    def event(kind,n,previous=None):
        events.append(dict(event=kind,qn=n['qn'],previous_qn=previous, file=n['file'],start=n['start'],end=n['end']))
    for qn in sorted(a.keys() & b.keys()):
        if a[qn]['body_hash'] != b[qn]['body_hash'] or a[qn]['kind'] != b[qn]['kind']:
            event('changed', b[qn])
        elif a[qn]['file'] != b[qn]['file']:
            event('moved', b[qn], qn)
    old,new = set(a)-set(b),set(b)-set(a)
    def groups(nodes):
        g=defaultdict(list)
        for q,n in nodes.items(): g[(n['kind'],n['name'],n['body_hash'])].append(q)
        return g
    ga,gb=groups(a),groups(b)
    for key in sorted(ga.keys() & gb.keys()):
        if len(ga[key]) == len(gb[key]) == 1:
            x,y=ga[key][0],gb[key][0]
            if x in old and y in new:
                event('moved', b[y], x)
                old.remove(x);new.remove(y)
    for q in sorted(old): event('removed',a[q])
    for q in sorted(new): event('added',b[q])
    return sorted(events,key=lambda e:(e['qn'],e['event']))


SCHEMA = '''
CREATE TABLE IF NOT EXISTS commits(
 sha TEXT PRIMARY KEY, position INTEGER NOT NULL UNIQUE, parents TEXT NOT NULL,
 parent_sha TEXT REFERENCES commits(sha), fingerprint TEXT NOT NULL, snapshot TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS symbols(
 qn TEXT PRIMARY KEY, first_observed_sha TEXT NOT NULL REFERENCES commits(sha),
 last_observed_sha TEXT NOT NULL REFERENCES commits(sha));
CREATE TABLE IF NOT EXISTS occurrences(
 sha TEXT NOT NULL REFERENCES commits(sha), qn TEXT NOT NULL REFERENCES symbols(qn),
 data TEXT NOT NULL, PRIMARY KEY(sha,qn));
CREATE TABLE IF NOT EXISTS symbol_events(
 sha TEXT NOT NULL REFERENCES commits(sha), qn TEXT NOT NULL REFERENCES symbols(qn),
 event TEXT NOT NULL CHECK(event IN ('added','removed','changed','moved')),
 previous_qn TEXT, file TEXT NOT NULL, start INTEGER NOT NULL, end INTEGER NOT NULL,
 PRIMARY KEY(sha,qn,event));
CREATE TABLE IF NOT EXISTS entry_links(
 sha TEXT NOT NULL, qn TEXT NOT NULL, entry_id TEXT NOT NULL,
 PRIMARY KEY(sha,qn,entry_id), FOREIGN KEY(sha,qn) REFERENCES occurrences(sha,qn));
CREATE INDEX IF NOT EXISTS events_symbol ON symbol_events(qn);
PRAGMA user_version=1;
'''


class Timeline:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path)
        self.db.execute('PRAGMA foreign_keys=ON')
        if self.db.execute('PRAGMA user_version').fetchone()[0] not in (0,1):
            self.db.close();raise ValueError('Unsupported timeline schema version')
        self.db.executescript(SCHEMA)

    def close(self): self.db.close()

    def parents(self,sha):
        row=self.db.execute('SELECT parents FROM commits WHERE sha=?',(sha,)).fetchone()
        if not row: raise ValueError('Unknown commit: '+sha)
        return json.loads(row[0])

    def ancestors(self,sha):
        seen=set();pending=[sha]
        while pending:
            current=pending.pop()
            if current not in seen:
                seen.add(current);pending.extend(self.parents(current))
        return seen

    def authorize(self,commit,cutoff):
        if commit not in self.ancestors(cutoff):
            raise ValueError('Requested commit is not an ancestor of the authorized cutoff')

    def snapshot(self,sha):
        row=self.db.execute('SELECT snapshot FROM commits WHERE sha=?',(sha,)).fetchone()
        if not row: raise ValueError('Unknown commit: '+sha)
        return json.loads(row[0])

    def ingest(self,snapshot):
        # Persist only semantic inputs; runtime logs and timing are not identity.
        s={k:snapshot[k] for k in ('sha','position','parents','nodes','edges','backend')}
        s['supplemental_edges']=snapshot.get('supplemental_edges',[])
        s['provenance']=snapshot.get('provenance',{})
        serialized=json.dumps(s,sort_keys=True,separators=(',',':'))
        digest=hashlib.sha256(serialized.encode()).hexdigest()
        old=self.db.execute('SELECT fingerprint FROM commits WHERE sha=?',(s['sha'],)).fetchone()
        if old:
            if old[0]!=digest: raise ValueError('Commit already has different snapshot inputs')
            return False
        for parent in s['parents']:
            p=self.db.execute('SELECT position FROM commits WHERE sha=?',(parent,)).fetchone()
            if not p: raise ValueError('Missing parent snapshot: '+parent)
            if p[0]>=s['position']: raise ValueError('Parent must precede child')
        if not s['parents'] and self.db.execute('SELECT count(*) FROM commits').fetchone()[0]:
            raise ValueError('Additional disconnected root is not supported')
        previous=self.snapshot(s['parents'][0])['nodes'] if s['parents'] else []
        events=symbol_diff(previous,s['nodes'])
        with self.db:
            self.db.execute('INSERT INTO commits VALUES (?,?,?,?,?,?)',(s['sha'],s['position'],json.dumps(s['parents']),s['parents'][0] if s['parents'] else None,digest,serialized))
            for q,n in sorted(symbols(s['nodes']).items()):
                self.db.execute('INSERT INTO symbols VALUES (?,?,?) ON CONFLICT(qn) DO UPDATE SET last_observed_sha=excluded.last_observed_sha',(q,s['sha'],s['sha']))
                self.db.execute('INSERT INTO occurrences VALUES (?,?,?)',(s['sha'],q,json.dumps(n,sort_keys=True)))
            for e in events:
                self.db.execute('INSERT INTO symbol_events VALUES (?,?,?,?,?,?,?)',(s['sha'],e['qn'],e['event'],e['previous_qn'],e['file'],e['start'],e['end']))
        return True

    def history(self,qn,commit):
        allowed=self.ancestors(commit)
        rows=self.db.execute('SELECT e.sha,e.event,e.previous_qn,e.file,e.start,e.end,c.position FROM symbol_events e JOIN commits c USING(sha) WHERE e.qn=? ORDER BY c.position',(qn,)).fetchall()
        return [dict(zip(('sha','event','previous_qn','file','start','end','position'),r)) for r in rows if r[0] in allowed]
