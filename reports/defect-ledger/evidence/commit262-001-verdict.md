# Verdict: commit-000262-001 (teacher Sol, guidance 12, unassisted; ran ahead of 261)

Reviewer: Fable. Date: 2026-11-17 (06:32 UTC). Upstream `d97bfdf1` "Add mixed-mode activation kernels".
Run: `.teacher/runs/commit-000262-001`. Packet: `.teacher/retrieval/000262-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. Both findings are accepted as
true as stated and as further observations of existing identities, as the request proposes:
`fp32-inplace-callers` under `exllamav3-fp32-mlp-intermediate-contract` and `odd-activation-tail` under
`exllamav3-activation-odd-tail`. The entry made the commit's central check itself: it went from the new
output dtype check to every caller. It stands without a rerun: 261 changes only `eval/prequant_test.py`.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 260 of 261 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 17 evidence
calls all cited and none bad, final equals annotation, 3469 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 260 of 261, as disclosed.

## Run checks (mine, tree at `d97bfdf1`)

- `silu_mul`/`gelu_mul`: half/half or float/float inputs, output must be half; float kernel multiplies in
  float and converts once; both kernels return at `idx >= numel / 2`. As stated.
- Callers: `GatedMLP.forward` (`mlp.py` line 243) and the ordinary expert path of `BlockSparseMLP`
  (line 258) call `activation(g, u, u)`, with `u` produced at `interm_dtype`; the fused path (line 312)
  writes to `interm_a`, a separate half buffer when `interm_dtype` is not half (line 199). As stated.

## Ledger

`exllamav3-skipped-state-strides` r002: accepted. File the two observations above with the next request.
