# Verdict: commit-000346-002 (teacher gpt-6.2-sol, guidance 12, unassisted; second attempt)

Reviewer: Opus. Date: 2026-11-18. Upstream `67e0fd74` "TP: Refactor/fix auto allocation".
Run: `.teacher/runs/commit-000346-002`. Packet: `.teacher/retrieval/000346-002`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 47 bad [], evidence 86 calls 86 bad [] uncited [], final==annotation True,
  ancestors 342 of 342, blobs 4,756 bad 0. Replay 86 calls, 0 mismatches. No validation refusal. Hindsight scan empty.
- Packet 000346-002 is byte-identical to 000346-001 (`diff -rq`), as the recovery verdict required.
- Stale import, the entry's main finding: `modules/transformer.py:11` still imports `..util.tp_split`, the file is gone,
  and it is the only remaining reference. I imported the tree with third-party modules stubbed: `exllamav3.modules` fails
  with `ModuleNotFoundError` through `modules/__init__.py:9`, bare `exllamav3` imports, and correcting that one line makes
  both succeed. So the entry's limit on bare imports is right and there is no second import cycle behind it.
- Planner, from `model_tp_alloc.py` and `ratio_split` (`util/misc.py:73-85`): budget growth runs before masking; budgets
  0 to 9 are fixed points of `m * 11 // 10`, so an all-small budget loops forever; limit 1 keeps slot 0 only; residuals
  [0,20] become [0,0] and `ratio_split` divides by zero; budgets [4,4] with a 5-byte replica give split [1,0] and [5,5];
  zero channels reach `// channels`.
- Offsets: Attention grouping traced for head_dim 64, 96, 128 and 192 and odd counts; width scaling is right for Attention,
  Linear and unsliced GatedMLP. Sliced GatedMLP counts `num_slices` with width 128 (`mlp.py`, `make_tp_allocation`), so its
  emitted ranges are neither slice indices nor channel offsets, as the finding says.
- Other structure: plain MLP now raises, with constructors only at `gemma3.py:450` and `mistral3.py:373`, each after a Conv
  in the module list. Embedding and PosEmbedding return []. BlockSparseMLP stays in experts. No caller of `TPAllocator`,
  `initial_split` or `compile_tp_plan`. The tensor-parallel branch of `load_gen` still raises (`model.py:385`).
- Carried findings all hold here: quantized cache `overhead_size` is the full K/V pair and sits in `overhead_to_split`;
  `k_proj` exists only under `key_k` and the estimator reads it first; DeciLM no-op blocks register no children and hit the
  assertion at `module.py:117`; the planner over-budget and zero-axis cases above.

## Not verified

No GPU, model load or native code. Discussion summaries were not checked against fetched text. `review.sh` printed an
open-issue list for the wrong date (2026-10-31, not the 2025-07-29 cutoff), so I did not use it, and the request's catalog
counts are unchecked by me.

## Must fix before canonical

Source Notes pad in many discussions the entry itself says are unrelated (#7, #8, #11, #16, #27, #34, #38, #42, #43, #48,
#52, #53, #55, #57, #58). Same pattern as every entry since 322.

## Decision

**Approved for ancestor retrieval only.** The entry itself establishes the commit's central points: the planner changes,
head grouping and offset scaling, that nothing calls them yet, and that the move breaks `exllamav3.modules`. I found no false
statement about the source. Canonical and training remain false. All eight findings are suspected and belong in the ledger
under the usual rules.
