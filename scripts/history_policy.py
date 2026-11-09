# SPDX-License-Identifier: MIT
"""Ancestry-bounded entry context and explicit merge integration policy."""
import hashlib
import subprocess
from mine import git, text


def parents(repo, sha):
    return text(git(repo, 'show', '-s', '--format=%P', sha)).split()


def eligible_ancestors(repo, sha):
    ps = parents(repo, sha)
    return set(text(git(repo, 'rev-list', *ps)).split()) if ps else set()


def ancestor_context(repo, sha, entries):
    allowed = eligible_ancestors(repo, sha)
    return sorted(position for position, entry in entries.items() if entry['sha'] in allowed)


def validate_entry_links(repo, sha, links, entries):
    eligible = set(ancestor_context(repo, sha, entries))
    if not isinstance(links, list) or any(type(i) is not int or i not in eligible for i in links):
        raise ValueError('Every entry link must identify a strict ancestor of this commit')


def merge_policy(repo, sha):
    ps = parents(repo, sha)
    if len(ps) < 2:
        return {'version': 1, 'is_merge': False, 'parents': ps, 'entry_role': 'change',
                'analysis_policy': 'ordinary_change', 'independent_training_example': True}
    introduced = text(git(repo, 'rev-list', '--reverse', '--topo-order', *ps[1:], '--not', ps[0])).split()
    unchanged = git(repo, 'rev-parse', sha + '^{tree}') == git(repo, 'rev-parse', ps[0] + '^{tree}')
    remerge = b''
    error = None
    if len(ps) == 2:
        try:
            remerge = git(repo, 'show', '--format=', '--remerge-diff', '--no-ext-diff', '--no-textconv', '--no-color', sha, '--')
        except subprocess.CalledProcessError as exc:
            error = 'remerge_diff_unavailable_exit_' + str(exc.returncode)
    else:
        error = 'octopus_merge_requires_manual_review'
    review = bool(error or remerge.strip() or (unchanged and introduced))
    return {'version': 1, 'is_merge': True, 'parents': ps, 'entry_role': 'integration',
            'introduced_shas': introduced, 'first_parent_tree_unchanged': unchanged,
            'strategy': 'not_recoverable_from_commit_object',
            'remerge_diff_sha256': hashlib.sha256(remerge).hexdigest() if not error else None,
            'remerge_diff_nonempty': bool(remerge.strip()) if not error else None,
            'remerge_error': error,
            'analysis_policy': 'merge_resolution_review_required' if review else 'integration_summary_only',
            'independent_training_example': False,
            'event_origin': 'merge_arrival',
            'note': 'Preserve first-parent events. A nonempty remerge diff is review evidence, not proof of a historical strategy or an independent new fix.'}
