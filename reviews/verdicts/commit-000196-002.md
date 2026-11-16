# Verdict: commit-000196-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000196-002`
Packet: `.teacher/retrieval/000196-001` (shared with the failed attempt 001)
Upstream: `a39fdfc4d5bdac1c677eecefbb1932b586c0dca9` "Attn: Fix head norm bias"
Request: `reviews/requests/commit-000196-002.md` (sha256 `48b4803ec5726c6e54e3797ea023c655e59d982af202fa84d5dca9d52393b7c7`)
Reviewed: 2026-11-16, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false. Attempt 001 stays failed and is
never retrieved from.

Every statement I checked is true. The entry read 185's entry, recognised this commit as the repair of the
overwritten-settings finding recorded there, and carried the two native findings unchanged.

The fix attribution is **confirmed**: `a39fdfc4` fixes the 185 normalisation-settings finding.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 19 of 19 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes (the accepted guidance-10 gate is in them); exactly 195 strict-ancestor entries; 2,877 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 19 of 19 recorded tool calls identical against the shared packet, including the `run` call. |
| Retry inputs | System message and opening user message byte-identical to 001's and the system message to 195/001's; the packet is the same directory. Neither the validator's error text nor the failed finding's identifier occurs anywhere in 002's transcript. |
| Unassisted | Packet version 8; guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fourteen open rows at 2025-05-27T09:55:04Z; my query agrees. Two closed rows, one by path alone, both selected; described as path overlap only. |
| The change | The two default assignments (`norm_eps = 1e-6`, `norm_constant_bias = 0.0`) move from after the `if`/`else` into the `else` branch, so they no longer overwrite the values copied from `q_norm`. Nothing else. Correct. |
| Effect | Gemma 3's head norms keep `constant_bias = 1.0` on the fused path; Qwen3 and Qwen3 MoE keep their configured epsilon; without head norms the values are as before. Correct. |
| Inherited findings | The unconditional store in `apply_norm` and the padded reads are unchanged. True. |
| Execution | The constructor assignments with stub objects; labelled as isolated statements. |

## Reviewer note (not a condition)

Attempt 001 had also reported that `q_norm = None` with a `k_norm` supplied is silently accepted while the
reverse is asserted. That is true of the code and is absent from 002. It is the kind of difference one run makes;
it is not carried into any ledger from a failed run.

## Not verified

- Any model run; that Gemma 3 output changes as expected.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: record `a39fdfc4` as the fix of the 185 settings identity; add it as an affected revision of the two
   native 185 identities. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 197.
