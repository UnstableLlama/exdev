# 02982fcc9fed57a8e5b2bdf55cdceb12cc70f594


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/02982fcc9fed57a8e5b2bdf55cdceb12cc70f594) · [Evidence ledger](draft.json)

Comments out three per-sample invariant assertions, relying on existing generator preparation. Performance is unmeasured; the inherited optional-output failure remains.

- [Remove repeated sampling-boundary assertions](#sampling)

## Problem

Job.receive_logits repeated three invariant checks at each sampling step: matching logit rows to sequences, completed prefill, and live sequences. [source; call_36cc8da6353647d5985aeb833df1a78a, call_0a91f9f6ec3c477ab2b91a61cc2a4eaa]

## Reasoning

Removing these checks plausibly reduces Python-side sampling overhead, trading local diagnostics for reliance on the generator's preparation. No speedup is established. [inference; call_36cc8da6353647d5985aeb833df1a78a, call_d734c3f7e759493390cad8c8c500f96a]

## Impact

The change comments out assertions only; token constraints, sampler arguments and result handling remain unchanged. [source; call_36cc8da6353647d5985aeb833df1a78a, call_0a91f9f6ec3c477ab2b91a61cc2a4eaa]

## Source Notes

The root generation entry was read. It describes the scheduling invariants and records an optional-output failure in receive_logits. [ancestor; call_7ca3d5dc028d47cbb2b7c638cdda1bf3, call_affc7f595ed34144adb852e403a184bb]

PR #30, “fix: don't add min_p and top_p samplers to stack if falsy,” concerns sampler parameter assertions. Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns job construction and prompt mode. Their relationship to this task is only an inferred topical overlap—assertions/sampling and job.py respectively—not evidence that this change fixes either report. [inference; call_03ca8d35db6a4e6593e307c15b39f6e8, call_f8865ad087aa4339afe6095041fa2b72, call_36a4f9c1a1b346fe81d794abc898fdff, call_36cc8da6353647d5985aeb833df1a78a]

<a id="sampling"></a>

## Remove repeated sampling-boundary assertions

The removed prefill assertion required every sequence's KV position to equal its token length minus one: the final input token remains for decoding. The other assertions rejected mismatched batch rows and any sequence marked non-live. No replacement checks are added inside receive_logits. [source; call_0a91f9f6ec3c477ab2b91a61cc2a4eaa, call_36cc8da6353647d5985aeb833df1a78a]

Whole-tree search finds Generator.iterate_gen as the sole active direct caller, plus a commented-out threaded caller. iterate_gen excludes unfinished-prefill jobs, builds logit boundaries from their input sequences, skips empty intervals, and passes each job's rows one token position at a time. receive_sample appends a token and advances KV position together, preserving the readiness equality during ordinary decoding. [source; call_3b7e1b4c0401465396ea75752d7bf664, call_d734c3f7e759493390cad8c8c500f96a, call_0a91f9f6ec3c477ab2b91a61cc2a4eaa]

Sequence initializes live=True; the generator-directory search finds no other live-field use besides the removed assertion. Thus no inspected normal caller establishes a false-live path. The scheduling checks and row construction remain, but malformed direct calls lose immediate assertion diagnostics. [source; call_14aeddf70d664490a882f888d5012a71, call_430956b73aa44f6fb4a86e33d62760a6, call_d734c3f7e759493390cad8c8c500f96a, call_36cc8da6353647d5985aeb833df1a78a]

The inherited optional-output failure remains: the task does not replace the pass branches that leave requested probability/top-token locals undefined. [source; call_0a91f9f6ec3c477ab2b91a61cc2a4eaa, call_36cc8da6353647d5985aeb833df1a78a]

## Authoring-time findings — pending review

### optional-sampling-outputs (suspected; defect)

The touched function retains an inherited failure when optional sampling outputs are requested.

Trigger: A job reaches receive_logits with return_probs=True or return_top_tokens>0 and its sampler returns normally.

Expected: Return the requested probability or top-token values for the caller to pass to receive_sample.

Actual: The enabled branches execute pass, leaving next_prob or next_k_tokens/next_k_probs unassigned; constructing the return tuple raises UnboundLocalError. The sole active repository caller, Generator.iterate_gen, directly unpacks this tuple.

Locations: 02982fcc9fed57a8e5b2bdf55cdceb12cc70f594:exllamav3/generator/job.py — Job.receive_logits

Source evidence: call_0a91f9f6ec3c477ab2b91a61cc2a4eaa, call_36cc8da6353647d5985aeb833df1a78a, call_3b7e1b4c0401465396ea75752d7bf664, call_d734c3f7e759493390cad8c8c500f96a

source_inspection: Compared parent implementation, task diff and the active caller; the defective branches are carried over unchanged. [call_0a91f9f6ec3c477ab2b91a61cc2a4eaa, call_36cc8da6353647d5985aeb833df1a78a, call_d734c3f7e759493390cad8c8c500f96a]. Limits: No end-to-end generation was executed.

scalar_transcription: A scalar transcription returned normally with both options disabled and raised UnboundLocalError for each enabled option. [call_ddbaeb10db9741c8881fd5931774c000]. Limits: Models Python conditional assignments only, not repository execution or tensor sampling.

## Uncertainty and limits

No generation, GPU execution or performance benchmark was run. The scalar check exercises optional-return control flow only.

The inspected repository caller preserves readiness and row mapping under its normal model-output contract; arbitrary external calls, custom sampler side effects and malformed model outputs were not validated.
