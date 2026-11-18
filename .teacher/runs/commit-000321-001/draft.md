# ba4304a44b267e88f3c882136302fd1e25c5384e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ba4304a44b267e88f3c882136302fd1e25c5384e) · [Evidence ledger](draft.json)

Pins FlashAttention to `2.7.4.post1` in both installation declarations. The patch narrows dependency resolution without changing attention dispatch or native build logic; the reason for choosing that release is unverified.

- [Pin FlashAttention in both installation declarations](#packaging)

## Problem

Both installation routes declared `flash_attn>=2.7.4.post1`. They agreed on a minimum version, but neither constrained dependency resolution to that release. [source; call_b19b82933dd749aaad377308d9b6d0c9, call_187dc0a8f350495e94e41442d933415a]

## Reasoning

The diff matches turboderp’s commit message: it replaces `>=` with `==` in both `requirements.txt` and `setup.py`’s `install_requires`. Changing both declarations keeps installation from the requirements file and installation through package metadata aligned on FlashAttention. [source; call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c]

The pin removes variation between FlashAttention releases at the cost of excluding newer releases that the old minimum would have allowed. It narrows a dependency choice without choosing a wheel or locking the rest of the environment. [inference; call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c, call_b19b82933dd749aaad377308d9b6d0c9, call_187dc0a8f350495e94e41442d933415a]

## Impact

No runtime import or attention dispatch changes. `exllamav3/modules/attn.py` still imports both FlashAttention functions at module load, so selecting the existing `sdpa_nc` branch does not bypass that import. The KV-quantization experiment in `science/kv_quant_exp.py` still imports and calls `flash_attn_func` directly. [source; call_353f8ef682884dcfaaaea56875b997a2, call_8619597d314248ca9a00063abf6360ce, call_0f31cdbf6fb4475e94b9a179311226eb, call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c]

## Source Notes

The initial installation chapter records that `requirements.txt` already named `2.7.4.post1` as the minimum while `setup.py` omitted FlashAttention. The later “Fix requirements” entry records adding the same minimum to `install_requires` and retaining the Torch-availability check and `EXLLAMA_NOCOMPILE` switch. The Formatron entry records later additions of `kbnf` and `formatron` to both lists. [ancestor; call_6665ce0d9c6344d2aa25b29e8343e0d8, call_e80fb51423ca40168e712e809ae6a6c4, call_64b6da7c01c94664ac3169face95c27a]

Issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” quotes the old requirement verbatim. The reporter describes missing Torch and a Windows wheel build that appeared to hang; a reply from `turboderp` suggests installing PyTorch first and points to a Windows wheel for `2.7.4.post1`. [source; call_f120dd881cdb4691aed2fa403a862c6a]

Issue #17 is relevant installation context because its quoted line is the one this diff replaces, but it does not establish why the release was pinned or that the pin fixes the report. The diff changes neither how Torch is obtained nor whether a compatible FlashAttention wheel is available. [inference; call_f120dd881cdb4691aed2fa403a862c6a, call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c]

Issue #2, “Error: setup script specifies an absolute path,” reports a wheel-build rejection, and PR #3 explicitly names that issue. Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports ExLlamaV3 extension compiler errors and was closed without a reported solution. [source; call_dfe467fa1d2c45d1a65ccbc4d5395b97, call_dca0550caa1a48cf827ecbef19c08f8e, call_f96762d3f0104527af903b74c6fdd855]

The earlier source-path fix entry describes making the native extension’s source paths relative to `setup.py`, rather than changing its dependencies. [ancestor; call_50a89bc143b84d77a88bb34ccb3f5d48]

Issues #2 and #21 overlap with this change through `setup.py` and the installation workflow, not through the reported failures. The inspected parent already uses relative native-source paths, and the pin changes neither source-path construction nor compiler configuration. [inference; call_dfe467fa1d2c45d1a65ccbc4d5395b97, call_f96762d3f0104527af903b74c6fdd855, call_187dc0a8f350495e94e41442d933415a, call_a6ed683b2701476aa88254878d270c8c]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” shows `decode_flash_attn_nc` in the conversion traceback, with the error reported during linear Hessian capture. The discussion attributes the failure to tokenizer truncation. Issue #49, “running the QTIP inference code,” discusses installing QTIP and a `fast-hadamard-transform`/Ninja blocker. [source; call_160c6e2dceb141cc95bc00ca5dcc512d, call_e4a1452e55f849a8b72a97842f4e8616]

Issue #16 shares the attention path that consumes FlashAttention, while #49 mentions requirements and setup files in its QTIP instructions. Neither match is evidence that the pin addresses the reported problem. [inference; call_160c6e2dceb141cc95bc00ca5dcc512d, call_8619597d314248ca9a00063abf6360ce, call_e4a1452e55f849a8b72a97842f4e8616, call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c]

Issue #27, “Attention Backend,” requests FlashInfer alongside FlashAttention for comparison. Issue #44, “Please Switch to Flash-Infer,” reports inability to run EXL3 quants on RTX 2000-series GPUs and attributes it to FlashAttention’s Turing support. [source; call_2fed37eadd774f86aca1473981e26252, call_c03e60e45ed24463981b30c2191120e6]

Both backend discussions concern the library used by the inspected attention module, but the pin neither registers a different backend nor establishes support for additional hardware. [inference; call_2fed37eadd774f86aca1473981e26252, call_c03e60e45ed24463981b30c2191120e6, call_8619597d314248ca9a00063abf6360ce, call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c]

<a id="packaging"></a>

## Pin FlashAttention in both installation declarations

`requirements.txt` and `setup.py` declare the same `flash_attn==2.7.4.post1` constraint. The setup edit is confined to `install_requires`; the separate Torch check and `EXLLAMA_NOCOMPILE` logic still govern whether ExLlamaV3 configures its own native extension for precompilation. [source; call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c, call_187dc0a8f350495e94e41442d933415a]

The existing no-cache decoder passes projected Q, K, and V to `flash_attn_func`. The cached decoder obtains the cache tensors, passes them with the block table and sequence lengths to `flash_attn_with_kvcache`, then calls `cache.update_layer`. The pin changes which dependency release is requested, not either call interface. [source; call_8619597d314248ca9a00063abf6360ce, call_f339723c6c9f4acc8fe14c644c057a56, call_a6ed683b2701476aa88254878d270c8c]

A standard-library check read the parent files and applied the inspected replacement in memory. Comparing requirements lines and the AST-extracted `install_requires` list found exactly one changed declaration in each, leaving 12 and 11 entries unchanged, respectively. [execution; call_19229d9840ca40c8ac239a10ad1059f9]

## Uncertainty and limits

The evidence does not identify a newer FlashAttention release, regression, or platform incompatibility that motivated the pin.

The execution check compared declarations only. It did not run pip, setuptools, a wheel build, an import, or GPU attention. Resolver behavior for particular wheel variants and compatibility with specific Python, Torch, CUDA, and GPU combinations were not established.

The parent-tree search covered literal package and module spellings; it does not establish dynamically constructed imports or downstream use.
