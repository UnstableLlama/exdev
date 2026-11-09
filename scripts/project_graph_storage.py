# SPDX-License-Identifier: MIT
"""Measure live graph storage and project its full-history size from sampled snapshots."""
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import sqlite3
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def size_tree(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def zipped_size(path):
    with tempfile.TemporaryFile() as out:
        with path.open('rb') as src,gzip.GzipFile(fileobj=out,mode='wb') as dst:
            shutil.copyfileobj(src,dst)
        return out.tell()


def interpolate(points,position,key):
    if position<=points[0]['position']:return points[0][key]
    for a,b in zip(points,points[1:]):
        if position<=b['position']:
            fraction=(position-a['position'])/(b['position']-a['position'])
            return a[key]+fraction*(b[key]-a[key])
    return points[-1][key]


def main():
    store=ROOT/'store';db=sqlite3.connect((store/'timeline.sqlite').as_uri()+'?mode=ro',uri=True)
    db.execute('BEGIN')
    version=db.execute('PRAGMA user_version').fetchone()[0]
    if version==1:
        rows=db.execute("SELECT sha,position,length(CAST(snapshot AS BLOB)),json_array_length(snapshot,'$.nodes'),json_array_length(snapshot,'$.edges') FROM commits ORDER BY position").fetchall()
    else:
        rows=[]
        for sha,position,relative in db.execute('SELECT sha,position,snapshot_path FROM commits ORDER BY position'):
            with gzip.open(store/relative,'rt') as handle:snapshot=json.load(handle)
            payload=len(json.dumps(snapshot,sort_keys=True,separators=(',',':')).encode())
            rows.append((sha,position,payload,len(snapshot['nodes']),len(snapshot['edges'])))
    allocation=dict(db.execute('SELECT name,sum(pgsize) FROM dbstat GROUP BY name'))
    occurrence_bytes=db.execute('SELECT sum(length(CAST(data AS BLOB))) FROM occurrences').fetchone()[0]
    db.rollback();db.close()
    occurrence_allocation=sum(v for k,v in allocation.items() if k=='occurrences' or k.startswith('sqlite_autoindex_occurrences'))
    occurrence_factor=occurrence_allocation/occurrence_bytes
    curve=[]
    for sha,pos,payload,nodes,edges in rows:
        curve.append(dict(position=pos,sha=sha,nodes=nodes,edges=edges,sqlite_snapshot_bytes=payload,
                          compressed_graph_bytes=(store/'graphs'/f'{sha}.json.gz').stat().st_size,
                          compressed_db_bytes=(store/'graphs'/f'{sha}.db.gz').stat().st_size,
                          log_bytes=size_tree(store/'logs'/sha)))
    points=[]
    for folder in (ROOT/'data/graph/validation').iterdir():
        result=folder/'result.json'
        if not result.exists():continue
        s=json.loads(result.read_text())
        bs=json.loads((folder/'bindings-v1.json').read_text())['edges']
        canonical={k:s[k] for k in ('sha','position','parents','nodes','edges','backend')}
        canonical.update(supplemental_edges=bs,provenance={'source_isolation':'archive-plus-empty-git','index_diagnostics':s['index']})
        payload=json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()
        nodes=[n for n in s['nodes'] if n['kind'] in ('Function','Method','Class','Struct','Enum') and n.get('body_hash')]
        occurrences=sum(len(json.dumps(n,sort_keys=True).encode()) for n in nodes)*occurrence_factor
        logs=sum(p.stat().st_size for p in folder.glob('*.log') if p.name=='index.log' or p.name.startswith(('nodes-','edges-')))+(folder/'bindings-v1.json').stat().st_size
        points.append(dict(position=s['position'],nodes=len(s['nodes']),edges=len(s['edges']),
                           sqlite_snapshot_bytes=len(payload),occurrence_allocated_bytes=round(occurrences),
                           compressed_graph_bytes=len(gzip.compress(json.dumps(canonical,sort_keys=True).encode())),
                           compressed_db_bytes=zipped_size(folder/'snapshot.db'),log_bytes=logs))
    points.sort(key=lambda p:p['position'])
    keys=['sqlite_snapshot_bytes','occurrence_allocated_bytes','compressed_graph_bytes','compressed_db_bytes','log_bytes']
    projected={k:round(sum(interpolate(points,i,k) for i in range(1,2265))) for k in keys}
    total=sum(projected.values());without=total-projected['sqlite_snapshot_bytes']
    report=dict(measured_at=datetime.now(timezone.utc).isoformat(),through_position=rows[-1][1],
                timeline_schema_version=version,
                note='sqlite_snapshot_bytes in the curve measures the uncompressed logical payload; v2 stores only its archive path, not this payload.',
                measured_sqlite_page_allocation=allocation,measured_prefix_curve=curve,sample_estimates=points,
                projected_components_bytes=projected,projected_total_bytes=total,
                projected_without_duplicate_snapshot_bytes=without,
                scenario_range_without_duplicate_bytes=[round(without*.7),round(without*1.3)],
                free_disk_bytes=shutil.disk_usage(store).free,
                method='Piecewise-linear interpolation of per-commit component sizes across four historical samples; occurrence page overhead calibrated on current SQLite. This is a sizing model, not measured full-history storage. The +/-30% range is a sensitivity scenario, not a confidence interval.',
                exclusions=['source mirrors and preliminary validation stores','temporary indexing caches','migration backup','SQLite events/index overhead beyond occurrences; small in current prefix'])
    (ROOT/'reports/graph-storage-projection.json').write_text(json.dumps(report,indent=2)+'\n')
    gib=lambda n:round(n/1024**3,2)
    print(json.dumps(dict(through_position=rows[-1][1],components_GiB={k:gib(v) for k,v in projected.items()},
                    total_GiB=gib(total),without_duplicate_GiB=gib(without),free_GiB=gib(report['free_disk_bytes'])),indent=2))

if __name__=='__main__':main()
