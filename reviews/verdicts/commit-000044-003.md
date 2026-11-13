# Verdict: commit-000044-003

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000044-003`
Packet: `.teacher/retrieval/000044-003`
Upstream: `3a7b4895e45b1eb2f291f8b09b0a5dac569e984c` "Fix DeciLM n_heads_in_group attn config"
Request: `reviews/requests/commit-000044-003.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only, as a reviewer-assisted entry.** It supersedes attempt 001 for future retrieval. Attempt 002 stays rejected. Commit 44 is closed.

Canonical and training remain false.

The entry now says where the faulty line came from, links that ancestor, and shows from tensor headers that the new expression matches the stored widths where the old one did not, model by model.

## Artifacts reviewed (sha256)

- draft.json: `8614b86c65166a84331a1cae12d2f881c61828aa837fd47638cd0c48ce7434a8`
- draft.md: `2ef8358d43ffd91e346687f77e933573e322e7839db46de2a55887e3c55f4a3f`
- raw-transcript.json: `3eb9c065d6152eb8b2a0463313e9133e70367f734009c4ded0ed7b1d37717b57`
- provenance.json: `80f9979d5a28b07acdf4edfabbd3e888ed94f3f3fb2385a733f7c51ae6e2dfe5`
- coverage.json: `0cc82cd16c028e82836bfcc65acad0c45199b39e94a165f66d7dacf0fb555455`
- packet manifest (on disk): `ec2a480d2639779ff104f6feea04aa8f2b110f152723597ed9f6532bb77732bf`
- coverage request: `94cb9f66058550ed29e1535d1ea3832862e16c2618c9053cbefbeabcb8ba24bf`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 30 of 30 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 37 of 37 implementation hashes match; exactly 43 strict-ancestor entries; all 781 blobs hash to their names; no evidence timestamp after the cutoff. |
| Assistance is recorded | Provenance and the review record carry `reviewer_assisted`; provenance carries the coverage request's path and hash. |
| Only the coverage request was added | Against attempt 002: the opening context gains one field, equal to the coverage file byte for byte, and nothing else differs. The standing instructions gain exactly the one fixed sentence about the coverage field. |
| No hindsight | No packet blob contains a defect-ledger id or `reviewer_observation`. See the correction below about the word "hindsight". |
| Coverage items 1 to 5 | All answered. Commit 39's entry (attempt 005) was read in full and is cited with the `ancestor` label; the introducing commit is named from `git_show` of that commit. Four configurations read in full. Six header calls cover the four models. |
| Introduction attribution | Correct. Git shows `decilm.py` was added by `75c7366b` and the line is unchanged until this commit. |
| Per-model comparison | Recomputed from the packet. 51B blocks 0, 1, 6, 7 have group sizes 8, 16, 32, 64 and stored key widths 1,024, 512, 256, 128: the old expression matches only block 0, the new one matches all four. Both Ultra models: stored 1,024, old 2,048, new 1,024. Super: 1,024 under both. As the draft says. |
| Assertions and empty blocks | 51B is still rejected at block 11; the other three pass before and after; Ultra's empty blocks start at 9; Super has none. Correct. |
| Source claims | The changed line, the projection widths and the reshape in `attn.py` (the truncated read reached them), the converter's unguarded division. Correct. The 51B configuration has a `num_key_value_heads` key whose value is null, which fits the draft's remark that the global field is not used. |
| Findings | Both are carried over from commit 39's entry and say so. Both are marked suspected with honest limits. |
| Scalar check | Re-ran: output identical. |
| Tests | 209 passed earlier in this session on the same implementation hashes. |
| Dependents | No later run read 44/001's prose. Agreed. |

## Correction to my verdict on attempt 002

That verdict says no packet blob contains the word "hindsight". That is false as written: tokenizer vocabulary files in the reference evidence contain it as a token. I had searched and misread an empty follow-up as no matches. The matches are all vocabulary entries; none is reviewer or ledger text. The conclusion (no hindsight reached the teacher) stands for 002 and for this attempt. I have not edited the 002 verdict, because its hash is bound in this request.

## Not verified

- Tensor shapes beyond the sampled blocks.
- Any model load, conversion or inference.

## Must fix before canonical use

Reviewer-only.

1. Reviewer-assisted; the selection of assisted entries for canonical use is undecided.
2. The Problem line says the checkpoints "require" the quotient, labelled source. The evidence is sampled blocks, as the limits section says. A canonical entry should carry that bound in the sentence.

## Follow-ups

- Defect ledger: the two findings are observations of defects first reported at commit 39 (the empty-block division) or of a limitation stated there (51B linear attention). One record each, several observations; no new defect.
- Ledger `exllamav3-decilm-kv-head-count` r002 can cite this entry as the fix's own corroboration from cutoff-eligible evidence.

## Next

1. Record this approval; mark 44/001 superseded for future retrieval.
2. Author `commit-000045-002` with `reviews/verdicts/commit-000045-002.coverage.md`, then stop for full review. Then `commit-000055-002`.
