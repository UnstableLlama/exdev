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

## Progress
Results are the directories under `gpu-tests/results/`. In flight: working down priority 1 of the queue, top first.
