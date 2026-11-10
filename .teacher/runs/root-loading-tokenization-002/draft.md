# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Loading tensors and translating text](#loading-tokenization)

## Problem

The root change introduces the boundary between model artifacts and execution: named safetensors become device tensors, while tokenizer files and control-token configuration become token IDs, padded batches and decoded text. [source; call_20390b8ede7a43feb5fdae8e5e4eebd9, call_3b88e5159896417e992145b5a4d7bc3d]

## Reasoning

Both interfaces separate metadata interpretation from bulk processing. Python resolves tensor names, shapes and offsets before native reads; the tokenizer wrapper resolves control tokens and batching around a tokenizer.json-backed engine. This keeps model-specific metadata outside the native loader, but does not reproduce every Transformers tokenizer configuration behavior. [inference; call_20390b8ede7a43feb5fdae8e5e4eebd9, call_88bb22ff3573455583cabaafa18bf654, call_3b88e5159896417e992145b5a4d7bc3d]

## Impact

Callers gain selectable native/Python tensor loading, prefix-routed model variants, explicit BOS/EOS insertion and special-token rendering. The inspected implementation also leaves important compatibility boundaries around padding, EOS filtering, added-token handling and native I/O failure cleanup. [source; call_20390b8ede7a43feb5fdae8e5e4eebd9, call_88bb22ff3573455583cabaafa18bf654, call_3b88e5159896417e992145b5a4d7bc3d]

## Source Notes

Gemma tokenizer evidence comes from unsloth/gemma-2-2b at revision 25319945f7fd83b8b903e12081777b7eef2ba993, an authorized public mirror of gated google/gemma-2-2b. Byte identity with upstream is unverified. [source; call_3c27009bec224393b56292aaf8b1f634, call_bd4b9851d3254e2c9f64b4c87f3c6d09, call_9320811537584c6eb3b54c9005efd81d, call_9fc0be27787443e7a683227f71bb0efd]

<a id="loading-tokenization"></a>

## Loading tensors and translating text

SafetensorsCollection scans *.safetensors directly rather than consulting an index JSON. read_header reads an eight-byte NumPy int64 header length, parses the following UTF-8 JSON and records the payload start. Metadata entries are excluded from the key-to-file map; later scanned files replace duplicate keys. get_tensor translates payload-relative data_offsets into absolute file offsets and asserts that shape product × element size equals the requested byte count. [source; call_20390b8ede7a43feb5fdae8e5e4eebd9]

The loader accepts I32, I16, F16, BF16 and F32. Missing required tensors raise an error; optional reads return None. BF16 is initially loaded as BF16, then converted to FP16 unless allow_bf16 is true. Prefix reads include an exact key or descendants separated by a dot. VariantSafetensorsCollection instead routes each read using the longest matching raw string prefix, allowing different tensor groups to come from different directories; its existence checks search all retained collections rather than validating that routing choice. [source; call_20390b8ede7a43feb5fdae8e5e4eebd9]

The default mt_fread path allocates a contiguous destination tensor and lazily caches five FILE handles per file. Pybind exposes stloader_open_file, stloader_read and stloader_close_file. Readers process 512 KiB blocks in stripes: worker i starts at i × block_size and advances by five blocks. Linux uses pread; the other branch uses a separate handle's _fseeki64/fread. Completed ranges enter a mutex-protected queue, and the GPU copy worker combines adjacent queued ranges before submitting cudaMemcpyAsync. [source; call_20390b8ede7a43feb5fdae8e5e4eebd9, call_88bb22ff3573455583cabaafa18bf654, call_ae55c5d675ed42a9af559dc163468a53, call_bb315f713e53464896a859a3d406e8b8]

Ownership differs by destination. CPU reads write directly into the tensor's storage. GPU reads allocate an ordinary malloc buffer for the entire tensor, populate it from disk, and copy completed chunks into the separately allocated GPU tensor on the captured current stream. The successful path joins workers, synchronizes the device and frees the staging buffer before returning. This is chunked scheduling, not bounded-size staging or direct disk-to-GPU I/O. Cached file handles remain open until close(), which resets them so later reads can reopen them. [source; call_88bb22ff3573455583cabaafa18bf654, call_20390b8ede7a43feb5fdae8e5e4eebd9]

