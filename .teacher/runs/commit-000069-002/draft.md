# f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5) · [Evidence ledger](draft.json)

Disables truncation on the loaded tokenizer backend before any encoding, leaving evaluation windows, calibration slices and generation context limits under caller control.

- [Disable backend truncation before caller-controlled length handling](#loading-tokenization)

## Problem

The wrapper loaded tokenizer.json without explicitly disabling backend truncation. Long-input consumers subsequently perform their own windowing, calibration slicing or context budgeting, so an earlier tokenizer-side cap could discard text before those operations. [inference; call_2e55b463add2495c93099c87c58c82c0, call_b54e861c82a34474873164df9c9c284e]

## Reasoning

The change calls self.tokenizer.no_truncation() immediately after loading tokenizer.json and the auxiliary dictionaries, before vocabulary probes or subsequent encoding. It changes the shared backend instance rather than adding separate length policies to individual encoding helpers. [source; call_f1d18b4384dc4edeb27e6666427c8215, call_2e55b463add2495c93099c87c58c82c0]

## Impact

Disabling backend truncation preserves input for caller-controlled processing, but does not enlarge model context or cache capacity. Potentially larger token lists and tensors are the corresponding memory tradeoff. [inference; call_f1d18b4384dc4edeb27e6666427c8215, call_b54e861c82a34474873164df9c9c284e, call_99e3ad3a547647a484cb22474581e847]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses low-bitrate regularization. Neither discussion identifies tokenizer truncation as its cause or links this change. [source; call_00721c137c324b3b980913637e43786b, call_6c241cf622e14d458e58fb71432f14ca]

<a id="loading-tokenization"></a>

## Disable backend truncation before caller-controlled length handling

The state being overridden belongs to the HFTokenizer loaded by HFTokenizer.from_file(<model directory>/tokenizer.json). The added call requests that this backend stop truncating encodings; it does not edit the serialized file, tokenizer_config_dict, model configuration or cache. The parent contains no tokenizer truncation override in the whole-tree truncat search. [source; call_2e55b463add2495c93099c87c58c82c0, call_f1d18b4384dc4edeb27e6666427c8215, call_273b0afc534b49df9ea88ff19a171cc4]

All nine inspected reference tokenizer.json prefixes have truncation: null: Qwen/Qwen2.5-0.5B, TinyLlama/TinyLlama-1.1B-Chat-v1.0, microsoft/Phi-3-mini-4k-instruct, mistralai/Mistral-7B-v0.1, unsloth/gemma-2-2b, and NVIDIA's Nemotron 51B-Instruct, Ultra-253B-CPT-v1, Ultra-253B-v1 and Super-49B-v1. These pinned examples therefore do not demonstrate an enabled serialized truncation policy. [source; call_48244c96c5f6428498ff7efacc10438c, call_230ec5c67e6c489c9439adcba015d7d6, call_41c4d414b71c4d78ba1c0fba9e9b4dc8, call_f1b7bf9d87254e62829e892aef65f0b0, call_c38b7aeed81b4ca0a16585490ef21e78, call_495b265576894be2b0933c76364cc001, call_5ee815336e53477b821432b009ec2369, call_2638c3a07f4f42e49721626e0a37ff3e, call_976b5c0c81bf4bf09f071c78898cd7af]

Internally, encode routes each unrestricted input string through encode_special_or_unspecial, which directly calls encode_special or encode_unspecial. Both ultimately use the same backend with add_special_tokens=False. encode then adds requested BOS/EOS and, for lists, left-pads to the longest result. No external direct calls to encode_special or encode_unspecial appeared in the search. No caller of num_tokens appeared either; that helper uses backend encode with its default special-token policy, so this change does not make its count necessarily identical to encode's output length. [source; call_4b3ccf72133147cb81fcc4ea7b7d1408, call_0afd1c1be985427583ff7096d4f0804c, call_2e55b463add2495c93099c87c58c82c0]

The earlier loading/tokenization entry already distinguished num_tokens' backend defaults from encode's explicit special-token suppression. The present change addresses truncation, not that distinction. [ancestor; call_12d2b510331e40e18c053d8d5f8b1cb3]

eval/ppl.py:get_test_tokens and eval/model_diff.py:get_test_tokens each encode the entire joined WikiText-2 test split without a pre-encoding length bound. They next select windows of 2048 tokens at stride 512, stopping at the requested row count. The former forwards each window for perplexity; the latter uses the window batch as both models' initial state. Their range excludes a start exactly equal to num_tokens - eval_len, so their immediate requirement is enough encoded text to produce a nonempty window list. [source; call_b54e861c82a34474873164df9c9c284e]

A bounded scalar transcription of that range produced zero windows at length 2048, one at 2049 and 2560, and two at 2561. Producing 100 windows requires at least 52737 tokens under the existing exclusive endpoint. These are window-arithmetic results, not measured dataset token counts. [execution; call_00c69f7bf9cc41c08823544d179e7bb8]

Calibration has two direct callers. split_art encodes an entire article or shuffled line, with no maximum text length, concatenates it into a row and explicitly keeps only columns tokens; it continues consuming articles until enough full rows exist. split_raw encodes an entire source file and selects rows consecutive columns-wide slices. It relies on sufficient source tokens rather than padding short slices. get_default_calibration applies these processors to bundled corpora, and prepare_state uses the resulting list as conversion's initial state. [source; call_b54e861c82a34474873164df9c9c284e, call_7fb04f028ae24a08823209160be081ea, call_00c69f7bf9cc41c08823544d179e7bb8]

The scalar slicing check illustrates why whole-file encoding matters: with a hypothetical 2048-token backend cap and three requested 2048-token rows, slice lengths are 2048, 0 and 0. Removing backend truncation cannot itself guarantee that a genuinely short corpus contains enough tokens. [execution; call_00c69f7bf9cc41c08823544d179e7bb8]

examples/chat.py:get_input_ids encodes the formatted system prompt plus accumulated conversation, optionally followed by <think>; these user-controlled inputs have no pre-encoding cap. It budgets encoded length + max_response_tokens + 1 against cache capacity. Once over capacity, it removes oldest conversation entries and re-encodes until the budget is at most context_length - 2 * max_response_tokens, then passes the IDs to Job. Backend truncation would precede and distort this application-level budgeting. [source; call_b54e861c82a34474873164df9c9c284e, call_8c198ff5c65a463b98b92020063a0a82]

Generator.generate has two encoding sites: a supplied string, or each string in a supplied tuple, across the prompt batch. Neither imposes a text-length bound before encoding; results go directly into Job and enqueue. eval/humaneval.py similarly encodes a dataset problem after template substitution, sometimes repeating the problem, without a local size cap, then reuses those IDs for sample jobs. [source; call_0009431714ca451f8fcaeb10ae5bf8b7, call_b54e861c82a34474873164df9c9c284e]

The other potentially long example/test inputs are bounded by their construction, not by token count. dynamic_gen.py encodes formatted fixed prompts, including sequences of up to 700 integers, and creates jobs allowing 500 new tokens. generator_stresstest.py:start_new_job encodes a counting prompt sliced to at most 8192 characters and then shortened through its last comma; its jobs request 50–2048 new tokens. Neither locally trims the encoded result. [source; call_0009431714ca451f8fcaeb10ae5bf8b7, call_b54e861c82a34474873164df9c9c284e]

Those job-based callers require nonempty CPU tensors shaped (1, n). enqueue calls prepare_for_queue, which prepares sequence pages and checks its computed page requirement against available cache pages. Consequently, retaining more input reaches explicit admission checks rather than increasing available cache. This inspection does not establish complete multi-sequence capacity correctness. [source; call_0009431714ca451f8fcaeb10ae5bf8b7, call_99e3ad3a547647a484cb22474581e847]

The remaining direct encode callers use short, fixed example text: async_generator.py:run_job receives three literal prompts and forwards IDs to AsyncJob; banned_strings.py:generate encodes one fixed formatted prompt for Job; generator.py's streaming and streaming-batched functions encode fixed instructions with a fixed system prompt for Job. generation_loop.py encodes one fixed formatted prompt, prefills all but its last token and then forwards its growing context against a fixed 2048-token batch/cache shape, with up to 500 new tokens. [source; call_b54e861c82a34474873164df9c9c284e, call_4b3ccf72133147cb81fcc4ea7b7d1408]

Search matches in standard_cal_data/code.utf8 are corpus text rather than executable wrapper callers, and job.py's string.encode calls perform UTF-32 encoding. Tokenizer initialization also calls the backend directly for single-space/newline probes and the short strings ' t' and ' '; placing no_truncation before initialization probes covers those calls as well. [source; call_4b3ccf72133147cb81fcc4ea7b7d1408, call_2e55b463add2495c93099c87c58c82c0]

## Uncertainty and limits

No tokenizer-library execution, model inference or conversion was performed. The no_truncation API's internal implementation and version-specific behavior were not available in the inspected evidence.

Reference tokenizer reads cover the top-level truncation fields, not their large vocabulary and merge payloads. None supplies a non-null truncation configuration reproducing the motivating condition.

Caller coverage is a whole-parent-tree literal search followed by source inspection; dynamic dispatch and external applications are not exhaustively established. Exact token counts depend on the selected tokenizer.

The numerical check models Python window and slice arithmetic only; it does not execute PyTorch slicing or the tokenizer.
