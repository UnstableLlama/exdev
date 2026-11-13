# Verdict: closed-discussion-salience-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/closed-discussion-salience-implementation-001.md`
Decision implemented: `reviews/verdicts/closed-discussion-salience.decision.md` (sha256 `e1fd1e90efd0153e2a2da00ae9ace8329a5adea54bea86df7db139a7bd65010f`)
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**NOT ACCEPTED as submitted. One required change, then resubmit as implementation 002.** Do not author commit 69 or 70 under contract 8 yet.

The machinery is right and I would accept it unchanged: the separate catalog, cutoff snapshots, fail-closed candidates, paging, contract binding, legacy boundary, tests. The gate is too loose. On real history it lists unrelated closed discussions at about two commits in three, and the audit shows the same thing at small scale. The fix is small and I have tested it: qualify a row on terms from the commit message only.

Canonical and training remain false.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk. Full suite: 219 passed with Codex 0.167.0 first on PATH (run by me).

## What is right

| Check | Result |
|---|---|
| Separate and bound | `closed_discussion_catalog` is its own manifest field. Its rows and served objects are hashed into `closed_discussions_sha256`, and the bundle file into `closed_bundle_sha256`. Validation runs only for contract 8 and later, so earlier packets are untouched. |
| Cutoff content | The validation packet's snapshot of issue 16 ends at the closing comment of 19:58:31 UTC, fourteen seconds before the cutoff, and contains the maintainer's diagnosis. `attach` rejects any row whose created, closed or revision time is after the cutoff. |
| Fail closed | A candidate needs an available snapshot in which every object is a full body; edit summaries disqualify it. At commit 69 all eleven discussions closed by then are eligible, so nothing is silently lost there. |
| Rows | Number, kind, title, author, times, state, URL, path hints, matched terms. No score, body or excerpt. |
| Task terms | Built from the task commit alone: message, changed paths, identifiers on changed code lines with string literals and comments stripped. |
| Kept out of the ancestor index | Closed snapshots are excluded from the general evidence index, so one commit's listing does not become a later commit's evidence. |
| Guidance | One sentence, sent only when the field is present. It says a listing is not an established relationship and keeps the inference-labelling rule. |
| Known case | At commit 69 only issue 16 is listed, on `tokenizer` and `truncation`. |

## Why the gate is too loose

**The rule.** A row qualifies when the sum of `1 / df²` over shared terms reaches 1. In practice that means: the discussion shares at least one term with the task that no other closed discussion contains. Any identifier will do. A discussion that contains a traceback has many such terms, and a commit that touches the same area of code matches one of them by accident.

**The audit shows it.** Of positions 2 to 68, 36 list at least one row, 66 rows in all. I read every row. I find none on point. Typical: commit 28 (custom split ratio) lists issue 6 (ROCm runtime) on `assert`; commit 64 (`--keep_b`) lists issue 12 on `type`; commit 56 lists issue 5 on `memory`; issue 8 is listed at twelve quantizer commits on path components such as `quant` and `exl3_lib`.

**It does not improve as the corpus grows.** I expected the squared penalty to tighten the gate later in the walk. It does not, because larger diffs carry more identifiers. I ran the submitted `terms`, `task_terms` and scoring over the whole upstream history: every issue and pull request (597) with its comments (1,476), each discussion's text limited to what existed at the commit's date. This approximates the cutoff snapshot (it ignores body edits), which is good enough to judge a gate. Forty random commits per band:

| Walk positions | Commits listing nothing | 1 to 2 rows | 3 to 4 rows | 5 or more rows |
|---|---|---|---|---|
| 100 to 400 | 11 | 19 | 7 | 3 |
| 400 to 1000 | 10 | 21 | 4 | 5 |
| 1000 to 1600 | 4 | 17 | 4 | 15 |
| 1600 to 2264 | 7 | 12 | 5 | 16 |

With the existing reading rule ("when the catalog has ten items or fewer, read every item that reports an error"), that is a steady stream of unrelated reads. The user's instruction on the evidence index was to offer everything without flooding the context; the same applies here.

## Required change

**Qualify a row only on terms that come from the task's commit message.** Keep your score and threshold exactly as they are, computed over message terms. Terms from paths and diff identifiers may still be shown in `matched_terms` for a row that has qualified, but must not qualify a row by themselves.

I tested this variant on the same data:

| Walk positions | Listing nothing | 1 row | 2 rows | 3 or more |
|---|---|---|---|---|
| 2 to 69 | 26 | 10 | 4 | 0 |
| 100 to 400 | 25 | 12 | 2 | 1 |
| 400 to 1000 | 25 | 13 | 2 | 0 |
| 1000 to 1600 | 22 | 13 | 2 | 3 |
| 1600 to 2264 | 28 | 7 | 2 | 3 |

It is stable across the walk and rarely lists more than two rows.

Recall, on the cases where an issue was closed within fifteen minutes before a commit (fourteen in the whole history; most are coincidences such as a version bump): the three where the commit plainly answers the issue are listed by both the submitted rule and the message-only rule. They are issue 16 at position 69 (`tokenizer`, `truncation`), issue 99 at 560 (`minimax`) and issue 233 at 1100 (`gather`, `offset`, `dst_offset`). In all three the deciding terms are in the commit message. A fourth plausible case, issue 436 at position 1947, is listed by neither: its shared terms (`cache`, `page`, `window`) are common ones.

The cost, stated plainly: a commit with an uninformative message ("Cleanup", "Fix typo") will list nothing. That is acceptable. Such a commit gives no lexical signal to gate on, and the open catalog and its path hints are unchanged.

If you find a better mechanical gate, propose it with the same two measurements (rows per commit by band; the three known cases). Not a time window.

Disclosure: I used later history to evaluate the gate. That is a judgement about trusted code, not teacher input. The gate itself still reads only the task and text older than the cutoff.

## Smaller points, fix in the same change

1. The comment above the second stop list says it is "independent of the audit", and the request says the stop list was fixed after the first score over-selected. Say in the code and in `docs/ancestor-context.md` what actually happened: a general stop list, extended after looking at the audit for positions 2 to 68.
2. The audit should report, per position, how many discussions were closed at the cutoff and how many were eligible, so a silent loss from the full-body requirement is visible. At position 69 it is eleven of eleven.
3. Add a test for the new rule: a discussion sharing a unique term only with a diff identifier is not listed; the same term in the commit message lists it.

## Audit outcome

No approved entry from commits 2 to 68 needs re-authoring on account of this decision. I judged that from the titles and matched terms of all 66 rows and from having read issues 2, 5, 6, 8, 11, 12 and pull requests 3 and 13 during the original reviews. Commit 69 remains the one case.

## Next

1. Make the required change and the three smaller ones; rerun the audit; send `closed-discussion-salience-implementation-002` with the new audit and the rows-per-commit distribution.
2. After acceptance: author commit 69 unassisted under the new contract, stop for review, then resume at commit 70.