The supported Python alternative seeks and reads into a bytearray, wraps it with torch.frombuffer, reshapes and calls .to(device); it does not use the imported mmap module. Compared with the native queue, this is a simpler whole-read path. Neither implementation establishes a speed advantage here. Loader metrics count source bytes and timed loading, report GiB/s using 1024³, and exclude the subsequent optional BF16-to-FP16 conversion. [source; call_20390b8ede7a43feb5fdae8e5e4eebd9]

A standard-library emulation checked nine sizes spanning empty input, block boundaries, the five-worker stride and a partial thirteenth block. Every size was partitioned into contiguous, nonoverlapping ranges with ceil(size / 524288) blocks and the expected worker assignment. The stride was 2621440 bytes. This verifies the small-case partition arithmetic, not concurrent I/O or transfer behavior; the source provides no measured rationale for choosing five readers or 512 KiB blocks. [execution; call_f06c193b5e1b4f86883235ef942c472a, call_ae55c5d675ed42a9af559dc163468a53, call_88bb22ff3573455583cabaafa18bf654]

The native failure path needs caution: the copy worker waits only for a nonempty queue, while a failed reader merely sets load_failed without notifying that condition variable. A read failure can therefore leave the copier asleep. load_failed is volatile rather than atomic, and TORCH_CHECK precedes staging-buffer cleanup. These are potential synchronization and resource-cleanup defects, not observed failures. The Python header parser also performs only limited validation, including no explicit file-bound or overlapping-range validation. [inference; call_88bb22ff3573455583cabaafa18bf654, call_20390b8ede7a43feb5fdae8e5e4eebd9]

Tokenizer always constructs the Hugging Face tokenizers engine from tokenizer.json. It additionally reads tokenizer_config.json and added_tokens.json, but not special_tokens_map.json or tokenizer.model. Config supplies BOS/EOS/PAD IDs from model config.json; a list-valued EOS retains its list in Config while its first entry becomes the scalar used by Tokenizer. Non-None model IDs take precedence over tokenizer-config strings or content objects. If those fields are absent, BOS/EOS default to IDs 1/2. Missing padding falls back to a truthy lookup of <pad>, then EOS when distinct from BOS, otherwise -1—not BOS as the nearby comment suggests. [source; call_3b88e5159896417e992145b5a4d7bc3d, call_b605efe605f94c61858b8ac445a508da]

Extended token mappings merge every added_tokens.json entry as special, followed by tokenizer_config added_tokens_decoder entries marked special. Non-special decoder entries are skipped; the initialized unspecial dictionaries are never populated here. encode_special uses escaped regex alternatives to insert mapped IDs between ordinary backend-encoded text segments. This manual path uses token content and IDs, not AddedToken lstrip/rstrip/normalized/single_word rules. With special handling disabled, encoding delegates to the backend with add_special_tokens=False; the wrapper itself does not force registered special spellings to become literal text. [source; call_3b88e5159896417e992145b5a4d7bc3d]

The pinned TinyLlama and Mistral configurations both map <unk>/<s>/</s> to 0/1/2. TinyLlama declares </s> as padding and requests right padding; Mistral declares no padding token and requests automatic BOS insertion. The wrapper instead always left-pads batches and defaults add_bos/add_eos to false. Thus these files supply token identities, not an automatically reproduced Transformers encoding policy. special_tokens_map.json corroborates the spellings but is not read by this implementation. [source; call_67e0041d2fd14d058cce35a6a2d24da1, call_44600a56a231473a9423b3f7b2d4dfda, call_c2f754dce73d4cda9456acad54b7bee9, call_634410ed286b48dfae41548888d8ba65, call_3b88e5159896417e992145b5a4d7bc3d]

Qwen2.5's pinned tokenizer configuration declares no BOS or unknown token, and uses <|endoftext|> at 151643 for EOS and padding. Special entries include <|im_start|>/<|im_end|> at 151644/151645, whereas tool-call and fill-in-middle entries are marked non-special and therefore skipped by the wrapper's added-token import. Phi-3 supplies an additional map covering 32000–32010, including <|endoftext|>, role markers and <|end|>; its EOS/padding is <|endoftext|>, while </s> at ID 2 is explicitly non-special. Phi's many rstrip=true entries highlight the difference between backend AddedToken behavior and the wrapper's literal regex split. [source; call_d56f4a87d068425b8e22e158b11f0bbc, call_52638cb20ad640a39d0c734bd9fbdda8, call_08561785b803475aa31ae33c291b04de, call_76a7be60da044a7cb79b4e581080bca9, call_3b88e5159896417e992145b5a4d7bc3d]

