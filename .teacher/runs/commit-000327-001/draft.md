# db533103b1827e83b55bac4f4531eeef3684a57f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/db533103b1827e83b55bac4f4531eeef3684a57f) · [Evidence ledger](draft.json)

Adds the existing generator filter subpackage to setup.py's explicit package list, addressing the installed import failure reported in #62. It does not change filter behavior or add the separately unlisted Transformers integration package.

- [Include the generator filter subpackage in distributions](#packaging)

## Problem

The parent checkout contains `exllamav3/generator/filter` with an initializer, `filter.py`, and `formatron.py`, but `setup.py` does not list it in `packages`. Listing `exllamav3.generator` and its `sampler` sibling does not explicitly select the new subpackage. [source; call_3e2f288bc1d34ae0bd4a9a45a39f3d6d, call_ff2ae973986546ee9d653e1a9a7c7f1f]

In issue #62, “Dev branch 15JUL2025 - ModuleNotFoundError: No module named 'exllamav3.generator.filter',” mindkrypted reported that `examples/chat.py` failed while importing an installed ExLlamaV3 from `site-packages`. The reporter added the filter package to `setup.py` and said EXAONE 4.0 chat worked after rebuilding. Turboderp's commit explicitly names #62 and applies that same list entry. [source; call_f92b5c4ed9c04b6b839165f2240cc6f5, call_e5c6b90b779b400f8a955ba3fb0142cc, call_f3e953c5fef64ac3a9513f4094b88b75]

## Reasoning

The traceback matches the parent's eager import chain: `exllamav3/__init__.py` imports from `.generator`; that package initializer imports `Generator`; `generator.py` imports `Job`; and `job.py` imports `.filter` at module scope. The missing package therefore stops startup before `chat.py` selects a prompt format or loads a model. EXAONE was the reporter's test case, not a condition for reaching the failing import. [inference; call_f92b5c4ed9c04b6b839165f2240cc6f5, call_72507da868534cffa10fe3a09a4c92fb, call_193d75f5a67c44a49b34cdcb3c56a074, call_d8fefa98e3a145c99b6bc390bf985f9d, call_ce194e3e297645afa6d83b1b3cfb544d, call_f9b7609a3ee9497d863399a5cca71c95]

Adding one name to the explicit package list preserves the existing packaging and public import design. Deferring the filter imports could reduce the number of callers blocked by a missing subpackage, but would not ship the files needed by callers that actually use filters. Automatic package discovery could reduce omissions of this kind, but would change how the entire distribution's package set is selected. [inference; call_3e2f288bc1d34ae0bd4a9a45a39f3d6d, call_f3e953c5fef64ac3a9513f4094b88b75, call_4b4fcb1751eb40f7a05881865cf61210, call_72507da868534cffa10fe3a09a4c92fb]

## Impact

The patch selects the existing filter subpackage for distribution. It changes no import statements, dependency declarations, native build flags, chat templates, or generation logic. The filter initializer still imports both `Filter` and `FormatronFilter`, and the adapter still imports `formatron` and `kbnf` at module scope; those dependencies were already declared in `install_requires`. [source; call_f3e953c5fef64ac3a9513f4094b88b75, call_3e2f288bc1d34ae0bd4a9a45a39f3d6d, call_76141dd8f13d4a9ab0d0f53fba9451d1, call_c8c92aed54f34127ad6bc21744452147]

An installation missing this subpackage can block ordinary `exllamav3` imports even when the caller never requests a filter. The parent search found examples importing `Generator` and `Job`, a constrained-generation example importing the filter classes explicitly, and callers such as `examples/loading.py` that import only model-loading names from the same root initializer. [inference; call_c945fc310e574b53a60fca20a07bf7d0, call_72507da868534cffa10fe3a09a4c92fb, call_193d75f5a67c44a49b34cdcb3c56a074, call_ce194e3e297645afa6d83b1b3cfb544d]

## Source Notes

Read the initial installation chapter and “Add Formatron support and improved logit masking.” The first describes the existing precompile, JIT-install, and checkout workflows; the second records the introduction of public filter exports and eager adapter imports. It also records runtime filter and sampler concerns, which the packaging-only edit does not address. [ancestor; call_c305606acda546b08f3dd84e7d5ee310, call_e95d63c6987a4d2ba3d3a53d0eb715f9]

The earlier Transformers integration entry records two separate concerns: the integration package was not listed in `setup.py`, and its eager root import made Transformers an undeclared startup dependency. [ancestor; call_a5f9155748fb4734ae527e804cedd34c, call_10341d4aec3e49d28ac303ebab1fa6db]

In the inspected parent, the integration omission persists and this patch leaves it in place. The earlier eager-import path does not persist: the parent root initializer does not import `integration`, its initializer is empty, and the in-tree example imports the adapter explicitly. [source; call_3e2f288bc1d34ae0bd4a9a45a39f3d6d, call_f3e953c5fef64ac3a9513f4094b88b75, call_0037ba18ca734612a7e279dc16e54152, call_72507da868534cffa10fe3a09a4c92fb, call_521480bb6056447bb380014289c907ec, call_a65924473c0e49999517941e3b418462]

Closed issues #2, “Error: setup script specifies an absolute path,” and #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” report wheel-build path validation and unresolved native compilation failures, respectively. The inferred overlap is the use of `setup.py`; this patch does not change its extension source paths or compiler settings. [inference; call_379f2cbcc41745778c77b169f6af86dc, call_afdbd5a05edd4d6aa9755c7b0a237411, call_3e2f288bc1d34ae0bd4a9a45a39f3d6d, call_f3e953c5fef64ac3a9513f4094b88b75]

Other discussions overlap only by file or entry point: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traces a native extension load error through `exllamav3/__init__.py`; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” traces a tensor-size mismatch through `job.py`; #49, “running the QTIP inference code,” gives QTIP installation advice using setup scripts; and #52, “Error converting moonshotai/Kimi-Dev-72B,” reports a Cholesky failure and mentions `examples/chat.py` in later troubleshooting for different models. Those overlaps are not evidence that this package-list edit addresses any of the four reports. [inference; call_2216c3bd5c764b89a86d9d75270784fe, call_2d04b67c8739463a8c385a4a110f2338, call_444e024dd0aa4bde8bd6a91db9c8ed15, call_06af4563c05046e7ae535db180ba4dca, call_f3e953c5fef64ac3a9513f4094b88b75]

<a id="packaging"></a>

## Include the generator filter subpackage in distributions

`setup.py` adds `exllamav3.generator.filter` alongside `exllamav3.generator` and `exllamav3.generator.sampler`. Supplying the existing package is the missing precondition for `Job`'s unchanged relative import in a distribution that previously omitted it. [source; call_f3e953c5fef64ac3a9513f4094b88b75, call_ff2ae973986546ee9d653e1a9a7c7f1f, call_ce194e3e297645afa6d83b1b3cfb544d]

A standard-library check parsed the parent's literal `packages` list and compared it with directories containing `__init__.py`. Before the change it found two unlisted packages, `exllamav3.generator.filter` and `exllamav3.integration`; applying the one-line addition to the list in memory left only `exllamav3.integration` unlisted. [execution; call_dda257ee4aed4fb3a7250e891daf77ed, call_f3e953c5fef64ac3a9513f4094b88b75]

## Authoring-time findings — pending review

### integration-remains-unlisted (suspected; defect)

The separate Transformers integration package remains absent from the explicit distribution package list.

Trigger: Install a distribution built from this package list, then explicitly import `exllamav3.integration.transformers` with its dependencies available and no checkout on the import path.

Expected: The installed package should provide the adapter imported by `examples/transformers_integration.py`.

Actual: `setup.py` selects the newly added filter subpackage but still does not select `exllamav3.integration`. If the artifact omits the adapter, the explicit import fails before `patch_transformers()` can run. Unlike the filter omission, this does not block the ordinary root import through the inspected initializer.

Locations: db533103b1827e83b55bac4f4531eeef3684a57f:setup.py — setup(packages=...), 327d1f99d691982c6db0e3d32528e7971560b8f8:examples/transformers_integration.py — module-level adapter import

Source evidence: call_f3e953c5fef64ac3a9513f4094b88b75, call_3e2f288bc1d34ae0bd4a9a45a39f3d6d, call_0037ba18ca734612a7e279dc16e54152, call_a65924473c0e49999517941e3b418462, call_72507da868534cffa10fe3a09a4c92fb

source_inspection: Compared the package inventory and diff with the root initializer and the sole literal in-tree `patch_transformers` import and call found by the parent search. [call_a2ea27ad635a4db5b4ac4fdb9a99c4ea, call_a65924473c0e49999517941e3b418462, call_72507da868534cffa10fe3a09a4c92fb, call_f3e953c5fef64ac3a9513f4094b88b75]. Limits: The example appends the checkout to `sys.path`, so running from source can mask the omission. No distribution or installed import was tested; literal search does not cover dynamic or external consumers.

## Uncertainty and limits

No wheel or source distribution was built or inspected, and no installed import, editable install, or chat run was reproduced. The reported rebuild success comes from mindkrypted.

The package inventory check compares explicit names with directories containing `__init__.py`; it does not execute setuptools or determine the contents of an installed artifact. The import reach is based on inspected static imports, not a survey of dynamic imports or downstream applications.
