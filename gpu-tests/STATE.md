# GPU test worker state

## Machine
- GPU: 2x NVIDIA GeForce RTX 3090 (24 GB). **The worker uses physical GPU 1 only** (`CUDA_VISIBLE_DEVICES=1`, `TORCH_CUDA_ARCH_LIST=8.6`), by the user's instruction. Exception: the user allowed both GPUs on 2026-11-19 for tests that need two devices (kernel-attribute-cache-device); `h.py run --gpus 0,1`.
- Driver 580.126.09; nvcc 12.8 (`/usr/local/cuda-12.8`). Torch builds must be CUDA 12 (cu126 or cu128), by the user's instruction.
- OS: Linux 6.8.0-94-generic. Python: 3.12.3 (system), 3.11.15 (uv). 8 CPU threads, 125 GB RAM.
- Disk: /home had only 44 GB free at start. Watch it; keep models small.

## Working area (outside the repository): `/home/unstable/exdev-gpu-work`
- `upstream.git`: bare clone of exllamav3. `wt/`: per-commit worktrees, removed after each test.
- `bin/cleanenv`: runs a command with an empty environment (no credentials), a private HOME, GPU 1 only.
- `lib/h.py`: harness (`new`, `run`, `finish`). `lib/rt.py`: reporting helper copied beside each repro.py.
- `extcache/`: native extension builds keyed by environment and extension tree hash.

## Environments built
- `py311-81fd62ef04f7-torch26cu126`: Python 3.11, torch 2.6.0+cu126, flash-attn 2.7.4.post1 (built for sm_86), numpy 2.1.3, tokenizers 0.21.1, safetensors 0.5.3.

- `py312-superset-torch26cu126`: Python 3.12.3, same pins. Needed where a commit calls `int.is_integer` (absent on 3.11).
- Both environments also hold the union of every requirements.txt variant in the queue (pillow, pyyaml, marisa_trie, kbnf, formatron, tabulate) plus prompt_toolkit and pyperclip, instead of one environment per requirements hash. transformers is deliberately absent. A finding about a missing or undeclared dependency needs a fresh environment.
- `deps/human-eval`: openai/human-eval at b9453e8f1865df0a0057a1383767caa400acfbcf, on the path through a .pth file (needed by eval/humaneval.py).

## Models (`models/`, unquantized)
- Qwen/Qwen2.5-0.5B-Instruct at 7ae557604adf67be50417f59c2c2f167def9a775: the default fixture. Hidden size 896 is a multiple of 128.
- HuggingFaceTB/SmolLM2-135M-Instruct at 12fd25f77366fa6b3b4b768ec3050bf629380bac: does NOT load (hidden size 576 fails the 128-multiple assertion in linear.py). Do not use it.

## Notes for the next session
- `lib/chatdrv.py` drives examples/chat.py through a pseudo-terminal. Copy it beside repro.py. Wait for the prompt with `(^|\\n)User:`.
- `h.py finish` derives the outcome from the tested commits unless the meta file sets `outcome`. Attempts are never overwritten; a failed fixture or driver is committed as `inconclusive` and retried under the next number.

- Default environment is now Python 3.12: later commits import `typing.override` (exllamav3/models/mimo.py), which 3.11 lacks.
- `eval/compare_q*.py` findings: use `envs/py312-compareq-torch26cu126` with `lib/cqcli.py` (real dependencies, no stubs; pass `--env`, and `--timeout 1100`). By the user's decision the real packages are installed, resolved as of 2025-06-01. `lib/stubmods.py` and `lib/cq.py` are obsolete.
- `bin/cleanenv` sets `CUDA_DEVICE_ORDER=PCI_BUS_ID`, because gptqmodel sets it on import; an allocation was confirmed on physical GPU 1.
- wikitext-2-raw-v1 is cached under `hf/` at b08601e04326c79dfdd32d625aee71d232d685c3.

- pydantic is pinned to 2.11.7 in both environments: formatron 0.5.0 fails to import with the newest pydantic, and exllamav3 imports formatron at later commits.

- Architectures without a small public checkpoint get a tiny random checkpoint generated inside repro.py (cohere-qk-normalization, empty-block-conversion). Disclose it in limits and the model field.

