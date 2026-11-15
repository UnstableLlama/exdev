# 702ebab361d2d07f513bc8702fe46f49dcd69608


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/702ebab361d2d07f513bc8702fe46f49dcd69608) · [Evidence ledger](draft.json)

Adds intermediate-state sampler tests, a multinomial validation step and optional state returns; fixes histogram sample shapes. Sorted multinomial samples lack token-index remapping.

- [Inspect intermediate sampler states with deterministic test cases](#sampling)

## Problem

Sampler tests needed access to intermediate distributions and index mappings; CustomSampler.forward previously required a completed sample and returned only reshaped token IDs. [source; call_11fcdc285a134c22b39ceb0e120b402d, call_b761cdb8b04c4335bffaf8f195b10081]

## Reasoning

The testing-only multinomial step preserves probabilities for inspection, unlike SS_Sample's in-place Gumbel transformation of probability buffers. [source; call_11fcdc285a134c22b39ceb0e120b402d, call_b761cdb8b04c4335bffaf8f195b10081]

## Impact

Default calls retain the token-tensor return contract. return_state=True exposes the flattened SamplingState and permits incomplete pipelines such as top-k filtering without sampling. [source; call_b761cdb8b04c4335bffaf8f195b10081, call_11fcdc285a134c22b39ceb0e120b402d, call_ea02a44b86f249b789ad133dd4d29745]

## Source Notes

The inspected discussions concern “quantizing model: undefined symbol: __cxa_call_terminate” and “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5”: respectively an extension-loading report and low-bitrate quantization output. Neither supplies evidence of a sampler-test motivation. [source; call_91f04c167985414ab8cc2e06b6dcbf1e, call_cd342c778e6d4bf2be410030d5b9fd1e]

<a id="sampling"></a>

## Inspect intermediate sampler states with deterministic test cases

SS_Sample_mn is exported from the sampler package. Its preparation requests normalization for initial logits or unnormalized probabilities; run accepts normalized sorted or unsorted probabilities, calls torch.multinomial with one sample, and marks the state DONE. [source; call_201752e2db0b46ea9be8e35d89d92745, call_b761cdb8b04c4335bffaf8f195b10081]

return_state bypasses only the final DONE requirement, not the assertion forbidding steps after completion. Existing presets continue using SS_Sample rather than the new multinomial alternative. [source; call_b761cdb8b04c4335bffaf8f195b10081, call_11fcdc285a134c22b39ceb0e120b402d, call_c6e807d111f44dfd8b3f841749e62d5f]

Four cases check temperature 0.75 followed by top-p 0.95, min-p 0.16 with and without sorting, and top-k 5. Temperature divides logits; min-p retains probabilities at least 16% of the maximum; top-k retains five ranked entries. The top-p fixture follows the existing cumulative-probability <= 0.95 cutoff, retaining the first token regardless. [source; call_ea02a44b86f249b789ad133dd4d29745, call_11fcdc285a134c22b39ceb0e120b402d]

A standard-library transcription reproduced top-p probabilities 0.79139147 and 0.20860853, and surviving min-p probabilities 0.10153632, 0.16740510, 0.27600434 and 0.45505423, consistent with the fixture values rounded to five decimal places. [execution; call_594b2c368e9345e79144f646bbf8579a]

The existing histogram tests now unsqueeze each batch-shaped sample into a column before concatenation. Their sample caps and discrepancy thresholds remain unchanged. New state comparisons inspect only expected-length prefixes; no supplied case specifies expect_sample, and the top-k case does not check the masked tail. [source; call_ea02a44b86f249b789ad133dd4d29745, call_17fb06ffc1cc43e3bad2ec5e95782b4f, call_11fcdc285a134c22b39ceb0e120b402d]

## Authoring-time findings — pending review

### multinomial-sorted-token-mapping (suspected; defect)

The new multinomial step returns sorted column positions rather than original token IDs when its input is sorted.

Trigger: Use SS_Sample_mn after a sorting or sorted filtering step with a nonidentity indices mapping.

Expected: Map the selected column through state.indices, as SS_Sample does for sorted distributions.

Actual: SS_Sample_mn stores torch.multinomial's column directly in state.sample. For the sorted min-p fixture, column 0 represents token 5 but is returned as 0. The new tests check probabilities and indices, not sampled token IDs. Parent-tree search found no pre-existing SS_Sample_mn callers; the task introduces three test constructions, two with sorted distributions. Existing presets remain on SS_Sample.

Locations: 702ebab361d2d07f513bc8702fe46f49dcd69608:exllamav3/generator/sampler/custom.py — SS_Sample_mn.run

Source evidence: call_b761cdb8b04c4335bffaf8f195b10081, call_11fcdc285a134c22b39ceb0e120b402d, call_ea02a44b86f249b789ad133dd4d29745, call_d971603f858e4bd4a9123a066a4dc7ac, call_49c2a2dda327491d84ddc3a2d5b82978, call_c6e807d111f44dfd8b3f841749e62d5f

source_inspection: Compared the new multinomial assignment against SS_Sample's explicit per-row index remapping and inspected introduced test callers and existing presets. [call_b761cdb8b04c4335bffaf8f195b10081, call_11fcdc285a134c22b39ceb0e120b402d, call_ea02a44b86f249b789ad133dd4d29745, call_c6e807d111f44dfd8b3f841749e62d5f]. Limits: No Torch sampling execution; reach outside inspected repository callers is unestablished.

## Uncertainty and limits

No repository tests or CUDA kernels were executed. The tests retain the hardcoded cuda:2 device.

The scalar check uses Python double-precision arithmetic, not Torch float32 operations, and does not establish assert_close outcomes or multinomial sampling behavior.
