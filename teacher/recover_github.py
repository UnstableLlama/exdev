# SPDX-License-Identifier: MIT
"""Trusted curator: paginate public GitHub edit history, then export cutoff-filtered evidence."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from .evidence import eligible_content

ROOT = Path(__file__).resolve().parents[1]
BASE = 'id url createdAt updatedAt lastEditedAt body'
EDIT = 'id createdAt editedAt deletedAt diff'


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


def recover(owner, repo, number):
    query = f'''query($owner:String!,$repo:String!,$number:Int!){{repository(owner:$owner,name:$repo){{
      issueOrPullRequest(number:$number){{__typename ... on Issue{{{BASE}}} ... on PullRequest{{{BASE}}}}}
    }}}}'''
    obj = graphql(query, dict(owner=owner, repo=repo, number=number))['repository']['issueOrPullRequest']
    if obj is None:
        raise ValueError('Issue or PR not found')
    kind = obj['__typename']
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
            'scope': 'administrative_raw_history', 'url': obj['url'], 'objects': objects}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse', action='store_true', help='Reuse previously retrieved raw history')
    args = parser.parse_args()
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
