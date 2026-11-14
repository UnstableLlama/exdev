# Verdict: commit-000071-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000071-002`
Packet: `.teacher/retrieval/000071-002`
Upstream: `e9a3b6a9256fc59f888b80a7d4a58883954b39de` "Add FP16 @ FP16 -> FP32 GEMM support, FP32 -> FP32 Had kernel, fused scales, some cleanup"
Request: `reviews/requests/commit-000071-002.md`
Reviewed: 2026-11-13, working tree on top of `41010aa`

## Decision

**APPROVED for ancestor retrieval only. Reviewer-assisted.** 71/002 is the entry in force for commit 71; 71/001 stays
rejected. The walk may continue from commit 72.

Canonical and training remain false. Whether reviewer-assisted entries may ever qualify for either is still undecided by
the user.

Every point of the thin rejection is covered, each with the teacher's own evidence: no shipped model enables the new
options and all linear outputs stay half; the before-and-after return contract; the intermediate dtype traced to a
recorded finding; packed and unpacked scales followed through construction, forward, export and reconstruction; the
extension callers including `science/`; issue 5 read and linked as inference.

## Artifacts reviewed (sha256)

- draft.json: `604ba79ccc53c0cdf08e96efaa6302d42bdb9252d2c1216da5b4fb3177bed060`
- draft.md: `49b76bec85439a498690f809f99af353cc408af44dcbd87fb663a2bd8b7da335`
- raw-transcript.json: `f85427697d3240a725376b816cf8e7d0e64ac6e05effd93cd25b6ea22d5a47a4`
- provenance.json: `2dcbdf181dd993aaab966761b3f41d627a6d42b3c4414f18e54e9438ab0bc462`
- coverage.json: `219d5e928b9605b7c9f7a5d59d377a0f00372405f1e7f7855b19c910f9cf7e49`
- packet manifest (on disk): `261c652424f9cb0a02a5e0ef704687a8b6d9472628925c407480fd4f6683e5e9`
- coverage request: `6f3b7c8bb0afe8e45552d49efcd1dbef4028dae8fdf2fe864a7a460c88259217`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 15 of 15 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; assessment is full review; 38 of 38 implementation hashes match; exactly 70 strict-ancestor entries; all 999 blobs hash to their names; the whole diff read in one call; no timestamp after the cutoff. |
| Assistance | Provenance has `reviewer_assisted: true` and binds the coverage request by path and hash. The text given to the teacher is byte-identical to my file. Standing instructions differ from the unassisted 71/001 by exactly one added sentence, the one that says the field holds requests, not facts. No reviewer-only wording from the 71/001 verdict appears anywhere in the packet. |
| Opening context, catalogs | Same as 71/001: correct. Issue 5 was fetched this time. |
| Shipped models | Verified at parent and task. `GatedMLP` is constructed in llama, gemma, phi3 and decilm with no dtype argument (mistral and qwen2 reuse llama); every `out_dtype` in the model files belongs to a norm; attention and MLP call `Linear.forward(x, params)` with no dtype. All linear outputs are half before and after. |
| Return contract | Verified against `to2` and both inner forwards at parent and task. |
| Scales | Verified. At the parent a packed-only layer kept `su`/`sv` and had no `suh`/`svh`; the task unpacks both and clears the packed attributes; `get_tensors` then writes the unpacked keys; `get_weight_tensor` is unchanged and its packed branches are no longer reached. |
| Parent and task forward paths | Verified. Parent: packed `sv` took the in-kernel output Hadamard; unpacked took a separate Hadamard and a Python multiply. Task: one path, `exl3_gemm` with no `sv`, then Hadamard with `svh` fused. |
| Extension callers | Verified. `had_r_128` only in `LinearEXL3.forward`; `exl3_gemm` there and four times in `science/qgemm_benchmark.py`, all with `sv` None. |
| Finding `fp32-mlp-intermediate-contract` | Traced independently before this attempt was written (71/001 verdict, reviewer-only note 2) and I reach the same result: the activation kernels cast to half with no dtype check, and the down projection then fails the half check on its input in `hgemm` or `exl3_gemm`. "Suspected" is the right status for source inspection without execution. |
| Execution claims | Five `run` calls. Four print or search parent-tree source files; the request reports them separately. The fifth is scalar arithmetic; replayed with identical output (3.60e-12, 65,536 words, 256 of 512 bytes). |
| Issue 5 | Quoted faithfully against the bound snapshot; the link to packed-scale loading is labelled inference. |

## Not verified

- Nothing compiled or run on a GPU, by the teacher or by me.
- The teacher had the parent tree and the diff, not a task checkout, and says so. I checked its reconstructed task
  behaviour against the real task tree; it holds.

## Must fix before canonical use

Reviewer-only.

1. The entry says the parent forward "passed only suh to the input transform, including when packed su was retained",
   and stops there. For a packed-only layer `suh` was None at the parent, so its forward applied no input sign flips at
   all, while `get_weight_tensor` (had it not raised on the tensor truth test) would have applied them. That looks like
   a parent defect for packed-scale models, present since the initial commit and repaired here by the constructor
   conversion. The entry has both facts and not the consequence. A canonical entry should state it, and it is a
   candidate for the defect ledger once someone establishes whether packed-scale models were ever published.
2. Likewise `if self.su` on a multi-element tensor raises; the entry calls it a "tensor truth test" without saying so.
3. This entry is reviewer-assisted. Its use beyond ancestor retrieval waits on the user's decision.

## Follow-ups

- Open thread, unchanged: whether `run` calls that print repository files should be counted as reads. Four of five here.
- The finding is recorded in the draft only; no ledger revision was submitted.

## Next

Record this approval (reviewer-assisted, supersedes nothing approved) and continue the walk from commit 72.
