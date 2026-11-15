# c7da6b7bb7e45ad06f168594ffb374501ba818cb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c7da6b7bb7e45ad06f168594ffb374501ba818cb) · [Evidence ledger](draft.json)

Adds ComboSampler with ordered penalties and filters and configurable temperature placement, resolving a missing export target but introducing an unusable min_p default.

- [Combined sampling preset](#sampling)

## Problem

Existing presets expose individual sampling policies; this change adds one constructor combining history penalties, temperature and probability filters. [source; call_76855d08aba145afba66aede6b266805, call_0c1f12314a274aec9acd4e56beaca701]

## Reasoning

ComboSampler delegates to CustomSampler rather than duplicating sampling execution. Its fixed order is repetition penalty, presence/frequency penalties, optional early temperature, min-p, top-k, top-p, optional late temperature, then categorical sampling. [source; call_0c1f12314a274aec9acd4e56beaca701, call_a0ae0631ddf94841861287e501b4702c]

## Impact

Adding the class resolves the existing sampler-package import of an undefined ComboSampler. It does not make default construction successful: min_p=0.0 violates SS_MinP's constructor assertion. [source; call_103f6452e2354b72a0e646a3f1c1219c, call_0c1f12314a274aec9acd4e56beaca701, call_a0ae0631ddf94841861287e501b4702c]

## Source Notes

The parent annotation identified the missing ComboSampler export target. The new definition removes that specific inherited problem. [ancestor; call_b4b99d7d21cf4ec4a5590f3e4e1d3049]

Reviewed discussions report separate problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate”; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5”; and #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022”. None identifies ComboSampler as its subject. [source; call_e95983cfeb69481788029a35ca70994c, call_4f69563ca204484e9604f60847bc3efa, call_d6340b05630f4f998a5d7d7cf5c7e52a]

<a id="sampling"></a>

## Combined sampling preset

temp_last chooses whether temperature changes filter selection or only reweights surviving candidates. SS_Temperature divides logits by temperature or raises probabilities to its reciprocal; SS_MinP compares against the maximum probability times min_p, SS_TopK retains sorted leading entries, and SS_TopP normalizes and sorts before applying its cumulative-probability mask. [source; call_0c1f12314a274aec9acd4e56beaca701, call_a0ae0631ddf94841861287e501b4702c]

A scalar illustration with probabilities [0.6, 0.3, 0.1], temperature 0.5 and min_p 0.3 retained only candidate 0 with early temperature, versus candidates 0 and 1 with late temperature. This demonstrates why placement is behaviorally meaningful. [execution; call_88a0c5dd65fe4989b482f744fb84b15b]

Both penalty stages share the sustain and decay arguments. Their documented meanings are a recent full-strength window and an older fading window; int(10e7) is a finite 100,000,000-token sustain default, with zero decay. [source; call_0c1f12314a274aec9acd4e56beaca701, call_a0ae0631ddf94841861287e501b4702c]

Neutral repetition, presence/frequency and temperature settings select SS_NoOp; top_k below one and top_p equal to one also do so. CustomSampler inserts preparation steps and executes the resulting state transformations. However, it records history requirements before no-op substitution, so a successfully constructed ComboSampler requests past IDs even when its penalties are neutral. [source; call_a0ae0631ddf94841861287e501b4702c, call_0c1f12314a274aec9acd4e56beaca701]

The convenience interface trades arbitrary step ordering for named parameters. CustomSampler remains the alternative for explicitly chosen ordering; existing CategoricalSampler and TopPSampler also retain explicit zero-temperature argmax branches that ComboSampler does not add. [source; call_76855d08aba145afba66aede6b266805, call_0c1f12314a274aec9acd4e56beaca701]

## Authoring-time findings — pending review

### combo-default-min-p (suspected; defect)

The new preset's default min_p conflicts with the existing step constructor, contradicting its comment that default parameters become no-ops.

Trigger: Construct ComboSampler() or omit min_p with Python assertions enabled.

Expected: Neutral defaults construct a sampler with min-p filtering disabled.

Actual: Stack construction calls SS_MinP(0.0), whose assertion requires 0.0 < min_p <= 1.0. AssertionError occurs before CustomSampler initialization; SS_MinP also supplies no no-op alternative. The parent-tree search finds only the package export, so reach is established for callers choosing the new constructor, not every generation workflow.

Locations: c7da6b7bb7e45ad06f168594ffb374501ba818cb:exllamav3/generator/sampler/presets.py — ComboSampler.__init__, 40863d0690eb1cb1164bb973c9a22b1155ace172:exllamav3/generator/sampler/custom.py — SS_MinP.__init__

Source evidence: call_0c1f12314a274aec9acd4e56beaca701, call_a0ae0631ddf94841861287e501b4702c, call_61212dc8b6ac4f1ab76eae19308474ab, call_103f6452e2354b72a0e646a3f1c1219c

source_inspection: Compared the new default and unconditional step construction with SS_MinP's assertion and searched the whole parent tree for ComboSampler references. [call_0c1f12314a274aec9acd4e56beaca701, call_a0ae0631ddf94841861287e501b4702c, call_61212dc8b6ac4f1ab76eae19308474ab]. Limits: No repository constructor or package import was executed.

scalar_transcription: Evaluated the constructor's scalar predicate at the new default; it returned False. [call_88a0c5dd65fe4989b482f744fb84b15b]. Limits: Checks the predicate only, not repository execution.

## Uncertainty and limits

Repository imports, tensor operations and CUDA sampling were not executed. The scalar calculation models filter mathematics, not GPU precision or sampling quality.

Whole-parent-tree literal search found only the ComboSampler export, not construction sites; external callers are unexamined.
