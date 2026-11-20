# 3805c77f4eea2165fdf8dcbb6b92033ea16d053f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3805c77f4eea2165fdf8dcbb6b92033ea16d053f) · [Evidence ledger](draft.json)

Merges the incoming 0.0.5 version bump into dev while preserving first-parent code. The new value feeds package metadata, newly created EXL3 quantization configs, and conditional wheel-release naming.

- [How the merged version reaches packages, checkpoints, and release names](#build-release)

## Problem

The first parent of turboderp’s merge still declared ExLlamaV3 0.0.4, while the incoming parent already declared 0.0.5. The merge message identifies the operation as merging `origin/dev` into `dev`; it does not claim a runtime fix. [source; call_450fe329d4454c7aa46f45b8f193f372, call_c23c9e975d704286b028486a00da34d1, call_34a6ba7683cb43e4830f4d75c3c0ae36]

## Reasoning

Relative to the first parent, the entire change is the one-line version bump. The same file diff appears in the incoming parent’s version-bump commit, which is signed off by kingbri. The supplied Git tree comparison shows that the merge result matches neither parent’s full tree: it takes the incoming version without replacing the first parent’s other content. For example, the first parent’s blockwise `proxy_err` computation is absent from the incoming parent and is not reverted by the merge. [source; call_450fe329d4454c7aa46f45b8f193f372, call_411072b1bf2d48f3b7071903afde3ea0, call_ae3c3893f2474af4be51b1bbd91df4ce, call_8a614575d74f45a99bf7e9b120a00695, call_27a52c32fd5047ce8437c65b88dd46b9]

## Impact

The merge changes the package base version, the stamp used when creating a new EXL3 quantization configuration, and the tag and name a manually requested wheel release would use. It does not change those consumers’ logic, rewrite existing checkpoints, or trigger a release. [source; call_411072b1bf2d48f3b7071903afde3ea0, call_769b59f380f54b53a3106c3b240daa86, call_65527f8338e542d282a62883174728db, call_174d7da3b18a4e258bcde5f63f5d4297, call_dcd63bf481dc4ae88b3af87f01321261]

## Source Notes

The initial runtime entry records the original 0.0.1 version and distinguishes install-time extension compilation from runtime JIT loading. The incoming parent’s version-bump entry documents the shared version consumers, including the existing-config branch that leaves the version alone and the manual release gate. [ancestor; call_0f385e29093c476db95b2d58143a5353, call_33462b771992444880d342a319c195ed]

Issue #33, “Error converting model,” reports a Qwen3 conversion file-open failure later logged as “Too many open files,” and separately a GLM4 repeated-output problem. Its concrete overlap is the traceback’s `qtensors_stc.get_tensors` call in `compile_model`, which also writes the version stamp later. The merge changes the stamp, not the failing tensor-read call. [inference; call_0c33bcb69d744144ae26b65ecc1fec4f, call_441b5afb4718403e9e0e085e8fc48489, call_65527f8338e542d282a62883174728db, call_411072b1bf2d48f3b7071903afde3ea0]

Issue #49, “running the QTIP inference code,” overlaps `setup.py` by filename, but its install commands target QTIP’s dependencies and kernels, not this package’s version assignment. Issue #10, “Soooo Cool !!! Thanks a lot for the new version ! I loved the v2,” is general feedback and does not identify 0.0.5. [inference; call_734420c288064366adf91f433277dca6, call_ff02a0ed5a4f4210a68bb2ac64b41c7a, call_411072b1bf2d48f3b7071903afde3ea0]

The closed PR #22, “OpenAI compatible API example,” proposes an endpoint for use with chat frontends; its discussion ends by recommending TabbyAPI’s EXL3 branch as a more robust option. Branch and quantization vocabulary provide context, but the endpoint proposal does not overlap the version change. [inference; call_baa24bc578814a51ba2abb7221247570, call_b491cb674b134e0e90e4a3cd8936ab70, call_411072b1bf2d48f3b7071903afde3ea0]

The first parent’s quantizer file is the overlap with PR #26, “Superior 3INST parameters,” and issues #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” #52, “Error converting moonshotai/Kimi-Dev-72B,” and #53, “Command A support.” These discuss a multiplier proposal, factorization or non-finite-state failures, and model support respectively. The merge does not edit the quantizer or establish a fix for those reports. [inference; call_f362f61486ef4f59893eb98b2eb26e79, call_1c8010b065ee41fcbc4f840bd1e4b4c2, call_985d8d5dfec04fc2aa35d1c83145b77b, call_c9badbdcbb6e4fb689291f11b82c73cc, call_e3b2d10030c34415b8027a32ca984133, call_8a614575d74f45a99bf7e9b120a00695, call_411072b1bf2d48f3b7071903afde3ea0]

<a id="build-release"></a>

## How the merged version reaches packages, checkpoints, and release names

`setup.py` executes `exllamav3/version.py` in a separate dictionary and passes `__version__` to setuptools. The CUDA build step still supplies its CUDA and Torch build tag separately. Keeping the assignment syntax unchanged also lets the workflow continue reading the base version as plain text. [source; call_411072b1bf2d48f3b7071903afde3ea0, call_769b59f380f54b53a3106c3b240daa86, call_174d7da3b18a4e258bcde5f63f5d4297]

`compile_model` writes `0.0.5` to `config.json` only when it creates the `quantization_config` section. If the input already has that section, it updates `bits` and `head_bits` without replacing or backfilling the version. The companion `quantization_config.json` copies the resulting section and adds tensor-storage metadata. [source; call_411072b1bf2d48f3b7071903afde3ea0, call_65527f8338e542d282a62883174728db, call_d7fa03e0f22c4510a27f510659b0e78c]

The manually dispatched workflow would use `v0.0.5` as the tag and `0.0.5` as the release name. Wheel upload requires a successful version parse and release input `1`; the input defaults to `0`. [source; call_411072b1bf2d48f3b7071903afde3ea0, call_174d7da3b18a4e258bcde5f63f5d4297, call_dcd63bf481dc4ae88b3af87f01321261]

A standard-library check executed the first-parent assignment and the replacement line transcribed from the diff, then applied the workflow regex in Python. The parsed and assigned versions agreed in both cases, yielding `0.0.4` and `0.0.5` and the corresponding `v`-prefixed strings. [execution; call_c2e16562f5214b4bba0c40a9b86dca35, call_411072b1bf2d48f3b7071903afde3ea0, call_174d7da3b18a4e258bcde5f63f5d4297]

## Uncertainty and limits

The bounded check used Python’s regex engine, not PowerShell or GitHub Actions. No package build, installation, model conversion, or publication was run. The repository search identifies literal references, not external consumers.
