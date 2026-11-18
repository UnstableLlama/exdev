# GPU test worker state

## Machine
- GPU: 2x NVIDIA GeForce RTX 3090 (24 GB). **The worker uses physical GPU 1 only** (`CUDA_VISIBLE_DEVICES=1`, `TORCH_CUDA_ARCH_LIST=8.6`), by the user's instruction.
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

## Progress
Results are the directories under `gpu-tests/results/`. In flight: working down priority 1 of the queue, top first.
