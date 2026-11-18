# Verdict: commit-000338-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (16:57 UTC). Run: `.teacher/runs/commit-000338-001`. Packet: `.teacher/retrieval/000338-001`.
Upstream `eeaabcdc457efa53ad56314c79e27bae06e7a88c` "Formatting, cleanup, typos".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false. The entry does well to look past the commit
title: two edits in `Model` change behavior, and one of them breaks image embedding.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 52 calls, 0 bad, 0 uncited; final equals annotation; 4,689 blobs,
  0 bad; 52 calls replay with 11 mismatches, equal to the 11 `ancestor_read` calls, as expected for this sparse packet. No
  discussion text dated after the cutoff. No repair turn.
- Run-ahead: the packet lacks the 337 entry. No file overlaps with 337, and 337's source is in the parent, so the missing
  entry did not matter.
- Vision break, by my own AST walk of the tree at the commit: of 23 `Model` subclasses, only `Gemma3VisionModel` and
  `Mistral3VisionModel` have no `prepare_inputs`, and neither overrides `forward`. Both `get_image_embeddings` methods call
  `self.forward`, which now reaches `raise NotImplementedError` first. `examples/multimodal.py` and `examples/imgsearch.py` call
  those methods. Loading does not use `Model.forward`: autosplit calls `module.forward` directly.
- `find_module`: `@lru_cache` on `Model.find_module` only; `Module.find_module` is undecorated. Model-level callers are the two
  tests named; `convert_model.py:256` calls the `Module` method. The stale-miss behavior follows from the decorator.
- Cleanup: every other edit is spacing, a docstring TODO, the `filenmame` rename (no occurrence left) or a duplicate
  `profile_opt` import.
- BF16 finding, rechecked at this commit: chunks are `min(bytesize, 2 MiB)`, `stloader.cpp:298` passes `bytesize / 2`, and the
  CUDA path converts `numel / 2` pairs with no tail, launching zero blocks for one element. As stated.
- Resize example, recomputed: 28×1541, limit 1540, patch 28 gives 28×1540 with floor and 28×1568 with ceiling. `vision.py:60`
  uses floor.
- Discussions: I read the #12, #16 and #61 threads for the claims made about them. They hold. Issue states come from the
  packet's cutoff-bounded data.
- Ledger: `prefill-flag-leaks-into-forward` r003 and `exaone4-null-window-pattern` r002 accepted. Both add a persistence
  observation at `fb63886b` that matches my 337 check; earlier observations byte-equal; status suspected; no fixes; not
  training-eligible.

## Requested next

File the 338 ledger candidates with the next request: `vision-input-preparation-missing` introduced here, the cached-miss
behavior change, and a persistence revision for `deferred-bf16-odd-tail`.

## Must fix before canonical

- The discussion paragraphs in Source Notes are long and mostly say that unrelated reports are unrelated. Cut them.
- Say that 337 removed the override writes and this commit removes the last one, in the base class.
