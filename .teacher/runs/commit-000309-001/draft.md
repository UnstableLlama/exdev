# 997ca85bcce1ad5da2f93c17df5f13bd77cc4800


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/997ca85bcce1ad5da2f93c17df5f13bd77cc4800) · [Evidence ledger](draft.json)

Adds cached, subject-selectable MMLU evaluation using one-token answer logits, optional choice shuffling and aggregate accuracy/confidence reporting. The few-shot counter is never advanced, so positive requested counts do not limit demonstrations.

- [Score MMLU answers through one-token generation jobs](#usage-evaluation)

## Problem

The change adds a standalone MMLU evaluator, complementing the existing code-completion evaluation workflow. [source; call_8110cb4b0e114daab558bae59d8bedbc, call_1fcbcf21a6934af4882fd8c300bb1cc5]

## Reasoning

Rather than judging generated text, the evaluator requests one token's logits and compares the four answer-token scores. Subject-specific development examples supply the prompt context. [source; call_8110cb4b0e114daab558bae59d8bedbc]

## Impact

The script reports question-weighted accuracy and mean probability assigned to the correct answer, normalized over A–D only. Its few-shot count option does not correctly limit positive example counts. [source; call_8110cb4b0e114daab558bae59d8bedbc]

## Source Notes

The root usage-evaluation entry establishes the earlier Generator/Job evaluation pattern in HumanEval; the cache documentation entry describes explicit cache namespaces and JSON-serialized arguments. [ancestor; call_0a1e891ad84f4813bde3fd3bb9fb4fc4, call_a357d19a316247efaf2dc382b63fe42a]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a dimension mismatch at held_logits.append. Its relevance here is inferred from the evaluator enabling return_logits and the parent containing the same append expression; it is not an MMLU reproduction. [inference; call_81192296ce7d4535a64c3d4e02b44438, call_4809cef82467416a828dedbe19ba352b, call_8110cb4b0e114daab558bae59d8bedbc]

The inspected discussion material frames #26 as “Superior 3INST parameters,” #33 as “Error converting model,” and closed #58 as “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT.” These are quantization discussions, not evidence that this MMLU addition resolves their reported problems. [source; call_dc3453c7e97e43f9a73baab3413ff949, call_8f43eb8dd3b148be95c8a3cabe3a124f, call_255fff4c06e5493589d139bc7c9872d0, call_72f0c7f0892f43c9b78a78d05e115fc4]

<a id="usage-evaluation"></a>

## Score MMLU answers through one-token generation jobs

get_dataset_mmlu loads cais/mmlu's all configuration, materializes rows, and caches dev and test separately through the split argument. The shared decorator uses JSON argument keys and stores its shelf beside sys.argv[0], creating __disk_lru_cache__ there. Existing callers cache dataset text, tokenized data, storage statistics and evaluation results; the new split string and row-list return require no additional argument preparation. [source; call_8110cb4b0e114daab558bae59d8bedbc, call_0191d3a9de0d45ffa5ccf2a5fa86e678, call_c9637d223c6d4e15b0e77d6b4e62167b]

Both splits are sorted by subject. Subjects default to all development-set subjects; a comma-separated selection is checked against that set. Optional shuffling permutes only selected test questions and relocates the answer index with perm.index, leaving development demonstrations unchanged. No shuffle seed option is added. [source; call_8110cb4b0e114daab558bae59d8bedbc]

format_question labels four choices A–D and ends unanswered questions at 'Answer:'. Demonstrations append the answer letter and a blank line. Each subject gets a shared preprompt encoded with BOS; each test question is encoded without BOS and concatenated to it. The default few-shot setting is five, but the demonstration loop never increments its counter. [source; call_8110cb4b0e114daab558bae59d8bedbc]

The generator is configured for at most 1024 parallel sequences, subject to available cache capacity, and max_q_size=1. Every question becomes a Job with max_new_tokens=1, return_logits=True and its row as identifier. Unlike HumanEval's text extraction and cancellation protocol, this evaluator waits for EOS events and consumes logits rather than the sampled completion. [source; call_8110cb4b0e114daab558bae59d8bedbc, call_cf124c1b145041e4993c8aeb0b438e81, call_29164e6a0d514ead83f04e145857649c, call_1fcbcf21a6934af4882fd8c300bb1cc5]

The four scores are selected using exact token IDs for ' A', ' B', ' C' and ' D'. Argmax determines correctness; softmax over those four scores supplies the correct-answer confidence. Consequently confidence is conditional on the four scored tokens, not the probability of the sampled token or a full-vocabulary confidence. Totals aggregate questions across subjects rather than averaging subject accuracies. [source; call_8110cb4b0e114daab558bae59d8bedbc, call_b0d6041217e2457d918a5356def2a970]

A bounded scalar transcription verified answer preservation for all 24 four-choice permutations and all four original answer indices: 96 cases. With five synthetic same-subject development rows, requested counts 0, 1, 2, 5, 6 and -1 included respectively 0, 5, 5, 5, 5 and 5 examples. [execution; call_cc9b1c13083c4af180a6328bc5c58511]

## Authoring-time findings — pending review

### fewshot-counter-not-advanced (suspected; defect)

The requested positive few-shot count does not limit the number of demonstrations.

Trigger: Run the new CLI with --fewshot_examples 1 or another positive count smaller than the available development examples for a selected subject.

Expected: Include only the requested number of same-subject development examples.

Actual: fewshots remains zero throughout the loop, so every matching development example is appended for any nonzero requested count. Zero exits immediately. The new __main__ block directly calls main; the whole-parent mmlu search found no existing evaluator caller, so the established reach is this new CLI and direct invocations of its main.

Locations: 997ca85bcce1ad5da2f93c17df5f13bd77cc4800:eval/mmlu.py — main

Source evidence: call_8110cb4b0e114daab558bae59d8bedbc, call_2881092493584a848df0c9baba2bfd8e

source_inspection: Inspected initialization, break condition, subject filtering, prompt append and CLI invocation; no increment follows the append. [call_8110cb4b0e114daab558bae59d8bedbc, call_2881092493584a848df0c9baba2bfd8e]. Limits: Literal parent search does not exclude external callers.

scalar_transcription: Reimplemented the inspected selection loop over five synthetic same-subject rows and observed all five included for requested counts one and two. [call_cc9b1c13083c4af180a6328bc5c58511]. Limits: Did not execute repository evaluator code, tokenize prompts or measure score changes.

## Uncertainty and limits

No dataset download, model inference, tokenizer compatibility test or MMLU score measurement was performed.

The scalar checks model Python control flow and permutations; they do not execute the evaluator, Torch operations or GPU kernels.

Answer scoring requires exact vocabulary pieces for space-prefixed A–D. single_id performs exact lookup; the script does not validate the resulting IDs or provide a multi-token scoring alternative.

Persistent shelf creation and serialization were inspected but not executed. The dataset revision is not pinned by the new loader.
