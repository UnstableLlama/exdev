# 4ab2b253533b19e461a01ce7b74957ae9834d557


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4ab2b253533b19e461a01ce7b74957ae9834d557) · [Evidence ledger](draft.json)

Adds an opt-in CPU workaround for LinearEXL3 packed-sign expansion, restoring output to the original device while leaving existing callers unchanged.

- [Opt-in CPU expansion of packed sign factors](#quantized-inference)

## Problem

The author reports that packed-sign expansion can cause a GPU assert with Transformers. The added comment identifies CPU execution as a workaround, but supplies no reproducer or root-cause diagnosis. [source; call_490d43c30b234fe8bb5fdb1cae46a278]

## Reasoning

The change makes CPU unpacking opt-in and restores the result to the input device, preserving the device contract expected by subsequent weight reconstruction and inference. [source; call_490d43c30b234fe8bb5fdb1cae46a278, call_76a7342ca5a2438190f7deb3c756a22c]

## Impact

Existing repository constructors remain compatible and leave the workaround disabled. Enabling it requires a caller to supply transformers_fix=True; this commit does not wire that option through Linear.load_exl3 or Linear.convert_exl3. [source; call_d5856d3ab6214bfdb22e961fa252a890, call_35722bfe67a54b5bb250a4f40a7b35e1, call_490d43c30b234fe8bb5fdb1cae46a278]

## Source Notes

The parent entry describes the nullable, unused config argument. The original quantized-inference entry establishes the loading/reconstruction interface and records incomplete historical packed-sign support. [ancestor; call_89530da2b0d241dd9c84c7613115a6ee, call_edb936e7f82a476e8bb5359fc14e6cc6]

Issue #11, “AssertionError: bias is wrong datatype,” concerns constructor bias validation, not bitfield expansion. Its relationship is inferred from the shared LinearEXL3 constructor. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports a Cholesky failure; its relationship is inferred only from its traceback through the inspected Linear.convert_exl3. Neither establishes the reported Transformers assert. [inference; call_3e48a97a32824992bcc3cb9be9abb209, call_a6f09264fc1f498c8b0aae2cc481f5d1, call_35722bfe67a54b5bb250a4f40a7b35e1, call_490d43c30b234fe8bb5fdb1cae46a278]

Closed issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses quantization regularization and output normalization, not this CPU-unpacking workaround. [source; call_e9c98679783948598840482aec39710b]

<a id="quantized-inference"></a>

## Opt-in CPU expansion of packed sign factors

LinearEXL3.__init__ appends transformers_fix: bool = False and stores it before either constructor call to unpack_bf. That ordering is necessary: packed su or sv is expanded immediately when its corresponding unpacked suh or svh is absent. Supplying both unpacked factors bypasses expansion entirely. [source; call_490d43c30b234fe8bb5fdb1cae46a278, call_76a7342ca5a2438190f7deb3c756a22c]

unpack_bf saves bitfield.device, conditionally moves the input to CPU, performs the unchanged expansion, and returns contiguous output moved to the saved device. The final device restoration is unconditional; only the initial CPU move is controlled by the flag. [source; call_490d43c30b234fe8bb5fdb1cae46a278]

Expansion reinterprets storage as unsigned 16-bit words, converts to integer values and tests masks 1 << i for i=0…15. Thus 16 is the packed word width: each word produces sixteen least-significant-bit-first FP16 factors, with set bits mapped to −1 and clear bits to +1. Flattening retains word order and puts each word's sixteen factors consecutively. [source; call_76a7342ca5a2438190f7deb3c756a22c, call_490d43c30b234fe8bb5fdb1cae46a278]

A standard-library scalar transcription exhaustively expanded all 65,536 unsigned 16-bit values and reconstructed each original word from the negative-factor positions. All round-trips passed; this checks the sign mapping, not the repository tensor implementation. [execution; call_00da48fe5b194770977fc65b15db0a35]

Whole-parent-tree searches find one LinearEXL3 definition, two direct construction sites and no other named unpack_bf callers outside the class. Linear.load_exl3 supplies checkpoint factors; Linear.convert_exl3 supplies quantizer factors. Both omit the new trailing argument and retain False. The remaining unpack_bf calls are conditional branches in get_weight_tensor; ordinary construction stores su and sv as None and uses the unpacked factors instead. [source; call_d5856d3ab6214bfdb22e961fa252a890, call_3892a23823fa410b949559a192a07702, call_35722bfe67a54b5bb250a4f40a7b35e1, call_76a7342ca5a2438190f7deb3c756a22c, call_490d43c30b234fe8bb5fdb1cae46a278]

The original entry's packed-sign concern is changed rather than carried over in this data flow: the inspected parent already unpacks packed inputs into suh/svh and clears stored su/sv. The task preserves that initialization while making its expansion device selectable. forward consumes suh/svh and does not call unpack_bf, so the workaround is not a new per-forward CPU fallback. [source; call_76a7342ca5a2438190f7deb3c756a22c, call_490d43c30b234fe8bb5fdb1cae46a278]

The design trades extra device transfers during packed-factor preparation for avoiding the reported GPU operation. Keeping it opt-in preserves the existing path for other callers; successful avoidance of the assert remains the author's reported motivation, not a measured result here. [inference; call_490d43c30b234fe8bb5fdb1cae46a278]

## Uncertainty and limits

No Torch, CUDA or Transformers execution was performed. Assert avoidance, transfer overhead and GPU numerical behavior remain unverified.

Whole-tree literal searches cover named repository callers, not dynamic or external integrations. The Transformers search found evaluation wrappers, examples and dependency references, but does not establish a triggering integration or affected version.

The scalar check models integer sign expansion only; it does not exercise tensor reinterpretation, device transfers, tensor layout or torch.where.