The Gemma mirror declares PAD/EOS/BOS/UNK as 0/1/2/3 and turn markers at 106/107. Its numerous non-special decoder entries, including whitespace and markup tokens, are not added to the wrapper's extended map and must be handled by tokenizer.json. The file requests left padding and automatic BOS insertion, but only left padding is inherent in this wrapper. Likewise, chat_template fields in TinyLlama, Qwen and Phi are stored in the loaded dictionary but never rendered by Tokenizer; callers must provide formatted text. [source; call_3c27009bec224393b56292aaf8b1f634, call_bd4b9851d3254e2c9f64b4c87f3c6d09, call_9320811537584c6eb3b54c9005efd81d, call_9fc0be27787443e7a683227f71bb0efd, call_44600a56a231473a9423b3f7b2d4dfda, call_d56f4a87d068425b8e22e158b11f0bbc, call_76a7be60da044a7cb79b4e581080bca9, call_3b88e5159896417e992145b5a4d7bc3d]

encode adds caller-requested BOS/EOS, left-pads to the longest sequence and optionally returns negative padding lengths. A scalar input produces shape (1, length). padding_mask compares IDs with pad_token_id, multiplies an integer mask by -65505 × 2, then casts to half. This targets a zero/unmasked versus negative-infinity/masked additive bias; sharing PAD with EOS also makes EOS positions match that mask. No tokenizer-config maximum length is enforced in encode. [source; call_3b88e5159896417e992145b5a4d7bc3d]

The bounded calculation reproduced left padding [[11], [12,13,14]] as [[0,0,11], [12,13,14]] with offsets [-2,0]. It also decoded binary16's maximum finite value as 65504 and calculated the mask's integer bias as -131010, confirming that the magnitude exceeds half's finite range. It did not execute PyTorch's conversion to infinity. [execution; call_f06c193b5e1b4f86883235ef942c472a]

decode_ without special rendering removes PAD, out-of-backend-vocabulary IDs and every EOS before its attempted EOS truncation, so the truncation branch cannot find EOS. Special rendering still removes PAD and IDs beyond the backend vocabulary, then renders mapped special pieces explicitly. Consequently, extended IDs can be represented in lookup tables yet be discarded by decode_. Also, decode returns a list for any rank-two tensor, including a one-row tensor, rather than following its documented batch-size-one string rule. [source; call_3b88e5159896417e992145b5a4d7bc3d]

A literal emulation of the ordinary decode filter transformed [11,2,12,0,99], with EOS=2, PAD=0 and vocabulary size 50, into [11,12]. The token after EOS survived. This checks the filtering order only; it neither invokes the backend decoder nor tests generation stopping. [execution; call_f06c193b5e1b4f86883235ef942c472a]

Tokenizer eagerly builds decoded-piece tables, a reverse piece map and an ordinal table. Piece enumeration probes ' t' to decide whether a space prefix is needed to preserve leading whitespace during single-token decoding; prefix queries then scan the piece table and cache up to 1000 results. These are local interfaces for token/text consumers, not a complete byte decoder: get_id_to_ord_list stores token_to_id results for backend-vocabulary entries, applying its byte-ordinal conversion only to appended entries. num_tokens also calls backend encode with defaults, unlike encode's explicit add_special_tokens=False calls. [source; call_3b88e5159896417e992145b5a4d7bc3d]

Related chapters: models (assembly link pending), quantized-inference (assembly link pending), generation (assembly link pending), sampling (assembly link pending), runtime (assembly link pending), usage-evaluation (assembly link pending)

## Uncertainty and limits

No real tensor payload loading, CUDA transfers, tokenizer round trips or throughput measurements were executed. The successful run checks only bounded standard-library emulations of inspected arithmetic and filtering.

The tokenizer configuration files were read completely; the large tokenizer vocabularies, merges and tokenizer.model files were not. Backend special-token matching and architecture-wide tokenization equivalence remain unverified.

The scalar checks use small Python integers without native overflow and inspect binary16 representation without executing PyTorch's half conversion. They do not test native threading, buffer ownership or CUDA synchronization.

Native loader failure-path risks are source-derived, not reproduced failures. Gemma mirror equivalence to the gated upstream remains unverified.
