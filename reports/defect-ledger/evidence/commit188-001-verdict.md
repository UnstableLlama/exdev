# Verdict: commit-000188-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000188-001`
Packet: `.teacher/retrieval/000188-001`
Upstream: `c2ec220c83d4a697f4726401aa8c7e6a5a551fa6` "LinearEXL3: Reduce CPU overhead"
Request: `reviews/requests/commit-000188-001.md` (sha256 `8e61f0118a5ce2b7efbb702727a511163d6a9b73e732eef6db99acca03cace66`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry reports no finding. It does state the fact that matters, that the
new cache of configured kernels is keyed by kernel pointer alone and not by device, and says multi-device
behaviour is unverified. That fact is a defect (reviewer finding below); the entry stops one step short of
saying so. Nothing it says is wrong.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 16 of 16 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 187 strict-ancestor entries; 2,814 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 16 of 16 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 187/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T11:33:39Z; my query agrees. Two closed rows by terms, both selected, described as inferred context. |
| Python | `forward` allocates `y` in its final shape in both branches; the reconstruction branch uses a two-dimensional view of it for `hgemm` and the output transform; the direct branch passes it to `exl3_gemm` as is; bias is added to `y`; the dtype is the per-call value, else the instance value, else half. The 32-row switch is unchanged. Correct. |
| Native checks | `C` is now checked on its last dimension; the comparison of `A`'s row count with `C`'s first dimension is commented out, as are the `suh` length check, the "must supply A_had" check, the `A_had` shape check and the `svh` length check. Correct, and the entry says which were removed. |
| Callers | `LinearEXL3.forward` and `science/qgemm_benchmark.py`; the benchmark's two-dimensional outputs satisfy the last-dimension check. Correct. |
| Attribute cache | A file-level `std::set<void*>`; `cudaFuncSetAttribute` is called only when the kernel pointer is not in it, then the pointer is inserted, in both `exl3_gemm` and `exl3_mgemm`. No device in the key, no check of the call's result. Correct. |
| Execution | Element-count arithmetic for four shapes; labelled as arithmetic only. |

## Reviewer finding (not in the entry; reviewer knowledge and hindsight, never to a teacher)

The kernel-attribute cache is not per device. Both functions read the current device a few lines earlier and
launch with a dynamic shared-memory request that needs the raised limit, but after the first call on any device
the pointer is in the set and the attribute is never set for the same kernel on another device. Upstream later
changes exactly this: `dc69b167` (2025-05-30) "GEMM: Set kernel attribute per device" turns the set into one set
per device indexed by `device`. I have not checked CUDA's documentation on whether the attribute is per device;
the later fix is my evidence that it mattered. Source reading only; nothing executed.

## Not verified

- Any CUDA execution; behaviour on more than one GPU; the cost saved.

## Must fix before canonical use

1. State the attribute-cache observation as a suspected finding for multi-device use, with the limit that the
   per-device nature of the attribute was not established from documentation.
2. With "must supply A_had" commented out, a call that passes `suh` without `A_had` now reaches the kernel with a
   null scratch pointer; the entry lists the removed check but not that consequence.

## Follow-ups

1. Ledger: a new reviewer-originated identity for the attribute cache, suspected, source-only, introduced at
   `c2ec220c`. Do not record the fix until the walk reaches `dc69b167` and its entry is approved.
2. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 189.
