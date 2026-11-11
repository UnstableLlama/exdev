# SPDX-License-Identifier: MIT
"""Select historical content without exposing post-cutoff metadata to an author."""
from datetime import datetime
import hashlib
import json


def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Evidence timestamps must include a timezone')
    return result


def eligible_content(obj, cutoff):
    bound = timestamp(cutoff)
    if timestamp(obj['createdAt']) > bound or 'lastEditedAt' not in obj:
        return None
    if 'publishedAt' in obj and (not obj['publishedAt'] or timestamp(obj['publishedAt']) > bound):
        return None
    last = obj['lastEditedAt']
    if last is None or timestamp(last) <= bound:
        content = obj['body']
        revision = last or obj['createdAt']
        representation = 'body'
        source_id = obj['id']
    else:
        # GitHub documents `diff` as a summary of changes. Preserve that meaning:
        # even when it resembles a complete body, never label it a recovered body.
        candidates = [e for e in obj.get('edits', []) if e.get('diff') is not None
                      and not e.get('deletedAt') and timestamp(obj['createdAt']) <= timestamp(e['editedAt']) <= bound]
        if not candidates:
            return None
        edit = max(candidates, key=lambda e: timestamp(e['editedAt']))
        content, revision, source_id = edit['diff'], edit['editedAt'], edit['id']
        representation = 'edit_event_text'
    return {'author_login': (obj.get('author') or {}).get('login'), 'url': obj['url'], 'source_id': source_id, 'created_at': obj['createdAt'],
            'revision_at': revision, 'representation': representation, 'content': content,
            'content_sha256': hashlib.sha256(content.encode()).hexdigest()}


def discussion_snapshot(bundle, cutoff):
    """Build one fail-closed, as-of-cutoff open-discussion snapshot.

    The returned catalog row contains only trusted metadata plus an optional
    structured content payload. Callers remove that payload from opening
    context and expose it only through an explicit evidence read.
    """
    bound = timestamp(cutoff)
    if timestamp(bundle['createdAt']) > bound:
        return None
    if not bundle.get('timeline_complete'):
        raise ValueError('Discussion timeline recovery is incomplete')
    state = 'OPEN'
    for event in sorted(bundle.get('state_events', []), key=lambda e: timestamp(e['createdAt'])):
        if timestamp(event['createdAt']) > bound:
            break
        if event['kind'] == 'closed':
            state = 'CLOSED'
        elif event['kind'] == 'reopened':
            state = 'OPEN'
        else:
            raise ValueError('Unknown discussion state event')
    if state != 'OPEN':
        return None
    title = bundle['title']
    title_events = sorted(bundle.get('title_events', []), key=lambda e: timestamp(e['createdAt']))
    for event in reversed(title_events):
        if timestamp(event['createdAt']) > bound:
            title = event['previousTitle']
    row = {'number': bundle['number'], 'kind': bundle['kind'], 'title': title,
           'author_login': (bundle.get('author') or {}).get('login'),
           'created_at': bundle['createdAt'], 'state': state, 'url': bundle['url']}
    eligible = []
    unavailable = []
    for obj in bundle['objects']:
        if timestamp(obj['createdAt']) > bound:
            continue
        if 'publishedAt' in obj and (not obj['publishedAt'] or timestamp(obj['publishedAt']) > bound):
            continue
        selected = eligible_content(obj, cutoff)
        if selected is None:
            unavailable.append(obj.get('url', obj.get('id', 'unknown')))
        else:
            eligible.append(selected)
    if unavailable or not eligible:
        row.update(available=False,
                   unavailable_reason='as-of-cutoff content unavailable for: ' + ', '.join(unavailable or ['discussion body']))
        return row
    content = json.dumps({'discussion': {k:row[k] for k in ('number','kind','title','author_login','created_at','state','url')},
                          'objects': eligible}, sort_keys=True, indent=2) + '\n'
    row.update(available=True, source_id=f"unreferenced-{bundle['kind']}-{bundle['number']}@{cutoff}",
               revision_at=max((item['revision_at'] for item in eligible), key=timestamp),
               representation='discussion_snapshot_json', content=content,
               content_sha256=hashlib.sha256(content.encode()).hexdigest(),
               retrieved_at=bundle['retrieved_at'])
    return row
