# SPDX-License-Identifier: MIT
"""Mechanical file-to-ancestor navigation, shared by startup and reporting."""
import json
from pathlib import Path
from .worker import load_blob


def matching_targets(packet, manifest):
    files=set(manifest.get('task_changed_files',[]))
    rows=json.loads(load_blob(Path(packet),manifest['ancestor_search_blob'])) if 'ancestor_search_blob' in manifest else []
    return sorted({(r['sha'],r['chapter']) for r in rows if r['file'] in files})


def opening_matches(packet, manifest):
    targets=matching_targets(packet,manifest)
    refs={r['sha']:r for r in manifest.get('ancestor_entries',[])}
    rank={sha:i for i,sha in enumerate(manifest['history_order'])}
    for sha,chapter in targets:
        if sha not in manifest['commits'] or sha not in refs or (chapter and chapter not in refs[sha]['chapters']):
            raise ValueError('Matching target outside approved ancestry')
    targets.sort(key=lambda t:(-rank[t[0]],t[1]))
    page=[]
    for sha,chapter in targets:
        row={'sha':sha,'chapter':chapter}
        if len(page)>=12 or len(json.dumps(page+[row]).encode())>4096:break
        page.append(row)
    return {'kind':'navigation_only','matching_target_count':len(targets),'targets':page,
            'truncated':len(page)<len(targets),'lookup_tool':'ancestor_read',
            'lookup_mode':'search'}
