# 3a7b4895e45b1eb2f291f8b09b0a5dac569e984c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3a7b4895e45b1eb2f291f8b09b0a5dac569e984c) · [Evidence ledger](draft.json)

Corrects DeciLM KV-head derivation from per-block group size, matching sampled Ultra and heterogeneous 51B checkpoint widths while leaving Super unchanged and existing compatibility barriers intact.

- [Correct DeciLM grouped-attention dimensions](#models)

## Problem

DeciLM passed n_heads_in_group directly as the KV-head count. The inspected Ultra checkpoints and several 51B blocks instead require the query-head count divided by that group size. [source; call_9d8ff4218c1c44fdb86d688bed96488b, call_1df8a8e4dde14a30902caf81e5eecd3d, call_5f998ee1239b4a0caca4560a33b67153, call_578d04f19a504cea85e636469c0c09f4, call_dad51f46f21b4e8a9bac91520333a050]

## Reasoning

The replacement interprets the configuration value as query heads per KV group: num_kv_heads = num_q_heads // n_heads_in_group. Attention then uses that count for K/V projection widths and activation reshaping; query and output projection dimensions remain unchanged. [source; call_9d8ff4218c1c44fdb86d688bed96488b, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9bb0cbfc0b5f4491b46b2309058290d1]

## Impact

The change resolves the inspected K/V declaration mismatches for both Ultra variants and the 51B blocks with group sizes 16, 32 and 64. Super-49B declarations do not change. This is a dimension correction, not evidence of successful end-to-end model execution. [inference; call_d7a148d1b8c545d78fb31f42d412a439, call_1df8a8e4dde14a30902caf81e5eecd3d, call_5f998ee1239b4a0caca4560a33b67153, call_578d04f19a504cea85e636469c0c09f4, call_dad51f46f21b4e8a9bac91520333a050, call_83410b00bd6948bc978acc40d18d542e]

## Source Notes

Commit 75c7366bb2e2a7671e38d079f9e5f54945b78006 introduced decilm.py and the direct n_heads_in_group assignment changed here. [source; call_cc953f21983e4266a8e8184329b664b3]

That ancestor entry reports the Ultra and 51B K/V mismatches, 51B's unsupported linear-replacement attention, and an empty-block conversion hazard in the Ultra configurations. [ancestor; call_61e3c88624cf4893aca23b12ef1f1b40]

Whole-parent-tree searches found the exact n_heads_in_group consumer only in decilm.py; a broader n_heads search also located the ordinary num_attention_heads configuration reads. [source; call_dd944e00a92545778b218d42f49b9c04, call_8e1a3b0d857e4d80a883ed96dcd88c70]

Issue 7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure while converting a Qwen-derived model, followed by the reporter's environment workaround. It does not report the DeciLM head-count mismatch. [source; call_30192b4cbc9a4b9b84d2c5338a79ba7b]

<a id="models"></a>

## Correct DeciLM grouped-attention dimensions

Only the active-attention constructor argument changes. no_op attention remains skipped, unsupported-feature assertions remain in place, and the global num_key_value_heads field is not substituted for the per-block group setting. This preserves heterogeneous per-layer grouping. [source; call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9d8ff4218c1c44fdb86d688bed96488b]

For hidden width H, query-head count Q and group size G, the old K/V output width is G × head_dim; the new width is (Q // G) × head_dim. All four inspected configurations omit head_dim, so the constructor fallback H // Q yields 128. The listed numeric group sizes divide Q exactly; integer floor division therefore loses no remainder in these cases. [execution; call_d7a148d1b8c545d78fb31f42d412a439, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_40be506146404ecd937a447eae20538b, call_3449c76642614e34abcf404b03e20209, call_8e861345018146a681d65978ae836fe5, call_7a79fb672e634c488fd6c46bc49b7f4e]

nvidia/Llama-3_1-Nemotron-51B-Instruct, revision 2e9bdbfa8e1ab73ce98f5960143cf927192d59e7: H=8192 and Q=64. For blocks 0, 1, 6 and 7, G is respectively 8, 16, 32 and 64. Their stored K and V weights have shapes [1024,8192], [512,8192], [256,8192] and [128,8192]. Old declarations have widths 1024, 2048, 4096 and 8192; new declarations have widths 1024, 512, 256 and 128. Thus block 0 is unchanged while the other three representative group sizes are corrected. The constructor still rejects the complete configuration at block 11 because attention replace_with_linear is true; this patch does not make 51B construct successfully under the existing assertions. [source; call_40be506146404ecd937a447eae20538b, call_1df8a8e4dde14a30902caf81e5eecd3d, call_5f998ee1239b4a0caca4560a33b67153, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9d8ff4218c1c44fdb86d688bed96488b]

nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1, revision 49dcb9457c714458d12c7c358889a3e8fc4f4904: H=16384, Q=128 and active attention uses G=16. Block 0's stored K and V weights are [1024,16384]. The parent declares 16 KV heads and width 2048; the patch declares 8 KV heads and width 1024. Its configuration satisfies the inspected DeciLM layer-count, activation and feature assertions before and after the patch. Fully disabled blocks, beginning at block 9, remain present. [source; call_a1caf2a643f64a15bcab6c979ceea969, call_3449c76642614e34abcf404b03e20209, call_578d04f19a504cea85e636469c0c09f4, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9d8ff4218c1c44fdb86d688bed96488b]

nvidia/Llama-3_1-Nemotron-Ultra-253B-v1, revision e155ab2c2de4c7656884e7bf63d3d2e4b266f993: its separately inspected configuration also has H=16384, Q=128 and G=16 for active attention. Shard 2 stores block 0's K and V weights as [1024,16384], matching the patched width 1024 rather than the parent's 2048. Its inspected DeciLM assertions accept the configuration before and after the change. It likewise retains fully disabled blocks beginning at block 9. [source; call_f45473cdeed8457e830b1409f04c58f8, call_8e861345018146a681d65978ae836fe5, call_dad51f46f21b4e8a9bac91520333a050, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9d8ff4218c1c44fdb86d688bed96488b]

nvidia/Llama-3_3-Nemotron-Super-49B-v1, revision 4605d825c59945d6f8a195826ae8ff3366653f83: H=8192, Q=64 and every active attention block uses G=8. Both expressions declare 8 KV heads and width 1024, matching block 0's stored K and V shapes [1024,8192]. This model's declarations are unchanged, and its configuration passes the inspected DeciLM assertions both before and after the patch. It has no fully disabled block. [source; call_7a79fb672e634c488fd6c46bc49b7f4e, call_83410b00bd6948bc978acc40d18d542e, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9d8ff4218c1c44fdb86d688bed96488b]

Attention consumes the count twice: Linear declarations use num_kv_heads × head_dim, and the inspected no-cache decode paths reshape K/V to [batch, sequence, num_kv_heads, head_dim]. Correcting the constructor aligns both declarations and reshape expectations with the sampled checkpoint widths, rather than merely changing a descriptive configuration field. [source; call_9bb0cbfc0b5f4491b46b2309058290d1, call_9d8ff4218c1c44fdb86d688bed96488b]

Source inspection of the parent plus the one-line task diff shows that the inherited Ultra empty-block conversion hazard is carried over, not removed. TransformerBlock omits None children, Module.weights_numel sums its children, and conversion still saves the empty tensor dictionary before dividing by the zero weight count. The group-count correction does not guard this path. [source; call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_50355117755042ad83bdcb8a11667f87, call_6ebae883ca4440a5831e98c629514081, call_d21f464365824fcaabe791e7f1887628, call_9d8ff4218c1c44fdb86d688bed96488b]

## Authoring-time findings — pending review

### remaining-51b-linear-attention-rejection (suspected; external_compatibility)

The head-count correction does not add support for 51B's linear-replacement attention.

Trigger: Construct the inspected Nemotron-51B configuration with assertions enabled and reach block 11.

Expected: Complete 51B compatibility would require implementing its linear-replacement attention blocks.

Actual: DeciLMModel.__init__ still raises the explicit replace_with_linear-not-supported assertion before evaluating that block's null group size. The direct generic constructor caller is Model.from_config; conversion reaches it through get_base_model. No claim is made that all other workflows were inspected.

Locations: 3a7b4895e45b1eb2f291f8b09b0a5dac569e984c:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_40be506146404ecd937a447eae20538b, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_9d8ff4218c1c44fdb86d688bed96488b, call_ca306687e6bd4a8486d5c9f20ea5b3d2, call_c54e7c4c778245038a1125e71b900380, call_fa3bb371f07a483e8e6addb1ac096b64, call_d21f464365824fcaabe791e7f1887628

source_inspection: Compared the configuration's block 11 attention flags with the unchanged assertion and inspected generic construction and conversion call sites. [call_40be506146404ecd937a447eae20538b, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_fa3bb371f07a483e8e6addb1ac096b64, call_d21f464365824fcaabe791e7f1887628]. Limits: Constructor and checkpoint loading were not executed.

### carried-over-empty-block-bitrate (suspected; defect)

Both inspected Ultra configurations retain zero-weight blocks that encounter unguarded bitrate reporting during conversion.

Trigger: Conversion reaches a fully disabled Ultra block, first at block 9, and serialization of its empty tensor dictionary returns normally.

Expected: Skip weight-based bitrate division or explicitly handle a zero-weight module.

Actual: convert_model.main divides num_bits by module.weights_numel(), whose empty-child sum is zero. The inspected direct CLI caller is convert.py; earlier setup or loading failures may prevent reaching this path.

Locations: 3a7b4895e45b1eb2f291f8b09b0a5dac569e984c:exllamav3/conversion/convert_model.py — main

Source evidence: call_a1caf2a643f64a15bcab6c979ceea969, call_f45473cdeed8457e830b1409f04c58f8, call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_50355117755042ad83bdcb8a11667f87, call_6ebae883ca4440a5831e98c629514081, call_d21f464365824fcaabe791e7f1887628, call_46e9cfdcf82b45f8a970de9f589bde40, call_425181baec2c4d90ad6099123e9aa23b, call_9d8ff4218c1c44fdb86d688bed96488b

source_inspection: Traced disabled branch construction through submodule registration and weight counting to the unchanged converter division and CLI caller. [call_b5b4f4db07b84bacb5d9db32d34ddcfa, call_50355117755042ad83bdcb8a11667f87, call_6ebae883ca4440a5831e98c629514081, call_d21f464365824fcaabe791e7f1887628, call_425181baec2c4d90ad6099123e9aa23b]. Limits: Serialization and conversion were not executed.

scalar_transcription: Evaluated 0 / sum([]); the modeled empty-module bitrate expression raised ZeroDivisionError. [call_d7a148d1b8c545d78fb31f42d412a439]. Limits: Standard-library scalar check, not execution of the repository converter.

## Uncertainty and limits

No checkpoint loading, conversion, attention execution or GPU test was performed. The successful Python run transcribed integer dimension arithmetic and an empty-denominator expression only.

Header comparisons cover representative active blocks, including all four numeric group sizes in 51B, rather than every checkpoint tensor.

Passing the inspected DeciLM configuration assertions does not establish complete runtime compatibility. Empty-dictionary safetensors serialization behavior was not executed.
