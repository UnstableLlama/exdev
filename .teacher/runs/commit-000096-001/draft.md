# a2ae48308aa813c67058c01f21bd4ab656a21d7a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a2ae48308aa813c67058c01f21bd4ab656a21d7a) · [Evidence ledger](draft.json)

Adds an exported shared-normalization parallel decoder block, without architecture wiring, while retaining optional-component and plain-MLP allocation inconsistencies.

- [Shared-input parallel decoder composition](#modules)

## Problem

The existing TransformerBlock feeds its attention-updated residual into the MLP path. This change adds a separate block whose attention and MLP consume the same normalized input. [source; call_f7a80d59c1b44575af1b82a205af8a0b, call_cfee53ee09e24b2a90dac2c78294bd03]

## Reasoning

Keeping ParallelDecoderBlock separate preserves the sequential block's computation while offering shared-input branch composition. “Parallel” describes data dependencies here: the Python implementation calls attention and then MLP, without introducing concurrent scheduling. [source; call_cfee53ee09e24b2a90dac2c78294bd03]

## Impact

ParallelDecoderBlock becomes importable from exllamav3.modules. The diff adds no architecture registration or model construction site; it also broadens TransformerBlock.mlp_norm's annotation to include LayerNorm without changing that block's forward implementation. [source; call_dfdb107e8cbb411197c23b61169ec1f1, call_cfee53ee09e24b2a90dac2c78294bd03]

## Source Notes

The immediate ancestor entry describes the preceding addition of the exported LayerNorm component, without model-constructor integration. [ancestor; call_9032c1ab477e4f21be2d09cac68d0b74]

The inspected discussions report “quantizing model: undefined symbol: __cxa_call_terminate,” “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022.” Their framing is extension loading, quantization quality, and compilation respectively; none identifies this parallel decoder addition as a remedy. [source; call_5825b6b521544247b37f5b91bf664491, call_caba4a8aacb94c4e98d9bb29b25a511f, call_5413d9db0690498082cf86aa31d90bfc]

<a id="modules"></a>

## Shared-input parallel decoder composition

forward computes y = input_norm(x), requesting torch.half, then adds Attention(y) and MLP(y) into x in place. The MLP receives y rather than the attention-updated residual. There are no separate branch normalizers or post-normalizers in the new block. [source; call_cfee53ee09e24b2a90dac2c78294bd03]

A scalar transcription with x=5, N(x)=2x, A(y)=y+1 and M(y)=3y returned 46, matching x+A(N(x))+M(N(x)); feeding the attention-updated residual through normalization into the MLP instead produced 112. The prefill transcription returned 16 after only the attention residual addition. [execution; call_efe1c5a0acea43e5afad5094fc68d9be]

A truthy params['prefill'] skips the MLP and final dtype conversion, but only after adding attention's output. Model.prefill sets this flag only at the last cache-affecting module and then stops, rather than setting it throughout prompt ingestion. The old TransformerBlock returns before its attention residual addition. [source; call_cfee53ee09e24b2a90dac2c78294bd03, call_497c35cb9a05405c92afb4411f88bbee, call_f7a80d59c1b44575af1b82a205af8a0b, call_331136b896c14809b798f39bddbf2634]

On the ordinary return path, to2 gives the forward-call dtype precedence over the constructor dtype, leaving x unchanged when neither is supplied. [source; call_cfee53ee09e24b2a90dac2c78294bd03, call_0c0848b514514b33b39b5f929a626444]

Registering the normalizer, attention and MLP connects them to Module's recursive traversal, loading, unloading and weight counting. num_slices is copied from the MLP, or defaults to one. The block-level qmap argument is not forwarded: the base constructor receives None. [source; call_cfee53ee09e24b2a90dac2c78294bd03, call_3a217a7de7df48c0902c82b567c4004a]

allocate_q follows TransformerBlock's allocation interface: it forwards the selected bit budget, surplus, attention projections and MLP projection collections to allocate_transformer. Conversion calls allocate_q for each model module before loading and calibration. This is reuse of existing allocation machinery, not a new quantization algorithm. [source; call_cfee53ee09e24b2a90dac2c78294bd03, call_7a4e377c6b7545ee86df1755ec1655ce, call_f711a909152143bdad05578ecf833786]

## Authoring-time findings — pending review

### optional-components-forward (suspected; defect)

The constructor permits omitted components, but forward unconditionally dereferences them; even a block named '(no-op)' cannot execute as an identity.

Trigger: Construct ParallelDecoderBlock with input_norm=None, or omit attention or the MLP and reach its corresponding forward call.

Expected: Either reject missing required components during construction or implement the advertised optional/no-op composition.

Actual: forward calls .forward on None. With all defaults, failure occurs at self.input_norm.forward before any residual computation.

Locations: a2ae48308aa813c67058c01f21bd4ab656a21d7a:exllamav3/modules/transformer.py — ParallelDecoderBlock.forward

Source evidence: call_cfee53ee09e24b2a90dac2c78294bd03, call_7907d74910504b0d9a97c23f42fe340b, call_497c35cb9a05405c92afb4411f88bbee

source_inspection: Compared optional constructor defaults and get_name's no-op label with unconditional forward calls. Whole-parent-tree search found no named users; Model.forward and Model.prefill are generic dispatch sites only if this block is installed. [call_cfee53ee09e24b2a90dac2c78294bd03, call_7907d74910504b0d9a97c23f42fe340b, call_497c35cb9a05405c92afb4411f88bbee]. Limits: No concrete integrated model or runtime failure was tested.

### plain-mlp-allocation (suspected; defect)

The new block copies an existing allocation mismatch for the explicitly accepted plain MLP type.

Trigger: Call ParallelDecoderBlock.allocate_q with a plain MLP and a valid quantization budget.

Expected: Allocate bits for the plain MLP's up and down projections.

Actual: Argument evaluation accesses self.mlp.ups and self.mlp.downs, whereas MLP defines singular up and down attributes, so allocation cannot reach allocate_transformer successfully.

Locations: a2ae48308aa813c67058c01f21bd4ab656a21d7a:exllamav3/modules/transformer.py — ParallelDecoderBlock.allocate_q

Source evidence: call_cfee53ee09e24b2a90dac2c78294bd03, call_bb8bc2d4f71446d384d4d4fa4fe1e127, call_f7a80d59c1b44575af1b82a205af8a0b

source_inspection: Compared MLP attributes with both block allocators. Whole-parent-tree caller search located conversion's generic module.allocate_q call, which runs before calibration; no named ParallelDecoderBlock construction was found. GatedMLP does define the plural collections and is outside this trigger. [call_bb8bc2d4f71446d384d4d4fa4fe1e127, call_724b0150170a471993c7c914f28cc1ca, call_f711a909152143bdad05578ecf833786, call_7907d74910504b0d9a97c23f42fe340b]. Limits: Source-level conditional reach only; conversion was not executed.

## Uncertainty and limits

No repository implementation, PyTorch operation, GPU kernel, or model integration test was executed.

The scalar check models branch dependencies with integer arithmetic and artificial functions; it does not establish tensor aliasing, half-precision rounding, numerical accuracy, or performance.

Whole-parent-tree searches found no named ParallelDecoderBlock callers; external or dynamically assembled consumers are not established.
