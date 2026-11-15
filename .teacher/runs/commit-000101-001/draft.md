# cf15bab0733bfecf327281987286b413299d353d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cf15bab0733bfecf327281987286b413299d353d) · [Evidence ledger](draft.json)

Adds Marlin GPTQ storage accounting to the Transformers comparison adapter and requests one GiB of reserved VRAM during ExLlamaV2 autosplit loading.

- [GPTQ storage accounting in quantization comparisons](#usage-evaluation)

## Problem

The Transformers comparison adapter lacked explicit storage accounting for GPTQModel's MarlinQuantLinear modules. [source; call_c228ab6237724b8180ef82ff54c58283, call_068e61f9ed5045348880d931ffeefa6a]

## Reasoning

The change extends the existing Transformers adapter rather than adding a GPTQ-specific loader or forward path. This lets recognized Marlin modules contribute to the comparison's existing storage metrics. [source; call_068e61f9ed5045348880d931ffeefa6a, call_c228ab6237724b8180ef82ff54c58283, call_6a5b08c876a24229b2e5d1ffeb1f2f1d]

## Impact

The new GPTQModel import is unconditional. Because compare_q.py imports the Transformers adapter before backend selection, that comparison entry point now requires the imported Marlin module to be available even when selecting another backend. [source; call_068e61f9ed5045348880d931ffeefa6a, call_c9924525f37f4a70a2b2d416f311ca19, call_6a5b08c876a24229b2e5d1ffeb1f2f1d]

## Source Notes

The earlier evaluation entry characterizes the plotted VRAM metric as calculated weight storage rather than measured peak allocation; the inspected comparison runner retains that distinction. [ancestor; call_3c324e2c753143168eff3529c0876301]

The reviewed discussions report separate problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns low-bitrate quantization; #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” concerns compilation. None supplies an explicit connection to this adapter change. [source; call_25386cc3fad142cc887ee190037f7634, call_52572eceec4c491da5fb400299ca8489, call_f3bcf23b0825490584a57a04b1a35fd9]

<a id="usage-evaluation"></a>

## GPTQ storage accounting in quantization comparisons

get_storage_info adds a MarlinQuantLinear branch that sums g_idx, g_idx_sort_indices, qweight, qzeros and scales. get_tensors_size ignores None values and computes eight times element size in bytes times element count. The denominator is the logical dense weight count, in_features × out_features, so metadata contributes to effective bits per weight. [source; call_068e61f9ed5045348880d931ffeefa6a, call_c228ab6237724b8180ef82ff54c58283]

The new branch contributes to the layer aggregate without a separate head-identification check. Existing ordinary Linear and Linear4bit branches retain their out_features >= 0.9 × vocab_size head heuristic. The returned storage total remains head_numel × head_bpw + sum_bits, not a scan of all runtime allocations. [source; call_068e61f9ed5045348880d931ffeefa6a, call_c228ab6237724b8180ef82ff54c58283]

load_transformers still delegates loading to AutoModelForCausalLM.from_pretrained with half precision and either cuda:0 or automatic device placement. The comparison runner consumes its layer BPW, head BPW and storage-bit results, converts storage to GiB, and evaluates logits through the unchanged forward adapter. [source; call_c228ab6237724b8180ef82ff54c58283, call_6a5b08c876a24229b2e5d1ffeb1f2f1d, call_068e61f9ed5045348880d931ffeefa6a]

The ExLlamaV2 adapter additionally passes reserve_vram=1024**3 to load_autosplit. Its batch-one, 2048-token loading cache and subsequent storage-accounting call are unchanged. Reserving evaluation headroom is a plausible motivation, but the diff does not establish the author's rationale. [inference; call_96a19df5d9b745429cb00a0424c1cb10, call_910fbb2c30e34d90a8f1619d15a39380]

An isolated execution of the repository's get_tensors_size helper with synthetic tensor-like objects returned 41,984 bits and 5.125 BPW for 8,192 logical weights, including two index arrays and scales while skipping absent qzeros. Python also evaluated 1024**3 as 1,073,741,824 bytes, or one GiB. This validates helper arithmetic, not a real Marlin layout or GPU behavior. [execution; call_179646b846b04001adc3f7208a4068e4]

## Uncertainty and limits

No model loading, GPTQ inference, GPU allocation measurement or perplexity evaluation was run.

GPTQModel class inheritance, supported versions and actual tensor layouts were not inspected; accounting applies to modules that reach the new MarlinQuantLinear branch, not necessarily every GPTQ backend.

The external ExLlamaV2 autosplit implementation was not available in the inspected source; acceptance and allocation semantics of reserve_vram remain unverified.
