# f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5) · [Evidence ledger](draft.json)

Disable backend tokenizer truncation during construction so serialized limits do not silently shorten inputs before calibration or other encoding consumers.

- [Disable inherited tokenizer truncation at load time](#loading-tokenization)

## Problem

A loaded tokenizer could retain a serialized truncation policy. Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports conversion failure; turboderp attributed it to a tokenizer.json limit of 4096 tokens, insufficient for calibration. [source; call_b0d2b9e22f97419aa500177d2672662a]

## Reasoning

The constructor now calls self.tokenizer.no_truncation() after loading the backend and auxiliary JSON files, before any vocabulary-probing encodes. This applies the policy once to the shared backend rather than modifying individual encoding calls. [source; call_cef9aa18f1124bff9e5389a0470ede9f, call_ba076f29ebee4910a6e6fc364ae46560]

## Impact

The override covers backend encoding used by ordinary and special-token paths, initialization probes, and num_tokens. Wrapper-level BOS/EOS insertion, batch padding and explicit calibration slicing remain unchanged. [source; call_cef9aa18f1124bff9e5389a0470ede9f, call_ba076f29ebee4910a6e6fc364ae46560, call_1fc36ecd4fd24cd59ab485b11e2b93d8]

Disabling backend truncation preserves input for downstream length management, but can increase tokenization output size and memory use when a serialized limit previously applied. It does not expand model context capacity. [inference; call_cef9aa18f1124bff9e5389a0470ede9f, call_ba076f29ebee4910a6e6fc364ae46560]

## Source Notes

The connection to issue #16 is inferred from its explicit tokenizer-truncation diagnosis and final comment about overriding the feature at load time, matching this constructor change. DekoMoon reported the failure; turboderp supplied the diagnosis. The discussion is not a locally reproduced conversion result. [inference; call_b0d2b9e22f97419aa500177d2672662a, call_cef9aa18f1124bff9e5389a0470ede9f]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns native-extension loading. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns low-bitrate quantization and regularization. Neither discussion identifies tokenizer truncation as its cause. [source; call_3197f4e871b74b55bc7ce1d09f39e0df, call_0556697311394d05a6e4a3790ca69e77]

The earlier tokenizer entry describes absence-safe BOS/EOS lookup. Those guards remain in the inspected parent and are not changed here. [source; call_ba076f29ebee4910a6e6fc364ae46560, call_cef9aa18f1124bff9e5389a0470ede9f]

<a id="loading-tokenization"></a>

## Disable inherited tokenizer truncation at load time

Tokenizer loads tokenizer.json through HFTokenizer.from_file and reuses that object throughout encoding. The new unconditional no_truncation call overrides backend truncation in memory; it does not rewrite tokenizer files or expose a per-call opt-in. [source; call_ba076f29ebee4910a6e6fc364ae46560, call_cef9aa18f1124bff9e5389a0470ede9f]

Calibration's split_raw encodes an entire text before slicing successive column-width rows. get_default_calibration uses this path for code and technical text, with weights 15 and 10 out of a total 128. A backend cap therefore acts before calibration chooses its rows. [source; call_1fc36ecd4fd24cd59ab485b11e2b93d8]

A standard-library slice model using the report's 100 rows, 2048 columns and 4096-token cap produced 11 requested code rows and 7 technical rows. Each had only two full slices, with remaining slices empty; full allocations would require 22528 and 14336 tokens respectively. [execution; call_d71bed89ff9c417d9a66fc112cddbf8c]

This supports the reported calibration-shortage mechanism without establishing the CUDA failure chain. Compared with the discussion's alternatives—editing truncation to null or replacing tokenizer.json—the constructor override centralizes the policy and leaves model assets untouched. [inference; call_b0d2b9e22f97419aa500177d2672662a, call_cef9aa18f1124bff9e5389a0470ede9f, call_1fc36ecd4fd24cd59ab485b11e2b93d8, call_d71bed89ff9c417d9a66fc112cddbf8c]

## Uncertainty and limits

No real tokenizers backend, complete tokenizer initialization, conversion or GPU workload was executed. Backend implementation and version-specific API behavior were not independently inspected.

The scalar check models calibration slice lengths only; it neither reproduces the reported CUDA error nor proves conversion succeeds after the change.
