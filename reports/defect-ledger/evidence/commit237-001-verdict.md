# Verdict: commit-000237-001

Reviewer: Fable. Date: 2026-11-16. Upstream `ab875ba7` "compare_q.py: Fix GGUF VRAM computation when
output.weight precedes token_embd.weight".

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding `cached-accounting` is
**accepted as true** (inherited; source inspection only). The ledger item owed from 236,
`exllamav3-mistral-template-prefix` r001, is **accepted**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 13 evidence
calls all cited, final equals annotation, 236 ancestors, 3258 blobs, nothing after the cutoff
(2025-06-04T21:34:42Z). Instructions identical to 236's run. Guidance 9.

## Run checks

- Replay: 12 of 13 identical. The one mismatch is the recorded tool error (the second PR 26 fetch asked for
  110000 bytes and was refused), the known replay quirk; the request discloses the failed call.
- Diff read at parent and task. The embedding is now excluded from the decoder sum whether or not the head was
  seen first, norm weights are excluded, and the embedding still serves as the head when no `output.weight`
  exists. As the entry says.
- The entry's numbers recomputed by hand from its synthetic sizes: before, 1360 bits with the embedding first
  and 2960 with the head first; after, 1200 bits and decoder 4 bits per weight in either order; 2000 bits with
  no explicit head. All correct.
- The finding: `get_storage_info` is wrapped in `disk_lru_cache("lcpp_get_storage_info")`, keyed on its
  argument, and `compare_q.py --clear_cache` clears only `test_ppl` entries. So a result cached before this
  commit is returned unchanged. True, and correctly described as carried over rather than new.
- Caller chain (`load_llamacpp`, the loader registry, `vram_gb` in `test_ppl`, the plot axis) matches the source.

## Ledger (owed from 236)

`exllamav3-mistral-template-prefix` r001: introduction `543c4b27` (position 1); I confirmed the root's
`examples/common.py` line 24 already has the stray `n`. Observation at 236, no fixes, both eligibility flags
false, status suspected. Accepted.

## Not verified

- No GGUF file was read by anyone; the accounting is checked on synthetic numbers only.
- The unread tails of PR 26 and issue 38 (disclosed).

## Follow-ups (ledger, with the next request)

- `exllamav3-llamacpp-embedding-order`: new revision recording `ab875ba7` (237) as the fix.
- `exllamav3-llamacpp-cached-accounting`: new revision adding the 237 observation; still no fix.

## Next

Record the approval. Then `guidance-11-adoption-001`; no 238 until it is accepted.
