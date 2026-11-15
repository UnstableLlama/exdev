# fc543509c67605f64ab75bea590c5b91bad0e875


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/fc543509c67605f64ab75bea590c5b91bad0e875) · [Evidence ledger](draft.json)

Adds chat sampling arguments through ComboSampler, preserving default filtering while exposing invalid top-k typing and an unsupported min-p disable value.

- [Command-line sampling controls for chat](#usage-evaluation)

## Problem

The chat example previously left sampling options as a TODO and constructed jobs without an explicit sampler. [source; call_6c4292a5b63e4b068296bfecb70297b7]

## Reasoning

The change constructs one ComboSampler from command-line arguments and reuses it for each response job, exposing existing sampling machinery rather than adding new filtering implementations. [source; call_53549afdddd64c71bfec5385221b34e6, call_71d1cb55e17e4786b8d69b329a3e9d13]

## Impact

Defaults retain the previous preset's min-p threshold of 0.08 and temperature of 0.8, with temperature applied after filtering and penalties disabled. ComboSampler nevertheless requests token history because CustomSampler records history requirements before replacing neutral penalties with no-ops; Job consequently allocates a pinned history buffer. [source; call_53549afdddd64c71bfec5385221b34e6, call_71d1cb55e17e4786b8d69b329a3e9d13, call_8321d55fffcc4bad962d194a9f3cf93c, call_17c2893563c94a1fbfbcf5ceb8668f45]

The parser also removes --refresh_per_second/-rps. Whole-parent-tree search found its declaration but no consumers. [source; call_53549afdddd64c71bfec5385221b34e6, call_bbb2b806fb594975b5909653c65bb823]

## Source Notes

The preceding ComboSampler entry identified its invalid min_p=0 default. [ancestor; call_70280a96860f4fda95c9a6372a3f44db]

That constructor restriction remains unchanged. Chat avoids it with its 0.08 default, but explicitly requesting the newly advertised --min_p 0 still reaches the assertion. [source; call_53549afdddd64c71bfec5385221b34e6, call_8321d55fffcc4bad962d194a9f3cf93c]

Reviewed discussions concern “quantizing model: undefined symbol: __cxa_call_terminate” (#7), “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5” (#15), and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022” (#21). Their reported subjects are extension loading, quantization and compilation, respectively; none identifies this chat argument change. [source; call_2b1d9d8749a949809e0ad7e675e99d7f, call_fd04a1332a5d43a0974f8d18c34384d0, call_bc76d7744ca14f9da9acbd2ffbcace90]

<a id="usage-evaluation"></a>

## Command-line sampling controls for chat

Arguments flow through ComboSampler into repetition and presence/frequency penalties, optional early temperature, min-p, top-k, top-p, optional late temperature and categorical sampling. Job.receive_logits supplies logits and current token history to the sampler. [source; call_53549afdddd64c71bfec5385221b34e6, call_71d1cb55e17e4786b8d69b329a3e9d13, call_17c2893563c94a1fbfbcf5ceb8668f45]

Repetition defaults to the neutral multiplier 1; presence and frequency default to zero. The single penalty_range option, default 1024, populates both sustain and decay: it means 1024 recent full-strength tokens plus an older 1024-token fading window, not merely a 1024-token total window. [source; call_53549afdddd64c71bfec5385221b34e6, call_8321d55fffcc4bad962d194a9f3cf93c]

Min-p retains probabilities at least max_probability × min_p. Top-k masks sorted entries after K; values below one select a no-op. Top-p defaults to the no-op value 1; its active implementation retains the first candidate and masks later candidates whose cumulative probability exceeds P. [source; call_8321d55fffcc4bad962d194a9f3cf93c, call_53549afdddd64c71bfec5385221b34e6]

--temperature_first changes which candidates survive probability-based filtering, whereas the default late temperature only reweights survivors. Temperature divides logits or raises probabilities to its reciprocal. [source; call_71d1cb55e17e4786b8d69b329a3e9d13, call_8321d55fffcc4bad962d194a9f3cf93c, call_53549afdddd64c71bfec5385221b34e6]

A scalar illustration with probabilities [0.6, 0.3, 0.1], temperature 0.5 and min-p 0.3 retained only candidate 0 with early temperature, versus candidates 0 and 1 with late temperature. [execution; call_c68a5af446fd4171bbd0eedd7d930807]

## Authoring-time findings — pending review

### chat-top-k-float (suspected; defect)

The CLI parses top-k as a float, but the selected sampler uses it directly as a slice boundary.

Trigger: Run chat with an explicit --top_k value at least 1, such as --top_k 40.

Expected: Keep the requested integer number of leading candidates.

Actual: The parser produces 40.0, which ComboSampler passes unchanged to SS_TopK.run's slice. This is an invalid slice index. The default zero bypasses that step. Reach is established for the newly added chat call; parent-tree searches found only the ComboSampler definition/export and separate SS_TopK uses in presets and tests, not a universal failure of other samplers.

Locations: fc543509c67605f64ab75bea590c5b91bad0e875:examples/chat.py — --top_k argument declaration

Source evidence: call_53549afdddd64c71bfec5385221b34e6, call_71d1cb55e17e4786b8d69b329a3e9d13, call_8321d55fffcc4bad962d194a9f3cf93c, call_79f0a2119a5d4607aafb497c4909d76e, call_bd54de763e51442bbfc116c5068ac067

scalar_transcription: Parsed 40 with the same argparse float conversion and attempted a list slice, obtaining TypeError. [call_c68a5af446fd4171bbd0eedd7d930807]. Limits: Standard-library reproduction of the type mismatch, not execution of PyTorch slicing or chat.

### chat-min-p-disable (suspected; defect)

The advertised min-p disable value violates the existing step constructor.

Trigger: Run chat with --min_p 0 and assertions enabled.

Expected: Construct a sampler with min-p truncation disabled, as the new help text promises.

Actual: ComboSampler unconditionally constructs SS_MinP(0), whose assertion requires 0 < min_p <= 1. Construction fails before the chat loop. The chat default 0.08 avoids this inherited restriction.

Locations: fc543509c67605f64ab75bea590c5b91bad0e875:examples/chat.py — main, c7da6b7bb7e45ad06f168594ffb374501ba818cb:exllamav3/generator/sampler/custom.py — SS_MinP.__init__

Source evidence: call_53549afdddd64c71bfec5385221b34e6, call_71d1cb55e17e4786b8d69b329a3e9d13, call_8321d55fffcc4bad962d194a9f3cf93c, call_79f0a2119a5d4607aafb497c4909d76e

source_inspection: Traced the new chat call through ComboSampler to SS_MinP and searched the parent tree for ComboSampler callers. [call_53549afdddd64c71bfec5385221b34e6, call_71d1cb55e17e4786b8d69b329a3e9d13, call_8321d55fffcc4bad962d194a9f3cf93c, call_79f0a2119a5d4607aafb497c4909d76e]. Limits: No repository constructor executed; external callers are unexamined.

## Uncertainty and limits

No chat session, repository sampler, tensor operation or CUDA kernel was executed. The standard-library checks model scalar predicates, slicing and filter mathematics, not GPU behavior or output quality.
