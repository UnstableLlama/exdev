# Verdict: commit-000323-002 (teacher gpt-6.2-sol, guidance 12, assisted retry of 323/001)

Reviewer: Fable. Date: 2026-11-18 (04:47 UTC). Upstream `544ba423` "Add Exaone4 architecture".
Run: `.teacher/runs/commit-000323-002`. Packet: `.teacher/retrieval/000323-002`.

## What I checked myself

- Request hashes 0 bad; the coverage file bound in the request is the one I filed. `check.py`: impl 45 bad [],
  evidence 95 calls 95 bad [] uncited [], final==annotation True, anc 322 entries 322 True, blobs 4570 bad 0.
  Replay 95, mismatch 1 (same refused-argument wrapper difference as 001).
- The fault in 001 is resolved from source: the entry now says the undefined-name diagnostic does not carry
  over, names the fixing commit `04dc5571` and the current `self.arch_string` expression. I confirmed both in
  source at `544ba423` (config.py 45-46; `git log -S`).
- It also re-checked the other inherited findings and says why each does or does not apply (parallel block not
  instantiated, GatedMLP has `.ups/.downs`, missing-norm failure removed by 322, SmolLM3 issue is separate).
- Everything 001 established is kept and equals my own pass over the eight configs and headers: 1.2B family
  null pattern and `len(None)` before any block is built; 32B `LLLG`, 48 local and 16 global layers, RoPE and
  window only on local layers; post-norm block with FP16 branch inputs; tied-head fallback for 1.2B and
  `lm_head.weight` for 32B; AWQ/GPTQ packed groups and FP8 `F8_E4M3` not loadable (`convert_dtype` has no such
  case, safetensors.py 15-22); SDPA assertion on a nonnegative window (attn.py 345).
- Repair (`validator-keep-rest-v2`): refused and final annotations compared as sorted JSON. 29 changed lines,
  all added evidence ids on four findings and their verification entries. No prose changed, nothing shortened.

## Must fix before canonical

- Two Source Notes paragraphs still summarise unrelated discussions; cut to one sentence.
- The entry attributes the stale diagnostic to "the Qwen3 entry"; name the entry that first recorded it.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false. Six suspected findings may go to
the ledger; split or merge against existing identities (kv sampler, prefill flag) rather than opening new ones.
