# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Adds DeciLM architecture dispatch and per-block attention/MLP construction, including optional branches, variable widths and compact cache indices; checkpoint compatibility remains untested.

- [DeciLM dispatch and heterogeneous block construction](#models)

## Problem

The architecture registry lacked DeciLMForCausalLM. The existing Llama constructor uses uniform attention and MLP settings, whereas the new adapter constructs branches and widths from per-block configuration. [source; call_5de3ced181bb4815921595e936d2fcb6, call_174274e0ca46472f8855afc4befc30e5, call_3d078f61ff7049a9830e644a7d7ae503]

## Reasoning

The implementation reuses shared transformer modules rather than introducing a separate execution kernel, preserving familiar checkpoint names while allowing heterogeneous blocks. [source; call_3d078f61ff7049a9830e644a7d7ae503, call_a31570fc45044da798110cf27eedecc8]

## Impact

Config.from_directory can now dispatch DeciLMForCausalLM to DeciLMConfig. This establishes architecture selection and construction logic, not verified compatibility with every Nemotron checkpoint. [source; call_5de3ced181bb4815921595e936d2fcb6, call_73a16df97e744641a62ffa999c39b395, call_3d078f61ff7049a9830e644a7d7ae503]

## Source Notes

Whole-parent searches found no Nemotron occurrence; Deci matches were unrelated calibration prose. The inspected discussion reports concern a native-extension symbol error, Qwen chat stop conditions, and missing-BOS tokenization, rather than reporting DeciLM support. [source; call_c515d56a81444078807d49d1a9dbd4b9, call_8782020fdb3147559298337727805c6d, call_4a027c1b229446c286d31601d768aa86, call_297be5ed780243fb91945186927efa5f, call_b4fb129eb89347da800f4f469422ef9e, call_c6064d18ef154d559bfd76f9d27c8ef4]

<a id="models"></a>

## DeciLM dispatch and heterogeneous block construction

The earlier architecture entry describes dispatch and checkpoint mapping through shared modules. This change extends that design with a dedicated DeciLM configuration and model pair. [ancestor; call_24f6ff4abcf74f659798c84ef820c66d]

DeciLMConfig requires block_configs to contain exactly num_hidden_layers entries. It retains global hidden width and query-head count, derives head_dim by integer division when absent or false, accepts SiLU or an omitted hidden_act, and requests the shared NEOX-style RoPE settings. [source; call_3d078f61ff7049a9830e644a7d7ae503, call_73a16df97e744641a62ffa999c39b395]

Each block reads attention and ffn dictionaries. A truthy no_op omits that branch and its norm; otherwise attention receives n_heads_in_group as num_kv_heads, while the MLP receives a block-specific intermediate width. Shared TransformerBlock.forward conditionally executes present branches with residual additions. [source; call_3d078f61ff7049a9830e644a7d7ae503, call_a31570fc45044da798110cf27eedecc8]

Active attention branches reject sink-token, linear-replacement, sparsification, unshifted-sink and prefill-window-in-sink options through assertions; active FFNs reject linear replacement and sparsification. These checks occur after the no_op decision, so omitted branches bypass them. [source; call_3d078f61ff7049a9830e644a7d7ae503]

MLP width is computed as int(2 * ffn_mult * hidden_size / 3), then rounded upward to a multiple of 256 using an added 255 before integer division. Truncation therefore precedes alignment. [source; call_3d078f61ff7049a9830e644a7d7ae503]

A scalar transcription produced widths 11008 for hidden_size=4096 and ffn_mult=4, 8192 for 4096 and 3, and 768 for 1024 and 1. Exhaustively checking intermediate integers 1 through 100000 confirmed that alignment returns a multiple of 256 no smaller than its input and adds fewer than 256 elements. [execution; call_1479fcfc61a243a9956bf3b8693b9117]

Checkpoint layer numbering remains the original block index, but attention layer_idx advances only for present attention branches. last_kv_module_idx tracks the latest attention-containing block. This separates checkpoint positions from compact cache indexing; the existing Cache constructor allocates one cache layer per model.get_cache_layers() entry rather than per configured hidden layer. [source; call_3d078f61ff7049a9830e644a7d7ae503, call_b4061cbefd684e06959cdcee2e914147]

The adapter retains model.embed_tokens, separate q_proj/k_proj/v_proj/o_proj and gate_proj/up_proj/down_proj names, final model.norm and lm_head. It preserves the tied-embedding alternate-key logic, marks the head as logits output, and delegates input preparation to prepare_for_attn. [source; call_3d078f61ff7049a9830e644a7d7ae503, call_174274e0ca46472f8855afc4befc30e5]

## Uncertainty and limits

No DeciLM checkpoint configuration, tensor header, reference implementation or model execution was available to establish checkpoint or numerical equivalence.

The width check is a Python scalar transcription, not repository model execution or a GPU test. The architectural rationale for the 2/3 multiplier and 256-wide alignment is not established by the inspected sources.

Conversion, generation quality and performance were not tested.
