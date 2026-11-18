# 42afcd7e6cd361b2be9aef1072f26ffccffb92db


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/42afcd7e6cd361b2be9aef1072f26ffccffb92db) · [Evidence ledger](draft.json)

Adds Gemma3ForCausalLM dispatch using root-level configuration and prefixless checkpoint keys while reusing the existing Gemma3 decoder and preserving conditional-generation defaults.

- [Language-only Gemma3 dispatch and checkpoint adaptation](#models)

## Problem

The registry supported Gemma3ForConditionalGeneration, but not Gemma3ForCausalLM. The existing adapter also expected nested text_config fields and language_model-prefixed tensors, unlike the inspected language-only checkpoints. [source; call_7a2174ba1d9c4e7fa61caf1c5c85f321, call_cfebea1ec8544a56bbbcbf1d8342781c, call_8f5b5c49092543b1803f479af9800d44, call_75b503de9ddb467d8fc5c1824482a4e3]

## Reasoning

Registration, top-level configuration parsing and tensor-prefix selection are complementary changes: dispatch selects Gemma3TextConfig, its text component selects Gemma3TextModel, and that subclass invokes the shared decoder with an empty prefix. [source; call_dcff204ce77a43a8a79a5d52867d3353, call_14f0036be3254fb8af61812023cdceb8, call_13fe06402f19430c94bf393e6dc5267a, call_08d9a075c0144144aa61208b21107340]

Sharing decoder assembly avoids duplicating Gemma3's normalization and local/global attention rules, while retaining separate adapters for the two checkpoint schemas. The tradeoff is duplicated configuration parsing and fallback values. [inference; call_cfebea1ec8544a56bbbcbf1d8342781c, call_14f0036be3254fb8af61812023cdceb8]

## Impact

Directory-based configuration dispatch can now recognize Gemma3ForCausalLM and construct its text decoder. Existing conditional-generation construction retains the default language_model. prefix; vision remains an unchanged stub, not newly implemented multimodal inference. [source; call_dcff204ce77a43a8a79a5d52867d3353, call_14f0036be3254fb8af61812023cdceb8, call_13fe06402f19430c94bf393e6dc5267a, call_cfebea1ec8544a56bbbcbf1d8342781c]

## Source Notes

The earlier Gemma3 entry was read. It establishes the adapter's introduction, separate local/global RoPE settings and explicit vision limitation; it records no defect finding. [ancestor; call_b081df3ed02b4500823c1e8834d1c115]

In PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” gakada separately reports that language-only gemma-3-1b cannot run with Gemma3ForCausalLM. Its relationship to this task is inferred from that exact architecture identifier and the missing parent registry entry, not an explicit upstream link. The supplied task author is turboderp, not the reporter. [inference; call_c9b6147ae7a04bf3b32587ef23d0a777, call_7a2174ba1d9c4e7fa61caf1c5c85f321, call_dcff204ce77a43a8a79a5d52867d3353]

Other inspected discussion openings concern different subjects: PR #4, “chore: update config.py,” corrects spelling; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading; issue #33, “Error converting model,” reports a file-opening failure; issues #34 and #42 report quantization/factorization failures; PR #26, “Superior 3INST parameters,” proposes decoder multipliers. Their relevance here is only inferred from shared inspected source paths, not evidence that this adapter change resolves those reports. [inference; call_19758f5ce9ae4a3197a993ccaa9c8dd2, call_22c1438944e04373a6ad0b9bc4b3272a, call_9803bb779b0e41dd8f6455e72d100fd0, call_a51855109cae41ae9ddea6531edc1f7b, call_21ac915a172d464db61b82054a67d447, call_7046b3bf4c554f579775bbc4fa27e331]

<a id="models"></a>

## Language-only Gemma3 dispatch and checkpoint adaptation

ARCHITECTURES derives identifiers from each model's config_class.arch_string. Adding Gemma3TextModel therefore exposes Gemma3ForCausalLM to Config.from_directory. Gemma3TextConfig supplies only a text component, which agrees with Model.from_config's default component and component-membership assertion. [source; call_7a2174ba1d9c4e7fa61caf1c5c85f321, call_dcff204ce77a43a8a79a5d52867d3353, call_14f0036be3254fb8af61812023cdceb8, call_13fe06402f19430c94bf393e6dc5267a, call_08d9a075c0144144aa61208b21107340]

Gemma3TextConfig reads decoder fields at the JSON root instead of under text_config. It requires num_hidden_layers; defaults include head_dim 256, hidden/intermediate widths 2304/9216, query/KV heads 8/4, query scalar 256, window 4096, period 6 and RMS epsilon 1e-6. Vocabulary fallback is 262208 only when the base configuration found no vocabulary. read_dict treats null as absent, so null softcaps select 0.0. [source; call_14f0036be3254fb8af61812023cdceb8, call_13fe06402f19430c94bf393e6dc5267a, call_7bfa5648bf0e41db9a08dd7278b1275e]

The shared constructor now prepends key_prefix to embedding, block, attention, MLP, normalization, output-head and alternative embedding keys. Its default reproduces every previous language_model.-prefixed key; Gemma3TextModel supplies ''. The whole-parent Gemma3 search found no other subclass or direct named constructor call requiring migration. The generic factory still passes config and keyword arguments without inserting a prefix. [source; call_14f0036be3254fb8af61812023cdceb8, call_cfebea1ec8544a56bbbcbf1d8342781c, call_4c7b9c48928d4105a11783ed46fc4dfe, call_8a6907267fa7484299b5c386d2f7c440, call_08d9a075c0144144aa61208b21107340]

Decoder computation is otherwise inherited: normalized embeddings, attention with Q/K RMSNorm, pre/post-normalized attention and GELU-gated MLP branches, final RMSNorm and vocabulary projection. Embedding normalization multiplies by sqrt(hidden width); RMSNorm constant_bias=1 applies weight+1. The output projection retains an unconditional alternative embedding key rather than consulting tie_word_embeddings. [source; call_cfebea1ec8544a56bbbcbf1d8342781c, call_14f0036be3254fb8af61812023cdceb8, call_e2837f5bc6894399bdd7cf419643ac3b, call_02c9e9a6f9f740d395a08840797755ff, call_e16de7c537ac44789f7414f8da847f42, call_cfa9ff07fe3344d5ba853e3fa6902aa2]

The new global RoPE call uses the helper's existing top-level-dictionary default with NEOX layout and theta fallback 1,000,000. Local RoPE explicitly reads {}, fixing theta at 10,000 and bypassing checkpoint scaling. Existing Gemma3 calls already use separate global/local dictionaries; the inspected other helper callers use its ordinary top-level default, without additional call-site guards omitted here. [source; call_14f0036be3254fb8af61812023cdceb8, call_13fe06402f19430c94bf393e6dc5267a, call_e374d23fba12410fb36cdda223fa40e5, call_a6d68a41207d415292a76d708ff03e3c]

google/gemma-3-1b-it, google/gemma-3-1b-pt, google/gemma-3-1b-it-qat-int4-unquantized and google/gemma-3-1b-it-qat-q4_0-unquantized each match the new root-level mapping: widths 1152/6912, 26 layers, 4/1 query/KV heads, head dimension and query scalar 256, window 512, period 6 and vocabulary 262144. Each overrides the width, head-count, window and vocabulary fallbacks; each supplies theta 1,000,000, local frequency 10,000 and null RoPE scaling/softcaps. None supplies tie_word_embeddings, leaving its stored default True. [source; call_8f5b5c49092543b1803f479af9800d44, call_84becef8b1bf404ebb9d6f635e8c7ecd, call_3d6043d3c944483da55ebef269fc6e27, call_e58d7561257044bd945be8749906dc95, call_14f0036be3254fb8af61812023cdceb8]

google/medgemma-27b-text-it also matches the new architecture and root-level mapping, but supplies widths 5376/21504, 62 layers, 32/16 heads, head dimension 128, query scalar 168 and window 1024. Its vocabulary is 262144 and period is 6. Its linear RoPE factor 8 reaches global settings, while the local empty dictionary excludes it; its explicit local frequency agrees with the fixed 10,000. Null softcaps and omitted tying select the same defaults as the 1B configurations. [source; call_43166014752d47f1b863040dd4bd54c1, call_14f0036be3254fb8af61812023cdceb8, call_13fe06402f19430c94bf393e6dc5267a, call_7bfa5648bf0e41db9a08dd7278b1275e]

The complete gemma-3-1b-it header matches the prefixless requests across layers 0–25: model.embed_tokens.weight [262144,1152], model.norm.weight [1152], four block norms [1152], Q/K norms [256], q_proj [1024,1152], k_proj/v_proj [256,1152], o_proj [1152,1024], up_proj/gate_proj [6912,1152] and down_proj [1152,6912]. lm_head.weight is absent, so Linear.load reaches model.embed_tokens.weight as its alternative. Optional biases and weight_scale_inv are absent, leaving no bias or FP8 scaling. The header contains no extra stored tensors outside these decoder requests. [source; call_75b503de9ddb467d8fc5c1824482a4e3, call_cfa9ff07fe3344d5ba853e3fa6902aa2, call_14f0036be3254fb8af61812023cdceb8, call_02c9e9a6f9f740d395a08840797755ff, call_e2837f5bc6894399bdd7cf419643ac3b]

All eleven medgemma-27b-text-it shard headers likewise contain the prefixless decoder requests for layers 0–61: embedding [262144,5376], final and block norms [5376], Q/K norms [128], Q [4096,5376], K/V [2048,5376], O [5376,4096], up/gate [21504,5376] and down [5376,21504]. There is no lm_head.weight, bias, weight_scale_inv or EXL3 tensor group; the embedding alternative supplies the dense head. No stored tensors fall outside the requested decoder families. Dense Linear loading requests transposition of these stored [output,input] matrices. [source; call_659b715dba1446fc8b7e0fdc3736a2ec, call_1f83cf0e2a7249559163df290f546b74, call_4ae29e13133640edaeb5f4b5a729df67, call_ef9c1d53cdc44376a5d81100142838e5, call_d757c4713689443daa2df0d9841397da, call_d795bd6bbbf64173bbe838a57d3decdb, call_e754998cca55430db7d742a2f77d6341, call_138e7b6c75e84dd2ac118a21e1c27d6a, call_f7916523a04d40ebb611763294cbce1b, call_e4e09b28ffdf46189d77c62316b68578, call_18f42f652432425995c0c07b804d77e6, call_cfa9ff07fe3344d5ba853e3fa6902aa2]

A bounded scalar transcription of bool((idx+1)%6) produced 22 local/4 global layers for the 26-layer configurations and 52 local/10 global layers for MedGemma. The query-scalar expression gives 0.0625 for 256 and approximately 0.077151675 for 168. Shape arithmetic produced the Q/K/O and MLP dimensions found in the reference headers. [execution; call_a6d68a41207d415292a76d708ff03e3c]

The component dictionary remains compatible with compilation's iteration over model classes for additional tensors. The text-only adapter does not register Gemma3VisionModel; the conditional-generation adapter still registers it, and its load/unload NotImplementedError methods and additional vision-tensor hook remain unchanged. [source; call_d2bde086000048feb3e9ddab2c6eefc7, call_f3eb0c7bb119418fbb256e56cd60f20d, call_cfebea1ec8544a56bbbcbf1d8342781c, call_14f0036be3254fb8af61812023cdceb8]

## Uncertainty and limits

No repository model construction, checkpoint loading, conversion, generation or GPU kernel execution was performed. Header agreement establishes names and shapes, not numerical correctness.

The Python computation transcribed scheduling and shape arithmetic using ordinary CPU integers and double-precision floats; it did not execute the decoder or reproduce half-precision kernel arithmetic.

Checkpoint evidence consists of hash-verified historical mirror files. Tensor headers were inspected for gemma-3-1b-it and medgemma-27b-text-it, not separately for all three other 1B variants.
