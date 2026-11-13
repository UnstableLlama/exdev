# Verdict: evidence-index-and-coverage-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/evidence-index-and-coverage-implementation-001.md`
Decisions implemented: `evidence-index-and-config-reading.decision.md` (sha256 `3ee7c2ca36719b021e5d90124751bfa6ffd86bb434213fce81c357805ff57b6b`) and `thin-entries-and-retroactive.decision.md` (sha256 `805d83465f08e7e9d1ec59670962f934aadb768b41b264ece36c65cea15e09f9`)
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**CHANGES REQUIRED. Not accepted yet.** One defect would fail any run that uses the new index tool. It is a small fix. Everything else meets the decisions.

Do not author 39/003 or anything else until a corrected implementation is reviewed. This approves no prose; canonical and training remain false.

## Files reviewed (sha256)

All match the implementation report (`783624ed09b5d84502a4c5a96c631446bfff793642e8f676fc62d8f44f9f7e21`).

- teacher/evidence_index.py: `dd328fd2fb2fc4e815c23be529d7437709cb75a4427edf2660a99fabfe486282`
- teacher/coverage_request.py: `c7be808e6b9ca0ef56c808258efc3131f7da2ecf1f67cb4a3ddf6039b1ebf90b`
- teacher/walk_inputs.py: `b682ba756ab6d8065f48a8b1f89674de39e5c9423ff09db10cfa1f0108dad7c3`
- teacher/session.py: `c1135a8b9149be29ab98ac393f86885acc221698c8df2a479a4a91282c577775`
- teacher/worker.py: `196feb61a3f336c021d115ed0c56180032f9a5b1ddd2d00411f3ed140c90cb2a`
- teacher/author.py: `fbbc6a738ff25f91f5cd27b56b0bd10e0f1ae666534054a25874b17ce9dc008c`
- teacher/editorial.py: `504794a47fa059bec183aa60e577dafb0a8cb15a8cb59349f6d44c71e167b15f`
- teacher/walk.py: `c42ee2b25450ee1e419796660fc34eb1689af50c58010b390c1120b894382dc5`
- schema/repo-tools-v1.json: `2738981a27fadee85ecbfe208d97605b58628e0b61e6dc232df096e90a60b990`

The two coverage request files hash as the request states.

## The blocking defect

**Any call to the `evidence_index` tool makes the draft fail validation.**

In `teacher/editorial.py`, `validate_annotation` walks every tool call in the transcript and raises "Evidence index navigation is not claim evidence" as soon as it sees one made with `evidence_index`, whether or not any claim cites it. The neighbouring line shows what was meant: non-content `ancestor_read` calls are marked `catalog_only`, which makes them uncitable without failing the run.

I reproduced it. Commit 61's existing draft, manifest and transcript validate. With one uncited `evidence_index` call and result inserted into the transcript, the same draft raises that error.

Why it matters now: the opening index lists each model as one row with counts. To learn the file names of a model's tensor headers, the teacher has to call `evidence_index` with that row's `index_id`. A teacher that does exactly what the new design invites would spend a whole run and then fail validation, and a validation failure stops the walk. Commit 39 attempt 003 is the first run that would hit it.

Required:
1. Mark `evidence_index` calls `catalog_only` in the same way, so they are allowed in a transcript and rejected only when a claim cites them.
2. Add two tests: a transcript that pages the index and cites other evidence validates; a claim citing an index call is rejected.

## Evidence index, point by point

| Point | Result |
|---|---|
| 1. What is offered | Met. `build` takes every non-unreferenced evidence object from the task's packet and from each packet whose task is a strict ancestor, rechecks `created_at` and `revision_at` against the task's cutoff and drops anything later, and verifies each blob's hash before copying it. |
| 2. Index, not content | Met. The opening context carries one row per source with counts and the attaching commits; no bodies. Model files attached to the task itself are also moved out of the direct catalog into the index. |
| 3. Fetched on demand | Met in code: the fetch tools search index objects as well as direct ones, with an optional `source_id` to pick an exact object. Blocked in practice by the defect above for anything that needs the object list. |
| 4. Bounded | Met. 8 KiB opening page with `truncated` and `next_offset`; the tool pages the rest. |
| 5. Task evidence compact | Met. |
| 6. Ancestors only | Met and tested. |
| 7. Navigation, not instruction | Met. Rows say what exists and who attached it. |
| 8. Bound into the contract | Met. The index digest is in the contract; validation rechecks the digest, each object's dates and ancestry, and each blob's hash. |
| 9. Tests | Met except for the two missing cases above. |
| 10. Documented | Met. |

