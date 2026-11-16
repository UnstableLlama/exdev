# Implementation request: cutoff-text path overlap for closed catalogs

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested by the user after the Catalog gap section of commit-000150-001.
I agree that path overlap should independently qualify a closed discussion.
This is a nonblocking, opt-in implementation request; ancestor retrieval only,
canonical and training remain false. Commit 151 was authored and fully replayed
under the accepted salience-v2 implementation before these changes; its separate
request is filed. No teacher has used the proposed rule and 152 has not started.

## Rule and scope

`salience-v3-paths` retains the v2 lexical rule and independently qualifies a row
when cutoff-visible title/body/comment text names a task-changed path. A bare
filename resolves only if unique across the parent tree plus task paths. Full
paths use the existing path-hint resolver (including filesystem-prefix/suffix
normalization); directory-qualified references to another file do not count as
a bare filename. The changed paths come from the exact first-parent diff with
rename detection disabled, so both rename sides are included. No future tree,
reviewer note, later comment, or current GitHub PR file list enters the match.

This implements the named-path route, not GitHub PR changed-file metadata. A
current PR file list does not by itself prove its historical cutoff state; PRs
with no named path may still be missed. A same-file discussion may also be
irrelevant, so matching remains navigation rather than an asserted relationship.

Path matches receive a ranking floor of 1, the existing lexical threshold.
Higher lexical scores retain priority, followed by the old kind/number tie break;
cap 20 and truncation remain visible. Rows expose sorted matched_paths alongside
matched_terms, which may now be empty for a path-only match. The changed-path
inventory must equal the task's manifest inventory. Rule identity and paths are
bound into the packet, and a versioned instruction explains the navigation hints.
State reconstruction, full-body requirements, cutoff checks, reopened discussions
and explicit-reference exclusions are unchanged.

Activation is explicit: pass changed_paths=task_paths(repo, sha) to select.
Omitting the argument retains v2, including legacy catalog fields and exact
standing instructions. Existing recovery call sites remain v2 until adoption is
reviewed. No bound bundle, packet or run was rebuilt or reauthored; 150 remains
approved as filed, with its canonical catalog condition tracked.

## Evidence and tests

The audit freezes the recovered histories and compares both rules at positions
2–151 without writing historical bundles. It adds 96 rows at 57 positions, removes
none, and reaches the cap at no position. At 150 it retains the two existing rows
and adds PR35 via its historical title's unique humaneval.py filename, resolving
to eval/humaneval.py. The 20:41:37 comment is present; the 21:08:59 maintainer
explanation is after the cutoff and absent. No PR35-specific exception exists.
Cutoff timestamps and explicit exclusions are checked for every selected object.

All 253 host-enabled tests pass without skips. Six new tests cover path-only
qualification, ambiguous/foreign names, future titles/comments, unknown or reopened
state, unavailable bodies, cap/order/exclusions, first-parent rename paths,
attachment validation/binding and real sandbox pagination. Boundary audit: 42
checks pass. An administrative clone of packet 150 pages the proposed catalog
through the isolated Runner and fetches PR35. The clone was deleted; it was not
a teacher packet or a replacement run.

That sandbox check found a related existing pagination defect: evidence_index's
closed_discussions branch attempted a relative import from a script executed with
no package context, and the target module is not mounted. The worker now serializes
the closed rows through its existing excerpt helper directly, matching the host
page function without widening the sandbox mounts. Closed-catalog pagination now
works rather than returning the import error; other dispatch behavior is unchanged.
The full suite and boundary/replay checks were repeated after this repair.

Legacy sessions 148, 150 and 151 retain byte-identical initial messages and replay
all 34 calls identically; rendering and coverage recompute identically. 1509 existing
run files/manifests were hash-checked unchanged across that replay. The three changed
runtime modules' pre-change snapshots are attached and match 151's original
provenance hashes. Thus reviewers should use those snapshots for 151 provenance;
the working-tree modules now contain this pending implementation. git diff --check
passes. Linux aarch64, Python 3.14.4. No new-rule teacher inference occurred.

Please review the qualifier, unique-filename resolution, ranking floor and
pagination repair for future adoption. The walk remains at the separate 151 full
review gate. This request does not authorize rewriting old packets or injecting
the reviewer commentary into a teacher.

## SHA256

- teacher/closed_discussions.py: `a9bc332c1d4e16fab3ec997497407c8c78cd2c41fc9da6dfb4d490f74f6242a3`
- teacher/session.py: `b7cfc63fef1f671e958cdeb1db82f6ca73f81ec89e313dabf998c37d1956cf67`
- teacher/worker.py: `d419d1043b9449556045b25bbd0c30ee46332aa58b072290c15ff0d1c1d41c62`
- tests/test_closed_path_overlap.py: `1843b741e17315441db06e17d20d85b51a0de5f0a0648ea6bf3f787a80eba96c`
- docs/ancestor-context.md: `20ad297b3d41ba361cc8e5426590fefcf1671a9a07e1c042e6157d7f3a87eaf4`
- reviews/verdicts/commit-000150-001.md: `79368fab71da8d5724b9b1c7679c12e1c74632eb59e14290d34aacce6a9336c2`
- reports/closed-path-overlap-implementation-001.json: `4317ab98334bcb73e303c478851c9e643852d4f68439c948b28f62acafd92159`
- reports/closed-path-overlap-implementation-001.patch: `eb1ee1e0c128df89db08fe352ba5413db4e6f492a8eefea670d2c375629570c9`
- reports/closed-path-overlap-tests-001.txt: `5e2aad4984263ef1a5230726e9e14ef7108c94b20366dee0c95f6782e22c6cff`
- reports/closed-path-overlap-inputs-001.json: `a83330cd2f540d2587f7af8cd5f656b5cb5b08753ce7c885b737356926d2b33f`
- reports/closed-path-overlap-audit-001.py: `76910c895a3ebc00e440c5235e44f21fde7f574d27ea72ac594b6f2b0f9bbd97`
- reports/closed-path-overlap-audit-001.json: `430a6c8bab61a01d84443311a53857d40cc78de300472de40103c5b3d30b8109`
- reports/closed-path-overlap-150-proposed-bundle-001.json: `18dd64b471654aeb227c53ec4e50095b264086a12452c53014410c49c702356a`
- reports/closed-path-overlap-replay-001.py: `5da83fedeb49bb9bc6dbc0a74fff2a73867f33d3caa770b9b8381171ebe61db1`
- reports/closed-path-overlap-replay-001.json: `bab15a4f7e78a1884de29ce206822923fb7284763daeefb7a8384407d0316554`
- reports/closed-path-overlap-boundary-001.json: `455898d200e8de63f72f48ea206c15e69ee754844636f81a2f3c47572aa828e6`
- reports/closed-path-overlap-live-001.py: `f39673a107e347f3ad317a59120a5ce2458b9cded4e202a98ab6b5aa6b987373`
- reports/closed-path-overlap-live-001.json: `c03bf0b967376a99dd0f0e42a5e8703a0f89ed65c1c9cfd9e44baec16b520b45`
- reports/closed-path-overlap-original-closed_discussions.py: `bdd88ca4a4d2112f893a58235429101f808c046986d1e1497e3c6c999ea8857f`
- reports/closed-path-overlap-original-session.py: `6037ee158ab5c2d55775e03727a121bf9a4393d52c5bea5ab953dae6597f4167`
- reports/closed-path-overlap-original-worker.py: `ceb99e96d5fb46e077ebbf59e219fb620d4e53d0a35946c41fa99da6f2dd60b2`

Reply in `reviews/verdicts/closed-path-overlap-implementation-001.md`.
