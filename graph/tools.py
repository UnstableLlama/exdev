# SPDX-License-Identifier: MIT
"""Version-one graph tools. The trusted runner owns cutoff; model args cannot change it."""
import argparse
from collections import defaultdict, deque
import fnmatch
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
from .timeline import Timeline, KINDS
from .validate import ROOT, call

SCHEMAS=json.loads((ROOT/'schema/graph-tools-v1.json').read_text())


def arguments(name,args):
    schemas={t['name']:t['parameters'] for t in SCHEMAS['tools']}
    if name not in schemas or not isinstance(args,dict):raise ValueError('Unknown graph tool or invalid arguments')
    schema=schemas[name];props=schema['properties']
    if set(args)-set(props) or set(schema['required'])-set(args):raise ValueError('Missing or unknown tool arguments')
    out={k:v['default'] for k,v in props.items() if 'default' in v};out.update(args)
    for k,value in out.items():
        spec=props[k]
        if spec['type']=='integer':
            if type(value) is not int or value<spec.get('minimum',value) or value>spec.get('maximum',value):raise ValueError('Invalid '+k)
        elif not isinstance(value,str) or len(value)<spec.get('minLength',0):raise ValueError('Invalid '+k)
        if 'enum' in spec and value not in spec['enum']:raise ValueError('Invalid '+k)
    return out


class GraphTools:
    def __init__(self,timeline,cutoff,store=None):
        self.timeline=timeline;self.cutoff=cutoff;self.store=Path(store or ROOT/'store')
        timeline.parents(cutoff)

    def invoke(self,name,args):
        a=arguments(name,args)
        self.timeline.authorize(a['commit'],self.cutoff)
        s=self.timeline.snapshot(a['commit'])
        if not s.get('provenance',{}).get('teacher_ready'):raise ValueError('Snapshot is not eligible for teacher context')
        result=getattr(self,name)(s,a)
        diag=s.get('provenance',{}).get('index_diagnostics',{})
        result.update(commit=s['sha'],schema_version=1,coverage={k:diag[k] for k in ('parse_partial_count','parse_unusable_count','skipped_count') if k in diag})
        return result

    def graph_search(self,s,a):
        nodes=sorted((n for n in s['nodes'] if n['kind'] in KINDS
                      and fnmatch.fnmatchcase(n['qn'],a['name_pattern'])
                      and fnmatch.fnmatchcase(n['file'],a['file_pattern'])
                      and ('kind' not in a or n['kind']==a['kind'])),key=lambda n:n['qn'])
        end=a['offset']+a['limit']
        return dict(nodes=nodes[a['offset']:end],has_more=end<len(nodes))

    def graph_trace(self,s,a):
        known={n['qn'] for n in s['nodes']}
        if a['symbol'] not in known:raise ValueError('Unknown symbol at this commit')
        edges=[dict(source=x,target=y,type=k,origin='backend') for x,k,y in s['edges'] if k=='CALLS']+s.get('supplemental_edges',[])
        adjacency=defaultdict(list)
        for e in edges:
            if a['direction'] in ('outbound','both'):adjacency[e['source']].append((e['target'],e))
            if a['direction'] in ('inbound','both'):adjacency[e['target']].append((e['source'],e))
        pending=deque([(a['symbol'],0)]);visited={a['symbol']};seen=set();found=[];truncated=False
        while pending:
            node,depth=pending.popleft()
            if depth>=a['depth']:continue
            for target,e in sorted(adjacency[node],key=lambda pair:(pair[0],pair[1]['origin'])):
                key=(e['source'],e['target'],e['origin'])
                if key not in seen:
                    if len(found)>=a['limit']:truncated=True;continue
                    seen.add(key);found.append(dict(e,hop=depth+1))
                if target not in visited:
                    visited.add(target);pending.append((target,depth+1))
        return dict(edges=found,truncated=truncated)

    def graph_query(self,s,a):
        path=self.store/'graphs'/(s['sha']+'.db.gz')
        expected=s['provenance'].get('backend_db_sha256')
        if not expected or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('Backend snapshot checksum mismatch')
        # Only this authorized snapshot is installed in the query cache.
        with tempfile.TemporaryDirectory(prefix='query-',dir=self.store) as tmp:
            cache=Path(tmp)
            with gzip.open(path,'rb') as src,(cache/'exllamav3.db').open('wb') as dst:shutil.copyfileobj(src,dst)
            # Merge derived edges into this disposable query database, preserving evidence.
            with sqlite3.connect(cache/'exllamav3.db') as db:
                db.execute('PRAGMA foreign_keys=ON')
                for edge in s.get('supplemental_edges',[]):
                    ids=[]
                    for endpoint in ('source','target'):
                        row=db.execute('SELECT id FROM nodes WHERE project=? AND qualified_name=?',('exllamav3',edge[endpoint])).fetchone()
                        if not row:raise ValueError('Supplemental edge endpoint missing from backend snapshot')
                        ids.append(row[0])
                    db.execute('INSERT OR IGNORE INTO edges(project,source_id,target_id,type,properties) VALUES (?,?,?,?,?)',
                               ('exllamav3',ids[0],ids[1],edge['type'],json.dumps(edge,sort_keys=True)))
            result=call('query_graph',dict(project='exllamav3',query=a['query'],format='json',max_rows=a['limit'],
                        offset=a['offset'],max_output_tokens=8000),cache,cache/'query.log')
        result['edge_scope']='backend_and_supplemental_bindings'
        return result

    def symbol_history(self,s,a):
        rows=self.timeline.history(a['symbol'],s['sha'])
        return dict(events=rows[-a['limit']:],truncated=len(rows)>a['limit'],identity='exact_qualified_name')

    def repo_map(self,s,a):
        nodes={n['qn']:n for n in s['nodes'] if n['kind'] in KINDS}
        if not nodes:return dict(text='',budget_measure='utf8_bytes',truncated=False)
        adjacency={q:set() for q in nodes}
        edges=[(x,y) for x,k,y in s['edges'] if k=='CALLS']+[(e['source'],e['target']) for e in s.get('supplemental_edges',[])]
        for x,y in edges:
            if x in nodes and y in nodes:adjacency[x].add(y)
        count=len(nodes);rank={q:1/count for q in nodes}
        for _ in range(40):
            dangling=sum(rank[q] for q in nodes if not adjacency[q])
            new={q:(.15+.85*dangling)/count for q in nodes}
            for q in sorted(nodes):
                if adjacency[q]:
                    for target in sorted(adjacency[q]):new[target]+=.85*rank[q]/len(adjacency[q])
            rank=new
        text='';included=0
        for q in sorted(nodes,key=lambda q:(-rank[q],q)):
            n=nodes[q];line=f'{q} ({n["file"]}:{n["start"]})\n'
            if len((text+line).encode())<=a['token_budget']:text+=line;included+=1
        return dict(text=text,budget_measure='utf8_bytes_conservative_token_upper_bound',truncated=included<len(nodes))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cutoff',required=True,help='Trusted runner configuration; never model-controlled')
    p.add_argument('--tool',required=True,choices=[t['name'] for t in SCHEMAS['tools']])
    p.add_argument('--args',required=True,help='JSON tool arguments including commit')
    a=p.parse_args();timeline=Timeline(ROOT/'store/timeline.sqlite')
    try:print(json.dumps(GraphTools(timeline,a.cutoff).invoke(a.tool,json.loads(a.args)),indent=2))
    finally:timeline.close()

if __name__=='__main__':main()
