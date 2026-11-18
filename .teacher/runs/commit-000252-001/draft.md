# 849c62fc6d0c634984f07f264b1564d515711910


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/849c62fc6d0c634984f07f264b1564d515711910) · [Evidence ledger](draft.json)

Makes LinearEXL3's unused config argument explicitly nullable without changing its required position, callers or runtime computation.

- [Declare nullable configuration without changing construction](#quantized-inference)

## Problem

LinearEXL3 declared config as Config even though its constructor never reads or stores that argument. [source; call_62aca3bcbdb4496a84d02899a1e99db2]

## Reasoning

The cleanup changes only the annotation to Config | None, making the declared interface agree with the argument's unused status rather than removing a positional parameter. [source; call_cbb9f1ebb5714e2496f7d3636700178d, call_62aca3bcbdb4496a84d02899a1e99db2]

## Impact

None becomes explicitly permitted by the annotation, but config remains required: no default is added. Tensor validation, initialization and inference code are unchanged. [source; call_cbb9f1ebb5714e2496f7d3636700178d]

## Source Notes

Closed issue #11, “AssertionError: bias is wrong datatype,” reports a conversion failure and subsequent successful fix. Its connection here is inferred solely from its traceback naming LinearEXL3.__init__; this annotation-only change does not alter bias handling. [inference; call_f8dbdcf93b9740ed9f045d89f7254008, call_cbb9f1ebb5714e2496f7d3636700178d]

<a id="quantized-inference"></a>

## Declare nullable configuration without changing construction

LinearEXL3.__init__ changes config: Config to config: Config | None. The constructor does not dereference config or assign self.config; its state comes from dimensions, quantization tensors, bias and output dtype. Accepting None therefore requires no new runtime branch. [source; call_cbb9f1ebb5714e2496f7d3636700178d, call_62aca3bcbdb4496a84d02899a1e99db2]

Whole-parent-tree search finds two direct construction sites, both in Linear: load_exl3 passes self.config with loaded tensors, and convert_exl3 passes self.config with quantizer outputs and the original bias. Both remain compatible; neither is changed to pass None. Other matches are imports, the class definition and an isinstance check, not additional constructors or subclasses. [source; call_7b9e2a29e47d4567a5198b3f2638c6d9, call_64916931b83640f086c26f87cee60f7c]

Retaining the argument preserves those positional calls while relaxing the declared type. This is interface cleanup, not evidence of a new configuration-free loading workflow: Linear.load_exl3 still reads checkpoint tensors through self.config.stc before construction. [inference; call_cbb9f1ebb5714e2496f7d3636700178d, call_64916931b83640f086c26f87cee60f7c]

The earlier quantized-inference entry establishes the loading/reconstruction interface and records incomplete packed-sign support in its historical implementation. [ancestor; call_b9e5981c7fe74f8c9074916f04c0783b]

That historical Python packed-sign concern is changed in the inspected parent: construction unpacks supplied su/sv into suh/svh and stores su/sv as None, so forward receives unpacked factors and get_weight_tensor avoids truth-testing stored packed tensors. The task leaves this initialization unchanged; this inspection does not validate GPU execution. [source; call_62aca3bcbdb4496a84d02899a1e99db2, call_cbb9f1ebb5714e2496f7d3636700178d]

## Uncertainty and limits

No repository execution or type-checker validation was performed. This annotation-only change offers no useful numerical computation to validate.

Literal whole-tree searches establish the named construction sites, not dynamic or external callers.
