# Verdict: commit-000317-001 (teacher Sol 6.2, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-18 (00:02 UTC). Upstream `c09f8098` "ppl.py: Add length argument".
Run: `.teacher/runs/commit-000317-001`. Packet: `.teacher/retrieval/000317-001`.

## Decision

**Approved for ancestor retrieval only. 317/001 is the entry in force for commit 317.** Canonical and
training stay false. Four new suspected findings accepted: a length below two yields no targets and a
division by zero; the exclusive range bound drops a window ending exactly at the corpus end and gives an
empty `torch.cat` when none fits; a length above 2048 exceeds the 2048-token chunk and output size the
loader plans placement with; on Phi3 LongRoPE the factors are still chosen for 2048, not the requested
length.

Ran ahead of 316 (module.py); irrelevant to the perplexity script, stands; 316 is approved, so record now.
This is the kind of commit where the central check is easy to miss: the new flag changes the forward width
while `override_dynamic_seq_len = 2048`, `max_output_size = 2048` and `max_output_factor = 5` stay fixed
two lines above. The entry makes that check itself, and also states the stride stays 512, that a row of
length L gives L-1 targets, that overlapping targets are pooled without deduplication, and that scoring is
in float32.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 33 evidence calls all cited, final equals annotation, 315 of 316 ancestors (sparse, as disclosed).
My plain replay matched 31 of 33; the other 2 are the `ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `c09f8098`)

Diff and the whole of `eval/ppl.py` read. `model_init.py` 78 forwards the override; `config.py` 165 is the
base no-op and `phi3.py` 49 stores it; `rope.py` 174 to 176 compares `a_override` with the original limit.
`model.py` 144 to 163 sizes the dummy state from `max_chunk_size` and narrows to `max_output_size` at the
logit layer; 202 to 206 add the output-factor tensors. As stated.

## Ledger

316 record cpu-endpoints-enter-p2p-workaround r001 accepted as filed (new identity at `2b3d8b54`,
behaviour change, suspected, training false). File 317's four with the next request.

## Must fix before canonical use

Nothing.
