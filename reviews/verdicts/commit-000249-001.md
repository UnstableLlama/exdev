# Verdict: commit-000249-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `7989c93b` "Add default single-round chat completion templates
to each model".

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false.

Both findings are **accepted as true as stated**: `gemma-system-interpolation` (the Gemma2 and Gemma3 methods
append the plain string `"{system_prompt}\n\n"`, no `f` prefix, so the placeholder is emitted and the system
text is lost) and `gemma-user-turn-closure` (no `<end_of_turn>` after the user text, where
`PromptFormat_gemma.format` in `examples/chat_templates.py` emits one). Reach is correctly limited to direct
callers of the new method; there are none in the tree.

The entry made the commit's central check itself: it read all sixteen changed sections, compared each new
template with the code, and found the two real template defects. Under the stricter standard that is an
approval. One real defect in the changed lines was missed; see below.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, `gpt-6.1-sol` medium, 44
implementation hashes, 34 evidence calls all cited and none bad, final equals annotation, 248 ancestors, 3359
blobs, nothing after the cutoff (2025-06-06T14:31:55Z).

## Run checks (mine, from the diff and tree)

- All sixteen templates as described: Cohere/Cohere2, Llama3 headers, ChatML for MiMo/Qwen2/Qwen3/Qwen3MoE
  with no BOS spelling, Mistral/Mixtral `<s>[INST]`, Mistral3 `[SYSTEM_PROMPT]`, DeciLM, Phi3, GLM4, Gemma.
  System text omitted when falsy everywhere.
- MiMo, Mistral and Qwen2 are `LlamaModel` subclasses, so their overrides do keep them off the Llama3 format.
  `Gemma3TextModel` inherits Gemma3's; `Gemma3VisionModel` and `Mistral3VisionModel` are direct `Model`
  subclasses and keep the base `NotImplementedError`. As stated.
- `Tokenizer.encode` defaults `encode_special_tokens = False` and `add_bos = False`. As stated.

## Missed by the entry (reviewer observation; must fix before canonical use)

The commit adds `from typing import override` to `mimo.py`, `mistral.py` and `qwen2.py`. Every other module in
the package (26 files) imports `override` from `typing_extensions`, which is a declared requirement.
`typing.override` exists only from Python 3.12, and `models/architectures.py` imports all three modules, so on
Python 3.11 or older importing the package fails with ImportError. The entry read these lines and says
nothing about them. This is a wider fault than either Gemma finding, but it is beside the commit's subject, so
it is recorded here and not grounds to reject. **Author: file this as a reviewer-observation ledger record
with the next request** (introduced at `7989c93b`; classification defect; status source-supported by
inspection, not executed on an older Python).

## Ledger candidates filed with this request

- `exllamav3-architecture-mismatch-diagnostic` r003: **accepted** (adds 110 as affected; introduction at 102
  and fix at 117 preserved).
- `exllamav3-qwen3-fp8-checkpoint-format-boundary` r001: **accepted** as a separate external-compatibility
  record, related to `exllamav3-fp8-dtype-not-loadable`; keep them linked, not merged.

## Next

Proceed with replacement 141 (guidance 12), then 250, one request at a time.
