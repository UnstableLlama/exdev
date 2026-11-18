# Verdict: commit-000316-001 (teacher Sol 6.2, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (23:53 UTC). Upstream `2b3d8b54` "Add EXLLAMA_NO_P2P_COPY env override
for device-to-device copies (driver bug workaround)".
Run: `.teacher/runs/commit-000316-001`. Packet: `.teacher/retrieval/000316-001`.

## Decision

**Approved for ancestor retrieval only. 316/001 is the entry in force for commit 316.** Canonical and
training stay false. One new suspected finding accepted (behaviour change): the override tests only device
inequality, so CPU-to-GPU and GPU-to-CPU handoffs also take the staged branch and print a dot, including on
a single GPU where the embedding sits on CPU.

Ran ahead of 315 (progress.py); irrelevant, stands; 315 is approved, so record now. The entry makes the
checks that matter itself: the variable is read once at import; the test is string truthiness, so `0` and
`false` enable it; the enabled branch is `print(".")` then `x.cpu().to(self.device)`; same-device input
is untouched; it is opt-in, not a retry or a capability check; the driver bug itself is not identified by
the commit.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 37 evidence calls all cited, final equals annotation, 314 of 315 ancestors (sparse, as disclosed),
4471 blobs, nothing after the cutoff. My plain replay matched 33 of 37; the other 4 are the
`ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `2b3d8b54`)

Diff read. Callers by my own grep: `models/model.py` 85, 99, 199; `conversion/convert_model.py` 350, 358,
474; three eval scripts; `science/kv_quant_exp.py`; `tests/test_quant_fn.py`. `embedding.py` line 35 sets
`prefer_cpu`. As stated.

## Ledger

314 carried record mmlu-fewshot-counter-not-advanced r003 accepted as filed (one observation appended at
`a6d79e5d`, earlier two equal). File 316's finding with the next request.

## Must fix before canonical use

Nothing. Editorial, third time: fourteen discussions fetched and most summarised for an eleven-line change.
One sentence for the ones that share only a file path is enough.
