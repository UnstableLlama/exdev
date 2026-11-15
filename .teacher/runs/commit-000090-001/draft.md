# 40863d0690eb1cb1164bb973c9a22b1155ace172


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/40863d0690eb1cb1164bb973c9a22b1155ace172) · [Evidence ledger](draft.json)

Adds composable CUDA-backed history penalties and pinned-history plumbing, with intermediate-logit tests. A newly exported but undefined ComboSampler appears to block package imports.

- [History-dependent logit penalties](#sampling)

## Problem

The sampler gains history-dependent repetition, presence and frequency penalties, complementing its existing temperature and probability filters. [source; call_3aeac119b6574611ac70dbee9b92618c, call_92e4d85add8846b3b476c8d169ce215c]

## Reasoning

History requirements are declared by sampling steps and aggregated by CustomSampler. Jobs allocate pinned CPU history storage only when requested, refresh it before sampling, and pass it through SamplingState to the native functions. Requirement aggregation happens before no-op replacement, so neutral penalty steps still request history. [source; call_3aeac119b6574611ac70dbee9b92618c, call_e620a548e59e4c1fa07f9ee12aac173d, call_7acec2984c9c4b95a5c9d003209eaae8]

## Impact

The new steps support initial or already-modified unsorted logits, produce FP32 logits, and reject other sampling states. Native wrappers explicitly limit penalties to batch size one. Existing default sampler presets are unchanged. [source; call_3aeac119b6574611ac70dbee9b92618c, call_a4f179f5cacf4535b823f57ef5e8843b, call_73e1a40a59cd4b4aa3d7ccda1b9a291c]

## Source Notes

The reviewed discussions concern distinct reported problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate”; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5”; and #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022”. Their text does not establish a relationship to this penalty implementation. [source; call_3a46185c5b7048afa9fabe198d59a93c, call_d8289a2029034844961ebe89bc7d4abe, call_3572c2f91aa24ee29c2ddbedced7d915]

<a id="sampling"></a>

## History-dependent logit penalties

SS_RepP applies a sign-dependent transformation: positive logits are divided by rep_p, while nonpositive logits are multiplied. Each token uses the strongest recency weight among its occurrences, interpolating between its original and penalized logit. SS_PresFreqP subtracts accumulated weighted frequency penalties and a maximum weighted presence penalty; despite its docstring saying “Added”, positive values reduce logits. [source; call_a4f179f5cacf4535b823f57ef5e8843b, call_3aeac119b6574611ac70dbee9b92618c]

Distance counts backward from one for the newest token. sustain_range gives the full-penalty window; decay_range fades older contributions linearly to zero. Defaults use a finite 100,000,000-token sustain window and zero decay. Neutral penalties or nonpositive combined windows select SS_NoOp. [source; call_a4f179f5cacf4535b823f57ef5e8843b, call_3aeac119b6574611ac70dbee9b92618c]

Each CUDA block covers 4,096 vocabulary entries with 1,024 threads and scans history for matching IDs. Repetition uses one shared float array; presence/frequency uses two. This partitions output ownership but repeats history scanning across vocabulary blocks. [source; call_a4f179f5cacf4535b823f57ef5e8843b]

A standard-library scalar transcription reproduced the finite decay fixture [2,2,2,1.75,1.5,1.25,1,1,1,1]. Arithmetic also gives 63 blocks for 256,000 vocabulary entries and shared-array footprints of 16 KiB and 32 KiB. This was not a CUDA test. [execution; call_03dbc4f2120c4c1585185cd22b9a2305]

Bindings expose both native penalty functions. New tests supply pinned history tensors and inspect intermediate logits for repeated IDs, recency decay, a negative logit and a large vocabulary. Their presence is test coverage intent, not evidence of passing execution. [source; call_a16c6d634e5643c78462db13c770d330, call_7b5092e7c9e84fe1a5c2dd7af469f3b3, call_3fd7ca52d4604945849f14dbf59d145a]

Alongside penalties, top_k below one now selects a no-op rather than asserting. top_p equal to one also selects a no-op; the added zero branch remains inaccessible under the unchanged constructor assertion when assertions are enabled. SS_NoOp itself leaves sampling state unchanged. [source; call_3aeac119b6574611ac70dbee9b92618c, call_92e4d85add8846b3b476c8d169ce215c]

## Authoring-time findings — pending review

### missing-combo-sampler (suspected; defect)

The sampler package newly imports ComboSampler, but presets.py does not define it and the task supplies no implementation.

Trigger: Importing exllamav3.generator.sampler, once preceding imports succeed.

Expected: The sampler package imports successfully and exposes its implemented samplers.

Actual: Source inspection predicts an ImportError for ComboSampler. The top-level package imports the sampler package, and Generator and Job also import it, so the failure is not confined to users choosing a new penalty.

Locations: 40863d0690eb1cb1164bb973c9a22b1155ace172:exllamav3/generator/sampler/__init__.py — ComboSampler import

Source evidence: call_4aa5c8ae0412454bbc1d504b099e5f70, call_73e1a40a59cd4b4aa3d7ccda1b9a291c, call_1a240252d25f42b2a0ec7f7fb1da4364, call_bff5fe79111a4ccfbf11c3922924f8de, call_a51962a8afed4f1b84beb3a337816b36

source_inspection: Compared the added import with the complete parent presets module, whole-tree ComboSampler search and task diff; inspected package import reach. [call_4aa5c8ae0412454bbc1d504b099e5f70, call_73e1a40a59cd4b4aa3d7ccda1b9a291c, call_1a240252d25f42b2a0ec7f7fb1da4364, call_a51962a8afed4f1b84beb3a337816b36]. Limits: No repository import was executed; earlier environment or extension failures could occur first.

## Uncertainty and limits

CUDA kernels and repository tests were not executed. Scalar calculations do not establish GPU concurrency, floating-point edge cases or pinned-host-memory accessibility.

The source labels the methods Transformers-style and OAI-style; exact correspondence with those external implementations or the cited paper was not independently established.
