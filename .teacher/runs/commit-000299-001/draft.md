# e370ed289d76f51d62e7300a213d64a4484355f3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e370ed289d76f51d62e7300a213d64a4484355f3) · [Evidence ledger](draft.json)

Adds cached trie searches and marisa_trie dependencies. Source inspection identifies incorrect exact-key selection, missing cache invalidation and unchanged metrics incompatibilities; scalar checks are reported separately.

- [Cached tensor-name prefix indexing](#loading)

## Problem

Several collection operations scanned every tensor name to select an exact prefix and its dot-separated descendants. [source; call_b2c1b1b37440485bb48f0e0c63ea07e4]

## Reasoning

Caching a tensor-name trie appears intended to reduce repeated prefix-search work. The source establishes the mechanism, not a measured performance improvement. [inference; call_27fb6264a2d54ac88cdac7ff6197a9a8]

## Impact

Both dependency declarations add marisa_trie, matching the helper's local import. A whole-parent-tree search for marisa found no existing occurrence; dynamic and external imports remain outside that result. [source; call_3c9e21f6d2a0454893befc1edf6d2703, call_fadf4be3ba6b40a69aaf8aecba19caba, call_4a67ab37dc4d4a21bfeb3e05e092b6af, call_27fb6264a2d54ac88cdac7ff6197a9a8]

## Source Notes

The root loading-tokenization entry establishes the original exact-or-dot-descendant contract. The tensor-override entry establishes main-based enumeration and wildcard source routing, and records inherited metrics incompatibilities. [ancestor; call_00d8de693314412ba20b77171595a5d7, call_3de2ee97a354494fb955e3787e257e96]

Issue #33, “Error converting model,” reports a file-opening failure through compile_model, get_tensors and get_tensor. Its connection to this change is inference from matching functions, not evidence that trie indexing fixes that failure. Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” instead concerns tensor padding. [inference; call_a68cb7aa0fa843939d90a068fb026a88, call_797f3df9c17b4f3c842434bf56e363b1, call_9a0ec88af1cf40eca54c290b68da2898, call_27fb6264a2d54ac88cdac7ff6197a9a8]

<a id="loading"></a>

## Cached tensor-name prefix indexing

get_tensor_file_map_trie imports marisa_trie on demand and constructs Trie(self.tensor_file_map.keys()), retaining the result with lru_cache. The trie indexes names; filenames and metadata remain in the existing dictionaries. [source; call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4]

Ordinary list_tensors and get_tensors, plus variant get_tensor_sizes and list_tensors, now query trie.keys(prefix + '.'). Ordinary get_tensor_sizes and variant get_tensors retain their full scans. Thus the change does not uniformly replace every prefix selector. [source; call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4]

Variant queries still enumerate main's namespace and resolve each selected name through find_stc; replacement-only names remain outside bulk enumeration. The added ordinary find_stc returns self. Parent-tree find_stc references were confined to the variant implementation and supplied tensor-name strings. [source; call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4, call_eff620e53b4e41da937e54b6c7708898]

compile_model obtains module sizes before reading each module's tensors through get_tensors(prefix, allow_bf16=True). Model.get_storage_info uses get_tensor_sizes for unloaded modules. These consumers retain string module prefixes and do not compensate for the changed selectors. [source; call_9a0ec88af1cf40eca54c290b68da2898, call_cbc0c84b251246889f6f7539a598b56d, call_27fb6264a2d54ac88cdac7ff6197a9a8]

The retained index introduces a coherence requirement because add_tensor_files can mutate the name map. Keeping live scans avoids that requirement; using a cached trie requires invalidation or an immutable-map contract, neither supplied by this diff. [inference; call_b2c1b1b37440485bb48f0e0c63ea07e4, call_27fb6264a2d54ac88cdac7ff6197a9a8]

A Python transcription selected a filename for an exact tensor prefix and raised KeyError when using it as a tensor-map key. A separate cached-snapshot model omitted a newly added descendant that live-map enumeration included. [execution; call_ed46dd336dbc40e78f854f595458e2c8]

The inherited metrics incompatibilities are carried over: the variant constructor initializes only main and stcs, shared initialization accesses config.stc.metrics, and Model.get_load_metrics calls get_metrics, which neither collection defines. The task diff does not change these interfaces. [source; call_b2c1b1b37440485bb48f0e0c63ea07e4, call_1c831e16b2714f0cbfe475066dcfb4cc, call_cbc0c84b251246889f6f7539a598b56d, call_27fb6264a2d54ac88cdac7ff6197a9a8]

## Authoring-time findings — pending review

### exact-prefix-uses-filename (suspected; defect)

All four rewritten selectors append the mapping value rather than the exact tensor name.

Trigger: Supply a prefix equal to a stored tensor key whose mapped filename is not itself a tensor key.

Expected: Include the exact tensor, preserving the previous equality predicate.

Actual: Metadata listing indexes the map with a filename and raises KeyError; bulk loading and variant size lookup pass the filename to required tensor lookup and raise a missing-tensor error.

Locations: e370ed289d76f51d62e7300a213d64a4484355f3:exllamav3/loader/safetensors.py — SafetensorsCollection.list_tensors / get_tensors; VariantSafetensorsCollection.get_tensor_sizes / list_tensors

Source evidence: call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4

source_inspection: Compared all four replacements with map construction and downstream lookups. Whole-tree searches located direct callers; inspected compilation and storage-statistics consumers supply module prefixes. [call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4, call_98d9c15439e34ed3b9710912a036474f, call_c7bfe862abf14d918133c895ce1d2e79, call_db43bff873c140c2a784f9d5fd8b9faf, call_9a0ec88af1cf40eca54c290b68da2898, call_cbc0c84b251246889f6f7539a598b56d]. Limits: Conditional API reach; no concrete checkpoint collision was demonstrated.

scalar_transcription: Transcribed exact-prefix selection with a synthetic tensor-to-filename map and observed KeyError. [call_ed46dd336dbc40e78f854f595458e2c8]. Limits: Did not execute repository code or marisa_trie.

### cached-index-after-additions (suspected; defect)

add_tensor_files does not invalidate the cached trie.

Trigger: Build the trie, add files containing new descendant names, then repeat a trie-backed query before cache eviction.

Expected: Include newly added names, as the previous live-map scan did.

Actual: The retained trie omits additions although dictionary-based lookup can see them.

Locations: e370ed289d76f51d62e7300a213d64a4484355f3:exllamav3/loader/safetensors.py — SafetensorsCollection.get_tensor_file_map_trie / add_tensor_files

Source evidence: call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4

source_inspection: Compared cached construction with map mutation and searched add_tensor_files callers. The evaluation helper adds overrides before model loading, so that inspected caller does not establish the problematic ordering. [call_27fb6264a2d54ac88cdac7ff6197a9a8, call_b2c1b1b37440485bb48f0e0c63ea07e4, call_1b1bef23dfca48f2a15cd9df1a7555af, call_d82ac1920b514a24ad24d97f70f4ea5e]. Limits: Public-method sequence, not a demonstrated shipped-workflow failure.

scalar_transcription: Modeled a cached name snapshot followed by dictionary mutation. [call_ed46dd336dbc40e78f854f595458e2c8]. Limits: Snapshot model, not trie-library execution.

### carried-metrics-interface (suspected; defect)

Inherited metrics consumers remain incompatible with collection interfaces.

Trigger: Reach shared initialization's metrics block with a variant collection, or call Model.get_load_metrics.

Expected: Print or return loader metrics.

Actual: The variant lacks metrics; ordinary and variant collections lack get_metrics, producing attribute lookup failures.

Locations: e370ed289d76f51d62e7300a213d64a4484355f3:exllamav3/loader/safetensors.py — VariantSafetensorsCollection.__init__

Source evidence: call_b2c1b1b37440485bb48f0e0c63ea07e4, call_1c831e16b2714f0cbfe475066dcfb4cc, call_cbc0c84b251246889f6f7539a598b56d, call_27fb6264a2d54ac88cdac7ff6197a9a8

source_inspection: Compared constructors and collection APIs with both metrics consumers and the task diff. Searches found only the get_load_metrics definition and shared initialization's metrics.print call. [call_b2c1b1b37440485bb48f0e0c63ea07e4, call_1c831e16b2714f0cbfe475066dcfb4cc, call_cbc0c84b251246889f6f7539a598b56d, call_27fb6264a2d54ac88cdac7ff6197a9a8, call_ce15c9ba92fa4df286f6c54a851c33ee, call_e6e640ed668a44908e8d0c5062f4c922]. Limits: Carried-over conditional failures, not introduced by trie indexing and not executed.

## Uncertainty and limits

No repository loader, marisa_trie implementation, checkpoint I/O or GPU code was executed. The Python check transcribed selection logic and modeled a cached snapshot.

Trie ordering, construction cost, memory use and measured search improvement remain unverified.

Literal caller searches do not establish external compatibility. No inspected checkpoint demonstrates an exact-prefix collision in a shipped workflow.

Only opening portions of discussions #7, #26, #33, #34, #42, #48, #52, #53, #55 and #58 were inspected; those reads do not establish this change's motivation.
