# Verdict: commit-000310-001 (teacher Sol 6.1, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (21:01 UTC). Upstream `08dde73e` "Add Formatron support and improved logit masking".
Run: `.teacher/runs/commit-000310-001`. Packet: `.teacher/retrieval/000310-001`.

## Decision

**Approved for ancestor retrieval only. 310/001 is the entry in force for commit 310.** Canonical and
training stay false. Three new suspected findings accepted (mask not refreshed between speculative samples;
prefix accepted in the constructor then reset at activation, conditional on Formatron's reset, plus
`None.encode`; list-valued `vocab_processors` cannot pass `lru_cache`). Three carried findings accepted as
observations of existing identities.

Ran ahead of 309 (new MMLU script); irrelevant to the generator, stands; 309 is approved, so this may be
recorded now. This is the last run on `gpt-6.1-sol`. The entry makes the checks that matter itself: one
`prepare_logit_mask` per iteration against a per-token inner loop that advances the filters; background
filters submitted before `model.forward`, foreground after, joined in the job; grammar masks postponed
during token healing and the trigger token not fed to the filter; the mask is additive (0 and -inf), in a
pinned `(1, padded_vocab)` half buffer; the base `Sampler.forward` keeps the old signature while `Job`
always passes `logit_mask`; and `import exllamav3` now needs formatron and kbnf.

## Artifacts

Request hashes match. `check.py` clean except one line that is not the run's fault: it reports
`teacher/codex_adapter.py` differing from provenance because the author edited that file for the 6.2
change at about 21:00 UTC, after this run and its request. Provenance says `gpt-6.1-sol` medium and the
other 44 implementation hashes equal the accepted set. 51 evidence calls all cited, final equals annotation,
308 of 309 ancestors (sparse, as disclosed), 4425 blobs, nothing after the cutoff. My plain replay matched
46 of 51; the other 5 are the `ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `08dde73e`)

Library diff read in full. `generator.py` 463 to 512: mask prepared once, then
`for i in range(batch_logits.shape[1])` calls `receive_logits` and `receive_sample` per position.
`sampler.py` 11 to 20 still declares `blocked_tokens` and `allowed_tokens`; all six presets subclass
`CustomSampler`. `filter/__init__.py` imports `formatron.py` unconditionally. `custom.py` masks ids at or
above `actual_vocab_size` before the mask is added, so padding ids stay excluded. As stated.

## Recording (read before you record)

`require_approval_model` accepts only `MODEL` or `LEGACY_MODEL`. With `MODEL` already edited to
`gpt-6.2-sol` in the working tree, recording this 6.1 run will be refused. My directive said "two constants,
nothing else"; that was too narrow. Do one of: record 310 with the 6.1 constants restored and then make the
change, or make the change accept `gpt-6.1-sol` runs for approval as a named earlier model. Say which in
the implementation request. No one-off script.

## Ledger

309 record mmlu-fewshot-counter-not-advanced r001 accepted as filed (new identity at `997ca85b`,
suspected, training false). File 310's three new and three carried with the next request.

## Must fix before canonical use

State the type of `logits + logit_mask` at the sampler (mask is half; say what the logits are). The filter
index pairing (`f_idx` counts active filters in both the submit and the join loops) deserves a sentence.
