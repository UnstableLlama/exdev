# 327d1f99d691982c6db0e3d32528e7971560b8f8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/327d1f99d691982c6db0e3d32528e7971560b8f8) · [Evidence ledger](draft.json)

Restores `flash_attn>=2.7.4.post1` in both installation declarations so newer releases can qualify without lowering the minimum. Attention dispatch and native build logic are unchanged. The change does not establish wheel availability or resolve the separately reported filter-package omission.

- [Restore the FlashAttention minimum in both installation routes](#packaging)

## Problem

Both installation routes required exactly `flash_attn==2.7.4.post1`, excluding higher releases even if a suitable wheel was available for one of them. turboderp's commit message describes the revert as temporary, pending resolution of the “wheel situation,” but names no affected platform or wheel. [source; call_3d2a8e9f281f4986aa03027c9ec46bbf, call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

## Reasoning

Changing `==` to `>=` in both `requirements.txt` and `setup.py`'s `install_requires` keeps the two installation routes aligned on FlashAttention. It retains `2.7.4.post1` as the minimum and adds no upper bound. [source; call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

The likely tradeoff is easier installation when a suitable newer wheel exists, at the cost of allowing FlashAttention versions to vary across environments. The change neither selects a wheel nor ensures that an eligible release has a compatible binary. [inference; call_3d2a8e9f281f4986aa03027c9ec46bbf, call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

## Impact

FlashAttention remains a required dependency. Attention dispatch is unchanged, and `exllamav3/modules/attn.py` still imports `flash_attn_func` and `flash_attn_with_kvcache` at module load. Choosing the existing Torch SDPA path does not bypass that import. The KV-quantization experiment also retains its direct import of `flash_attn_func`. [source; call_75663378a59b4a4d8ed6de773d7d0401, call_9289f7ed325e446d9c970ea3167f42a6, call_4b5d9ba2e7e5411a8fa51a44912e5263, call_51b007efdc604365a918905e44bd1430, call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

## Source Notes

The initial installation entry records the minimum in `requirements.txt` but not in package metadata. “Fix requirements” records adding that same minimum to `install_requires`; “Pin flash-attn at 2.7.4.post1” records changing both declarations to equality. The current change restores the form documented before the pin. [ancestor; call_67af8c281c1042f59b7035d309acad99, call_e63008d5409c40eb8a3de8db9eabd6f6, call_17e40463683941bb96d84626167debf2]

Issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” quotes the restored requirement and reports a Windows FlashAttention build that appeared to hang. A reply by `turboderp` recommends installing PyTorch first and points to a prebuilt `2.7.4.post1` wheel. [source; call_de77a278152841d8b74cfd368f334a3d]

The quoted requirement and wheel discussion make #17 relevant context, not evidence that the report prompted this revert or that relaxing the pin fixes it. The parent README and CI also mention wheels, but those references concern ExLlamaV3's own installation and wheel builds, not an inventory of FlashAttention wheels. [inference; call_de77a278152841d8b74cfd368f334a3d, call_cf015b3b2b944633b20f778b9fa6d012, call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

Issue #2, “Error: setup script specifies an absolute path,” reports rejection of absolute source paths during a wheel build. Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” reports ExLlamaV3 extension compiler errors and was closed without a reported solution. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports failure loading `exllamav3_ext` after installation and a workaround involving a new Conda environment and toolchain. [source; call_2131bbaa1f594668aeed26cfb216b613, call_d946182d24d6488ab40c61c800d7156b, call_325553cc55c54df7a7703ce02338560c]

Those three reports overlap with the native-extension installation workflow, not with the changed FlashAttention constraint: the parent already constructs relative source paths, and the diff changes neither extension compilation nor loading. [inference; call_2131bbaa1f594668aeed26cfb216b613, call_d946182d24d6488ab40c61c800d7156b, call_325553cc55c54df7a7703ce02338560c, call_6fd7f330441141f6961236ed23da0c02, call_3915be451a31405d9f451051e31adb70]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports a conversion failure during linear Hessian capture, reached through `decode_flash_attn_nc` and `project_qkv`; the discussion identifies tokenizer truncation as the likely cause and reports overriding it. Issue #49, “running the QTIP inference code,” gives setup instructions for QTIP and describes a `fast-hadamard-transform` installation blocker involving Ninja. [source; call_3cb322c9aa934c25af7875f098c2bebe, call_2456aa12e502413489c35dbfef24ae1e]

Issue #16 shares the no-cache decoder, but the matching projection call precedes `flash_attn_func`. Issue #49 mentions `setup.py` and `requirements.txt` for QTIP and its dependencies, not the ExLlamaV3 FlashAttention declaration. Neither match indicates that the revert addresses the report. [inference; call_3cb322c9aa934c25af7875f098c2bebe, call_2456aa12e502413489c35dbfef24ae1e, call_4b5d9ba2e7e5411a8fa51a44912e5263, call_3915be451a31405d9f451051e31adb70]

Issue #62, “Dev branch 15JUL2025 - ModuleNotFoundError: No module named 'exllamav3.generator.filter',” reports that an installed package failed when chat imported `exllamav3`. The reporter says adding `exllamav3.generator.filter` to `setup.py` and rebuilding restored chat. [source; call_54142e72286c41258d7ebf4f98d77f88]

The earlier Formatron entry records the introduction of public `Filter` and `FormatronFilter` exports and their eager imports through package initializers. [ancestor; call_e02387a34fa340dfa91bbe430653ef6e]

The concrete match to #62 is the missing filter package in the explicit `setup.py` list and the eager import through the generator. That omission is carried over: the task changes `install_requires`, not `packages`. [inference; call_54142e72286c41258d7ebf4f98d77f88, call_6fd7f330441141f6961236ed23da0c02, call_3dc8ac4d54d14fff9d623cca1bb83a34, call_153257f30e5f4e87b49c80a5dc40e371, call_3915be451a31405d9f451051e31adb70]

<a id="packaging"></a>

## Restore the FlashAttention minimum in both installation routes

`requirements.txt` governs installation from the requirements file; `install_requires` supplies the dependency to setuptools. Each changes one FlashAttention declaration from equality to a lower bound. The Torch requirement stays unchanged, as do `setup.py`'s separate check for an already installed Torch and its `EXLLAMA_NOCOMPILE` switch for the native extension. [source; call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70, call_6fd7f330441141f6961236ed23da0c02]

The no-cache decoder still supplies projected Q, K and V to `flash_attn_func`. The cached decoder supplies Q, K and V plus cache tensors, block table and sequence lengths to `flash_attn_with_kvcache`, then updates the cache layer. A release satisfying the new declaration must still satisfy these unchanged call interfaces. [source; call_4b5d9ba2e7e5411a8fa51a44912e5263, call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

A standard-library check applied the inspected substitution in memory to the parent files, comparing requirements lines and extracting the `install_requires` list with Python's AST. It found exactly one changed declaration in each file, leaving 12 requirements lines and 11 setup dependencies unchanged. [execution; call_3df2bc066b5f4443b6fabaa8c655e4bd, call_e1e2b5b7db444ec481557918f10a61d0, call_3915be451a31405d9f451051e31adb70]

## Authoring-time findings — pending review

### installed-filter-package-omitted (suspected; defect)

The explicit package list still omits the generator filter subpackage that installed code imports eagerly.

Trigger: Import `exllamav3` from an installation that follows the explicit package list and does not otherwise expose the filter source, for example when starting the chat example outside the checkout.

Expected: The installed distribution provides `exllamav3.generator.filter` so that the generator and public filter exports can be imported.

Actual: `setup.py` lists `exllamav3.generator` and `exllamav3.generator.sampler` but not `exllamav3.generator.filter`. If the latter is absent from the installation, the eager generator import can raise `ModuleNotFoundError` before chat launches, as #62 reports. The FlashAttention edit does not change that list.

Locations: 327d1f99d691982c6db0e3d32528e7971560b8f8:setup.py — setup(packages=...), 1f7f3e94c0e6055ff1aee1121294a1ddb7c79c94:exllamav3/generator/job.py — module-level Filter import

Source evidence: call_6fd7f330441141f6961236ed23da0c02, call_3915be451a31405d9f451051e31adb70, call_3dc8ac4d54d14fff9d623cca1bb83a34, call_153257f30e5f4e87b49c80a5dc40e371, call_54142e72286c41258d7ebf4f98d77f88

source_inspection: Compared the explicit parent package list with the task diff and followed literal filter imports. `job.py`, `generator.py`, and the generator initializer import the filter subpackage directly; the top-level package initializer reaches them through its generator import. The reported chat traceback shows one entry point affected by that chain. [call_6fd7f330441141f6961236ed23da0c02, call_3915be451a31405d9f451051e31adb70, call_3dc8ac4d54d14fff9d623cca1bb83a34, call_153257f30e5f4e87b49c80a5dc40e371, call_54142e72286c41258d7ebf4f98d77f88]. Limits: No distribution was built or installed. The observation is conditional on the installed module being absent; it does not establish failure for a source checkout, an editable install, or every packaging workflow.

## Uncertainty and limits

The evidence does not identify the specific wheel, release, or environment that prompted the revert, or establish why `2.7.4.post1` remains the minimum.

The standard-library check compared declarations only. No dependency resolver, wheel build or installation, package import, or GPU attention ran. Candidate selection and compatibility across Python, Torch, CUDA, and GPU combinations remain unverified.

The import search covers literal `flash_attn` and `flash-attn` spellings in the parent tree, not dynamic imports or downstream code.
