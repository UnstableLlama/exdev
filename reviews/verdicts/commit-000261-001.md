# Verdict: commit-000261-001 (teacher Sol, guidance 12, unassisted; ran ahead of 260)

Reviewer: Fable. Date: 2026-11-17 (06:22 UTC). Upstream `fce1b96e` "prequant_test.py: Add some more options".
Run: `.teacher/runs/commit-000261-001`. Packet: `.teacher/retrieval/000261-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`retained-state-histogram-strides` is accepted as a further observation of the existing identity
`exllamav3-skipped-state-strides`, not a new defect, as the request says. It stands without a rerun: 260
changes only `eval/compare_q.py`.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 259 of 260 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 15 evidence
calls all cited and none bad, final equals annotation, 3463 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 259 of 260, as disclosed.

## Run checks (mine, tree at `fce1b96e`)

- The bounds compare against `idx` from `enumerate(model.modules)`, half-open; both gate module and state
  inspection; `no_inspect_modules` gates only module inspection; load, forward, unload and `free_mem` stay
  unconditional. As stated.
- Weight histograms now use four standard deviations with `exclusive` false; the state histogram's middle
  range is still three with `exclusive` true. As stated.
- `inspect_state` still slices `state[:, skip_tokens:, :]` and moves it without `contiguous()`; the kernel
  indexes `input_ptr[i]`. As stated, with the right condition (whether the device move copies).

## Ledger

Add this observation to `exllamav3-skipped-state-strides` with the next request.