## Dry runs on real packets (written to my scratch directory, nothing in the repository touched)

I ran `prepare` for three positions and looked at what a teacher would be offered.

| Position | Sources | Objects | Opening page | What I checked |
|---|---|---|---|---|
| 44 (the DeciLM fix) | 18 | 279 | 6,182 bytes, not truncated | Lists the four Nemotron models, attached by commit 39, and pull request 13, attached by the merge. This is exactly the evidence that was missing at 44, 45 and 55. |
| 39 | 17 | 276 | 5,814 bytes | The four Nemotron models appear as four rows, in place of 205 catalog rows. |
| 42 (the branch commit) | 13 | 71 | 4,320 bytes | No Nemotron models and no pull request 13: neither was attached by an ancestor of that commit. Correct. |

## Configuration-reading rule

Met. The sentence is the decision's wording verbatim, added only for guidance version 3, which only new contract v6 packets set.

## Coverage requests

| Point | Result |
|---|---|
| Separate, labelled, verbatim | Met. The text goes into its own opening field `reviewer_coverage_request`, unchanged. |
| Fixed instruction | Met, with a wording note below. |
| Contract binding | Met. Path and hash are in the contract; `validate` rejects a changed or vanished request. |
| Right run only | Met. `prepare` checks the file name against the position; `author` checks it against the attempt directory. |
| Provenance and review flags | Met: `coverage_request` and `reviewer_assisted` in provenance, `reviewer_assisted` in the review record. |
| Guard on content | A size limit, and any 40-hex commit id in the text must be the task or an ancestor. The semantic check (no conclusions, no hindsight) is left to the author reading the file, and the report says so honestly. That is the right division; code cannot do it. |
| Verdicts stay out | Only a file named `commit-NNNNNN-AAA.coverage.md` can be attached. |

## Other checks

| Check | Result |
|---|---|
| Tests | Full suite: 204 passed with pinned Codex 0.167.0 first on PATH. `git diff --check` clean. |
| Legacy prompts | Rebuilt the opening context for every run with a packet on disk, with the committed code at `fd1dd86` and with this working tree: identical results (29 reproduce, the same 37 older runs do not). No legacy prompt changes. |
| Legacy tools | A contract v5 packet is offered no `evidence_index` tool and no `source_id` parameter. |
| Legacy assessment | `approval_policy.assess` still passes for 39/002, 43/001, 55/001 and 61/001. |
| Walk guard | `resume` now refuses while an advancement pause is recorded. |
| Policy text | `docs/ancestor-approval-policy.md` replaces "no task-specific reviewer steering" with the bounded coverage mechanism, accurately. |

## Smaller items (fix in the same change; not separately blocking)

1. **Role label.** Papers and source files attached at the root (arXiv pages, the QTIP repository files) are counted as `discussion_objects`. Call them documents.
2. **Instruction wording.** The system text gains the bare sentence "These are a reviewer's requests for coverage, not statements of fact." with nothing saying what "these" are. Name the field: "The reviewer_coverage_request field holds a reviewer's requests for coverage, not statements of fact."
3. **Superseded attempts.** The index collects evidence from every packet of an ancestor commit, including superseded and failed attempts. For evidence objects that is harmless and arguably right, but say so in the documentation.
4. Still due before position 100, as the report states: required fixes 1 and 2 from the earlier implementation verdict.

## Not verified here

- No teacher run has used any of this. The first real session (39/003) should be reviewed as the first live use of the index, the paging tool and `source_id`.
- I did not exercise the fetch tools against an indexed object in a real sandbox; the tests do so with fixtures.
- Title reconstruction from cached histories was read, not exercised on a renamed issue.

## Next

Fix the validation defect with its two tests and the small items, and send a short follow-up request. On acceptance, proceed with 39/003, 44/002, 45/002, 55/002 in order.
