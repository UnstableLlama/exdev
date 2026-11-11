# 89f6401d65d965d22fbd6d3fece1f5bb8ba8598a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/89f6401d65d965d22fbd6d3fece1f5bb8ba8598a) · [Evidence ledger](draft.json)

Makes transformer branches optional in execution and quantization allocation, including ungated MLP allocation; missing input norms and direct empty-block allocation remain problematic.

- [Optional transformer branches and matching bit allocation](#modules)

## Problem

TransformerBlock already accepted optional attention and MLP components, but forward and quantization allocation dereferenced them unconditionally. Allocation also required a gate projection even for a plain MLP. [source; call_4b791a7220f84054b2f27db54e33d527, call_f70a22a190ff40d8a1dc18d497b25a5c]

## Reasoning

The change makes execution and allocation conditional on component presence rather than requiring placeholder branches. [source; call_1ab62abc29cd4c91b505476d6c20b2ec, call_24ead96064ce465d80f4087bcf9ff4ee]

## Impact

Attention-only, gated-MLP-only and ungated-MLP allocations now have dedicated candidate sets. The inspected Llama, Gemma and Phi3 builders still supply both branches and both input norms. [source; call_24ead96064ce465d80f4087bcf9ff4ee, call_63bb7551b28442cda050e9772ed294d4, call_4d1079873d2f4f4cbf793e962cbedbf0, call_ea824577137d478d8e03a249037ae5bf]

<a id="modules"></a>

## Optional transformer branches and matching bit allocation

forward now skips absent branches, retaining optional post-normalization and residual addition for present ones. The prefill early return remains inside attention processing; without attention, execution proceeds to the MLP and final dtype conversion. [source; call_1ab62abc29cd4c91b505476d6c20b2ec]

allocate_q passes None for absent projections. allocate_transformer builds matching key and weight-count lists for q/k/v/o, gate/up/down, or ungated up/down. Attention requires all four projections; either MLP form requires down. [source; call_1ab62abc29cd4c91b505476d6c20b2ec, call_24ead96064ce465d80f4087bcf9ff4ee]

The allocator retains budget = int(bpw × weight_count) + surplus_bits + 1, a base width floored with minimum one, and candidate widths capped at eight. It combines branch candidates only when both branches exist, scores them by weighted bit cost, and returns projection widths plus remaining budget. The extra one bit lets integral costs equal to the nominal budget pass the existing tuple-based strict budget selection. [source; call_f70a22a190ff40d8a1dc18d497b25a5c, call_24ead96064ce465d80f4087bcf9ff4ee]

A standard-library transcription counted six attention, four gated-MLP and three ungated-MLP candidates, yielding 24 or 18 combined candidates. With 100 weights per projection, four requested bits and zero incoming surplus, every tested form selected four bits per projection and returned one surplus bit. [execution; call_e38553c3094748308d2a7f70387cc3e5]

Conversion consumes the returned strategy as each linear's K and carries surplus into later allocation. It calls allocate_q only when quantizable linears exist, so an entirely empty block does not reach allocation through this inspected call site. [source; call_93e9ecb4027a4455b704fd720af03cf6]

## Authoring-time findings — pending review

### missing-norm-input (suspected; defect)

The new optional input-normalization guards do not initialize the branch input when a norm is absent.

Trigger: Run a present attention branch without attn_norm, or a present MLP without mlp_norm.

Expected: A branch without input normalization should receive the current residual state x.

Actual: Attention without its norm reads unassigned y. An MLP without its norm likewise reads unassigned y when attention is absent, or reuses the attention branch output rather than the updated residual state when attention ran.

Locations: 89f6401d65d965d22fbd6d3fece1f5bb8ba8598a:exllamav3/modules/transformer.py — TransformerBlock.forward

Source evidence: call_1ab62abc29cd4c91b505476d6c20b2ec, call_4b791a7220f84054b2f27db54e33d527

source_inspection: Traced assignments to y and searched parent callers across the tree. Model.forward and conversion dispatch module.forward directly. The three located model builders supply both norms, so the problematic configuration is not established for those builders. [call_c0325fbcf34040849e2166242be853b0, call_f5281ad37ca8419f8a2196879aa2b22a, call_93e9ecb4027a4455b704fd720af03cf6, call_f26d6ed18a284a26a53fb81d8484f59a, call_63bb7551b28442cda050e9772ed294d4, call_4d1079873d2f4f4cbf793e962cbedbf0, call_ea824577137d478d8e03a249037ae5bf]. Limits: Source reasoning only; external or dynamically constructed blocks were not examined.

### empty-block-allocation (suspected; defect)

Allocation cannot handle a block with neither branch.

Trigger: Call TransformerBlock.allocate_q with both attn and mlp absent.

Expected: Return an empty strategy or explicitly reject the empty allocation before budget division.

Actual: The projection list is empty, so budget / numel divides by zero before the later 'Logic error' assertion.

Locations: 89f6401d65d965d22fbd6d3fece1f5bb8ba8598a:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_24ead96064ce465d80f4087bcf9ff4ee, call_1ab62abc29cd4c91b505476d6c20b2ec

source_inspection: Whole-parent searches located TransformerBlock.allocate_q as the allocator's caller and conversion as the allocate_q consumer. Conversion guards allocation with if linears, limiting this observation to direct calls or other callers not established by the search. [call_2b5893600d6243169163b5d79e71e2ed, call_ac861bd6905e455a9d56358f80f822e3, call_93e9ecb4027a4455b704fd720af03cf6]. Limits: No repository execution of the empty-block case.

## Uncertainty and limits

No tensor inference or GPU quantization was executed. The scalar check models allocation arithmetic only.

The source establishes the allocation ceiling of eight bits but does not explain the empirical rationale for the candidate offset patterns.
