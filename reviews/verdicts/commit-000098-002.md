# Verdict: commit-000098-002 (replacement of 98/001 at guidance 11)

Reviewer: Fable. Date: 2026-11-16. Upstream `875e503e` "Add Cohere architecture".

## Decision

**Approved for ancestor retrieval only. 98/002 replaces 98/001 as the entry in force for commit 98** for
packets prepared from now on; 98/001 is kept as history. Canonical and training stay false.

The finding `cohere-qk-normalization-omitted` is the same defect as 98/001's `cohere-qk-normalization` and
remains **accepted as true**. Its classification changes from external compatibility to defect; I accept
that, since the architecture name now selects a constructor that silently ignores stored weights. No finding
was lost.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 44 evidence
calls all cited, final equals annotation, 97 ancestors, 1418 blobs, nothing after the original cutoff
(2025-04-27T15:06:11Z). The new manifest differs from 98/001's in `guidance_version` only. The supervisor's
filename mistake before inference and its repair are disclosed; one teacher session ran.

## Run checks

- Replay: 44 of 44 identical.
- **Headers (mine, all ten repositories from the packet's blobs).** Every shape the entry quotes is right:
  K/V `[1024,4096]` and `[1024,8192]` where it says eight KV heads, square `[8192,8192]` for the 64/64 models,
  the Plus models' `q_norm [96,128]` and `k_norm [8,128]`, the 4-bit models' U8 packed MLP weights
  `[92274688,1]` and `[207618048,1]`, embedding `[256000,4096]`. The statement that the bitsandbytes auxiliary
  tensors have no reader is right.
- The entry now says in its own words what 98/001's "must fix" item 1 asked for: full-precision checkpoints
  match, the Plus checkpoints carry unused Q/K norm weights, the 4-bit repositories are another storage format.

## What is still missing (for a canonical entry)

1. **No checkpoint stores an `lm_head` tensor** (none of the ten). So the tied-embedding path is the one that
   always runs, including for the models whose config omits `tie_word_embeddings` and get the new default
   (item 2 of 98/001's list). The entry describes the alternate-key mechanism and names one model that ties
   explicitly, but does not state the fact. This is the same kind of miss as 214 in the guidance-11 trial: a
   tensor the code names that the checkpoint does not store. Second occurrence; see the pattern note to the
   user.
2. The 4-bit Plus repository also carries the Q/K norm weights; the entry's finding names only the two dense
   releases. Harmless, since that repository cannot load anyway.

## Differences that matter for later entries

None. Nothing the old entry stated is withdrawn. The inventory shows one later run that read 98's entry; the
new entry is a superset on every point that run could have used. No downstream action.

## Ledger

- `exllamav3-unconditional-anyprecision-import` r002: fix `db65151b` recorded. Accepted.
- `exllamav3-optional-class-sentinels` r001: introduced and observed at `db65151b`, no fix. Accepted.
- Owed with the next request: observation revision on the Cohere Q/K record for run 98/002.

## Not verified

GPTJ as the right rotary layout and the shared-norm parallel block as the real layer structure (no reference
implementation in evidence), as at 98/001. No load, conversion or generation.

## Next

Record the replacement approval. Further replacements stay on hold per `teacher-model-trial.decision.md`.
Continue with 240 and the trial implementation request.
