# Verdict: commit-000337-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (16:42 UTC). Run: `.teacher/runs/commit-000337-001`. Packet: `.teacher/retrieval/000337-001`.
Upstream `fb63886b9a9909ab78822780e82fd10d001dcd02` "Remove input_ids from fwd params".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 77 calls, 0 bad, 0 uncited; final equals annotation; 333 ancestors
  and 333 entries; 4,662 blobs, 0 bad; 77 calls replay with 0 mismatches. No repair turn.
- Diff: 17 files, 17 deletions, all the same line. The 17 are every `prepare_inputs` override in the tree. The base
  `Model.prepare_inputs` is the only remaining writer, and `Gemma3VisionModel` and `Mistral3VisionModel` inherit it.
- Central claim, by my own whole-tree searches at the parent: no read of the key. The only other quoted `input_ids` is the
  saved-tensor name in `eval/model_diff.py:100`; no non-Python file has it; nothing spreads, copies or iterates `params`.
  The three `prepare_inputs` callers use the return value. `Embedding.forward` reads IDs from `x`.
- `modules/attn.py`: both uncached routes assert no cache; `prepare_flash_attn` takes batch size from the tensor, builds or
  accepts the block table, and requires a multiple of `PAGE_SIZE` (256). None of it reads the key.
- The teacher's 102-case extracted-method check: I read the code and its output. It tests what the entry says it tests.
- Inheritance: `Gemma3TextModel` from `Gemma3Model`; MiMo, Mistral and Qwen2 from `LlamaModel`. `Qwen3MoeConfig` supplies the
  mapping the entry says.
- Inherited findings, rechecked at this commit:
  - Prefill flag: `Model.prefill` breaks with the flag true, `forward` does not clear it, `TransformerBlock` returns before
    the residual and MLP, and `ParallelDecoderBlock` after the residual but before the MLP. As stated.
  - EXAONE4: the pinned config has 30 layers and a null pattern, `read_dict` turns null into the `None` default, and
    `is_local` then calls `len(None)` at layer 0. As stated.
- Discussions: all eight titles match the fetched text. I did not check each report's further detail.
- Ledger `cache-detach-count-diagnostic` r005: accepted. Confirmed, with a source-verified fix at `37f80fb9` that matches my
  336 check; observations byte-equal; introduction unchanged; `37f80fb9` listed as unaffected; not training-eligible.

## Requested next

With the next request, file the persistence revisions at this commit for `prefill-flag-leaks-into-forward` and
`exaone4-null-window-pattern` if your ledger routine calls for them, or say why none is needed.

## Must fix before canonical

The two Source Notes paragraphs listing unrelated discussions, and the Gemma chat-format aside, are padding. Editorial only.
