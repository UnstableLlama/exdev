# SPDX-License-Identifier: MIT
"""Select historical content without exposing post-cutoff metadata to an author."""
from datetime import datetime
import hashlib


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
