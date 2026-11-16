# Verdict: closed-path-overlap-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/closed-path-overlap-implementation-001.md`
Patch: `reports/closed-path-overlap-implementation-001.patch`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED**, the implementation and its use. `salience-v3-paths` may be selected for packets from commit 152 on,
under the three conditions below. Packets and runs up to 151 stay as they are; nothing is rebuilt. Canonical and
training remain false.

The rule does what the gap at 150 called for and no more: a closed discussion also qualifies when its
cutoff-bound title or text names a file the task changes. It adds rows and removes none, it reads nothing that the
old rule did not already read, and it is off unless asked for. The paging repair is correct and, as far as the
record shows, no past run ever met the fault.

The request says the user asked for this. I have no way to confirm that from here; I am accepting on the merits and
have told the user what I accepted.

## Artifacts reviewed (sha256)

All twenty-one hashes in the request match the files on disk.

## Checks

| Check | Result |
|---|---|
| The patch | `closed_discussions.py`: new `task_paths` (first-parent `diff-tree` with `--no-renames`), new `path_mentions`, an optional `changed_paths` argument to `select`, a second accepted rule name and `matched_paths` validation in `attach`. `session.py`: the instruction text is chosen by the catalog's rule. `worker.py`: the closed-catalog branch of `evidence_index` no longer imports. One test file, one documentation section. |
| Off by default | Without `changed_paths`, `select` returns the `salience-v2` rule name and the old fields. I recomputed v2 for positions 2 to 151 with the patched code: the selected rows equal the bound bundle's rows at every position that has one. |
| Cutoff | `path_mentions` reads the same row the lexical rule reads, the snapshot built at the cutoff, with its historical title. The new tests cover a later title change and a later comment; both fail to qualify. |
| Matching | A full path uses the existing hint resolver. A bare file name counts only when exactly one path in the parent tree plus the task's paths has that name, and only when it is not part of a longer path or name. The tests cover an ambiguous name, a different directory, a longer name and a suffix. |
| Ranking | A path-qualified row is ranked at least at the threshold, 1; a higher lexical score still wins; ties fall to kind and number as before; the cap of 20 and the truncation flag are unchanged. |
| Binding | The bundle carries the task's changed paths, `attach` refuses a bundle whose list differs from the manifest's, each row's `matched_paths` must be a sorted subset of it, and a row with neither terms nor paths is refused. |
| Tests | I ran the full suite with the sandbox tests on: 253 pass. |
| Audit, recomputed | I ran both rules over positions 2 to 151 myself without writing anything. 96 rows added, none removed, the added rows equal the audit report's at every position, and the largest qualified count at any position is 7. |
| Position 150 | The proposed bundle keeps pull request 25 and issue 16 and adds pull request 35 through `humaneval.py` in its title. The 20:41:37Z comment is in it; nothing after the cutoff is. |
| Paging repair | The old branch imported a module that the sandbox does not mount. The new branch serialises the rows exactly as the host's `page` does, and the new test compares the two through the real runner. I searched every transcript: no run ever called `evidence_index` for the closed catalog, and none of the 87 packets with a catalog had more rows than fit in the first page. So the fault was latent and no past entry was affected. |
| Legacy runs | The 151 replay I ran for its verdict was against this working tree and matched 8 of 8. |

## What the new rows are (so nobody is surprised)

Of the 96 added rows, most are closed issues whose pasted traceback passes through a file the task touches:
`convert_model.py` 31 times, `linear.py` 26, `chat.py` 14. The same few issues (6, 8, 11, 16) come back at
every commit that changes those files. They are true path matches and mostly not about the change. The row that
motivated this, pull request 35 at 150, is the minority kind. That is acceptable for a navigation list of at most
20 that says of itself that it asserts no relationship, and it is why I set the conditions below.

## Conditions

1. **Report it.** Each request for a commit authored under the new rule states how many catalog rows qualified by
   path alone and whether the cap truncated.
2. **Stop at the first truncation.** Ties among path-only rows are ordered by kind and then by rising number, so
   when more than 20 qualify, the newest discussions and all pull requests after the issues are the ones cut. With
   576 discussions by the tip that will happen. At the first position where a path-qualified row is cut, stop and
   propose an ordering before authoring that commit.
3. **No rewriting.** Bound bundles, packets and runs up to 151 are not regenerated, and the canonical-use condition
   on 150 stays as recorded.

## Known limits (accepted)

- A bare file name followed by a full stop ("see humaneval.py.") does not match, because the same guard that
  rejects `humaneval.py.bak` rejects it. Worth a small refinement some time; not required now.
- A pull request that changes a file without naming it in its text is still missed. Using GitHub's file list
  would need its state at the cutoff, which is not established. Correctly left out.

## Next

1. Record this acceptance.
2. Select the new rule for 152 and later, report as in condition 1, and continue the walk.
