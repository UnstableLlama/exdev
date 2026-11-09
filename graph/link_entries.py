# SPDX-License-Identifier: MIT
"""Load explicit entry/symbol links; validate source revision and ancestry before writes."""
import json
from .timeline import Timeline
from .validate import ROOT


def load_links(timeline, seeds, entries):
    records=[]
    for row in seeds['entries']:
        entry=entries[row['entry_id']];sha=entry['sha']
        timeline.parents(sha)
        links=[]
        for ref in row['symbols']:
            if ref['revision']=='entry':source=sha
            elif ref['revision']=='first_parent' and entry['parent_shas']:source=entry['parent_shas'][0]
            else:raise ValueError('Invalid link revision')
            timeline.authorize(source,sha)
            found=timeline.db.execute('SELECT data FROM occurrences WHERE sha=? AND qn=?',(source,ref['qn'])).fetchone()
            if not found:raise ValueError(f'Unresolved explicit symbol link: {row["entry_id"]} {ref["qn"]}')
            n=json.loads(found[0])
            links.append(dict(qn=ref['qn'],source_sha=source,file=n['file'],start=n['start'],end=n['end'],revision=ref['revision']))
        records.append(dict(entry_id=row['entry_id'],entry_sha=sha,symbols=links,scope_note=row.get('scope_note','')))
    # Validate the entire seed set first, then atomically replace only those entries' links.
    with timeline.db:
        for row in records:
            timeline.db.execute('DELETE FROM entry_links WHERE entry_id=?',(row['entry_id'],))
            for ref in row['symbols']:
                timeline.db.execute('INSERT INTO entry_links VALUES (?,?,?)',(ref['source_sha'],ref['qn'],row['entry_id']))
    return dict(schema_version=1,entries=records)


def main():
    seeds=json.loads((ROOT/'seeds/entry-symbol-links.json').read_text())
    entries={p.stem:json.loads(p.read_text()) for p in (ROOT/'encyclopedia/entries').glob('*.json')}
    timeline=Timeline(ROOT/'store/timeline.sqlite')
    try:
        result=load_links(timeline,seeds,entries)
        (ROOT/'encyclopedia/symbol-links.json').write_text(json.dumps(result,indent=2)+'\n')
        print(f'{len(result["entries"])} entries, {sum(len(r["symbols"]) for r in result["entries"])} symbol links')
    finally:timeline.close()

if __name__=='__main__':main()
