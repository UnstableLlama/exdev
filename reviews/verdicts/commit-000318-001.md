# Verdict: commit-000318-001 (teacher Sol 6.2, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-18 (00:13 UTC). Upstream `4265c9e1` "Add Transformers ppl test (equivalent
to eval/ppl.py)". Run: `.teacher/runs/commit-000318-001`. Packet: `.teacher/retrieval/000318-001`.

## Decision

**Approved for ancestor retrieval only. 318/001 is the entry in force for commit 318.** Canonical and
training stay false. Five suspected findings accepted: the shared parser accepts `--gpu_split`,
`--load_metrics` and `--override` but the script never reads them; the copied exclusive window bound; a
one-token length leaves no targets; the row cap is tested after the append, so zero or negative rows still
score one; and `log_probs` is no longer deleted before the next forward while the `1e-10` add became
out of place (behaviour change).

Ran ahead of 317 (ppl.py --length); the new file copies that script, but the entry read the parent
`eval/ppl.py` directly and reached the same two inherited points on its own, so the missing entry did not
matter; stands. 317 is approved, so record now. The entry makes the checks that matter itself: what
"equivalent" does and does not cover; that tokenization still goes through ExLlamaV3's `Config` and
`Tokenizer` and only the forward is Transformers; `device_map = "auto"` with ids sent to bare `.cuda()`;
what `--tight` does; and the line-by-line difference from the native loop.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 51 evidence calls all cited, final equals annotation, 316 of 317 ancestors (sparse, as disclosed),
4483 blobs, nothing after the cutoff. My plain replay matched 45 of 51; the other 6 are the
`ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `4265c9e1`)

New file read in full against `eval/ppl.py`: no `del log_probs`; `.float() + 1e-10`; `AutoTokenizer`
imported and unused; `model_init.add_args` registers the three loader flags (`model_init.py` 26 to 28) and
`main` never calls `model_init.init`. As stated.

## Ledger

The four 317 records are accepted as filed (length-without-next-token-targets r001,
longer-window-outgrows-load-estimate r001, length-can-cross-longrope-tier r001 introduced at `c09f8098`;
window-ending-at-corpus-boundary-skipped r001 introduced at the root). File 318's with the next request;
the window bound and one-token ones are observations of those identities, not new ones.

## Must fix before canonical use

Nothing.
