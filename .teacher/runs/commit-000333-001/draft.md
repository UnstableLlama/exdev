# 0460dda4e410e1311c8474b1c1e980b6cbbba152


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0460dda4e410e1311c8474b1c1e980b6cbbba152) · [Evidence ledger](draft.json)

Adds `-tp` / `--tensor_parallel` to shared model initialization and forwards it to the loader. The default load path is unchanged; opting in reaches an existing `NotImplementedError`, not tensor-parallel loading.

- [Wire the tensor-parallel flag to the existing loader switch](#model-init)

## Problem

The shared model CLI had only a commented-out tensor-parallel option. The loader already accepted a `tensor_p` argument, but the branch for `tensor_p=True` was a stub. The patch exposes that argument without implementing the branch. [source; call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_68e46cf6d9204d908678840f260f563d, call_93b80a74be594dd8887a185cefcb2f5f]

## Reasoning

`add_args` registers `-tp` and `--tensor_parallel` as aliases for a boolean switch, outside the optional cache arguments. This supplies the `args.tensor_parallel` attribute that `init` now reads unconditionally when calling `model.load`. The two edits depend on one another: registration alone would not change loading, and forwarding alone would leave callers using the shared parser without the new attribute. [source; call_68e46cf6d9204d908678840f260f563d, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_f7920cf859784111b3b43d71bbcdc63d]

The narrow change is consistent with turboderp's subject, “TP: model_init args”: it connects the shared parser to the existing loader API rather than adding a second loading implementation. The diff and discussions do not establish why the flag was exposed while that API branch still raised. [inference; call_68e46cf6d9204d908678840f260f563d, call_93b80a74be594dd8887a185cefcb2f5f]

## Impact

On CLI paths that use both helper functions, omitting the flag supplies `False` and preserves the ordinary load selection. Passing either alias supplies `True`; without an explicit device, `Model.load_gen` raises `NotImplementedError` before loading any module. With an explicit device and otherwise valid arguments, the single-device branch rejects `tensor_p=True`. No branch implements the help text's promise to attempt to respect `--gpu_split` in tensor-parallel mode. [source; call_68e46cf6d9204d908678840f260f563d, call_93b80a74be594dd8887a185cefcb2f5f, call_f7920cf859784111b3b43d71bbcdc63d]

The inspected CLI entry points that both register and consume the option are `eval/humaneval.py`, `eval/longctx.py`, `eval/mmlu.py`, `eval/ppl.py`, `examples/batched_translation.py`, `examples/chat.py`, and `examples/imgsearch.py`. PPL and imgsearch register it even with cache options disabled. PPL forwards sizing options but no `tensor_p` override. Imgsearch's later vision-component load is a separate call and receives no flag. `eval/ppl_transformers.py` accepts the option through the shared parser but does not consume it: it calls Transformers with `device_map="auto"`. `eval/compare_q_logits.py` and `eval/prequant_test.py` only import the helper in the inspected references. [source; call_443262e0babc4281af82e505b0d62e18, call_d78a02ad25c94ccfb5124b9c6ba783d7, call_8403d889a8ce49319fef527213d27b03, call_68e46cf6d9204d908678840f260f563d]

Programmatic calls to `model_init.init` have two new failure modes at the load call: a namespace built without `tensor_parallel` fails attribute access, and a caller still forwarding `tensor_p` through `**kwargs` supplies the keyword twice. No inspected in-tree caller uses either old form. Direct calls to `Model.load` or `Model.load_gen` are not subject to the new namespace requirement or duplicate keyword. [source; call_68e46cf6d9204d908678840f260f563d, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_443262e0babc4281af82e505b0d62e18, call_af7e0461214143d99707a1e53ff5e5b3, call_d78a02ad25c94ccfb5124b9c6ba783d7, call_f7920cf859784111b3b43d71bbcdc63d]

## Source Notes

The root entry's `models` chapter describes the original shared initialization order and explicitly identifies tensor-parallel loading as unimplemented. The later YAML-override entry describes the variant tensor collection and records missing metrics APIs and the deferred CUDA BF16 odd-tail issue. [ancestor; call_2cde6f477a6a454f8913a9a08be6e310, call_8db0067106804ea4803d67a2bb2e1c8f]

Comparing the complete patch with the parent source shows that it leaves the override wrapper, metrics block, and ordinary deferred-load path unchanged. The separate `Model.get_load_metrics()` wrapper also still calls `stc.get_metrics()`, for which the parent search found no definition. The search for callers of that wrapper found only its definition; it is not the call used by `--load_metrics`. [source; call_68e46cf6d9204d908678840f260f563d, call_a9c6c68f8c2f45109eac12524108c635, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_93b80a74be594dd8887a185cefcb2f5f, call_efedbbc0b64f4a92a76746275468b978, call_f0b8e0f922bd45ffa4deea794144e03f]

Issue #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM',” quotes the exact pre-change `model.load` call and traces into `_load_autosplit`. The reporter said that changing the CUDA allocator backend worked. The matching call and error connect it to the existing split path, not to the new flag or to a fix by this patch. Its `-tps` was chat's throughput-display option, not `-tp`. [inference; call_13ac838a981a41cba2ef133cc6c988c1, call_68e46cf6d9204d908678840f260f563d, call_d78a02ad25c94ccfb5124b9c6ba783d7, call_93b80a74be594dd8887a185cefcb2f5f]

PR #22, “OpenAI compatible API example,” proposed an endpoint for web clients. A posted example uses both `model_init.add_args` and `model_init.init`, and the discussion quotes the cache-quantization option from the same parser. This illustrates how parser changes can surface in downstream tooling; it does not show that the PR motivated this patch or that any deployed endpoint took the new flag. [inference; call_9c04b7d3025749378026f01742bc6c34, call_e2a75b3a161e4a48a5a29a9b840682c1, call_68e46cf6d9204d908678840f260f563d]

Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” reports that same autosplit error under TabbyAPI. Issue #54, “GPU split isn't followed here?”, asks about split limits under TabbyAPI and reports improvement after an allocator setting change. The matching error in #50 and matching split-budget terminology and dummy-forward behavior in #54 connect them to ordinary autosplit, not to a working tensor-parallel path. [inference; call_b9bd76003bbb4b1e864b2960c46dab63, call_230d6322d7b444be9ccb8cbc868a92b2, call_93b80a74be594dd8887a185cefcb2f5f, call_acb86c198cca4c73ad97da772ed19aca]

Other discussion matches are file or entry-point overlaps, not evidence of a TP failure: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” mentions `models/model.py` in an import traceback; #33, “Error converting model,” traces a file-open failure through the safetensors loader and later discusses GLM4 sampling; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” references `gemma3.py` in a logit-width investigation; #52, “Error converting moonshotai/Kimi-Dev-72B,” reports a conversion Cholesky failure and mentions `examples/chat.py` in later diagnosis of Qwen output. [inference; call_1d74d300039f4d8ea8111a330cb55913, call_7b20009efaf3451482a2ca81f43f9deb, call_d028e2a9e5f04446a82d65646f908aac, call_f56069b009bd46aabd7085de01b250b5, call_19da90a7981644198d8f953bdea97962, call_9234802973c9494984893e57f74d285d, call_68e46cf6d9204d908678840f260f563d]

<a id="model-init"></a>

## Wire the tensor-parallel flag to the existing loader switch

Config, tensor overrides, model construction, and optional cache setup still precede the load call. `init` passes `use_per_device=None` for an absent split or `auto`; otherwise it parses comma-separated floats. The patch adds `tensor_p` alongside that same split and progress value. Tokenizer creation and metrics reporting still follow the load, so neither runs after a loader exception. [source; call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_68e46cf6d9204d908678840f260f563d]

`Model.load` consumes `load_gen` with generator progress yields disabled. The existing direct `load_gen` calls in `examples/loading.py` instead iterate progress and leave `tensor_p` at its default. In the normal no-device branch an explicit budget is converted with `int(x * 1024**3)`, so the help text's GB units are interpreted as GiB, and only positive budgets select devices. The loader places whole modules, tests their memory use with dummy forwards, and retries on another device for recognized out-of-memory errors. This is sequential module placement, not tensor sharding. The tensor-parallel branch reaches none of that budget logic. [source; call_93b80a74be594dd8887a185cefcb2f5f, call_acb86c198cca4c73ad97da772ed19aca, call_2b15599b2fbd4dc4a49db2bba52a3a3d, call_d78a02ad25c94ccfb5124b9c6ba783d7]

A standard-library transcription selected autosplit when the flag was omitted and converted a `1.5,0` split to `[1610612736, 0]` bytes. It raised `NotImplementedError` for either alias, including with a valid split, and reached the single-device assertion when a device was supplied with the flag and no split. [execution; call_f7920cf859784111b3b43d71bbcdc63d]

## Authoring-time findings — pending review

### tensor-parallel-flag-selects-stub (suspected; defect)

The shared CLI advertises a load mode that the unchanged loader does not implement.

Trigger: Pass `-tp` or `--tensor_parallel` to a CLI that uses both shared helpers, such as `examples/chat.py`, and reach the load call with otherwise valid arguments and no explicit device.

Expected: Load in tensor-parallel mode and attempt to honor any supplied `--gpu_split`, as stated in help.

Actual: `Model.load_gen` raises `NotImplementedError` before module loading, with or without a valid split. An explicit device with no conflicting budget instead reaches the single-device assertion.

Locations: 0460dda4e410e1311c8474b1c1e980b6cbbba152:exllamav3/model_init.py — add_args and init, 3279fe188edb9e4be423fc828e5a8444c6aa6d06:exllamav3/models/model.py — Model.load_gen

Source evidence: call_68e46cf6d9204d908678840f260f563d, call_93b80a74be594dd8887a185cefcb2f5f, call_443262e0babc4281af82e505b0d62e18, call_d78a02ad25c94ccfb5124b9c6ba783d7

scalar_transcription: Modeled parsing and loader dispatch using argparse and the inspected branch conditions. [call_f7920cf859784111b3b43d71bbcdc63d]. Limits: Did not import or execute the repository loader.

### legacy-model-init-namespace (suspected; new_requirement)

`model_init.init` now requires `tensor_parallel` on caller-built namespaces.

Trigger: Supply a namespace equivalent to the old parser's output, but without `tensor_parallel`, and reach the load call.

Expected: An omitted TP setting retains ordinary loading, as it does with the updated parser.

Actual: Reading `args.tensor_parallel` raises `AttributeError` before the loader is called.

Locations: 0460dda4e410e1311c8474b1c1e980b6cbbba152:exllamav3/model_init.py — init

Source evidence: call_68e46cf6d9204d908678840f260f563d, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_443262e0babc4281af82e505b0d62e18, call_d78a02ad25c94ccfb5124b9c6ba783d7

scalar_transcription: Called the transcribed wrapper with a namespace lacking the new attribute. [call_f7920cf859784111b3b43d71bbcdc63d]. Limits: Programmatic API case; no old-form in-tree caller was found.

### duplicate-tensor-p-keyword (suspected; external_compatibility)

The formerly forwarded `tensor_p` keyword now collides with the explicit keyword.

Trigger: Call `model_init.init(args, tensor_p=False)` using an otherwise valid namespace with the new attribute.

Expected: Forward `False` to the loader as before through the documented extra keywords.

Actual: Python raises `TypeError` for multiple values for `tensor_p` before the loader runs, even when both values are false.

Locations: 0460dda4e410e1311c8474b1c1e980b6cbbba152:exllamav3/model_init.py — init

Source evidence: call_68e46cf6d9204d908678840f260f563d, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_af7e0461214143d99707a1e53ff5e5b3

scalar_transcription: Exercised the explicit keyword plus `**kwargs` call with the same key in both. [call_f7920cf859784111b3b43d71bbcdc63d]. Limits: No in-tree caller passing this keyword through `init` was found.

### inherited-override-metrics (suspected; defect)

The YAML override metrics failure recorded by the ancestor persists on the ordinary load path.

Trigger: Run a shared-init CLI with nonempty YAML overrides and `--load_metrics`, omit TP, and reach the metrics block after an otherwise successful load.

Expected: Print load metrics and return the initialized objects.

Actual: The variant collection does not initialize `metrics`; `config.stc.metrics.print()` fails with `AttributeError`.

Locations: 0460dda4e410e1311c8474b1c1e980b6cbbba152:exllamav3/model_init.py — init, 3279fe188edb9e4be423fc828e5a8444c6aa6d06:exllamav3/loader/safetensors.py — VariantSafetensorsCollection.__init__

Source evidence: call_68e46cf6d9204d908678840f260f563d, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_a9c6c68f8c2f45109eac12524108c635, call_95ecec46c3ae4dc7be8221591668be59, call_d78a02ad25c94ccfb5124b9c6ba783d7

source_inspection: Checked the wrapper constructor and the unchanged metrics access reached by shared-init callers. [call_a9c6c68f8c2f45109eac12524108c635, call_ae3c64a5060c4db4ab2930d5ed7aa7c3, call_68e46cf6d9204d908678840f260f563d]. Limits: Conditional on reaching the metrics block; no YAML-backed model load was executed.

### inherited-deferred-bf16-tail (suspected; defect)

Ordinary shared initialization still reaches the deferred CUDA converter with no odd-element cleanup.

Trigger: During an ordinary load, a module takes deferred CUDA loading for an odd-element BF16 tensor with BF16 disallowed.

Expected: Convert every element to FP16.

Actual: The native caller supplies the 16-bit element count; the CUDA wrapper launches only `numel / 2` pair conversions with integer division and no scalar tail.

Locations: 3279fe188edb9e4be423fc828e5a8444c6aa6d06:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_68e46cf6d9204d908678840f260f563d, call_acb86c198cca4c73ad97da772ed19aca, call_475b7f712968443089b63e2f1cf5bf5d, call_83e73f8105b2474b8c14b42945d55e50, call_ccb09c26e2bd4f0786720eea3707b6b1, call_f58d86559b9f4456914660272454ad80

scalar_transcription: Counted the elements covered by the pair bound and 1024-thread block size; counts of 3 and 2049 each left one uncovered element, unlike counts of 2 and 2048. [call_c1e741f04ec24f3fb1f55d43580c6057]. Limits: Python integer coverage only; no affected checkpoint, CUDA launch behavior, or conversion output was verified.

## Uncertainty and limits

The Python checks transcribed argument binding, branch selection, and pair coverage. They did not run the repository CLI, a model load, a CUDA kernel, or an allocator.

Whole-parent-tree literal searches establish the inspected in-tree call sites, not dynamic references or compatibility with unobserved external callers.

The historical reports are not reproductions of this commit; none establishes why the flag was added or how a future tensor-parallel split would use the budgets.
