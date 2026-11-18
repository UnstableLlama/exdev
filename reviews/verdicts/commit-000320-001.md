# Verdict: commit-000320-001 (teacher Sol 6.2, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-18 (00:32 UTC). Upstream `1be81eed` "chat.py: Add Exaone template".
Run: `.teacher/runs/commit-000320-001`. Packet: `.teacher/retrieval/000320-001`.

## Decision

**Approved for ancestor retrieval only. 320/001 is the entry in force for commit 320.** Canonical and
training stay false. One suspected finding accepted: `single_id("[|endofturn|]")` returns `None` when the
tokenizer has no exact entry, and `Job` rejects `None` in the stop list, so the literal string stop beside
it is not a fallback. Same unguarded pattern as the ChatML and Dots templates.

Ran ahead of 319 (model_diff.py); irrelevant, stands; 319 is approved, so record now. The entry states the
format exactly (role markers each followed by a newline, `[|endofturn|]` straight after each completed
part, open assistant prefix for a pending turn, system turn only when truthy), that `add_bos` is false and
the formatter writes no BOS itself, that the "double BOS" comment is unverified, and the three stop entries
and how `Job` splits them.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 33 evidence calls all cited, final equals annotation, 318 of 319 ancestors (sparse, as disclosed),
4496 blobs, nothing after the cutoff. My plain replay matched 28 of 33; the other 5 are the
`ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `1be81eed`)

Diff read. `tokenizer.py` 205 to 216: `single_id` is two dictionary `get` calls and returns `None` on a
miss. `job.py` 193 to 196: anything that is not an int or a string raises. Mode key `exaone` registered.
As stated.

## Ledger

319 record ppl-axis-bound r003 accepted as filed (one observation appended at `5cb70f59`, earlier five
equal). File 320's finding with the next request; if an identity for the unguarded `single_id` stop
pattern already exists from ChatML or Dots, revise that one.

## Must fix before canonical use

Nothing.
