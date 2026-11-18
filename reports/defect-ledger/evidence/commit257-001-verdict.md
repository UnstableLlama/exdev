# Verdict: commit-000257-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-17 (05:41 UTC). Upstream `32d98c24` "compare_q.py: Add QTIP wrapper".
Run: `.teacher/runs/commit-000257-001`. Packet: `.teacher/retrieval/000257-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`invalid-70b-qtip-spec` is accepted as true as stated. The entry made the commit's central check itself.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 16 evidence calls all cited and none bad, final equals annotation, 256 of 256
ancestors, 3434 blobs, nothing after the cutoff. Orchestration hashes in provenance equal the accepted files;
complete packet; ran ahead of none. Repair enabled, unused.

## Run checks (mine, tree at `32d98c24`)

- The 70B specification fails `json.load` (trailing comma before the closing bracket); the 8B one parses to
  three entries. `main` loads every selected specification file before any filtering, so one bad file stops
  the whole invocation. As stated.
- `compare_q_qtip.py`: optional import guarded by `ModuleNotFoundError`; `max_mem_ratio = 0.7`; unused
  `auto` and `bf16`; head rule `out_features >= vocab_size * 0.9`; SU, SV, tlut, trellis accounting;
  `cuda:0`; `output.logits`. As stated. The AnyPrecision adapter's import is guarded in the parent, as stated.
- The runner divides by 8 and 1024**3 under a "GB" label. As stated.

## Must fix before canonical use

- Say what happens without the package: the guarded import leaves `model_from_hf_path` and
  `QuantizedLinear` undefined, so `load_qtip` raises `NameError`. The entry says only that there is no
  availability check.

## Ledger

`exllamav3-compare-q-split-result-serialization` r002 (fix at `f02c9afd`): accepted. File
`invalid-70b-qtip-spec` as a new identity with the next request.

## Reviewer knowledge (never to a teacher)

History of the 70B specification file, newest first: 74b5534f 2026-07-23 Remove compare_q.py and examples;32d98c24 2025-06-08 compare_q.py: Add QTIP wrapper;
