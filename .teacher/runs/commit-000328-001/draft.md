# 1c8378a5c1a48eb76bf2a2000406d61479d4b65d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1c8378a5c1a48eb76bf2a2000406d61479d4b65d) · [Evidence ledger](draft.json)

Bumps ExLlamaV3 from 0.0.4 to 0.0.5, updating package metadata, the version stamp for newly created EXL3 quantization configs, and conditional release naming.

- [How the 0.0.5 version reaches packages, checkpoints, and releases](#build-release)

## Problem

The shared ExLlamaV3 version was 0.0.4. The commit, signed off by kingbri, announces v0.0.5, and the sole changed line sets __version__ to "0.0.5". [source; call_919d756383af4747a100cfc47dc9d57e, call_fe815383647e4eef8b58ca30c2ffeaff]

## Reasoning

One assignment supplies the package base version, the version stamped into newly created EXL3 quantization metadata, and the base version parsed by the release workflow. Keeping the assignment syntax unchanged lets all three consumers pick up the new value without separate edits. [source; call_fe815383647e4eef8b58ca30c2ffeaff, call_d4e2a681e431445aa3e1c98f13992e5c, call_22472de624414a9ebe994d2264426ed6, call_9c197a162be24859bbec715e03096325]

## Impact

This commit changes version metadata, not dependency declarations, package membership, model code, or the build matrix. It does not rewrite already generated artifacts or start a release. [source; call_fe815383647e4eef8b58ca30c2ffeaff, call_d4e2a681e431445aa3e1c98f13992e5c, call_9c197a162be24859bbec715e03096325]

## Source Notes

The initial runtime chapter records version 0.0.1. The entries for the 0.0.2, 0.0.3, and 0.0.4 bumps describe the same shared version source and the existing manual release gate. [ancestor; call_c3ce826693234debb6ee1842d32f5045, call_5c4a5d4a01ba439a9edaa5bfe3fbaf55, call_c4b872691d774497b5af0375eefda0b7, call_37323181432140f1b13367842f51a02d]

Issue #33, “Error converting model,” reports a Qwen3 conversion file-opening failure, later diagnosed in the thread as too many open files, and a separate GLM4 repeated-token report. Its connection to the bump is inferred only from the traceback matching the tensor-read call in compile_model, which also writes the version metadata. The assignment edit does not touch either reported mechanism. [inference; call_c7be1177772647e68296cb8551eb925f, call_8fa31d6c89884e7eb118d1c67c54e733, call_948b509d805f4e2086eb58c834a19d35, call_22472de624414a9ebe994d2264426ed6, call_fe815383647e4eef8b58ca30c2ffeaff]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure during converter startup. Issue #49, “running the QTIP inference code,” discusses installing and testing QTIP, including setup.py commands for other projects. Closed issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” reports a FlashAttention installation problem and mentions kingbri1 in a suggested wheel URL. The overlaps are converter startup, packaging vocabulary and dependencies, and the login string in this commit's sign-off; none indicates that the bump addresses those reports. [inference; call_76721da8868841c8ac1e7b6e7f35d955, call_6b97bcd6e77b4e2b9aae483dbd188b8d, call_10150aef5d844e3abb54c24232261eb3, call_d4e2a681e431445aa3e1c98f13992e5c, call_919d756383af4747a100cfc47dc9d57e, call_fe815383647e4eef8b58ca30c2ffeaff]

Issue #10, “Soooo Cool !!! Thanks a lot for the new version ! I loved the v2,” is general feedback with no release number in its title or body. The shared word “version” does not connect it to v0.0.5. [inference; call_fbe856b0b21f47809878aa7464943f44, call_919d756383af4747a100cfc47dc9d57e]

<a id="build-release"></a>

## How the 0.0.5 version reaches packages, checkpoints, and releases

setup.py executes version.py in a separate dictionary and passes its __version__ value to setup(version=...). That makes 0.0.5 the package base version; the CUDA wheel build still supplies its CUDA and Torch build tag separately. [source; call_fe815383647e4eef8b58ca30c2ffeaff, call_d4e2a681e431445aa3e1c98f13992e5c, call_9c197a162be24859bbec715e03096325]

compile_model imports __version__ and writes 0.0.5 as quantization_config.version in the output config.json only when the input has no quantization_config. If the section already exists, the function updates bits and head_bits without replacing or backfilling its version. The companion quantization_config.json takes that resulting section and adds tensor-storage metadata. [source; call_fe815383647e4eef8b58ca30c2ffeaff, call_22472de624414a9ebe994d2264426ed6, call_c5c5a97c093b4fd3b754f79eb6c4bb57]

The manually dispatched build workflow reads version.py as text. With 0.0.5 captured, it uses v0.0.5 as the release tag and 0.0.5 as the release name. The upload step targets ./dist/*.whl and requires both a successful version parse and release input '1'; that input defaults to '0'. [source; call_fe815383647e4eef8b58ca30c2ffeaff, call_9c197a162be24859bbec715e03096325]

A standard-library check executed the parent assignment and the new assignment transcribed from the diff, then applied the workflow regex in Python. The assignment and capture agreed for both inputs, yielding 0.0.4 and 0.0.5 and the corresponding v-prefixed tag strings. [execution; call_fe815383647e4eef8b58ca30c2ffeaff, call_9c197a162be24859bbec715e03096325, call_b353eca4bb2c498598a1b7b9fa9aa959]

## Uncertainty and limits

The bounded check ran the version assignments and the workflow's regex in Python, not PowerShell, setuptools, a model conversion, or GitHub Actions. Wheel contents, installation, publication, and compatibility were not verified.

The parent-tree search locates literal version references; it does not establish how external consumers use the package or checkpoint version.
