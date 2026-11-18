# Verdict: commit-000269-001 (teacher Sol, guidance 12, unassisted; ran ahead of 268; validation-repaired)

Reviewer: Fable. Date: 2026-11-17 (08:03 UTC). Upstream `13fa9ca2` "BlockSparseMLP: Allow float32 output from down projection".
Run: `.teacher/runs/commit-000269-001`. Packet: `.teacher/retrieval/000269-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All three findings are accepted
as true as stated: `ordinary-output-accumulator-dtype` is new; `carried-fused-shared-return` and
`carried-all-expert-fused-cardinality` are observations of existing identities. The entry made the commit's
central check itself: it followed the new float down output into the buffer that receives it. It stands
without a rerun: 268 changes only the EXL3 export method.

## Validation repair

Checked by me from the transcript: refused annotation at index 68 ("Source inspection requires source
evidence"), that message returned verbatim at 70, final annotation at 71 with no further tool call. Same
three findings before and after; the final version cites direct source reads where the refused one cited
searches. Nothing of substance lost.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 267 of 268 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 33 evidence
calls all cited and none bad, final equals annotation, 3523 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 267 of 268, as disclosed.

## Run checks (mine, tree at `13fa9ca2`)

- Ordinary path: `final_hidden_states = torch.zeros_like(y)` takes the input's dtype;
  `TransformerBlock.forward` calls `mlp_norm` with `out_dtype = torch.half`; `Qwen3MoeModel` builds the
  layer with `out_dtype = torch.float`, so the down projection now returns float and
  `index_add_` receives a float source for a half buffer. The path is taken for more than one token. As
  stated, and correctly left as suspected since nothing was run.
- Mixtral passes half for both, so it is unaffected. As stated.
- The activation destination is now a separate half tensor when intermediates are not half. As stated.

## Reviewer knowledge (never to a teacher)

The next upstream commit to this file, `b8c830c1` "BlockSparseMLP: Add DS3/Dots routing" (same day),
changes the buffer to `torch.zeros_like(y, dtype = self.out_dtype)`. That confirms the new finding.

## Ledger

File with the next request: the new accumulator identity, and observations on `fused-shared-unreachable`
and `all-expert-fused-shape`.
