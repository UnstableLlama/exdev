# 3254aa071a8960a3ffee8a63193e5d9d51249f2a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3254aa071a8960a3ffee8a63193e5d9d51249f2a) · [Evidence ledger](draft.json)

Consolidates EXL3 tensor export into a None-filtered comprehension, normalizing every exported tensor and retaining present zero-valued multiplier metadata.

- [Uniform EXL3 tensor export](#quantized-inference)

## Problem

LinearEXL3.get_tensors used repeated assignments and different inclusion rules for ordinary tensors and decoder-multiplier metadata. [source; call_ee3ad65868904109a651d82999a35b06]

## Reasoning

The cleanup centralizes export in one comprehension: enumerate known attributes, exclude None, prefix each name with the layer key, and make every exported tensor contiguous. This reduces repetition but is not strictly behavior-preserving. [source; call_ee3ad65868904109a651d82999a35b06]

## Impact

Present mcg and mul1 tensors are now exported even when their decoded multiplier is zero; previously their integer truth value controlled inclusion. Both metadata tensors also gain contiguous() normalization. Constructor decoding and inference calls remain unchanged. [source; call_ee3ad65868904109a651d82999a35b06, call_6897bb297a3f4015968ce6f3f7e37d57]

## Source Notes

Read the initial quantized-inference entry and the experimental-codebook entry d359bcc. They establish the earlier loading/export interface and the introduction of per-tensor multiplier metadata, respectively. [ancestor; call_9c5f45ab2b09421d9fb13e750b97363b, call_78fed9277eba4186b525508b693b1921]

Issue #11, “AssertionError: bias is wrong datatype,” reports a constructor failure and subsequent successful fix. Its contextual relationship is inferred from the same exl3.py constructor; the inspected parent already converts FP32 bias to half, and this task changes only export. [inference; call_88a3b1cef6a8481fbbc0174c97b4b1fb, call_6897bb297a3f4015968ce6f3f7e37d57, call_ee3ad65868904109a651d82999a35b06]

PR #26, “Superior 3INST parameters,” discusses alternative codebooks and explicitly identifies d359bcc as their implementation. Its relationship to this cleanup is inferred specifically from mcg/mul1 metadata, not an explicit reference to the task commit. [inference; call_ebf07b44b9574cb1aa45edd9fe1b65ed, call_5ba1668f2fb54029804adb7d9600a21e, call_ee3ad65868904109a651d82999a35b06]

Other discussions matching inspected conversion paths concern distinct failures: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns native-extension loading; #33, “Error converting model,” develops from file-opening failures into a GLM sampling report; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern factorization/nonfinite-state failures. Their contextual links are inferred from shared source paths, not evidence that this export cleanup fixes them. [inference; call_972d0df856064b0dbc0c6aca0fcd23d0, call_f88c1f7080a342d1b2d7cfcc6bd42500, call_4034eaaf25d34a2aa3c0925d320e2b98, call_9c07186f14ec40b686ff992fae5bde98, call_ee3ad65868904109a651d82999a35b06]

<a id="quantized-inference"></a>

## Uniform EXL3 tensor export

get_tensors retains the key argument and dictionary return interface. Its candidate list contains su, sv, suh, svh, trellis, bias, mcg and mul1; each non-None value becomes tensor.contiguous() under key.subkey. The obsolete commented scale export disappears. [source; call_ee3ad65868904109a651d82999a35b06]

The uniform None filter also replaces unconditional trellis export. For normally constructed instances this does not weaken the required-trellis invariant: __init__ still asserts trellis is present. It stores unpacked suh/svh and sets su/sv to None, so ordinary exports contain the unpacked representation. [source; call_6897bb297a3f4015968ce6f3f7e37d57, call_ee3ad65868904109a651d82999a35b06]

The removed multiplier truth checks previously omitted zero-valued metadata. The replacement preserves presence instead of testing decoder selection. Linear.load_exl3 reads either optional tensor and __init__ decodes its unsigned value, with absence defaulting to zero. create_quantization_config_json still lists stored tensors but emits named multiplier fields only for nonzero values; it therefore accepts the newly retained zero tensors without reporting an active experimental multiplier. [source; call_ee3ad65868904109a651d82999a35b06, call_6897bb297a3f4015968ce6f3f7e37d57, call_7fff6598c8ca42fcb483b8752a85a87f, call_fc71d5aeca3343479f4be8894ca12968]

The whole-parent search locates Linear.get_tensors as the direct inner-export caller. It supplies self.key only for a loaded layer. Conversion collects these dictionaries, saves them, and reloads from the same dictionary; Model.get_storage_info and the evaluation adapter consume values for byte accounting. These consumers retain compatible dictionary usage, although a present zero multiplier now contributes storage bytes. The FP16 alternatives keep their existing get_tensors(key) interface; no LinearEXL3 subclass appeared in the class-name search. [source; call_6b9188b85a4f450d850eec1061e4cbd5, call_1e4cb70a85134fee9db1ae293abfb41a, call_7fff6598c8ca42fcb483b8752a85a87f, call_0962319d8d304c0e83d91acac63414c2, call_531f19c0c45f40a7af0392dfc01f12e0, call_b2a63885ca444721ab997f7d03440c5b, call_9a73e7a1868e44a0af1fd2e1e3c40150, call_2edb0d641c8e40aaa067d85462e7abcb]

A bounded Python check compared the extracted parent method with a transcription of the replacement using fake tensors. Absent and nonzero metadata produced matching key sets; present zero metadata added exactly k.mcg and k.mul1. This checks selection logic, not real tensor contiguity or saved-file compatibility. [execution; call_ffa016c34323403297e6a729ad2ad318]

## Uncertainty and limits

No PyTorch tensor operation, serialization round trip, model conversion or GPU execution was tested. The bounded check used fake tensor objects and a transcription of the new comprehension.

Repository searches establish visible callers, not dynamic or external consumers. No performance improvement is measured.
