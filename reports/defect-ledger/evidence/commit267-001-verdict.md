# Verdict: commit-000267-001 (teacher Sol, guidance 12, unassisted; ran ahead of 266)

Reviewer: Fable. Date: 2026-11-17 (07:37 UTC). Upstream `d5c48a64` "BlockSparseMLP: Add shared experts".
Run: `.teacher/runs/commit-000267-001`. Packet: `.teacher/retrieval/000267-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All three findings are accepted
as true as stated: `fused-shared-unreachable` and `shared-mlp-allocation-interface` are new;
`inherited-all-expert-fusion-cardinality` is an observation of the existing identity. The entry made the
commit's central check itself (both return paths, and both admitted shared types against the new attribute
reads). It stands without a rerun: 266 changes `linear.py` and `fp16.py`, which this entry does not rest on.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 265 of 266 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 33 evidence
calls all cited and none bad, final equals annotation, 3509 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 265 of 266, as disclosed. Repair enabled, unused.

## Run checks (mine, tree at `d5c48a64`)

- Fused branch: the old `return final_hidden_states.view(x.shape)` is still there, directly above the new
  three lines, so the shared addition can never run on that path. As stated.
- `MLP` defines `up` and `down`; only `GatedMLP` defines `gates`, `ups`, `downs`. `allocate_q` reads the
  list attributes of the shared module. As stated.
- The only constructions of `BlockSparseMLP` are in `mixtral.py` and `qwen3_moe.py`; neither passes
  `shared_experts`. As stated.

## Ledger

Accepted: `reversed-slice-comparisons` r001, `none-full-dimensions` r001, `deferred-bf16-odd-tail` r003,
`native-read-wait` r002. File this entry's two new identities and one observation with the next request.