- Native calls that can kill the process (SIGFPE, segfault) run in a child process from repro.py; match the binding's arity per commit (gemm-zero-grid-cap 001 failed on that).

- Upstream 6735462a (2025-07-06) cannot run Config.from_directory: architectures.py imports ernie4_5, added only in 47d83f56. Build the config class directly (e.g. MixtralConfig(dir)) for commits in that window.

- Extension tree 3571fd3b (commit 647bb7d5, 2025-05-03) does not build: stloader.cpp and stloader.cu both produce stloader.o under ninja. Its failed cache dir has no .ok; do not retry without a reason.

- eval/compare_q* functions with @disk_lru_cache write __disk_lru_cache__ beside sys.argv[0] (the result dir). Use fresh paths per run and delete the directory before finish.

- h.py finish now hashes files in subdirectories of a result dir by relative path (e.g. environment shims).

- Extension tree fcbd6dd8 (initial commit 543c4b27) does not build: bindings.cpp includes quant/exl3_gemv.cuh, absent from the tree.

- Commits before any MoE architecture exists (e.g. 6fc153d7): build EXL3 experts by quantizing a dense Llama with the repo converter and copying each layer's MLP tensors to experts.{e}.{w1,w3,w2} (see block-sparse-fused-intermediate-dtype 002).

## Progress
Results are the directories under `gpu-tests/results/`. Nothing is in flight.
- Finished, in queue order: architecture-mismatch-diagnostic, chat-context-count-overwritten, chat-stream-argument-mismatch, chat-top-k-float, cohere-qk-normalization, compare-q-cache-clear-argument-mismatch, compare-q-no-reference-finalization, compare-q-split-result-serialization, disabled-options-unbound, dots-default-prompt-format, eager-undeclared-transformers, empty-block-conversion, fp32-mlp-intermediate-contract, fused-shared-unreachable, gemm-zero-grid-cap, grouped-routing-unassigned, in-memory-weight-transpose, integration-example-stale-import, llamacpp-embedding-order, min-p-one-endpoint, kernel-attribute-cache-device, min-p-zero-assertion, missing-combo-sampler, missing-ernie-registry-modules, model-typing-override-import, native-router-argument-mismatch, mlp-ignored-activation, pin-heredoc-powershell (not_testable_here), optional-output-return, ordinary-output-accumulator-dtype, none-full-dimensions, top-p-zero-assertion, top-k-int-is-integer-compatibility, unconditional-tk-import, same-stem-object-conflict, unset-max-total-tokens, unsupported-cache-default-argument, tensor-truth-dispatch, missing-gemv-kernel-header, scalar-codebook-double-transform (blocked: unbuildable commits), vision-floating-ceiling-overflow, torch-gptj-reference, unchecked-output-capacity, qwen3-moe-component-migration, sliced-fp16-padding-target, conversion-handle-accumulation, repetition-penalty-masked-nan, tokenizer-truncation-calibration, normalization-settings-overwritten, unconditional-anyprecision-import (inconclusive: ledger roles look inverted).
- The three compare-q findings were rerun with real dependencies and are `fix_confirmed` at their highest attempt.
- Skipped for now, no result yet: humaneval-unconditional-bos (the encoded prompt is only observable by wrapping Job, which the rules treat as a patch; the user had no view on whether a pass-through recorder counts as a patch; left for the reviewer to decide, kept skipped); reference-test-discarded-results (the claim is that tests/test_rope.py is vacuous; showing it needs a fault injected into the code under test, which caps it at inconclusive; same reviewer question);
- Extension tree c54b3c67 (commit e9a3b6a9) is now cached for py312-superset.
- Priority 1 done except the skipped items above (main merged 2026-11-19; it added multi-gemm-leading-dimension-validation, done).
- Priority 2 (single-commit tests, no fix recorded) in progress. Done: async-job-doc-reference, asymmetric-norm-validation, activation-odd-tail, chat-empty-history-retry-edit, chat-explicit-load-falls-through, all-expert-fused-shape, block-sparse-fused-intermediate-dtype, chat-tps-toggles-multiline (basic-console multiline needs EOF, which the pty driver cannot send reliably; use the prompt_toolkit console and Alt+Enter = ESC CR).
