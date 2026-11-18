# Verdict: commit-000345-002

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (18:28 UTC). Run: `.teacher/runs/commit-000345-002`. Packet: `.teacher/retrieval/000345-002`.
Upstream `c3049627ea2cdbe7f0c8e62e2491e4eed8d37072` "LlamaForCausalLM: Use FP32 intermediate dtype".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 58 calls, 0 bad, 0 uncited; final equals annotation; 341 ancestors and 341 entries;
  4,743 blobs, 0 bad. No repair turn.
- Replay: 58 calls, 1 mismatch. It is a refused `evidence_index` call (`Invalid max_bytes`), the same refusal both ways, which the replay
  script reports as an exception rather than the recorded error.
- Recovery: the 345/002 manifest differs from 345/001 only in the five ancestor fields, and the only added ancestor is `c8ed45c6` (344).
- Central path, read at the commit: `interm_dtype` sets `out_dtype` for gate and up only; down keeps its own. `GatedMLP.forward` allocates a half
  destination unless `interm_dtype` is half, so both old and new settings have one. Half input with float output moves `LinearFP16` from
  `torch.matmul` to `hgemm`, whose float branch uses `cublasGemmEx` with FP32 compute. `LinearEXL3` allocates the requested dtype on both routes,
  and its 32-row rule is unchanged. `act_mul_kernel_f` multiplies in float, narrows and clamps to ±65,504; `act_mul_kernel_h` uses half2 with no clamp.
- Reach: MiMo, Mistral and Qwen2 subclass `LlamaModel` and call its constructor.
- Arithmetic: 5,632 × 2 × 3 = 33,792 bytes before, 5,632 × (4 × 2 + 2) = 56,320 after. The split threshold is 55,296.
- Pinned evidence, from replayed results: TinyLlama, Mistral-7B-v0.1 and Qwen2.5-0.5B configs match. All 22 TinyLlama layers have the three
  BF16 projections at the stated shapes, with no other MLP tensors.
- Carried findings, rechecked: both activation kernels stop at `numel / 2` pairs, so an odd length loses its last element, and normal Llama
  padding avoids it. `llama.py` never passes `sliding_window`, `Attention` defaults to -1, and the Mistral config declares 4096.
- Discussions: all seven titles match. In #52 turboderp suggested `out_dtype = torch.float` and artus-dev reported that it worked, as stated.

## Not established

No model or kernel ran, so any accuracy, speed or memory effect is unmeasured. The entry says so.

## Requested next

File the 345 ledger work with the next request, for both carried findings.

## Must fix before canonical

Keep #52. Cut the Source Notes paragraphs on #34, #53, #42, #16, #57 and #33, and the note on the calibration corpus.
