# c0e9242315c554c3767883abfc8c2c8c46c9314c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c0e9242315c554c3767883abfc8c2c8c46c9314c) · [Evidence ledger](draft.json)

Clarifies that users should install CUDA-enabled PyTorch first and have the CUDA Toolkit available; existing full-install and JIT commands remain unchanged.

- [Explicit prerequisites for native-extension installation](#installation)

## Problem

The installation instructions previously began with pip commands without explicitly requiring a CUDA-enabled PyTorch installation or CUDA Toolkit. [source; call_a9c847fd10fc430eba50aa051a1ea406, call_efd652de47894c2393137a9fe6a41c8e]

## Reasoning

Making PyTorch a prerequisite matches setup.py's build-time dependency: it probes for torch before configuring CUDAExtension. The JIT alternative also imports torch and uses its extension loader. [source; call_de968624b420451e8b673ec9eb653999, call_7401c8f9e27d41c28ec570455be8c8d1]

## Impact

README now directs users to install appropriate PyTorch with CUDA 12.4 or later first, and explicitly requires the CUDA Toolkit while precompiled wheels are unavailable. Installation commands and executable code are unchanged. [source; call_a9c847fd10fc430eba50aa051a1ea406]

## Source Notes

DekoMoon's issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” reports missing torch during flash_attn installation, a subsequent CPU-only torch installation, and switching to cu124. Its connection to this documentation edit is inferred from those matching prerequisites, not an explicit upstream reference. [inference; call_74f448b3f1d64f85bd70015f2608d34b, call_a9c847fd10fc430eba50aa051a1ea406]

Other contemporary reports concern an undefined __cxa_call_terminate symbol (#7), incoherent low-bitrate output (#15), and an invalid CUDA configuration argument during conversion (#16). They do not establish that this installation-text change resolves those failures. [source; call_413db8ee65184deea4e314b042bae6f2, call_b1bc792783a3423a91e94d1c6d2fe1d8, call_4470ff3c62384bafa4aef417e2e4ed15, call_a9c847fd10fc430eba50aa051a1ea406]

<a id="installation"></a>

## Explicit prerequisites for native-extension installation

The full-install sequence remains pip install -r requirements.txt followed by pip install .; requirements.txt declares torch>=2.6.0 and flash_attn>=2.7.4.post1. The new prose adds an explicit PyTorch selection step rather than changing dependency constraints. [source; call_efd652de47894c2393137a9fe6a41c8e, call_fb6f3be8d3a54dbebacf735fadb965ff, call_a9c847fd10fc430eba50aa051a1ea406]

EXLLAMA_NOCOMPILE=1 suppresses setup-time native compilation because setup.py tests the variable's presence, not its numeric value. Without that variable, available torch enables CUDAExtension and BuildExtension; without torch, setup prints a warning and omits those extension settings. [source; call_de968624b420451e8b673ec9eb653999]

JIT defers compilation rather than eliminating it: ext.py first imports exllamav3_ext, then on ModuleNotFoundError gathers C/C++/CUDA sources and calls torch.utils.cpp_extension.load. This explains the local compilation path behind the added Toolkit prerequisite, while preserving the existing installed-extension path. [source; call_7401c8f9e27d41c28ec570455be8c8d1, call_a9c847fd10fc430eba50aa051a1ea406]

## Uncertainty and limits

CUDA 12.4 is a documented minimum here; the inspected build code and dependency declarations do not establish why that precise minimum is necessary or guarantee compatibility with every later version.

No installation or compilation was executed. A scalar computation would not meaningfully validate these environment prerequisites.

The documentation does not establish that these prerequisites alone resolve FlashAttention wheel-building or compiler/runtime compatibility problems.
