# Verdict: commit-000171-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000171-001`
Packet: `.teacher/retrieval/000171-001`
Upstream: `475dfcca479d4333d69e759f96d50045663cf69b` "compare_q.py: Add more GPTQ layer types"
Request: `reviews/requests/commit-000171-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and both inherited findings are correctly carried and correctly labelled as
inherited. The entry read 165's entry and drew the practical consequence: the new example spec, run on its own,
still ends in the zero-over-zero division, so it is not evidence that a standalone run works.

Ledger revision `exllamav3-unsupported-cache-default-argument--r002` is **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 170 strict-ancestor entries; 2,629 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 170/001's. Guidance 5, the last commit under it. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Twelve open rows at 2025-05-17T22:19:19Z; my query agrees. One closed row by terms, selected, and said to be unrelated. |
| The change | Two imports from `gptqmodel`; a `TritonV2QuantLinear` branch that counts `g_idx`, `qweight`, `qzeros` and `scales`; an `ExllamaV2QuantLinear` branch that counts `q_tensors`; both add `in_features * out_features` to the denominator. A new spec file for an AutoRound model using the `transformers` loader and forward function. Correct. |
| The helper | `get_tensors_size` is eight times the sum of element size times count over non-`None` values. Correct. |
| Inherited findings | Both present and unchanged at this commit: the unconditional `kl_div_sum_ab / kl_div_count` and the two-argument `disk_lru_cache_clear` against the three-argument cached call. These are 165's identities. Correct. |
| Execution | Recorded output: unequal keys, the division raises, 68,096 bits and 4.15625 bits per weight for the illustrative sizes, which the entry labels hypothetical. Matches the prose. |

## Ledger

- `exllamav3-unsupported-cache-default-argument--r002`: accepted; fix at `2432c64e`, affected revision 169.

## Not verified

- Anything inside `gptqmodel`, including whether these classes exist under those module paths in a given
  version; the entry says the same.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: add `475dfcca` as an affected revision of both 165 records.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval with `--approve`.
2. Then the guidance-7 adoption request. No 172 until that verdict.
