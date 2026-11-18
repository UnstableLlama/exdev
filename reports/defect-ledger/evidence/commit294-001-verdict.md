# Verdict: commit-000294-001 (teacher Sol, guidance 12, unassisted; ran ahead of 293)

Reviewer: Fable. Date: 2026-11-17 (14:38 UTC). Upstream `6f9928b3` "Ernie4.5: Use float32 intermediate in MoE layers".
Run: `.teacher/runs/commit-000294-001`. Packet: `.teacher/retrieval/000294-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. Both findings are accepted as
observations of existing identities (all-expert fused shape; fused output contract); neither is new. The
entry made the central check itself: it followed the wider gate and up outputs through to the next
consumer on both paths (a separate half activation buffer in ordinary evaluation and in the fused
workspace, and a fused kernel that accepts float output), and says plainly that the product is narrowed to
half again, so the change does not make the whole expert float.

It stands without a rerun: 293 changes only the chat example's statistics.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 292 of 293 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 46 evidence
calls all cited and none bad, final equals annotation, 4271 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 292 of 293, as disclosed. Repair enabled, unused.

## Run checks (mine, tree at `6f9928b3`)

- Only the routed experts' `interm_dtype` changes; dense prefix and shared experts keep half. As stated.
- `BlockSparseMLP`: gate and up take `interm_dtype`; `interm_a` is a separate half tensor when the
  intermediate type is not half (line 305), and the ordinary path allocates one per call (line 364). As
  stated.
- `exl3_mgemm` accepts a float or half output (`c_fp32`). As stated.
- The buffer arithmetic (36,864 to 92,160 bytes and 114,688 to 286,720 bytes) is right.
- Configuration values for the eleven MoE checkpoints are those I verified at 292.

## Ledger

Accepted: `chat-context-count-overwritten` r002 (fix at 293), `chat-tps-toggles-multiline` r002,
`nonpositive-codeblock-index` r004. File this entry's two observations with the next request.
