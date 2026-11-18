# Verdict: commit-000103-002 (replacement of 103/001; teacher Sol, guidance 11)

Reviewer: Fable. Date: 2026-11-16. Upstream `0ff9fd2e` "Add Cohere2 architecture".

## Decision

**Approved for ancestor retrieval only. 103/002 replaces 103/001 as the entry in force for commit 103** for
packets prepared from now on; 103/001 is kept as history. Canonical and training stay false. First
replacement authored by `gpt-6.1-sol`.

Both findings are inherited identities and are **accepted as true as stated**:
`inherited-config-mismatch-diagnostic` (the undefined name in the base constructor's assertion message) and
`inherited-partial-rope-frequency-read`. The entry says plainly that neither is triggered by the three
reference configurations or by normal factory dispatch. 103/001 had no findings, so none was lost.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree (`gpt-6.1-sol`, medium), 44
implementation hashes, 53 evidence calls all cited, final equals annotation, 102 ancestors, 1532 blobs,
nothing after the original cutoff (2025-04-28T02:22:35Z). The manifest differs from 103/001's in
`guidance_version` only.

## Run checks

- Replay: 53 of 53 identical.
- **Headers (mine, the three Cohere2 repositories from the packet's blobs).** Every shape the entry quotes
  is right: Command A Q/O `[12288,12288]`, K/V `[1024,12288]`, gate/up `[36864,12288]`, down `[12288,36864]`,
  embedding `[256000,12288]`; both R7B models `[4096,4096]`, `[1024,4096]`, `[14336,4096]`, `[4096,14336]`,
  `[256000,4096]`. All BF16. No tensor family outside what the constructor loads, as the entry says.
- Constructor and config statements agree with what I verified at 103/001 (window and pattern schedule,
  rotary settings only on local layers, `logit_scale` 0.25, absent `tie_word_embeddings`). The 48/16 and 24/8
  local/global layer counts are right.
- New and correct beyond the old entry: the three decode routes now guard a missing rotary object; SDPA
  rejects windowed layers so only FlashAttention serves them; the unguarded `attn.rope.apply` in
  `science/kv_quant_exp.py` sits behind a `TransformerBlock` test and is not reached by this model; the two
  branches share one calibration capture through the `.input` suffix.
- The historical-mirror label on the December R7B config is carried into the entry's limits.

## What is still missing (for a canonical entry)

**None of the three checkpoints stores an `lm_head` tensor**, so the tied-embedding path always runs. The
entry describes the alternate key and that tying defaults to true, and does not state the fact. This is the
third occurrence (214 in the trial, 98/002, now 103/002) of the same gap: a tensor the code names that the
checkpoint does not hold. Both models do it. It is now a pattern and I am raising it with the user as a
wording change to paragraph F.

## Differences that matter for later entries

None. The new entry is a superset of the old on every statement a later entry could have used.

## Ledger

- Owed from 244, filed here: `tps-toggles-multiline` r001, `context-count-overwritten` r001,
  `nonpositive-codeblock-index` r003. Accepted.
- Owed with the next request: observation revisions on the mismatch-diagnostic and partial-frequency-read
  identities for run 103/002.

## Not verified

The positional scheme itself (rotary on local layers, none on global) against a reference implementation;
no load or generation. As at 103/001.

## Next

Record the replacement approval. Continue with 245 and replacement 110.
