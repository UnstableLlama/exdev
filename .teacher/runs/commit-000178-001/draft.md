# 02982fcc9fed57a8e5b2bdf55cdceb12cc70f594


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/02982fcc9fed57a8e5b2bdf55cdceb12cc70f594) · [Evidence ledger](draft.json)

Comments out three sampling-entry assertions, trading local diagnostics for less repeated checking; an inherited optional-output failure remains.

- [Skip repeated sampling-entry assertions](#sampling)

## Problem

Every Job.receive_logits call checked logit batch size, prefill completion and sequence liveness before sampling. [source; call_e0ff3533510d4c319da1badfa46d1601]

## Reasoning

Removing these repeated checks plausibly reduces Python-side sampling overhead, at the cost of local invariant diagnostics. Performance motivation is an inference, not a measured speedup. [inference; call_98ce086d5e6f4a7c90a710326956e614, call_7517338f52a44380b4fe13129fde0451]

## Impact

The three assertions become comments; sampler arguments, token constraints and return handling are unchanged. Invalid state no longer fails at these particular checks. [source; call_98ce086d5e6f4a7c90a710326956e614, call_e0ff3533510d4c319da1badfa46d1601]

## Source Notes

The root generation entry was read. It records the ready-sequence invariant and an incomplete optional-output implementation in receive_logits. [ancestor; call_f9ad7128e3e143fabbc5a58c57b81902, call_f9dcaed7b0ee44dab048d7614197067f]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a constructor failure and discusses using chatml instead of llama3 mode. Its relationship here is only inferred from the shared job.py path and matching constructor exception; the task does not change that code. [inference; call_8fc4634a0d614074828812b3e74e7bc4, call_e0ff3533510d4c319da1badfa46d1601, call_98ce086d5e6f4a7c90a710326956e614]

<a id="sampling"></a>

## Skip repeated sampling-entry assertions

The removed prefill check scans sequences for kv_position == len(sequence_ids) - 1: the final input token remains for decoding. The liveness check separately scans seq.live; the shape check compares logits' first dimension with the sequence count. [source; call_e0ff3533510d4c319da1badfa46d1601, call_98ce086d5e6f4a7c90a710326956e614]

Whole-tree search finds one active direct caller, Generator.iterate_gen, and one commented threaded call. iterate_gen excludes unready jobs while constructing its batch, maps sequence rows back to each job and passes one token-position slice per sampling call. These upstream controls remain; removing local assertions does not introduce support for arbitrary shapes or unready jobs. [source; call_30bc8169d10a414bb600367319cf0d55, call_7517338f52a44380b4fe13129fde0451, call_98ce086d5e6f4a7c90a710326956e614]

The inherited optional-output failure remains: enabled probability or top-token branches still contain only pass, leaving return variables unassigned. The task changes neither these branches nor their caller. [source; call_e0ff3533510d4c319da1badfa46d1601, call_98ce086d5e6f4a7c90a710326956e614, call_7517338f52a44380b4fe13129fde0451]

## Authoring-time findings — pending review

### optional-output-return (suspected; defect)

An inherited optional-output failure persists in the modified function.

Trigger: Job.receive_logits reaches its return with return_probs=True or return_top_tokens greater than zero.

Expected: Return requested probabilities or top-token arrays alongside the sampled token.

Actual: The enabled branches assign nothing, so tuple construction raises UnboundLocalError. This reaches the active Generator.iterate_gen caller before receive_sample can consume the result.

Locations: 02982fcc9fed57a8e5b2bdf55cdceb12cc70f594:exllamav3/generator/job.py — Job.receive_logits

Source evidence: call_e0ff3533510d4c319da1badfa46d1601, call_98ce086d5e6f4a7c90a710326956e614, call_30bc8169d10a414bb600367319cf0d55, call_7517338f52a44380b4fe13129fde0451

scalar_transcription: Transcribed conditional assignments returned the default tuple with both options disabled and raised UnboundLocalError for each enabled option. [call_4e4e6604e94f4dfbaac003df7bdd329c]. Limits: Scalar Python model, not execution of Job or its sampler.

## Uncertainty and limits

No generation workload or GPU benchmark was executed; overhead reduction and output equivalence are unmeasured.

The scalar check exercises optional-return control flow only, not repository sampling or tensor operations.
