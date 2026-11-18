# 1385615f4b993b1e6c1ba210eee081bfa2ea35bc


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1385615f4b993b1e6c1ba210eee081bfa2ea35bc) · [Evidence ledger](draft.json)

The shared ProgressBar now asks Rich to use a ten-minute speed-estimation period for enabled bars. The patch changes the ETA setting, not the work being counted or the converter's separate module-level estimate.

- [Set a shared speed-estimation period for progress bars](#runtime)

## Problem

Before this change, the shared progress bar displayed elapsed and remaining time but left the speed-estimation period to Rich's default. The commit describes a settings tweak, not a fix for a reported error. [source; call_e95e14cf3e194e13a69d74517f60b560, call_768ee54a9fa947a394937cb77bad5788, call_ad76a0c1a06d479e92c2514b4493643f]

## Reasoning

Setting the period once in the wrapper gives every enabled bar the same policy without changing callers. A ten-minute speed-estimation window can make the ETA less sensitive to brief bursts or stalls, at the cost of reacting more slowly to a lasting change in throughput. That is a likely rationale, not a measured effect. The setting targets speed estimation, not the display refresh rate. [inference; call_ad76a0c1a06d479e92c2514b4493643f, call_e95e14cf3e194e13a69d74517f60b560, call_cefc995e2de540f584a7b5622547cd99]

## Impact

Direct users include model loading, conversion capture and forward passes, EXL3 quantization, and several evaluation and example scripts. The keyword is passed only when the bar is enabled: single-device loading and autosplit both pass None when progress display is disabled. The patch does not change work counts, model placement, quantization arithmetic, or the converter's separate printed module-level ETA. [source; call_aae8978cea244c938725ecb794264375, call_411859c7305b4cdda3ee663f5ac0c1eb, call_057e58134c93476e8c9ecd827b86a2a1, call_ad76a0c1a06d479e92c2514b4493643f]

## Source Notes

The initial commit's runtime chapter describes ProgressBar as a Rich wrapper that is inactive for empty text and marks non-transient bars complete on exit. The later “More feedback from conversion” entry describes reusing one progress task across conversion phases and distinguishes the separately printed module-level ETA. [ancestor; call_764881dc09874ec8a777d510ffbc9959, call_db5f624f0bed4936b9fba746b5395be2]

The older conversion entry recorded a negative-minute formatter defect. The parent source already uses floor division after rounding seconds, so that specific defect is not carried into this patch. The formatter and its conversion caller are separate from the Rich constructor change. [source; call_db5f624f0bed4936b9fba746b5395be2, call_a8fbc724bf214077b90a30229b97921b, call_438870f7328a4ea589e7aab1ec7fce30, call_ad76a0c1a06d479e92c2514b4493643f]

Running the parent repository's human_time function in isolation returned “29 minutes”, “30 minutes”, and “1 hour, 30 minutes” for 1,770, 1,800, and 5,400 seconds, respectively. This checks the old formatter examples, not conversion execution. [execution; call_d976fa85a85d4045b6bbb335ab4224cc]

Issue #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM'”, shows a traceback through the autosplit loader that uses this wrapper. Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI)”, reports the same error text raised by that loader. The overlap is the loading path, not the cause: the patch changes Rich construction, not the out-of-memory branch. In #61 the reporter credited an allocator change with getting the model to load. [inference; call_e1b250add2474a71a89ed85296c33b48, call_4802e2826d9e4fb78509d425ff7472b2, call_411859c7305b4cdda3ee663f5ac0c1eb, call_ad76a0c1a06d479e92c2514b4493643f]

Issue #19, “Any chance of a single model file?”, discusses tweaking model configuration in the context of keeping the Hugging Face directory format. The wording overlaps the commit title, but the subject is checkpoint packaging, not progress estimation. [inference; call_64dcd6e27dca43dfba6a52cfa1662b50, call_ad76a0c1a06d479e92c2514b4493643f]

Other discussion matches do not explain the Rich setting. Issue #7 (“quantizing model: undefined symbol: __cxa_call_terminate”) names model.py in an import traceback; #33 (“Error converting model”) shows the separate printed ETA before a file-opening failure; #34 (“torch._C._LinAlgError on last layer of quant”), #42 (“converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values”), and #52 (“Error converting moonshotai/Kimi-Dev-72B”) trace failures through quantize_exl3 into factorization. PR #26 (“Superior 3INST parameters”) concerns decoder parameters, and #53 (“Command A support”) asks about model and quantized checkpoint availability. Issue #48 (“`RuntimeError` when requesting logprobs with Gemma 3 models”) reports a tensor-size mismatch, not the loader failure or an ETA problem. [inference; call_97ccc679af6f478fb213a79265f5f07c, call_bbe6a9ba61864eecbd156c15aec29567, call_b73f44d2aac64881996d09c4117f7b2f, call_057e58134c93476e8c9ecd827b86a2a1, call_7537620e4dd9440fb2e723b7bdc63388, call_e25952c4895a4b50908dddfde089ff58, call_993ac5e4b6ca4123b1bd002eb97b824a, call_dc4d539b65e24f8b956b03a91997018d, call_9f5d61da6bba4458a629f433d29c2a0c, call_3471fc9ae1b54d06a29358baaaabb4c3, call_5387eaf1c54b4c2c8f68ab07c8b80a72, call_ad76a0c1a06d479e92c2514b4493643f]

<a id="runtime"></a>

## Set a shared speed-estimation period for progress bars

ProgressBar.__init__ now passes speed_estimate_period=600.0 to rich.progress.Progress when the label is truthy. It still creates one task with the caller's total, retains the description, bar, percentage, elapsed-time and remaining-time columns, and forwards the transient flag. Updates still report an absolute completed count rather than an increment. [source; call_ad76a0c1a06d479e92c2514b4493643f, call_e95e14cf3e194e13a69d74517f60b560]

EXL3 quantization keeps one wrapper instance: it starts with a total of 100 for preparation, sets completion back to zero, then changes the existing task's label and total to the number of input tiles. The new constructor setting belongs to that same Rich instance in both phases; the patch adds no explicit speed-history reset at the transition. [source; call_5387eaf1c54b4c2c8f68ab07c8b80a72, call_72de20d610ec422daf9f7b5851da6eed, call_e95e14cf3e194e13a69d74517f60b560, call_ad76a0c1a06d479e92c2514b4493643f]

A standard-library check ran the parent wrapper and the wrapper with the one-line patch against a recording stand-in for Rich. Both transient settings forwarded 600.0 only in the patched wrapper, and a None label constructed no bar in either version. The check also converted 600 seconds to ten minutes. It did not run Rich's estimator or render a terminal bar. [execution; call_cefc995e2de540f584a7b5622547cd99]

## Uncertainty and limits

Rich itself was not run. The inspected requirements list Rich without a version pin, and no approved Rich reference was retrieved. The previous numerical default, version compatibility, exact sample retention and reset behavior, and observed ETA stability remain unverified.

The commit does not explain why 600 seconds was chosen over a shorter or longer period.
