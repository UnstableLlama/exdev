# Verdict: commit-000309-001 (teacher Sol 6.1, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (20:49 UTC). Upstream `997ca85b` "Add MMLU eval".
Run: `.teacher/runs/commit-000309-001`. Packet: `.teacher/retrieval/000309-001`.

## Decision

**Approved for ancestor retrieval only. 309/001 is the entry in force for commit 309.** Canonical and
training stay false. One new suspected finding accepted: the few-shot counter is never advanced, so any
nonzero `--fewshot_examples` includes every dev row of the subject and zero includes none.

Ran ahead of 308 (chat.py commands); irrelevant to a new eval script, stands. 308 is approved, so this may
be recorded now. The entry makes the checks that matter itself: the counter bug with its reach, that the
score is an argmax over exactly four token ids from `single_id(" A".." D")`, that confidence is a softmax
over those four only, that accuracy is question-weighted, that shuffling relocates the answer with
`perm.index` and leaves dev rows alone, and that BOS is on the preprompt only.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal to the accepted
set, 24 evidence calls all cited, final equals annotation, 307 of 308 ancestors (sparse, as disclosed), 4410
blobs, nothing after the cutoff. My plain replay matched 19 of 24: four are the `ancestor_read` calls it
refuses on a sparse packet, the fifth is the refused oversized `web_fetch` of #26, where the recorded error
and mine are the same text ("Invalid max_bytes") in a different wrapper.

## Run checks (mine, tree at `997ca85b`)

Diff read in full. `job.py` 563 to 572: with `max_new_tokens = 1` the single step appends
`logits[:1, :, :]` and emits EOS with held logits, so the EOS result does carry `"logits"`; 727 makes that
buffer `(1, n, padded_vocab)` float. `file.py` 34 to 45: key is the JSON of the arguments, so `dev` and
`test` are separate entries. As stated.

## Ledger

The three 308 records are accepted as filed: explicit-load-falls-through r001 and
empty-history-retry-edit r001 (new identities, introduced at `e12a1a5d`), nonpositive-codeblock-index r005
(one observation appended, earlier ones equal). All suspected, training false. File 309's finding next.

## Must fix before canonical use

State the shape and type of the returned logits: `result["logits"]` is `(1, 1, padded_vocab)` float, so
`[0, 0]` is the vocabulary vector for the one generated position.
