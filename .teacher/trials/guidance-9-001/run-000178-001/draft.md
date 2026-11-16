# 02982fcc9fed57a8e5b2bdf55cdceb12cc70f594


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/02982fcc9fed57a8e5b2bdf55cdceb12cc70f594) · [Evidence ledger](draft.json)

Comments out three per-token sampling assertions while retaining scheduler-side readiness filtering. Performance is unmeasured; the inherited optional-output failure remains.

- [Remove repeated sampling-boundary assertions](#sampling)

## Problem

Each Job.receive_logits call checked logit batch size, prefill readiness and sequence liveness before sampling. The change comments out these three assertions. [source; call_fd491c65a15d45409c2d40ae272b840e, call_c3fce2b0a2994e278ca19e6a9e26e565]

## Reasoning

Avoiding repeated validation on the per-token path is a plausible performance rationale, rather than a change to the sampling algorithm. No speedup is established. [inference; call_fd491c65a15d45409c2d40ae272b840e, call_b76530404aab498a9bbb14a66a397cf1]

## Impact

Sampling arguments, token constraints and return handling remain unchanged. Invalid state no longer receives these early assertion failures; normal scheduling still filters unready jobs and constructs per-job logit slices. [source; call_fd491c65a15d45409c2d40ae272b840e, call_c3fce2b0a2994e278ca19e6a9e26e565, call_b76530404aab498a9bbb14a66a397cf1]

## Source Notes

The root generation entry was read. It describes the scheduler/readiness contract and records incomplete optional probability outputs in receive_logits. [ancestor; call_5f7fcf954ac04a9b8a408be6f9f221af, call_791dd84904d44dc6a47044504e5c166d]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a Job constructor failure and a discussion recommending chatml mode. Its connection here is only an inferred shared-file relationship: the traceback matches the constructor's unchanged stop-condition validation, not the sampling assertions. [inference; call_1ddb8592cc584d228ae15515f51fb8e8, call_c3fce2b0a2994e278ca19e6a9e26e565, call_fd491c65a15d45409c2d40ae272b840e]

<a id="sampling"></a>

## Remove repeated sampling-boundary assertions

The removed checks guaranteed, when assertions were enabled, one logit row per job sequence, kv_position equal to sequence length minus one, and truthy live flags. The minus one leaves the final token for the next decode forward pass. No replacement validation is added. [source; call_fd491c65a15d45409c2d40ae272b840e, call_c3fce2b0a2994e278ca19e6a9e26e565]

Generator.iterate_gen remains the sole active direct caller found by whole-tree search. It skips unready jobs while assembling inputs, records their row boundaries, skips empty slices and passes one token-position slice at a time to receive_logits. receive_sample appends a token and increments each sequence's KV position, preserving the readiness relation during ordinary acceptance, including successive accepted draft tokens. [source; call_1e06442cd3c745d5a911a8e51efea1ed, call_b76530404aab498a9bbb14a66a397cf1, call_c3fce2b0a2994e278ca19e6a9e26e565]

Sequence initializes live=True; the generator-subtree search found no other live access beyond that initialization and the removed assertion. Thus this check does not track allocation or completion transitions in the inspected implementation. [source; call_61db455648db4d51a420dee3866696bf, call_3bbb941c70ce4ea3bd4670e4a88e1bc2]

A scalar check preserved readiness after incrementing both sequence length and KV position for lengths 1, 10 and 100. A separate transcription returned the ordinary four-item tuple with optional outputs disabled and raised UnboundLocalError for each enabled optional-output branch. [execution; call_72e1e9d3dedd44afac9f9883d184c8c1]

The optional-output defect recorded by the ancestor remains in the changed function: the task modifies only assertions, leaving the TODO/pass branches and their unassigned return variables intact. [source; call_c3fce2b0a2994e278ca19e6a9e26e565, call_fd491c65a15d45409c2d40ae272b840e]

## Authoring-time findings — pending review

### sampling-optional-output-carryover (suspected; defect)

Inherited optional probability/top-token output failure persists in receive_logits.

Trigger: A job reaches sampling with return_probs=True or return_top_tokens greater than zero.

Expected: Return the requested probability or top-token values alongside the sampled token.

Actual: Enabled branches execute pass and leave next_prob or next_k_tokens/next_k_probs unassigned, so tuple construction raises UnboundLocalError. The active Generator.iterate_gen caller unpacks this tuple without handling that failure locally.

Locations: 02982fcc9fed57a8e5b2bdf55cdceb12cc70f594:exllamav3/generator/job.py — Job.receive_logits

Source evidence: call_c3fce2b0a2994e278ca19e6a9e26e565, call_fd491c65a15d45409c2d40ae272b840e, call_1e06442cd3c745d5a911a8e51efea1ed, call_b76530404aab498a9bbb14a66a397cf1

source_inspection: Compared unchanged conditional assignments and tuple return with the active caller and assertion-only diff. [call_c3fce2b0a2994e278ca19e6a9e26e565, call_b76530404aab498a9bbb14a66a397cf1, call_fd491c65a15d45409c2d40ae272b840e]. Limits: No repository generation execution.

scalar_transcription: Reimplemented the optional conditional assignments using a scalar token; each enabled option raised UnboundLocalError. [call_72e1e9d3dedd44afac9f9883d184c8c1]. Limits: Tests Python control flow only, not the sampler or probability computation.

## Uncertainty and limits

No inference workload, GPU test or timing benchmark was run. The standard-library check models conditional assignments and integer state transitions, not repository tensor execution.

Whole-tree receive_logits search found one active direct caller and one commented-out threaded caller. No invalid-state route through the inspected active caller was established; external direct calls and custom model behavior remain unverified.
