# 921f0c4155e6f74b43b74fe823f3607eea12e203


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/921f0c4155e6f74b43b74fe823f3607eea12e203) · [Evidence ledger](draft.json)

Catches KeyboardInterrupt at the main chat prompt and routes it through the existing /x command. Other reads and generation are outside the handler, and multiprocess cleanup was not verified.

- [Route an interrupted chat prompt through /x](#chat)

## Problem

In the parent chat loop, a KeyboardInterrupt raised by the main prompt read escapes main instead of following the existing /x exit path. The commit by turboderp describes the goal as a cleaner multiprocess exit; the diff addresses the prompt exception, not process management. [source; call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362]

## Reasoning

Mapping the interrupt to /x reuses the same message and loop exit as a typed command. This avoids duplicating the exit branch and limits the behavior change to the main prompt read rather than catching interrupts around the entire application. [inference; call_659a9acfc03d436c90d39474d06c1362, call_f9e4dcbe12b74dcca13771c5a073d0cb]

## Impact

If the main prompt raises KeyboardInterrupt, chat prints its usual exit message and main returns normally instead of propagating the exception. The patch installs no signal handler and adds no explicit worker shutdown, process join, or session save. [source; call_659a9acfc03d436c90d39474d06c1362, call_f9e4dcbe12b74dcca13771c5a073d0cb, call_251b5eb2dacd4a119758753a22996438]

## Source Notes

The initial usage-evaluation entry describes chat.py's original format–tokenize–generate loop. The console-extraction entry identifies read_input_ptk as the reader selected by both output modes. The clipboard-feature entry records the introduction of /x and its normal loop exit; the later interactive-controls entry describes the first-token command dispatcher the patch now feeds. [ancestor; call_caf92bbdaa954b73b9ae867b98d7cb1e, call_9d1253ea422c47c599a74a6945fc75f0, call_43b69f5074a44ef19ec45960a4ec5d3b, call_026244a1e1484ac284945bd662a37f81]

The more-commands entry records the prefilled prompt reads for /e, /sp and /ban, plus the empty-history and explicit-filename /load defects. The other entries record the clipboard feedback, code-block indexing and rich-streaming boundary defects. [ancestor; call_880ce4821f794d539808aeb819df9d4d, call_43b69f5074a44ef19ec45960a4ec5d3b, call_026244a1e1484ac284945bd662a37f81, call_9d1253ea422c47c599a74a6945fc75f0]

PR #22, “OpenAI compatible API example,” proposes an HTTP endpoint. The closest parallel is a comment's server example, which catches KeyboardInterrupt around serve_forever and closes the server in finally; the discussion also cites chat.py for prompt formatting and comparison. The shared exception and example are contextual overlap, not evidence that this PR motivated the CLI change or that the CLI now performs equivalent cleanup. [inference; call_081d416aed8f41fa9a2e98aed313b0a1, call_ce7ee3893e594a6d88955ba95aefbaca, call_659a9acfc03d436c90d39474d06c1362]

The overlap with #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #62, “Dev branch 15JUL2025 - ModuleNotFoundError: No module named 'exllamav3.generator.filter',” is the traceback's top-level `from exllamav3 import Generator, Job, model_init` in chat.py. #6 reports an extension-build assertion after the ROCm notice; #62 reports a missing packaged module. Both fail before the edited prompt read. [inference; call_16dc0c3399f94f519fdd3ba3e51d6c0b, call_5e57a5ae2107479595f920e326ff63db, call_f9e4dcbe12b74dcca13771c5a073d0cb]

#12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a quantized-model chat failure at Job construction after a prompt was entered with llama3 mode; the thread recommends ChatML. #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM',” matches chat.py's model_init.init call and reports success with a different CUDA allocator. These are matches to distinct, unchanged call sites, not evidence about Ctrl-C. [inference; call_4b581668b4ec47db919bf7fb2347b119, call_895b839e5db4489294c292f31c55ecc3, call_9fe82f5ddf174b08bd1be98a4f6cede6, call_f9e4dcbe12b74dcca13771c5a073d0cb]

#39, “Gemma 3 architecture not in list?,” asks about architecture availability and mentions chat.py in follow-up comparisons of output and loading behavior. #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” reports a Cholesky failure during conversion and suggests chat.py for testing raw weights. #52, “Error converting moonshotai/Kimi-Dev-72B,” reports conversion failures for some bitrates and later suggests the chat.py ChatML mode for a separate output-quality comparison. Their overlap is use of the same CLI, not a report of interrupted prompt input. [inference; call_f12fa97cd00b4e968154c77744e61eb3, call_0bc92e95055644b8813f9236205e4d23, call_d489f5befb1144f993e54259e620f364, call_fb38582e60174a1ea943317e339725c7, call_61547aa26b234b6fb77528684b3517fc, call_f9e4dcbe12b74dcca13771c5a073d0cb]

<a id="chat"></a>

## Route an interrupted chat prompt through /x

Basic and rich output both select read_input_ptk, which calls prompt_toolkit with the active multiline setting. The new except block replaces an interrupted top-level input read with the exact string `/x`. That string begins with `/` and produces `/x` as the first token, satisfying the same dispatch conditions as a typed exit. The parent had only the typed-command route, introduced with the clipboard commands. [source; call_251b5eb2dacd4a119758753a22996438, call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362, call_e1e3d4ac33814e8eb36d41718bea9952, call_ad922b94096c4cafabc2822cffb1bd26]

A successful read still initializes `prefix` to an empty string. An interrupted read skips that assignment, but the /x case calls print_info("Exiting") and breaks before any use of `prefix`, context insertion, tokenization, or job enqueue. Because no code follows the loop inside main, the break leads to a normal return. [source; call_659a9acfc03d436c90d39474d06c1362, call_f9e4dcbe12b74dcca13771c5a073d0cb]

The handler is local to the ordinary user prompt, not to read_input_ptk itself. The other three reads—reply editing (/e), system-prompt editing (/sp), and banned-string editing (/ban)—still pass their prefilled text to the same reader outside the try block. Startup, generation and streaming are also outside it, and exceptions other than KeyboardInterrupt from the main read are not caught by the new block. [source; call_3ebec2d206274e16acf4fe6b8f943eaf, call_707533dfd3034ecab6c2aff30edc2759, call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362]

A standard-library probe extracted the parent prompt and /x dispatch fragment, applied the task edit to a copy, and supplied stub readers. An injected KeyboardInterrupt propagated in the parent fragment but returned normally and logged `Exiting` in the edited fragment. Typed `/x` returned normally with the same message in both, and ordinary `hello` retained an empty prefix in both. [execution; call_788cc70efcfc46a38091b773920cf62f]

## Authoring-time findings — pending review

### carried-over-empty-history-retry-edit (suspected; defect)

The prompt hook leaves the existing /r and /e history access unguarded in the shared CLI loop.

Trigger: Submit /r or /e with no turns, for example just after starting chat, after /clear, or with --amnesia enabled.

Expected: Report that there is no previous turn and keep accepting commands.

Actual: Both branches index context[-1] before checking for history and raise IndexError; the new handler covers neither branch.

Locations: 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat.py — main

Source evidence: call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362

source_inspection: Checked initial and reset history, both command branches and the direct script call to main. Both output modes use this dispatcher. [call_f9e4dcbe12b74dcca13771c5a073d0cb, call_b533013259a64e7494a4f760feb183aa, call_659a9acfc03d436c90d39474d06c1362]. Limits: No interactive reproduction or external callers checked.

### carried-over-explicit-load-fallthrough (suspected; defect)

The /load dispatcher still calls the file reader only in the no-filename branch.

Trigger: Submit `/load saved.json` at the ordinary user prompt.

Expected: Attempt to read saved.json and return to command input without treating the command as a chat turn.

Actual: The extra token bypasses both load_session and continue, so the command text enters the ordinary context insertion and generation path.

Locations: 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat.py — main

Source evidence: call_f9e4dcbe12b74dcca13771c5a073d0cb, call_a773ca4020e240b5809cc3dec214c1e0, call_659a9acfc03d436c90d39474d06c1362

source_inspection: Compared the unchanged /load indentation and following context append in the loop reached by the direct script call to main. [call_f9e4dcbe12b74dcca13771c5a073d0cb, call_b533013259a64e7494a4f760feb183aa, call_659a9acfc03d436c90d39474d06c1362]. Limits: No file or model generation was exercised.

### carried-over-codeblock-index (suspected; defect)

The clipboard command still forwards negative block numbers to a helper with only an upper clamp.

Trigger: Submit `/cc -2` after a response containing exactly two matched fenced code blocks.

Expected: Reject or normalize a nonpositive block number without terminating chat.

Actual: `matches[-num]` becomes `matches[2]`, raising IndexError. The command's try block guards integer conversion, not the helper call.

Locations: 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat_util.py — copy_last_codeblock, 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat.py — main

Source evidence: call_f0d1f6028e4b4827afbc0d5e5155225f, call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362

source_inspection: The whole-parent helper search found the /cc branch as the only literal caller; inspected its unguarded call in the dispatcher shared by both output modes. [call_99089258e16c43689e22efd58b65bfbc, call_f0d1f6028e4b4827afbc0d5e5155225f, call_f9e4dcbe12b74dcca13771c5a073d0cb]. Limits: No interactive run; dynamic and external callers are not covered.

### carried-over-empty-codeblock-feedback (suspected; defect)

The clipboard command still treats an empty extracted snippet as if no block matched.

Trigger: Submit /cc with a whitespace-only last matched fenced block, assuming the clipboard write succeeds.

Expected: Distinguish an empty matched block from an absent block and report consistently with the write.

Actual: The helper strips the contents, copies an empty string and returns it; main treats it as false and reports that no code block was found.

Locations: 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat_util.py — copy_last_codeblock, 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat.py — main

Source evidence: call_f0d1f6028e4b4827afbc0d5e5155225f, call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362

source_inspection: Compared the helper's empty-string return with the truthiness test at its sole literal parent caller, unchanged by the prompt hook. [call_99089258e16c43689e22efd58b65bfbc, call_f0d1f6028e4b4827afbc0d5e5155225f, call_f9e4dcbe12b74dcca13771c5a073d0cb]. Limits: No clipboard backend was executed.

### carried-over-rich-reasoning-boundary (suspected; defect)

The unchanged rich streamer can still omit answer text that shares the closing think-tag chunk.

Trigger: In rich output with --think, a generated chunk completes the closing think tag and includes answer text after it.

Expected: Include the suffix after the tag in the rendered answer and the stored response.

Actual: The thinking branch appends the whole chunk to think_text and starts answer rendering without transferring its suffix to all_text. main then stores only all_text.strip().

Locations: 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat_console.py — Streamer_rich.stream, 921f0c4155e6f74b43b74fe823f3607eea12e203:examples/chat.py — main

Source evidence: call_251b5eb2dacd4a119758753a22996438, call_f9e4dcbe12b74dcca13771c5a073d0cb, call_659a9acfc03d436c90d39474d06c1362

source_inspection: Inspected the shared CLI loop's prefix and generated-chunk stream calls, the rich thinking branch, and the history write. The basic streamer does not take this branch. [call_44f779d86ff84e0aaeb9af02d383d031, call_251b5eb2dacd4a119758753a22996438, call_f9e4dcbe12b74dcca13771c5a073d0cb]. Limits: No model-generated chunk boundaries or terminal rendering were exercised.

## Uncertainty and limits

The bounded check injected a Python exception; it did not run the full CLI, prompt_toolkit, a real terminal, GPU inference, or a multiprocess setup. Actual Ctrl-C delivery, exit status under a launcher, and worker cleanup were not measured.

Whole-parent literal searches found no matches for `Ctrl-C`, `KeyboardInterrupt`, `multiprocess`, or `Process(`. That does not rule out external launchers, dynamic calls, or process management under other names.
