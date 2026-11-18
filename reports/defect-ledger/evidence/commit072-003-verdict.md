# Verdict: commit-000072-003 (replacement of 72/002 at guidance 11)

Reviewer: Fable. Date: 2026-11-16. Upstream `c44e56c7` "Add GLM4 architecture".

## Decision

**Approved for ancestor retrieval only. 72/003 replaces 72/002 as the entry in force for commit 72** for
packets prepared from now on. 72/002's draft, transcript, packet and approval record are kept as history.
Canonical and training stay false. First replacement under `guidance-11-reauthoring-plan-001`.

The finding `glm4-partial-rope-frequency-read` is the same defect as 72/002's `partial-rope-frequency-load`
and remains **accepted as true** (source level; no device fault measured). No finding was lost.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 43 evidence
calls all cited, final equals annotation, 71 ancestors, 1056 blobs, nothing after the original cutoff
(2025-04-18T00:49:19Z). The new packet's manifest differs from 72/002's in `guidance_version` only.

## Run checks

- Replay: 43 of 43 identical.
- **Headers (mine, all six repositories from the packet's own blobs).** Every shape the entry quotes is right:
  32B embed `[151552,6144]`, Q/O `[6144,6144]`, K/V `[256,6144]`, fused gate/up `[46080,6144]`; 9B Q/O
  `[4096,4096]`, K/V `[256,4096]`, fused `[27392,4096]`, Q/K/V biases present (and no O bias); Rumination K/V
  `[1024,6144]`. All tensors BF16. No tensor family outside what the constructor loads. The three repositories
  the teacher did not open (32B-Base, Z1-32B, Z1-9B) match their siblings, so its "one per distinct
  configuration" sampling lost nothing here.
- Precision statements checked at the task: `Embedding` defaults to `out_dtype = torch.float`; the two
  post-norms and the MLP request FP32 output with `interm_dtype = torch.half`; the final norm returns FP16.
  As the entry says, and it now makes the link to commit 71 that 72/002 lacked.
- The finding's arithmetic (64 launched indices against 32 frequencies for head dimension 128 and factor 0.5)
  is as accepted at 72/002.

## Against 72/002's "must fix before canonical use"

1. Headers read and stated: **met**, with one remainder. The entry gives the fused shape for each layout but
   does not say outright that these checkpoints store *only* the fused tensor (I count zero separate gate or
   up tensors in all six). A canonical entry should say so.
2. Link to commit 71's precision facility: **met**.

## Differences that matter for later entries

None found. The new entry adds facts and corrects one narrow statement (the residual stream is FP32 because of
the embedding's default); it withdraws nothing a later entry could have relied on. The request's inventory
shows no later run that read 72's entry. No downstream action.

## Guidance note

This is a guidance 5 to 11 replacement, so paragraphs 6 to 9 applied as well as F. The header paragraphs are
F's doing; the caller comparison in the last section and the guard remark on MLP slicing look like the earlier
paragraphs. 43 tool calls.

## Ledger

- `exllamav3-unconditional-anyprecision-import` r001 (owed from 238): introduction and observation `162f99ab`,
  no fix, flags false, suspected / new requirement. Accepted.
- Owed with the next request: an observation revision on the partial-RoPE record for run 72/003, keeping the
  earlier observations.

## Not verified

- Nothing compiled, loaded or run on a GPU, as before.
- The inventory's two runs with unavailable coverage.

## Next

Record the replacement approval (one active selection for `c44e56c7`), then continue: 239, and replacement 98
at the next opportunity.
