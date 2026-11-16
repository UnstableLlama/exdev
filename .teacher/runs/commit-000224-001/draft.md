# 074019737caac1c6e6a457e3bed7e4a30e0a5877


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/074019737caac1c6e6a457e3bed7e4a30e0a5877) · [Evidence ledger](draft.json)

Adds white-background RGB conversion and dtype-aware channel normalization utilities, plus a Pillow requirement; model integration and pixel rescaling remain outside this change.

- [RGB conversion and channel normalization](#vision)

## Problem

The change adds reusable RGB conversion and channel normalization helpers for vision inputs; neither helper name occurs in the parent tree. [source; call_6d3d3cc8648e433f9a5aedcd0c43a66b, call_ff3bad50b0d54b8ebcfc38a977bd76a4, call_54e58d816ca148e7ab3c691b2d5e627b]

## Reasoning

Adding pillow to requirements.txt supplies the package used by the new module's PIL import. The parent already has a local PIL import in save_tensor_image, which converts a colormapped tensor to an image and saves it. [source; call_94b43b4d827b4deb9763d78df9b4974a, call_414195f2d41a4bcbb713cf24afaf1a54, call_3d3c7666b69a4a0b8fa56db7b24aeca4]

## Impact

This introduces preprocessing primitives, not a connected VLM inference workflow: the task diff adds no callers or model integration. [source; call_6d3d3cc8648e433f9a5aedcd0c43a66b, call_94b43b4d827b4deb9763d78df9b4974a]

## Source Notes

The dependency-alignment ancestor entry was read. It records previously matching installation declarations and the removal of pillow from package metadata, establishing historical context rather than verification of current packaging behavior. [ancestor; call_30cf994c5688418dbf0ad1e85855c6f3]

Related requirements.txt discussions concern different reported failures: #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns quantization and tokenizer truncation; #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” concerns Torch/Flash-Attention installation; #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” concerns native compilation and closed without a reported solution. [source; call_243d01b8ec59426499a3e00f30829e2e, call_a485c41bc6a646b9809c3bd38e3b4f95, call_59f8c89c7e6d46b8a8842fa5eb6087ad]

Their shared requirements.txt reference is insufficient to connect those failures to these image helpers; no causal relationship is established. [inference; call_243d01b8ec59426499a3e00f30829e2e, call_a485c41bc6a646b9809c3bd38e3b4f95, call_59f8c89c7e6d46b8a8842fa5eb6087ad, call_94b43b4d827b4deb9763d78df9b4974a]

<a id="vision"></a>

## RGB conversion and channel normalization

convert_to_rgb returns an RGB input unchanged, preserving object identity. Other modes are converted to RGBA, pasted onto a white RGBA canvas using the image itself as mask, then converted to RGB. This explicitly chooses white rather than simply discarding transparency. [source; call_6d3d3cc8648e433f9a5aedcd0c43a66b]

normalize_image asserts three mean and three standard-deviation values, corresponding to RGB channels. It casts nonfloating input to float32, preserves existing floating dtype, constructs mean/std arrays in that dtype, and returns (image - mean) / std. It neither computes image statistics nor rescales bytes to [0,1]; the docstring's mean(image) notation is therefore less precise than the implementation. [source; call_6d3d3cc8648e433f9a5aedcd0c43a66b]

The three-element arrays are applied without reshaping or a channel-axis argument, so callers must supply a broadcast-compatible layout and statistics in the same value scale as their image. Conversion to floating point prevents integer subtraction arithmetic but is not pixel-range normalization. [source; call_6d3d3cc8648e433f9a5aedcd0c43a66b]

A scalar transcription with pixel (0,128,255) and mean/std both (0.5,0.5,0.5) produced (-1,255,509); explicitly dividing pixels by 255 first produced approximately (-1,0.00392,1). These illustrative constants demonstrate the caller's scale responsibility, not model-specific defaults. [execution; call_c612835c25894905a4eda15a593f8b15]

## Uncertainty and limits

No repository helper, NumPy operation or Pillow operation was executed; the numerical check models only normalization arithmetic using Python scalars.

No integrated caller establishes required image layout, value scale or handling of zero standard deviations. Literal parent searches do not exclude dynamic imports or external callers.
