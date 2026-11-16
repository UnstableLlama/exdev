# Verdict: commit-000195-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000195-001`
Packet: `.teacher/retrieval/000195-001`
Upstream: `965f5b2f0aa69e8d079cbeaffee59443ba9c8044` "Add cache_rotate kernel"
Request: `reviews/requests/commit-000195-001.md` (sha256 `88ce7ff294ccd1b8614ff974788016f9198f861e647d9ccf3e7a7e6bf598e23c`)
Reviewed: 2026-11-16, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and both findings are true as stated. One more consequence of the same kind
is listed only as an unverified precondition (below).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 194 strict-ancestor entries; 2,865 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 194/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fourteen open rows at 2025-05-27T09:27:51Z; my query agrees. No closed row qualifies. |
| The kernel | 128 blocks of 512 threads; each block takes a byte interval of every page; each thread copies 16-byte vectors at a stride of 8,192 bytes; the first page in `order` goes to the scratch page, each page then receives its successor, and the last receives the scratch. Correct. |
| The wrapper | Requires cache rank above one, a one-dimensional int32 `order`, and scratch byte size equal to one page; the comment says "long", the check is `kInt`. Bound as `cache_rotate`. Correct. |
| Callers | The new test only; nothing in the library calls it at this commit. Correct. |
| Rotation example | For order [4, 1, 3] over six pages the result is [0, 3, 2, 4, 1, 5]; I worked it by hand and agree. |
| Finding: partition | For a 129-byte page each block gets two bytes but copies 16; block 65 starts at 130 with its end clamped to 129, and the unsigned subtraction wraps, so the early return is not taken. True. The same over-copy applies, without the wrap, to any page whose per-block length is not a multiple of 16; the entry's point about vector tails covers this. |
| Finding: test dtype | The cache is created with `dtype = torch.half` whatever `cache_dtype` is. True. (The test function is also still named `test_rope`.) |
| Execution | Rotation order, the test's block lengths and the unsigned subtraction in Python; labelled as models. |

## Not verified

- Any build or GPU execution; that the test passes.

## Must fix before canonical use

1. An empty `order` is accepted by the wrapper. In the kernel `rotate_len - 1` is then an unsigned wrap, the loop
   bound is enormous, and `order[0]` is read from an empty tensor before that. The entry lists "nonempty order"
   among unverified caller preconditions; it is the same kind of unsigned underflow as its first finding and
   should be stated as one.

## Follow-ups

1. Ledger: identities for the two findings may be filed as suspected, introduced at `965f5b2f`; the empty-order
   case may be added to the partition record as a second trigger. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 196.
