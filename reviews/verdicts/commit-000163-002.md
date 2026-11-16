# Verdict: commit-000163-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000163-002`
Packet: `.teacher/retrieval/000163-002`
Upstream: `830b6a018070a327d6d261628dff496f1303cf93` "Preparation for multimodal models"
Request: `reviews/requests/commit-000163-002.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only**, as a **reviewer-assisted** entry. Canonical and training remain false.
This attempt replaces the rejected 163/001, which stays as a rejected, unpublished run.

Every statement I checked is true, and the finding is correct and is the important one. All five coverage
questions are answered from the teacher's own evidence: it parsed every configuration constructor, found the one
left on the old form, read the entry that introduced that architecture, and followed the factory's callers far
enough to say that ordinary conversion fails before the compiler hook is ever reached.

Ledger candidate `exllamav3-qwen3-moe-component-migration--r001` is **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 18 of 18 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 162 strict-ancestor entries; 2,501 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 18 of 18 recorded tool calls identical, including the three `run` calls. |
| Assistance, and only that | Against 163/001 the standing instructions gain the one sentence that the coverage field holds requests, not statements of fact. The bound coverage text equals `reviews/verdicts/commit-000163-002.coverage.md` byte for byte. Provenance has `reviewer_assisted: true`. |
| No hindsight | The only packet file naming `reviews/verdicts` is the manifest, as the coverage request's path. The transcript has nothing from the 001 verdict, its reviewer-only notes or the old attempt's prose. The one occurrence of the Python error text is the output of the teacher's own stand-in run. |
| Catalog | Same bundles as 001 in a fresh packet: eleven open rows, two closed, one by path alone, nothing cut. |
| The inventory | Twelve configuration classes; eleven pass a dictionary (Llama through `derived_model` or its default, Mistral and Qwen2 through `LlamaConfig`); `Qwen3MoeConfig` passes the bare class. Matches my own reading of all twelve files at the task commit. |
| Registry against the diff | Twelve registered architectures, eleven of their files changed, `qwen3_moe.py` the one omitted; `config.py` and `model.py` are infrastructure. Correct. |
| The ancestor | `a5caa423` (position 141), which describes `Qwen3MoeConfig` handing `Qwen3MoeModel` straight to `Config`. Correct. |
| Callers | Sixteen call sites of `Model.from_config` in fifteen files at the parent: conversion (two), `model_init.init`, two evaluation scripts, six examples, one science script, three tests. The entry's list matches my search. None passes `component`. Correct. |
| Finding `qwen3-moe-component-migration` | Correct. `from_config` evaluates `component in config.model_classes` on a class, which raises `TypeError`; `compile_model` would raise on `.items()`. `get_base_model` calls the factory before any quantization, so conversion stops there. Suspected is right: shown with a stand-in class, no repository model built. |
| Everything else | The mapping, the default component, Mistral and Qwen2's class identity, the hook, shard planning and the two write paths are as in 001 and as I verified there. |
| Source notes | Issue 33's last comment before the cutoff does mention wanting the vision part of a model separated; the entry's link is labelled inference. Pull request 25 as inference. Correct. |

## Not verified

- Any model load or conversion, including the failure itself against the repository.

## Must fix before canonical use

- This entry is reviewer-assisted (seventh in force, with 39/005, 44/003, 45/002, 55/002, 71/002 and 153/002).
- It does not carry the correct finding of the rejected first attempt: the oversize warning in the new
  additional-tensor loop prints `module.key`, the previous loop's variable, not the tensor's key. I verified that
  finding at 001. It is not in any approved entry.

## Follow-ups

1. Ledger: file the warning-name observation as a reviewer-confirmed record so it is not lost: introduced at
   `830b6a01`, `compile_model`, conditional on a hook that returns a tensor larger than a shard; first seen in
   rejected run 163/001, confirmed by me from source. Excluded from teacher input.
2. The separate reviewer-observation record I asked for in the 001 verdict is no longer needed: this attempt
   found the Qwen3 MoE identity itself and the accepted record has the authoring origin.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval by hand, mark 163/001 superseded for retrieval, and record the acceptance.
2. Continue at 164 with the driver, detached.
