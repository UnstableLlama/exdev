# 81a0a7d2409ae682522b7cf051b066b6baa6f471


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/81a0a7d2409ae682522b7cf051b066b6baa6f471) · [Evidence ledger](draft.json)

Integrates HumanEval's integer top-k correction, removes its repetition-penalty option, and adds an opt-in Qwen3 empty-thinking-block prompt.

- [Integrate HumanEval sampling and Qwen3 prompting changes](#usage-evaluation)

## Problem

HumanEval parsed top_k as a float, although the enabled sampling step uses it as a slice boundary. [source; call_ee8744b53f3f4426a165e51595abbadc, call_786328ad23c94f3e892c521eec7126b8]

## Reasoning

The merge corrects the CLI type rather than changing the shared sampler, removes HumanEval's repetition-penalty control, and adds a Qwen3-specific prompt prefill. [source; call_785911ba0b1e45aa9cc52df3cd01e39a]

## Impact

Integer top-k values now reach the sampler; decimal spellings such as 5.0 are rejected. Removing rep_p preserves the neutral default but removes this script's ability to request non-neutral repetition penalties. [source; call_785911ba0b1e45aa9cc52df3cd01e39a, call_1dbcf10eb1f846ae80750bc3784c252f, call_786328ad23c94f3e892c521eec7126b8]

## Source Notes

In PR #35, gakada reports both the index-type mistake and zero scores with several repetition-penalty settings. Later discussion reports prompt-dependent scores and repetitive completions; these are contributor reports, not independently reproduced results. [source; call_13e04284b3fd49f788c8d068cea44f73, call_198cc568265c4cef805b789057e0293a, call_1bb95b027220414b8c985d6d131daf8e, call_68b64b44f7a44a41b596dba29ff7a37c]

Turboderp attributes the penalty failure to interpolation involving masked negative-infinity logits producing NaN, and subsequently says penalties can be tested on dev. This HumanEval diff itself contains no penalty-kernel repair. [source; call_d158a15bc8654bc3ab3a9f83f0030551, call_bfcd135c25034774994906297afef6fc, call_7b64c18f482e416fade4d226f351ab8a, call_785911ba0b1e45aa9cc52df3cd01e39a]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns context scaling; its connection is only inferred shared Qwen3 terminology. PR #36, “added max_total_tokens variable to class Generator, fixed type assert…”, reports a TabbyAPI missing-attribute failure. Shared generator terminology does not establish that this HumanEval change addresses it. [inference; call_2591a795d69b417a8e7404fdba47d82f, call_a163edee3f3c4dc496fdc0f11c341cd6, call_785911ba0b1e45aa9cc52df3cd01e39a]

<a id="usage-evaluation"></a>

## Integrate HumanEval sampling and Qwen3 prompting changes

The second-parent annotation describes the same three changes: integer top-k parsing, removal of the repetition-penalty control, and an empty-thinking-block Qwen3 preset. [ancestor; call_87a78f6c5ec44b2fb97ab3d37533e249]

main passes top_k directly into ComboSampler. For nonzero temperature, SS_TopK sorts candidates and masks positions starting at k; values below one become a no-op. Changing the parser and default from float/0.0 to int/0 removes the CLI mismatch. Temperature zero instead selects argmax and bypasses top-k. [source; call_ee8744b53f3f4426a165e51595abbadc, call_785911ba0b1e45aa9cc52df3cd01e39a, call_1dbcf10eb1f846ae80750bc3784c252f, call_786328ad23c94f3e892c521eec7126b8]

A standard-library transcription parsed 5 as float before the change and encountered TypeError when using it for list slicing. The revised parser produced integer 5 and a valid slice, rejected 5.0, and retained the disabled default. [execution; call_cb34b83966144aa1a2bf5c86ca581145]

Omitting rep_p selects ComboSampler's existing default of 1.0, which SS_RepP replaces with a no-op. The underlying penalty API remains available elsewhere; this is removal of a HumanEval control, not removal or repair of the shared implementation. [source; call_785911ba0b1e45aa9cc52df3cd01e39a, call_1dbcf10eb1f846ae80750bc3784c252f, call_786328ad23c94f3e892c521eec7126b8]

The opt-in qwen3 preset follows ChatML but inserts an already-closed <think> block before the assistant's code prefill. The existing path substitutes the problem into both the user request and Python fence, encodes special tokens with BOS requested, and saves generated function bodies with a four-space prefix. It does not change the default prompt selection. [source; call_785911ba0b1e45aa9cc52df3cd01e39a, call_ee8744b53f3f4426a165e51595abbadc]

The prefill steers toward immediate code completion rather than generating a reasoning stage. Discussion explicitly contrasts it with /no_think and proposes generating reasoning before injecting the function header as an alternative; that staged pipeline is not implemented here. [inference; call_785911ba0b1e45aa9cc52df3cd01e39a, call_68b64b44f7a44a41b596dba29ff7a37c, call_d158a15bc8654bc3ab3a9f83f0030551]

## Uncertainty and limits

No model generation, CUDA sampling, PyTorch indexing or HumanEval scoring was executed. The bounded check exercises argparse and Python list slicing only.

The discussion's penalty-kernel diagnosis and reported scoring differences were not independently validated; the kernel was not inspected.
