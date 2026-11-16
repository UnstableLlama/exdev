# 07ffea7f89c5a701130e48fd0aeaefe52a660210


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/07ffea7f89c5a701130e48fd0aeaefe52a660210) · [Evidence ledger](draft.json)

Broadens llama.cpp BPW accounting to non-head .weight tensors and moves metadata inspection before model construction; cached results and tensor-order sensitivity remain caveats.

- [Broader GGUF weight accounting](#usage-evaluation)

## Problem

GGUF storage accounting previously included only seven projection-name suffixes, excluding other weight tensors from both the decoder BPW numerator and denominator. [source; call_4616113e9a824c6f91521ab5cfe4dd02]

## Reasoning

Replacing the projection whitelist with a .weight suffix test broadens coverage without maintaining architecture-specific projection names. The tradeoff is that normalization and other matching weights now contribute too; this is not exclusively an MoE change. [source; call_4616113e9a824c6f91521ab5cfe4dd02]

## Impact

The returned tuple retains its interface. compare_q.test_ppl consumes its layer BPW, head BPW and storage bits, converts bits to GiB, and exposes the values to result reporting and plotting. These are tensor-storage estimates, not measured runtime GPU allocations. [source; call_0165472d929341ca97eef52f91f816a3, call_68a74a8a5ce44291a9cab509c1a0e9ca]

## Source Notes

The initial usage-evaluation entry was read. It establishes the earlier projection-based GGUF accounting, embedding fallback for the head, and the distinction between calculated storage and runtime VRAM. [ancestor; call_33c135f959214cb9ac96f705208947c2]

<a id="usage-evaluation"></a>

## Broader GGUF weight accounting

get_storage_info reads GGUF tensor metadata and computes an element-weighted BPW: total n_bytes × 8 divided by total n_elements. The factor eight converts bytes to bits. Explicit output.weight takes precedence as the head; token_embd.weight supplies a fallback while head_bpw is zero. Other .weight tensors now enter the aggregate through an elif branch; nonmatching tensors remain excluded. [source; call_0165472d929341ca97eef52f91f816a3, call_4616113e9a824c6f91521ab5cfe4dd02]

A Python scalar transcription with a synthetic expert weight demonstrates the accounting change: decoder BPW changes from 8 to 5.333333333333333 and decoder-plus-head storage from 2400 to 3200 bits. Including more weights can therefore increase counted storage while decreasing the weighted BPW. [execution; call_a3be7d745a0b4047a4c5885a9e56a47a]

load_llamacpp now obtains storage information after backend initialization but before constructing Llama. Its constructor options and forwarding implementation are unchanged. The broader selection does not require this reordering to perform its arithmetic. [source; call_4616113e9a824c6f91521ab5cfe4dd02, call_0165472d929341ca97eef52f91f816a3]

## Authoring-time findings — pending review

### embedding-order (suspected; defect)

The new fallback branch makes decoder accounting sensitive to embedding/head tensor order.

Trigger: A positive-sized output.weight precedes token_embd.weight in GGUFReader.tensors.

Expected: Reordering identical tensor metadata should not change decoder BPW or decoder-plus-head storage.

Actual: Once output.weight sets head_bpw, token_embd.weight fails the head condition and falls into the new .weight aggregate. With embedding first it is excluded instead. The synthetic check changes the result from (5.333333333333333, 16, 3200) to (8, 16, 4800).

Locations: 07ffea7f89c5a701130e48fd0aeaefe52a660210:eval/compare_q_llamacpp.py — get_storage_info

Source evidence: call_4616113e9a824c6f91521ab5cfe4dd02, call_0b1d5bc396dd40c1af1bd7445cddef7e, call_68a74a8a5ce44291a9cab509c1a0e9ca

source_inspection: Whole-tree caller search identifies load_llamacpp as this helper's direct caller; compare_q dispatches to that loader through its llamacpp registry entry. The observation concerns fresh accounting on that path, not every evaluation backend. [call_0b1d5bc396dd40c1af1bd7445cddef7e, call_7a261e185ae349279f5a570d31ffbde5, call_68a74a8a5ce44291a9cab509c1a0e9ca]. Limits: No actual GGUF ordering was inspected.

scalar_transcription: Executed Python versions of the old and changed classification loops on synthetic metadata, then swapped head and embedding order. [call_a3be7d745a0b4047a4c5885a9e56a47a]. Limits: This does not execute GGUFReader or the repository helper.

### cached-accounting (suspected; defect)

Existing disk-cache entries can bypass the corrected accounting.

Trigger: get_storage_info is called with arguments already cached under lcpp_get_storage_info before this change.

Expected: Storage reporting reflects the updated tensor-selection rule.

Actual: The unchanged decorator returns the previously stored tuple without running the modified loop. Its key contains serialized arguments, not a code version. The comparison CLI clears only test_ppl entries, not this storage cache.

Locations: 07ffea7f89c5a701130e48fd0aeaefe52a660210:eval/compare_q_llamacpp.py — get_storage_info

Source evidence: call_0165472d929341ca97eef52f91f816a3, call_4616113e9a824c6f91521ab5cfe4dd02, call_af7bf2074fc54123a7bc63fb7bba4801, call_68a74a8a5ce44291a9cab509c1a0e9ca

source_inspection: Traced the direct loader caller, cache-hit return, unchanged cache namespace, and comparison CLI invalidation. [call_0b1d5bc396dd40c1af1bd7445cddef7e, call_af7bf2074fc54123a7bc63fb7bba4801, call_68a74a8a5ce44291a9cab509c1a0e9ca]. Limits: No persistent cache or filesystem behavior was executed; fresh cache keys run the changed implementation.

## Uncertainty and limits

No real GGUF file, llama.cpp inference, or GPU memory measurement was executed. The scalar check uses synthetic tensor metadata and does not establish actual GGUF tensor ordering or naming coverage.

The reason for moving metadata accounting before model construction is not established by the supplied evidence.
