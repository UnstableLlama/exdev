# SPDX-License-Identifier: MIT
"""Trusted export of strict-ancestor graphs; never expose the host timeline to a teacher."""
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
from graph.timeline import read_snapshot


def attach_graphs(packet, store):
    packet, store = Path(packet), Path(store).resolve()
    manifest = json.loads((packet/'manifest.json').read_text())
    if 'graphs' in manifest:
        raise ValueError('Graph packet is already published')
    graphs = {}
    def blob(data):
        digest = hashlib.sha256(data).hexdigest()
        (packet/'blobs'/digest).write_bytes(data)
        return digest
    with closing(sqlite3.connect((store/'timeline.sqlite').as_uri()+'?mode=ro', uri=True)) as db:
        db.row_factory = sqlite3.Row
        for sha in manifest['history_order']:
            row = db.execute('SELECT snapshot_path,fingerprint FROM commits WHERE sha=?', (sha,)).fetchone()
            if row is None:
                raise ValueError('Missing ancestor graph: '+sha)
            snapshot = read_snapshot(store, row['snapshot_path'], row['fingerprint'])
            if snapshot['sha'] != sha or snapshot['parents'] != manifest['commits'][sha]['parents']:
                raise ValueError('Graph identity/ancestry mismatch')
            provenance = snapshot.get('provenance', {})
            if provenance.get('teacher_ready') is not True:
                raise ValueError('Graph is not teacher eligible')
            archive = (store/'graphs'/(sha+'.db.gz')).read_bytes()
            if hashlib.sha256(archive).hexdigest() != provenance.get('backend_db_sha256'):
                raise ValueError('Backend archive checksum mismatch')
            # Exclude administrative paths, indexing suggestions and runtime logs.
            snapshot['provenance'] = {k:provenance[k] for k in
                ('teacher_ready','backend_binary_sha256','backend_db_sha256') if k in provenance}
            snapshot['provenance']['index_diagnostics'] = {k:v for k,v in
                provenance.get('index_diagnostics',{}).items() if k in
                ('parse_partial_count','parse_unusable_count','skipped_count')}
            events = []
            for event in db.execute('SELECT qn,sha,event,previous_qn,file,start,end,origin,parents FROM symbol_event_provenance WHERE sha=?', (sha,)):
                event = dict(event)
                event['parents'] = json.loads(event['parents'])
                event['position'] = snapshot['position']
                events.append(event)
            graphs[sha] = {'snapshot':blob(json.dumps(snapshot,sort_keys=True).encode()),
                           'backend':blob(archive), 'events':blob(json.dumps(events,sort_keys=True).encode())}
    manifest['graphs'] = graphs
    temporary = packet/'manifest.new'
    temporary.write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    temporary.replace(packet/'manifest.json')
    return len(graphs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--store', type=Path, default=Path('store'))
    args = parser.parse_args()
    print(json.dumps({'ancestor_graphs':attach_graphs(args.packet,args.store)}))


if __name__ == '__main__':
    main()
