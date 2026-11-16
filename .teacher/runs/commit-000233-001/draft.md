# d4cdab818dfaa29854a5d218366e4c603036783a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d4cdab818dfaa29854a5d218366e4c603036783a) · [Evidence ledger](draft.json)

Adds optional ordinary-MLP output sizing while preserving default dimensions and existing alignment requirements; residual consumers remain unchanged.

- [Independent ordinary-MLP output width](#modules)

## Problem

Ordinary MLP previously fixed its down projection's output width to hidden_size, preventing independently sized outputs. [source; call_6aea68fa6011459389cd4781a90bbf86]

## Reasoning

The new optional out_size controls only the down projection. None preserves hidden_size; the up projection, activation and forward sequence remain unchanged. [source; call_6aea68fa6011459389cd4781a90bbf86, call_440d16af5d2f415a833578a581b1fd10]

## Impact

The whole-tree MLP search found one ordinary MLP construction site, in Gemma3 vision. It uses keyword arguments and omits out_size, preserving its existing dimensions. GatedMLP is unchanged. [source; call_3a15c22c2e4d4f73aadd0fe350798f96, call_d6b3e05768e743e2812d57076dcb619f, call_6aea68fa6011459389cd4781a90bbf86]

Inserting out_size before key_up changes positional binding for external callers that supplied optional arguments positionally; the inspected in-tree caller does not do so. [source; call_6aea68fa6011459389cd4781a90bbf86, call_d6b3e05768e743e2812d57076dcb619f]

## Source Notes

Read the initial modules entry and the ordinary-MLP alignment and activation entries. They establish the original projection pipeline, configurable alignment and subsequent activation selection. [ancestor; call_dd01318fb9964c56abb2705d25b53c40, call_5e2f1861aa064904ac940c3f94cf33c4, call_42f0cfac319746f9affaecf19037da51]

The earlier ignored-activation observation is no longer present: the parent selects SiLU or GELU. Its unsupported-activation observation persists because this patch changes neither selection nor forward dispatch. [source; call_440d16af5d2f415a833578a581b1fd10, call_6aea68fa6011459389cd4781a90bbf86]

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns sliced GatedMLP loading. Issues #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern quantization failures. Their relationship here is inferred only from shared mlp.py or linear.py paths; none establishes a motivation or fix for ordinary MLP output sizing. [inference; call_e3b677c26a384987aa6e9bfb29aacd59, call_dee7ec8101ee47f7bd74ec84cb497c8d, call_07b13d4dc078430aa048d7017f2d6485, call_6aea68fa6011459389cd4781a90bbf86]

<a id="modules"></a>

## Independent ordinary-MLP output width

MLP now constructs hidden_size → intermediate_size → out_size projections, falling back to hidden_size when out_size is None. Forward still applies up, the selected activation, down, and output-dtype conversion; it introduces no residual projection or output cropping. [source; call_6aea68fa6011459389cd4781a90bbf86, call_440d16af5d2f415a833578a581b1fd10]

out_size remains subject to Linear's alignment: dimensions round upward to multiples of pad_to, whose default 128 is an alignment quantum, not a token threshold. pad_to=1 preserves exact widths. Both MLP projections retain the input-padding assertion, so default alignment still requires aligned hidden and intermediate dimensions. [source; call_94f0a38ff9b7490e85d0e668293d1c4d, call_440d16af5d2f415a833578a581b1fd10]

A standard-library transcription with hidden=128 and intermediate=256 produced down dimensions (256,128) for the default output, (256,256) for out_size=130 with alignment 128, and (256,130) with alignment 1. All three satisfied the inspected input-alignment conditions. [execution; call_82ca1de1abcf42c4aa0c9c45280fc527]

TransformerBlock and ParallelDecoderBlock still add MLP results directly to their residual tensors; neither adapts the residual width. Their interfaces therefore do not generally accommodate independently sized outputs. Gemma3's existing keyword-based MLP construction retains the default equal width, while its separate multimodal Linear projection remains unchanged. [source; call_0895754ec6a94dcf949387cb5341e557, call_d6b3e05768e743e2812d57076dcb619f, call_6aea68fa6011459389cd4781a90bbf86]

## Authoring-time findings — pending review

### unsupported-activation-carried-over (suspected; defect)

Unsupported activation strings still leave ordinary MLP's activation callable unset.

Trigger: An external caller constructs an otherwise valid MLP with activation_fn="relu" and calls forward after loading its projections.

Expected: Reject the unsupported selection explicitly or provide a defined activation.

Actual: Neither match arm assigns activation_fn_call, so forward accesses a missing attribute after the up projection. The only identified in-tree constructor uses supported GELU; this trigger is limited to the exposed API.

Locations: d4cdab818dfaa29854a5d218366e4c603036783a:exllamav3/modules/mlp.py — MLP.__init__ / MLP.forward

Source evidence: call_440d16af5d2f415a833578a581b1fd10, call_6aea68fa6011459389cd4781a90bbf86, call_3a15c22c2e4d4f73aadd0fe350798f96, call_d6b3e05768e743e2812d57076dcb619f

source_inspection: Compared parent activation dispatch with the complete task diff and inspected the constructor caller and transformer consumers. [call_440d16af5d2f415a833578a581b1fd10, call_6aea68fa6011459389cd4781a90bbf86, call_0895754ec6a94dcf949387cb5341e557]. Limits: No MLP execution or external caller inspection.

## Uncertainty and limits

No model, PyTorch operation, weight loader or GPU kernel was executed. The scalar check validates dimension arithmetic only, not backend support for arbitrary widths.

Literal whole-tree searches do not establish compatibility for dynamic or external callers.
