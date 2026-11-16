# a027848ddc37899274b540ed5ba009aa742d9d94


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a027848ddc37899274b540ed5ba009aa742d9d94) · [Evidence ledger](draft.json)

Normalizes top-K counts at the chat parser and shared sampling step, and routes ComboSampler’s K=1 case directly to greedy selection.

- [Normalize top-K counts and shortcut greedy sampling](#generation)

## Problem

Chat parsed explicit top-K values as floats, then passed them through ComboSampler to SS_TopK, which used the value directly as a slice boundary. [source; call_218737aea6ba4f578930ad443fe65ab9, call_f05b1bc339fd4fdc994ef8b64fd9b7fd, call_98d31c2482674eeb9b532eb3fb6c87e8]

## Reasoning

The change repairs both the chat input boundary and the shared sampling step: chat parses integers, while SS_TopK asserts integrality and converts accepted values to int. [source; call_13b38fff3bdd4f178f4115333780d67c, call_d62056f4e0b6435b922431e5693fca1b]

## Impact

ComboSampler additionally selects greedy sampling when top_k equals 1, matching the existing TopKSampler shortcut. [source; call_a1b3555af48d4347a2271a316dab168d, call_f05b1bc339fd4fdc994ef8b64fd9b7fd]

## Source Notes

PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3,” was opened by gakada and explicitly reports the float-index problem. Its relationship to this turboderp-authored change is inferred from the matching top_k indexing mechanism, not an explicit upstream link; its repetition-penalty report is separate. [inference; call_d89d58d56e364920a22159de57d16d89, call_d62056f4e0b6435b922431e5693fca1b]

PR #22, “OpenAI compatible API example,” concerns an API example and integration problems. Its discussion includes chat.py usage and a ComboSampler call; those overlaps do not establish that this commit addresses its reported problems. [inference; call_94f2d9e4093244a0942e4ece9966a034, call_120abd8b40144bab9b6fc48b5cab0f23]

<a id="generation"></a>

## Normalize top-K counts and shortcut greedy sampling

SS_TopK prepares sorted scores, then masks entries from index K onward with zero probabilities or negative-infinite logits. Its unchanged alternative replaces K < 1 with a no-op, so zero continues to mean disabled rather than an empty candidate set. [source; call_98d31c2482674eeb9b532eb3fb6c87e8]

The constructor now checks top_k.is_integer() before storing int(top_k). This accepts integral floating-point counts without silently rounding fractional values when assertions are enabled. Centralizing conversion also covers callers other than the chat parser; the parent HumanEval parser still declares top_k as float and is not changed here. [source; call_d62056f4e0b6435b922431e5693fca1b, call_1f94562b3102457cbcd16ddf7e3e29cd]

For top_k == 1, ComboSampler retains repetition, presence and frequency penalty steps but bypasses temperature, min-P, top-K, top-P and categorical sampling. SS_Argmax selects the maximum input or penalty-adjusted logit and marks sampling complete. The penalty steps produce unsorted logits, so this new route does not require the callee's sorted-state branches. [source; call_a1b3555af48d4347a2271a316dab168d, call_f05b1bc339fd4fdc994ef8b64fd9b7fd, call_98d31c2482674eeb9b532eb3fb6c87e8]

The shortcut plausibly avoids unnecessary filtering and random sampling for a single retained candidate; no performance improvement or tie-behavior equivalence was measured. [inference; call_a1b3555af48d4347a2271a316dab168d, call_98d31c2482674eeb9b532eb3fb6c87e8]

A standard-library transcription on Python 3.14.4 accepted 0, 2, 0.0 and 2.0, rejected 2.5 with AssertionError, and reproduced TypeError for a list slice using 2.0. A minimal argparse check parsed the new integer option successfully. These checks exercise Python scalar behavior, not repository tensors or generation. [execution; call_9484a29d10f34e808f449539d5948950]

## Uncertainty and limits

No repository sampling or GPU tests were executed. The scalar check used Python 3.14.4; availability of int.is_integer on historical supported Python versions is unestablished by the inspected evidence.

The assertion-based integrality guard was checked with assertions enabled; optimized-Python behavior and end-to-end generation were not tested.
