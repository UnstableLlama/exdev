# SPDX-License-Identifier: MIT
"""Trusted curator: paginate public GitHub edit history, then export cutoff-filtered evidence."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
from .evidence import eligible_content, discussion_snapshot, timestamp

ROOT = Path(__file__).resolve().parents[1]
BASE = 'id url createdAt updatedAt lastEditedAt body author { login }'
EDIT = 'id createdAt editedAt deletedAt diff'
PATH_HINT_LIMIT = 20
PATH_CANDIDATE = re.compile(
    r'(?:[A-Za-z]:)?(?:[/\\]|\.{0,2}[/\\])?[A-Za-z0-9_.~+@%=-]+'
    r'(?:[/\\][A-Za-z0-9_.~+@%=-]+)+'
    r'(?:\.[A-Za-z0-9_+-]+)'
)


def parent_tree_paths(repo, task_sha):
    parents = subprocess.run(
        ['git', '--git-dir', str(repo), 'show', '-s', '--format=%P', task_sha],
        text=True, capture_output=True, check=True,
    ).stdout.split()
    if not parents:
        return []
    output = subprocess.run(
        ['git', '--git-dir', str(repo), 'ls-tree', '-r', '--name-only', parents[0]],
        text=True, capture_output=True, check=True,
    ).stdout
    return sorted(filter(None, output.splitlines()))


def discussion_text(item):
    if not item.get('available'):
        return ''
    payload = json.loads(item['content'])
    return '\n'.join(obj['content'] for obj in payload.get('objects', [])
                     if isinstance(obj.get('content'), str))


def repo_path_hints(item, paths, limit=PATH_HINT_LIMIT):
    """Extract cutoff-bound path navigation hints that exist in the parent tree."""
    if not item.get('available'):
        return None
    text = discussion_text(item).replace('\\\\', '/').replace('\\', '/')
    known = set(paths); found = set()
    for path in paths:
        if re.search(r'(?<![A-Za-z0-9_.+-])' + re.escape(path) + r'(?![A-Za-z0-9_.+/-])', text):
            found.add(path)
    for match in PATH_CANDIDATE.finditer(text):
        candidate = match.group().replace('\\', '/').lstrip('./')
        if 'site-packages/' in candidate:
            candidate = candidate.split('site-packages/', 1)[1]
        suffixes = [path for path in known if candidate == path or candidate.endswith('/' + path)]
        found.update(suffixes)
    ordered = sorted(found)
    return {'repo_paths_mentioned': ordered[:limit],
            'repo_paths_mentioned_truncated': len(ordered) > limit}


def graphql(query, variables):
    result = subprocess.run(['gh', 'api', 'graphql', '--input', '-'],
                            input=json.dumps({'query': query, 'variables': variables}),
                            text=True, capture_output=True, check=True)
    data = json.loads(result.stdout)
    if data.get('errors'):
        raise ValueError('GitHub GraphQL returned errors: ' + str(data['errors']))
    return data['data']


def connection(node_id, typename, field, fields):
    cursor = None
    result = []
    while True:
        query = f'''query($id:ID!,$cursor:String){{node(id:$id){{... on {typename}{{
          {field}(first:100,after:$cursor){{nodes{{{fields}}}pageInfo{{hasNextPage endCursor}}}}
        }}}}}}'''
        data = graphql(query, {'id': node_id, 'cursor': cursor})['node'][field]
        result.extend(data['nodes'])
        if not data['pageInfo']['hasNextPage']:
            return result
        next_cursor = data['pageInfo']['endCursor']
        if not next_cursor or next_cursor == cursor:
            raise ValueError('Pagination did not advance')
        cursor = next_cursor


def timeline(node_id, typename):
    cursor=None;result=[]
    while True:
        query=f'''query($id:ID!,$cursor:String){{node(id:$id){{... on {typename}{{
          timelineItems(first:100,after:$cursor,itemTypes:[RENAMED_TITLE_EVENT,CLOSED_EVENT,REOPENED_EVENT]){{
            nodes{{__typename ... on RenamedTitleEvent{{createdAt previousTitle currentTitle}}
              ... on ClosedEvent{{createdAt}} ... on ReopenedEvent{{createdAt}}}}
            pageInfo{{hasNextPage endCursor}}}}
        }}}}}}'''
        page=graphql(query,{'id':node_id,'cursor':cursor})['node']['timelineItems']
        result.extend(page['nodes'])
        if not page['pageInfo']['hasNextPage']:return result
        next_cursor=page['pageInfo']['endCursor']
        if not next_cursor or next_cursor==cursor:raise ValueError('Timeline pagination did not advance')
        cursor=next_cursor


def recover(owner, repo, number):
    query = f'''query($owner:String!,$repo:String!,$number:Int!){{repository(owner:$owner,name:$repo){{
      issueOrPullRequest(number:$number){{__typename
        ... on Issue{{{BASE} number title state closedAt}}
        ... on PullRequest{{{BASE} number title state closedAt}}}}
    }}}}'''
    obj = graphql(query, dict(owner=owner, repo=repo, number=number))['repository']['issueOrPullRequest']
    if obj is None:
        raise ValueError('Issue or PR not found')
    kind = obj['__typename']
    events=timeline(obj['id'],kind)
    obj['edits'] = connection(obj['id'], kind, 'userContentEdits', EDIT)
    objects = [obj]
    for comment in connection(obj['id'], kind, 'comments', BASE):
        comment['edits'] = connection(comment['id'], 'IssueComment', 'userContentEdits', EDIT)
        objects.append(comment)
    if kind == 'PullRequest':
        for review in connection(obj['id'], kind, 'reviews', BASE + ' publishedAt'):
            review['edits'] = connection(review['id'], 'PullRequestReview', 'userContentEdits', EDIT)
            objects.append(review)
            for comment in connection(review['id'], 'PullRequestReview', 'comments', BASE + ' publishedAt'):
                comment['edits'] = connection(comment['id'], 'PullRequestReviewComment', 'userContentEdits', EDIT)
                objects.append(comment)
    return {'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'scope': 'administrative_raw_history', 'kind':'issue' if kind=='Issue' else 'pull_request',
            'number':obj['number'],'title':obj['title'],'state':obj['state'],'createdAt':obj['createdAt'],
            'closedAt':obj['closedAt'],'author':obj.get('author'),'url':obj['url'],
            'timeline_complete':True,
            'title_events':[e for e in events if e['__typename']=='RenamedTitleEvent'],
            'state_events':[{'kind':'closed' if e['__typename']=='ClosedEvent' else 'reopened','createdAt':e['createdAt']}
                            for e in events if e['__typename'] in ('ClosedEvent','ReopenedEvent')],
            'objects': objects}


def repository_discussions(owner, repo, cutoff):
    result=[]
    for field,kind in (('issues','issue'),('pullRequests','pull_request')):
        cursor=None
        while True:
            query=f'''query($owner:String!,$repo:String!,$cursor:String){{repository(owner:$owner,name:$repo){{
              {field}(first:100,after:$cursor,orderBy:{{field:CREATED_AT,direction:ASC}}){{
                nodes{{number createdAt}} pageInfo{{hasNextPage endCursor}}}}
            }}}}'''
            page=graphql(query,{'owner':owner,'repo':repo,'cursor':cursor})['repository'][field]
            stop=False
            for node in page['nodes']:
                if timestamp(node['createdAt'])>timestamp(cutoff):stop=True;break
                result.append((kind,node['number']))
            if stop or not page['pageInfo']['hasNextPage']:break
            next_cursor=page['pageInfo']['endCursor']
            if not next_cursor or next_cursor==cursor:raise ValueError('Discussion pagination did not advance')
            cursor=next_cursor
    return result


def bounded_discussions(items, limit=100):
    ordered=sorted(items,key=lambda r:(timestamp(r['created_at']),r['kind'],r['number']))
    return ordered[-limit:],len(ordered)>limit


def retrospective_path(through_position):
    return ROOT/'reports'/f'unreferenced-discussion-retrospective-002-{through_position-1:03d}.json'


def recover_unreferenced_catalogs(through_position, reuse=False, only_positions=None):
    directory=ROOT/'data/evidence/github';directory.mkdir(parents=True,exist_ok=True)
    records=[]
    for position in range(2,through_position+1):
        path=next((ROOT/'data/exllamav3-v5/records').glob(f'{position:06d}_*.json'))
        records.append((position,json.loads(path.read_text())))
    latest=records[-1][1]['commit_date']
    histories=[]
    for kind,number in repository_discussions('turboderp-org','exllamav3',latest):
        path=directory/f'discussion-{kind}-{number}-history.json'
        bundle=json.loads(path.read_text()) if reuse and path.exists() else recover('turboderp-org','exllamav3',number)
        if bundle['kind']!=kind:raise ValueError('Recovered discussion kind mismatch')
        path.write_text(json.dumps(bundle,indent=2)+'\n');histories.append(bundle)
    report=[]
    selected_positions=set(only_positions or [])
    for position,record in records:
        if selected_positions and position not in selected_positions:
            continue
        tree_paths=parent_tree_paths(ROOT/'.sources/exllamav3.git',record['sha'])
        items=[]
        for bundle in histories:
            row=discussion_snapshot(bundle,record['commit_date'])
            if row is not None:
                hints=repo_path_hints(row,tree_paths)
                if hints is not None:row.update(hints)
                items.append(row)
        referenced=set()
        referenced_path=directory/f'{position:06d}-eligible.json'
        if referenced_path.exists():
            for evidence in json.loads(referenced_path.read_text()).get('items',[]):
                match=re.match(r'(https://github\.com/[^/]+/[^/]+/(?:issues|pull)/\d+)',evidence.get('url',''))
                if match:referenced.add(match.group(1))
        items=[item for item in items if item['url'] not in referenced]
        selected,truncated=bounded_discussions(items)
        result={'task_sha':record['sha'],'cutoff':record['commit_date'],'complete':True,
                'limit':100,'truncated':truncated,'items':selected}
        (directory/f'{position:06d}-unreferenced.json').write_text(json.dumps(result,indent=2)+'\n')
        report.append({'position':position,'sha':record['sha'],'cutoff':record['commit_date'],
                       'truncated':result['truncated'],
                       'items':[{k:v for k,v in item.items() if k not in ('content','retrieved_at','revision_at','representation','source_id')}
                                for item in result['items']]})
    if not selected_positions:
        retrospective_path(through_position).write_text(
            json.dumps({'scope':'report_only_no_reauthoring','positions':report[:-1]},indent=2)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse', action='store_true', help='Reuse previously retrieved raw history')
    parser.add_argument('--catalog-through-position',type=int)
    parser.add_argument('--catalog-position',type=int,action='append',default=[])
    args = parser.parse_args()
    if args.catalog_through_position or args.catalog_position:
        through=args.catalog_through_position or max(args.catalog_position)
        if args.catalog_position and any(p>through for p in args.catalog_position):
            raise ValueError('Catalog position exceeds recovery range')
        report=recover_unreferenced_catalogs(through,args.reuse,args.catalog_position)
        print(json.dumps([{'position':r['position'],'items':len(r['items']),'truncated':r['truncated']} for r in report],indent=2))
        return
    directory = ROOT / 'data/evidence/github'
    directory.mkdir(parents=True, exist_ok=True)
    bundles = []
    for number in (2, 3):
        path = directory / f'{number}-history.json'
        bundle = json.loads(path.read_text()) if args.reuse and path.exists() else recover('turboderp-org', 'exllamav3', number)
        path.write_text(json.dumps(bundle, indent=2) + '\n')
        bundles.append(bundle)
    report = []
    for position in (9, 10):
        path = next((ROOT/'data/exllamav3-v5/records').glob(f'{position:06d}_*.json'))
        record = json.loads(path.read_text())
        eligible = []
        for bundle in bundles:
            for obj in bundle['objects']:
                content = eligible_content(obj, record['commit_date'])
                if content is not None:
                    content['retrieved_at'] = bundle['retrieved_at']
                    eligible.append(content)
        result = {'task_sha': record['sha'], 'cutoff': record['commit_date'], 'items': eligible}
        (directory / f'{position:06d}-eligible.json').write_text(json.dumps(result, indent=2) + '\n')
        report.append({'position': position, 'sha': record['sha'], 'cutoff': record['commit_date'],
                       'eligible': [{k:v for k,v in item.items() if k!='content'} for item in eligible]})
    (ROOT/'reports/github-evidence-recovery.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps([{'position': r['position'], 'eligible_objects': len(r['eligible'])} for r in report], indent=2))


if __name__ == '__main__':
    main()
