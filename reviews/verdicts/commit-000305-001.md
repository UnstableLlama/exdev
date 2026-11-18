# Verdict: commit-000305-001 (teacher Sol, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (19:54 UTC). Upstream `2cf3e4c1` "MLP: Fix for mixed-precision".
Run: `.teacher/runs/commit-000305-001`. Packet: `.teacher/retrieval/000305-001`.

## Decision

**Approved for ancestor retrieval only. 305/001 is the entry in force for commit 305.** Canonical and
training stay false. One carried finding accepted (odd activation tail), none new. Continue at 306.

Ran ahead of 304 (a chat template); irrelevant, stands. The central checks are the entry's own: the old
call passed `u` as destination, which the wrappers reject unless it is half; the new `a` is a separate half
tensor whenever `interm_dtype != torch.half`, which includes the default `None` used by eight builders (so
those now allocate although their projections already return half); explicit half keeps the alias; no
shipped builder passes float to `GatedMLP`, so the repaired case is not exercised in the tree. This is the
fix of ledger identity `exllamav3-fp32-mlp-intermediate-contract`.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal to the accepted
set, 24 evidence calls all cited, final equals annotation, 303 of 304 ancestors (sparse, as disclosed), 4381
blobs, nothing after the cutoff. My plain replay matched 20 of 24; the other 4 are the `ancestor_read` calls
it refuses on a sparse packet.

## Run checks (mine, tree at `2cf3e4c1`)

Diff read in full (three lines in `GatedMLP.forward`). The builder split equals my list from the 295
review: explicit half at qwen3, glm4, ernie4_5, ernie4_5_moe (dense, shared), dots1 (dense, shared) and now
smollm3; no `interm_dtype` at cohere, cohere2, decilm, gemma2, gemma3, llama, phi3, mistral3 (two sites).

## Ledger

File the two scoped revisions (fix of the FP32 contract identity, observation on the odd tail) with 306.

## Must fix before canonical use

Nothing.
