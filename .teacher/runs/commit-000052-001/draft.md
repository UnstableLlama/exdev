# 70e79cc880a40aa0aa7a41cc80c574622a658197


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/70e79cc880a40aa0aa7a41cc80c574622a658197) · [Evidence ledger](draft.json)

Adds memory-first tensor lookup with disk fallback, while restricting collection metadata operations and requiring tensor groups to be complete within one source.

- [Memory-first tensor lookup with a restricted collection interface](#loading-tokenization)

## Problem

SafetensorsCollection previously resolved tensor reads only through its file index. This change adds an in-memory source without replacing the existing disk loader. [source; call_4185fc103e5045a7934fd05e36521c1f, call_1fd902f43176455fa3c932c1a7e4e4a5]

## Reasoning

The new source is a mutable overlay: set_new_tensors stores the supplied object directly, and matching memory keys take precedence over file keys. Missing memory keys still use the existing file path. [source; call_4185fc103e5045a7934fd05e36521c1f]

## Impact

Single-tensor presence checks and reads accept memory tensors, but sizing, listing, prefix reads and close explicitly assert that new_tensors is None. Even an empty dictionary activates these restrictions; passing None restores the file-only interface. [source; call_4185fc103e5045a7934fd05e36521c1f, call_1fd902f43176455fa3c932c1a7e4e4a5]

## Source Notes

The earlier inventory entry describes list_tensors as a header-derived metadata interface. The new assertions make that interface unavailable while a memory mapping is installed. [ancestor; call_127aeb6a603c4d0b885eeae65f020b5d]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and the reporter's environment workaround, not a request for memory loading. No connection to this change is established. [source; call_821159274aa643c0bed8421feb8c564d]

<a id="loading-tokenization"></a>

## Memory-first tensor lookup with a restricted collection interface

Construction still scans the directory and builds file metadata before initializing new_tensors to None. set_new_tensors assigns a mapping rather than merging it into tensor_file_map, so file metadata remains separate. [source; call_4185fc103e5045a7934fd05e36521c1f, call_1fd902f43176455fa3c932c1a7e4e4a5]

get_tensor first resolves an omitted device to CPU, then returns new_tensors[key].to(device) for a memory hit. This bypasses file opening, payload validation, loading metrics and the file branch's BF16-to-FP16 conversion. Consequently allow_bf16 does not control the memory branch's dtype. [source; call_4185fc103e5045a7934fd05e36521c1f, call_1fd902f43176455fa3c932c1a7e4e4a5]

Memory misses retain required-versus-optional file lookup behavior: absent required keys raise ValueError, while optional keys return None. Existing mt_fread and python implementations remain the fallback alternatives. [source; call_4185fc103e5045a7934fd05e36521c1f, call_1fd902f43176455fa3c932c1a7e4e4a5]

has_tensor_group evaluates an entire group separately against each source, rather than against their union. String subkeys are required members; nested alternatives need at least one match. Linear.is_exl3_storage uses this predicate for sv/svh, su/suh and trellis before load_exl3 fetches individual tensors. [source; call_4185fc103e5045a7934fd05e36521c1f, call_e157cfa3d9554a18951c696e7ccd282b, call_c42c1f9ae37044dab301caf51d4ffd62]

A bounded transcription returned false for a group with trellis only on disk and su/sv only in memory, although every individual key was available. Putting the complete group in either source returned true. [execution; call_08d4ea425a6f4896a326e102ba0c4dc2]

This design offers inexpensive memory overrides but not a fully interchangeable memory-backed collection: group completeness is source-local and metadata operations are deliberately guarded rather than synthesized from tensors. [inference; call_4185fc103e5045a7934fd05e36521c1f]

The earlier loading entry records a native read-failure synchronization risk. Inspection of the parent implementation and this single-file diff shows that the risky wait/error logic is carried over unchanged for disk fallback; memory hits bypass it. [source; call_e9d5ce5d5dc54f8c8010902fe849dc15, call_425fe7c0994d4fc484d68d12a6bd699d, call_4185fc103e5045a7934fd05e36521c1f, call_1fd902f43176455fa3c932c1a7e4e4a5]

## Authoring-time findings — pending review

### split-source-group (suspected; behavior_change)

Group detection does not compose the same disk-plus-memory availability offered by individual lookup.

Trigger: A requested group is complete only across the union of tensor_file_map and new_tensors, for example disk trellis plus memory su and sv.

Expected: If group detection is intended to reflect individual lookup availability, this group would be recognized.

Actual: has_tensor_group returns false because neither source independently contains the complete group. Linear.load_exl3 consequently declines that storage layout.

Locations: 70e79cc880a40aa0aa7a41cc80c574622a658197:exllamav3/loader/safetensors.py — SafetensorsCollection.has_tensor_group

Source evidence: call_4185fc103e5045a7934fd05e36521c1f, call_c42c1f9ae37044dab301caf51d4ffd62, call_e157cfa3d9554a18951c696e7ccd282b

source_inspection: Whole-parent literal search found direct application callers in Linear.load_fp16 and Linear.is_exl3_storage; load_exl3 checks the latter before reading tensors. The multi-member EXL3 group is the concrete affected case. [call_c42c1f9ae37044dab301caf51d4ffd62, call_e157cfa3d9554a18951c696e7ccd282b]. Limits: Whether source-local completeness is intentional is unestablished; no model workflow was executed.

scalar_transcription: Transcribed the changed predicate and checked split-source and complete-source groups. [call_08d4ea425a6f4896a326e102ba0c4dc2]. Limits: Standard-library membership test only, not repository or tensor execution.

### inherited-native-read-wait (suspected; defect)

The existing native disk fallback can leave its GPU copy worker waiting after a read failure.

Trigger: A GPU-target mt_fread load has a copy worker waiting on an empty queue when a reader fails, with no subsequent successful enqueue.

Expected: The failure should wake the copy worker and allow the loader to report its I/O error.

Actual: The reader only sets load_failed; the wait predicate checks only queue nonemptiness and receives no failure notification, so thread joining may not complete.

Locations: d908052e96929a4f92e90256838f9cad9b72226d:exllamav3/exllamav3_ext/stloader.cpp — stloader_read

Source evidence: call_425fe7c0994d4fc484d68d12a6bd699d, call_9a1a495170904d0abe32364e6e581284, call_1fd902f43176455fa3c932c1a7e4e4a5, call_4185fc103e5045a7934fd05e36521c1f

source_inspection: Whole-parent search located the binding and get_tensor's native call. The task leaves this fallback unchanged while bypassing it on memory hits. [call_9a1a495170904d0abe32364e6e581284, call_425fe7c0994d4fc484d68d12a6bd699d, call_4185fc103e5045a7934fd05e36521c1f]. Limits: No concurrent execution or injected I/O failure; CPU and python-loader paths do not use this copy-worker wait.

## Uncertainty and limits

No PyTorch tensor transfers, model loading, native I/O or GPU execution were tested. The Python check transcribed only dictionary membership logic.

The change supplies no usage example or mapping validation. End-to-end lifecycle compatibility with the restricted metadata and close methods remains untested.

The native failure-path observation is source-derived, not a reproduced deadlock.
