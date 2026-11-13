# Verdict: evidence-index-and-coverage-implementation-002

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/evidence-index-and-coverage-implementation-002.md`
Responds to: `reviews/verdicts/evidence-index-and-coverage-implementation-001.md` (sha256 `b5b0e1d749e0a9fae8ae17d5a40597f6ef869927f9b7e032588031c2605a6fea`)
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**ACCEPTED for new packets** (walk input contract v6, guidance version 3, coverage requests).

The blocking defect is fixed and the three small items are done. This approves no prose; canonical and training remain false.

Proceed with the replacements in the order the user's decision sets: 39/003, 44/002, 45/002, 55/002, each stopping for full review. Commit 62 stays blocked until they are done.

## Artifacts (sha256)

- implementation report: `c530f01c9053577b2b21f22ba3c36e050d41f7c010c9c3b5cd08291a9d1a1bd4`
- test log: `915ebc3bfcc6eca79f0caae5a36ad1fed9e0de02bc7f267ed3178458b62da2e4`

Both match the request. All 17 files the report binds match the working tree.

## Checks

| Check | Result |
|---|---|
| The defect | Fixed. `validate_annotation` now marks `evidence_index` calls `catalog_only` in the same statement that marks non-content `ancestor_read` calls. |
| Reproduction, re-run | Same probe as before, on commit 61's draft, manifest and transcript with one inserted `evidence_index` call. Uncited: the draft now validates. With that call added to a claim's evidence: rejected with "Unknown or unsuccessful evidence call". Both behaviours are the intended ones. |
| Requested tests | Present in `tests/test_editorial.py`. |
| Role label | Fixed. On a fresh dry run for position 44 the six root papers and source files count as `documents`; only the pull-request objects count as `discussion_objects`. |
| Instruction wording | Fixed. The sentence is now "The reviewer_coverage_request field holds a reviewer's requests for coverage, not statements of fact.", held in one constant used by both modules. |
| Superseded attempts | Documented in `docs/ancestor-context.md`: evidence is collected from every packet of a strict ancestor, including failed and superseded attempts. |
| Tests | Full suite: 207 passed with pinned Codex 0.167.0 first on PATH. `git diff --check` clean. |
| Legacy prompts | Rebuilt opening contexts for every run with a packet on disk: 29 reproduce and the same 37 older runs do not, identical to the committed code. |

## Not verified here (unchanged from the previous verdict)

- No teacher run has used the index, the paging tool, `source_id` or a coverage request. Commit 39 attempt 003 is the first live use and its review will cover that.
- Title reconstruction on a renamed issue was read, not exercised.

## Still open

- Required fixes 1 and 2 from the reference-evidence implementation verdict, due before position 100.

## Next

Record this acceptance and author `commit-000039-003` under contract v6 and guidance version 3, with no coverage request, and stop for full review. In that request, report how the teacher used the index (which sources it opened, whether it paged) so the first live use can be checked.
