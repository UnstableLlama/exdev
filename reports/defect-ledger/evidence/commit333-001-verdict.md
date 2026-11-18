# Verdict: commit-000333-001 (teacher gpt-6.2-sol, unassisted; ran ahead of 332)

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (07:05 UTC). Upstream `0460dda4` "TP: model_init args".
Run: `.teacher/runs/commit-000333-001`. Packet: `.teacher/retrieval/000333-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 46 bad [], evidence 41 calls 41 bad [] uncited [], final==annotation
  True, blobs 4614 bad 0. anc 328 entries 328 True, replay 41, mismatch 0: a complete packet.
- Run-ahead judged: this commit's parent is `3279fe18`; 332 is a later merge outside its ancestry, so no entry
  is missing and 332 could not matter.
- Diff read in full. Central claim confirmed at the sha: `model_init.py:27` adds the switch and `:138` forwards
  it; `model.py:333-340` sends `tensor_p=True` either to the single-device assertion (`:335`) or, with no device,
  past the split branch to the bare `raise NotImplementedError()` at `:387`, before any module loads. The new
  option therefore cannot load a model in tensor-parallel mode. The entry says so in its summary and tested the
  branch selection itself.
- Callers confirmed by my own grep: seven files both register and consume (humaneval, longctx, mmlu, ppl,
  batched_translation, chat, imgsearch); `ppl_transformers.py` registers only and uses `device_map="auto"`;
  `compare_q_logits.py` and `prequant_test.py` only import. No in-tree `tensor_p` forwarding through `init` and
  no caller-built namespace.
- New findings hold: `args.tensor_parallel` is read unconditionally (`AttributeError` on an old namespace), and
  `tensor_p` in `**kwargs` collides with the explicit keyword (`TypeError`). `init` documents kwargs as forwarded
  to `Model.load`, so the compatibility finding is fair. All three stay suspected.
- Inherited findings re-checked at this commit: `VariantSafetensorsCollection.__init__` sets only `main` and
  `stcs`, calls no parent constructor, and `model_init.py:149` still reads `config.stc.metrics`; `stloader.cpp:298`
  passes `bytesize / 2` and `stloader_cu.cu:51-52` converts `numel / 2` pairs with no tail. `get_load_metrics` still
  calls an undefined `get_metrics` and has no callers.
- Other source claims confirmed: GiB conversion and positive-budget selection (`model.py:367-371`), out-of-memory
  retry in `_load_autosplit`, `load` forcing `generator=False`, `-tps` as chat's `--show_tps`.
- Discussion claims checked against the recorded fetches: #61 quotes the old call and the reporter confirms the
  allocator backend fix; PR #22's example uses `add_args` and `init`; #54, #50, #48, #33, #52 and #7 are as described.
- The entry made the central check itself.
- Ledger: no record carried from 332, which proposed none.

## Must fix before canonical

- Four Source Notes paragraphs cover discussions the entry itself says do not bear on this change; keep at most a
  short #61 note.
- Mention that the commented `-tp` TODO at `model_init.py:35-36` is left in place beside the live option.
- `inherited-override-metrics` continues the ancestor's `override-load-metrics`; say so by name.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
