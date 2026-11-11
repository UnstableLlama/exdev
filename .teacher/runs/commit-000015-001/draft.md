# 2591348cf879664aeebb2ba188cdcf9c3fe07311


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2591348cf879664aeebb2ba188cdcf9c3fe07311) · [Evidence ledger](draft.json)

Fixes duplicated working-directory prefixes when saving converted module tensors, preserving absolute-path destinations and the shared serialization helper.

- [Resolve module output paths once](#conversion)

## Problem

Module saving prefixed the filename with work_dir twice: main() constructed a work-relative destination, then save_tensor() joined work_dir again. Ordinary relative working directories therefore targeted an unintended nested directory. [source; call_0bdef51fe5d5479595ea6fa87d8ac7ea, call_67c625fffe024cbb9e4155ffe0ea456c]

## Reasoning

The fix leaves path resolution in save_tensor() and passes only qtensors/<module-key>.safetensors from main(), matching the helper's existing checkpoint caller rather than changing the shared helper. [source; call_67c625fffe024cbb9e4155ffe0ea456c, call_c82a1b7b03784486aee26082bdb52813, call_0bdef51fe5d5479595ea6fa87d8ac7ea]

## Impact

The corrected destination matches the qtensors directory created by prepare_env(). Tensor collection and serialization are unchanged. [source; call_0bdef51fe5d5479595ea6fa87d8ac7ea, call_67c625fffe024cbb9e4155ffe0ea456c]

## Source Notes

The earlier conversion entry identified this relative-path hazard; the task removes that specific hazard. [ancestor; call_2cdda5c583f24eb7bff93f5171dce3c6]

<a id="conversion"></a>

## Resolve module output paths once

main() merges each module's get_tensors() results into a dictionary and passes it to save_tensor(), whose dictionary branch writes the named tensors with save_file(). The patch changes only the filename argument, so the correction applies to every processed module reaching this save point, not just modules with quantization targets. [source; call_0bdef51fe5d5479595ea6fa87d8ac7ea, call_67c625fffe024cbb9e4155ffe0ea456c]

A standard-library transcription produced work/work/qtensors/layer.safetensors before the patch and work/qtensors/layer.safetensors afterward. For /tmp/work both expressions produced the same absolute destination; for '.' they normalized identically. Thus the commit message's 'double absolute path' wording describes redundant construction, but the demonstrated destination error concerns relative paths. [execution; call_9ebba8a3f793428ba722971d6347384e, call_67c625fffe024cbb9e4155ffe0ea456c]

The inspected CLI entrypoint calls prepare() and then main(). The other direct save_tensor() caller already supplies ckpt_new/state.safetensors relative to work_dir and is unchanged. The patch does not alter checkpoint rotation or resume loading. [source; call_f8fdd6c983424c47b80a54a69a4ddb2c, call_c82a1b7b03784486aee26082bdb52813, call_0bdef51fe5d5479595ea6fa87d8ac7ea, call_67c625fffe024cbb9e4155ffe0ea456c]

## Authoring-time findings — pending review

### checkpoint-rotation-gap (suspected; defect)

The inherited interruption window in checkpoint rotation remains unchanged by this path fix.

Trigger: Conversion is interrupted after renaming ckpt to ckpt_old but before renaming ckpt_new to ckpt, then the user resumes.

Expected: Resume recovers an available complete checkpoint.

Actual: prepare() loads ckpt/job.json without falling back to ckpt_old or ckpt_new; prepare_env() can recreate an empty ckpt directory, but not its missing job.json.

Locations: 2591348cf879664aeebb2ba188cdcf9c3fe07311:exllamav3/conversion/convert_model.py — main, 2591348cf879664aeebb2ba188cdcf9c3fe07311:exllamav3/conversion/convert_model.py — prepare

Source evidence: call_0bdef51fe5d5479595ea6fa87d8ac7ea, call_67c625fffe024cbb9e4155ffe0ea456c, call_f8fdd6c983424c47b80a54a69a4ddb2c, call_8b84b7439ae64e14abfa13e171738016

source_inspection: Inspected the two sequential renames, resume loader and CLI calls; the complete task diff changes only the module-save filename. Reach is the inspected conversion CLI's checkpoint/resume workflow. [call_0bdef51fe5d5479595ea6fa87d8ac7ea, call_67c625fffe024cbb9e4155ffe0ea456c, call_f8fdd6c983424c47b80a54a69a4ddb2c]. Limits: No interruption was injected; literal caller search does not establish all external callers.

## Uncertainty and limits

Validation models POSIX path joining only; no safetensors write, model conversion, GPU execution or interruption/recovery test was run.
