# 1f7f3e94c0e6055ff1aee1121294a1ddb7c79c94


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1f7f3e94c0e6055ff1aee1121294a1ddb7c79c94) · [Evidence ledger](draft.json)

Ignore AnyPrecision ImportError during comparison startup so unrelated evaluations can proceed. Selecting an unavailable AnyPrecision backend still fails later on an unbound class.

- [Keep comparison startup independent of AnyPrecision import errors](#usage-evaluation)

## Problem

The AnyPrecision adapter already ignored ModuleNotFoundError, but a different ImportError from either of its two external class imports could abort compare_q.py before argument parsing or backend selection. That also blocked compare_q_logits.py, which imports dataset and tensor-saving helpers from compare_q.py without using AnyPrecision. [source; call_e69fb9538d054ffd8e01a2c231f8c0e6, call_5b9a58b34c304ce2983dfb93856f661d, call_5fe84a009b8c44239cc5a717718e4b45]

## Reasoning

The patch adds a silent ImportError handler to the existing try block around both AnyPrecision class imports. It neither retries the imports nor removes the adapter from dispatch. This lets startup continue past an optional backend's import failure, at the cost of losing the original diagnostic if that backend is later selected. [source; call_a3dc81220c1e47058d632aa532313c60, call_e69fb9538d054ffd8e01a2c231f8c0e6, call_5b9a58b34c304ce2983dfb93856f661d]

Turboderp's commit message attributes the problem to a Transformers version mismatch. The diff supports the narrower claim that comparison startup no longer stops on an ImportError from this optional import block. It does not change Transformers or repair a failing AnyPrecision installation. [source; call_c4476a991e0546fbb8f7822f3da26d7b, call_a3dc81220c1e47058d632aa532313c60]

## Impact

The only direct importer found in the parent tree was compare_q.py; compare_q_logits.py reaches the adapter indirectly. Both can now get past this specific import failure if their other imports succeed. The exception handler does not cover the adapter's own Torch import or the separate Transformers adapter's imports. [source; call_fbbd0b36f4a64c018f4c9922214ee31c, call_37038e471dbc4c968e9c0c1919059b0b, call_5fe84a009b8c44239cc5a717718e4b45, call_e69fb9538d054ffd8e01a2c231f8c0e6, call_3d6a4ceb97dd45a6a4968780dae7f5d8, call_a3dc81220c1e47058d632aa532313c60]

The six bundled AnyPrecision model specs still select the same loader and forward function. On a cache miss, the loader must construct the model and compute its storage statistics before the evaluation loop can call the forward function. A suppressed import can therefore still prevent all six specs from producing results. [source; call_855aa3f41e7a40feb0b7413c671bc2fe, call_5b9a58b34c304ce2983dfb93856f661d, call_e69fb9538d054ffd8e01a2c231f8c0e6, call_a3dc81220c1e47058d632aa532313c60]

## Source Notes

The AnyPrecision introduction entry records the original eager-import requirement. The later optional-import entry records how the ModuleNotFoundError guard deferred that requirement without guarding the loader, and separately records the Transformers storage-accounting failure with None class sentinels. [ancestor; call_71d9163456e143c4b56460f394baccee, call_c5169552430d45dba120172fe52b9115]

Parent-tree searches found Transformers evaluation imports, a Transformers integration, and a transformers>=4.50.0 declaration in requirements_eval.txt, but no literal 'version mismatch' match. The only any_precision imports found were the two in the adapter. None of these occurrences identifies the incompatible version pair. [source; call_d231a005476b485ca1baf0cfb95b6314, call_22e2cd619109467b9ee1592fad6f0ace, call_c8e2adaf7a4a467ca3f1b1f4eb04c8d5, call_6d5bfd8a18914df8b619984b5391f415]

PR #26, “Superior 3INST parameters,” proposes changing EXL3's codebook multiplier and reports perplexity comparisons. Its shared compare_q.py path and evaluation context make it background for the benchmark, not evidence that it motivated the AnyPrecision import fix. [inference; call_f11fa762274345588b97d762afa0f0f1, call_a5da5d7337614ac7a5f0ecb7908ac874, call_5b9a58b34c304ce2983dfb93856f661d]

Issue #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” reports NaNs and a conversion-time factorization failure that the reporter later could not reproduce. The reporter explicitly mentions eval/compare_q.py for KL-divergence plots, which connects the discussion to the evaluation script, not to the ImportError fixed here. [inference; call_97849b9cf543413983d7836171c43d6e, call_3522b9f11c734c11817ff377b11e41ac, call_a3dc81220c1e47058d632aa532313c60]

<a id="usage-evaluation"></a>

## Keep comparison startup independent of AnyPrecision import errors

Both imports share one try block, with AnyPrecisionForCausalLM first. If that import fails, the second is not attempted; if only the second fails, the first binding remains. Neither handler supplies a replacement class, so successful module import does not imply a usable backend. [source; call_a3dc81220c1e47058d632aa532313c60, call_e69fb9538d054ffd8e01a2c231f8c0e6]

The bounded Python check injected failures at each import in the parent adapter and in an in-memory copy with the new handler. Plain ImportError moved from module startup to a NameError in the selected loader path: AnyPrecisionForCausalLM when the first import failed, AnyPrecisionLinear during storage accounting when only the second failed. ModuleNotFoundError already followed those deferred paths in the parent. [execution; call_e69fb9538d054ffd8e01a2c231f8c0e6, call_a3dc81220c1e47058d632aa532313c60, call_5c048d01bc54452ab3db200669b2b03e]

An alternative would be to record the import exception and report it only when AnyPrecision is selected, or to import the classes lazily inside its loader. Either would keep unrelated startup working while explaining why the selected backend is unavailable; the patch instead leaves the registries and loader unchanged. [inference; call_a3dc81220c1e47058d632aa532313c60, call_5b9a58b34c304ce2983dfb93856f661d, call_e69fb9538d054ffd8e01a2c231f8c0e6]

## Authoring-time findings — pending review

### anyprecision-import-failure-deferred-to-loader (suspected; defect)

The optional import guard leaves the AnyPrecision backend registered even when a required class is unbound. The patch carries this behavior over for ModuleNotFoundError and extends it to other ImportErrors.

Trigger: In a fresh process, either AnyPrecision class import fails with an exception caught by the guard, other startup and dataset setup succeed, and an uncached comparison selects load_fn "anyprecision". For the second-import case, model construction must succeed and storage accounting must encounter a module.

Expected: Selecting the unavailable backend reports the import problem before attempting model construction or storage accounting.

Actual: A failure at the first import leaves AnyPrecisionForCausalLM undefined, so load_anyprecision raises NameError at from_quantized. A failure only at the second import leaves AnyPrecisionLinear undefined, so get_storage_info raises NameError on its first module check. Neither path reports the original import exception.

Locations: 1f7f3e94c0e6055ff1aee1121294a1ddb7c79c94:eval/compare_q_anyprecision.py — load_anyprecision, 1f7f3e94c0e6055ff1aee1121294a1ddb7c79c94:eval/compare_q_anyprecision.py — get_storage_info

Source evidence: call_a3dc81220c1e47058d632aa532313c60, call_e69fb9538d054ffd8e01a2c231f8c0e6, call_7185ac8fa2b04a3c90ba3884c880c636, call_fdeb4706ce8b4e5e95c6e375fa19ec70, call_5b9a58b34c304ce2983dfb93856f661d

source_inspection: The parent search found compare_q.py registering the loader and dispatching it through test_ppl. The adapter's load_anyprecision is the direct caller of its storage helper. compare_q_logits.py imports shared helpers but does not call this loader. [call_7185ac8fa2b04a3c90ba3884c880c636, call_fdeb4706ce8b4e5e95c6e375fa19ec70, call_5b9a58b34c304ce2983dfb93856f661d, call_5fe84a009b8c44239cc5a717718e4b45]. Limits: Literal repository search; no external callers or real installed backend were tested.

scalar_transcription: The patched-source harness reproduced both missing-name failures using synthetic import exceptions. [call_5c048d01bc54452ab3db200669b2b03e]. Limits: In-memory diff application with stub dependencies, not an installed AnyPrecision or Transformers test.

### transformers-storage-none-sentinel-carried-over (suspected; defect)

The sibling Transformers adapter still passes optional class sentinels to isinstance. The AnyPrecision-only patch leaves this earlier finding unchanged.

Trigger: A missing bitsandbytes import sets Linear4bit to None, a Transformers model loads successfully through one of compare_q.py's three Transformers loader selections, and storage accounting reaches a named module.

Expected: Skip the unavailable quantized class and continue checking the model's modules.

Actual: The first module check evaluates isinstance(module, None) and raises TypeError before returning storage metadata. Other missing optional classes can cause the same failure when their checks are reached.

Locations: 1f7f3e94c0e6055ff1aee1121294a1ddb7c79c94:eval/compare_q_transformers.py — get_storage_info

Source evidence: call_3d6a4ceb97dd45a6a4968780dae7f5d8, call_fdeb4706ce8b4e5e95c6e375fa19ec70, call_5b9a58b34c304ce2983dfb93856f661d, call_a3dc81220c1e47058d632aa532313c60

source_inspection: load_transformers calls the storage helper directly; the auto and auto-BF16 wrappers delegate to it. The task diff does not modify this path. [call_3d6a4ceb97dd45a6a4968780dae7f5d8, call_fdeb4706ce8b4e5e95c6e375fa19ec70, call_5b9a58b34c304ce2983dfb93856f661d, call_a3dc81220c1e47058d632aa532313c60]. Limits: Requires a successful model load followed by storage accounting; the data-tokenization path does not call this helper.

scalar_transcription: The first isinstance generator expression with a None sentinel raised TypeError. [call_5c048d01bc54452ab3db200669b2b03e]. Limits: Tests the Python expression only, not the Transformers adapter or a real model.

## Uncertainty and limits

The external AnyPrecision traceback, failing symbol, and incompatible Transformers versions are unestablished. The requirements file's lower bound is not a compatibility matrix.

The Python check used stub imports, a stub Torch decorator, and a dummy model. It did not load installed backends, run a real comparison CLI, or execute GPU inference.

Importer and caller reach is based on literal parent-tree searches and inspected call sites; dynamic imports and external callers are not covered. Only excerpts of PR #26 were inspected.
