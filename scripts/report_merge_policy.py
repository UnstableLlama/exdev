# SPDX-License-Identifier: MIT
"""Administrative merge-policy inventory; never expose this future-wide report to a teacher."""
from collections import Counter
import json
from pathlib import Path
from history_policy import merge_policy
from mine import git, text

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / '.sources/exllamav3.git'


def main():
    manifest = json.loads((ROOT/'data/exllamav3-v5/manifest.json').read_text())
    commits = text(git(REPO, 'rev-list', '--reverse', '--topo-order', manifest['head'])).split()
    policies = []
    merge_shas = set(text(git(REPO, 'rev-list', '--min-parents=2', manifest['head'])).split())
    positions = {sha: index + 1 for index, sha in enumerate(commits)}
    for sha in commits:
        if sha not in merge_shas:
            continue
        policy = merge_policy(REPO, sha)
        policy.update(sha=sha, position=positions[sha],
                      introduced_positions=[positions[s] for s in policy['introduced_shas']])
        policies.append(policy)
    report = {'head': manifest['head'], 'scope': 'administrative_only', 'merges': len(policies),
              'counts': dict(Counter(p['analysis_policy'] for p in policies)), 'policies': policies}
    (ROOT/'reports/merge-policy.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='policies'}, indent=2))


if __name__=='__main__':
    main()
