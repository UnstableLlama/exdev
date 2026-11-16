# Verdict: commit-000163-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000163-001`
Packet: `.teacher/retrieval/000163-001`
Upstream: `830b6a018070a327d6d261628dff496f1303cf93` "Preparation for multimodal models"
Request: `reviews/requests/commit-000163-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**REJECTED: one statement is false and the entry misses the commit's most consequential effect.** The packet is
sound and most of the entry is right, including its own finding. Commit 163 has no approved entry, so the walk
does not move past it. Please author attempt 002 with the coverage request in
`reviews/verdicts/commit-000163-002.coverage.md`. That attempt is reviewer-assisted and must be flagged as such.

Canonical and training remain false.

Ledger candidate `exllamav3-compare-q-inference-mask-context--r001` is **accepted** as filed.

## Why

The entry says: "Existing architecture constructors supply a text mapping." That is true of eleven of the twelve
configuration classes in the task tree and false of the twelfth, and the twelfth is what matters. The reason and
its consequence are in the reviewer-only section; they are not for a teacher and not in the coverage request.

The teacher read all fourteen diff sections and no ancestor entry (27 were offered). It did not look at any
model file the diff leaves untouched. A reader who lands on this commit needs to know what it does to the
architectures already registered, and the entry as written tells them something untrue about that.

## What is right in this attempt

| Check | Result |
|---|---|
| Run integrity | 17 of 17 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 162 strict-ancestor entries; 2,501 blobs hash to their names; no evidence timestamp after the cutoff. Every request hash matches. |
| Replay | 17 of 17 recorded tool calls identical. |
| Unassisted | Standing instructions byte-identical to 162/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Eleven open rows at 2025-05-15T22:35:44Z; my query agrees. Two closed rows, one by path alone, both selected, nothing cut. |
| Architecture trigger | Does not fire: no new or renamed architecture and no identity change. Checked with `trigger_details` myself. |
| `Config` and `from_config` | `model_class` becomes `model_classes`, a dictionary; `from_config` takes `component = "text"`, asserts membership and instantiates the mapped class. Correct. |
| Llama, Mistral, Qwen2 | `LlamaConfig` takes `derived_model` and falls back to `{"text": LlamaModel}`; `MistralConfig` and `Qwen2Config` now pass their own model classes, where before they inherited `LlamaModel`. Correct, and a good observation. |
| The hook and `compile_model` | `get_additional_compiled_tensors` returns an empty dictionary by default; `compile_model` merges the result from every class in `model_classes`, plans shards with the existing soft limit, and writes module entries from the quantized working directory and string entries from the original collection. Correct. |
| Finding `extra-tensor-warning-name` | Correct. The warning in the new loop prints `module.key`, the loop variable of the previous loop, not the tensor's key; with no module ever bound it would raise instead. Conditional on a hook that returns something, as the entry says. It will carry into attempt 002 only if that session finds it again. |
| Source notes | Pull request 25 as inference; the others described by their own subjects. Correct. |

## Reviewer-only notes (never to a teacher, never in a coverage request)

- `exllamav3/models/qwen3_moe.py` is not among the changed files. At the task commit `Qwen3MoeConfig.__init__`
  still calls `super().__init__(directory, Qwen3MoeModel, **kwargs)`: a bare class where every other
  configuration now passes a dictionary. `Model.from_config` then evaluates `component in config.model_classes`
  on a class. In plain Python that is `TypeError: argument of type 'type' is not a container or iterable`; with
  assertions disabled the subscript on the next line raises instead; and `compile_model` would fail on `.items()`.
  Demonstrated with a stand-in class, not with the repository. `from_config` is on the path of conversion, every
  example and the evaluation scripts, so by this reading every Qwen3 MoE model fails to load or convert at this
  commit, twelve positions after the architecture was added at 141 and ten after it reached master at 153.
- Expect a one-line fix upstream soon. When it comes, 163's approved entry is its natural ancestor, which is
  why a false sentence here is not acceptable.
- This is the third commit in a row whose teacher read no ancestor entry or missed something an ancestor would
  have shown (158, 162, 163). The teacher's inputs and instructions are unchanged by the token-cost work; the
  pattern predates it (136, 140, 154). I am raising it with the user as a possible guidance change.

## Ledger

- `exllamav3-compare-q-inference-mask-context--r001`: accepted. Reviewer observation, new requirement,
  introduced at `a19538cf`, satisfied by `main` at that commit, source inspection only.
- Please also file, as a reviewer observation excluded from teacher input until an approved entry carries it:
  `Qwen3MoeConfig` passes a class where a mapping is required, introduced at `830b6a01`, with the mechanism in
  the first reviewer note. If attempt 002 finds it, the record takes the authoring origin instead.

## Next

1. Record this rejection. Keep run 001 as a rejected, unpublished attempt.
2. Author attempt 002 with the coverage request, same packet rules, by hand as at 153 (the driver's `--approve`
   refuses replacement and assisted runs by design), and file its request.
3. Do not start 164 until 163 has an approved entry.
