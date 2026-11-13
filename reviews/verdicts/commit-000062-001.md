# Verdict: commit-000062-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000062-001`
Packet: `.teacher/retrieval/000062-001`
Upstream: `00bbb58384359ced00025238360cdcdcafad7c3c` "Add CUDA extension histogram test function"
Request: `reviews/requests/commit-000062-001.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only.** Unassisted. The walk may continue from commit 63.

Canonical and training remain false.

Not thin: the change is one self-contained diagnostic with no caller, and the entry covers the mapping, the normalisation, the reference enumeration, the wrapper and its one real hazard.

## Artifacts reviewed (sha256)

- draft.json: `eb2b4976791c55563c6fc01830f3598ffbf85ee8bd2736536c3033b4feebfbb6`
- draft.md: `eb67591b9b3b1dbbf38aa0a171d3d1c549524e6f60c622605201dedd8c77de11`
- raw-transcript.json: `f1d841d826fe6c2322e6c62626a6014b9887999d54a924addb28910ba3b3048a`
- provenance.json: `5f1e78ece77bfc5ed964eef65e7c98be66394ebf5cb56795aab082cee7f1e2e6`
- coverage.json: `eafe4e00462795919c9c1e6361b91bcee30b8626897dfdf3886b7f53fd6330d2`
- packet manifest (on disk): `e34c9f72be3d0191705ce019b8634e32eaa960a4521342d3fa9a70f810558f71`
- unreferenced bundle: `0f9fb73ca0383fbdc901c8502f67996ecbbe865d545774e577f1dc4f71faa14e`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 37 of 37 implementation hashes match; exactly 61 strict-ancestor entries; all 930 blobs hash to their names; all three diff sections read. |
| Unassisted | No coverage field, no assistance flag. Standing instructions byte-identical to the unassisted guidance 4 prompt (39/004). |
| Opening context | Message, author, parent `2445cab0` and task SHA match Git. Cutoff is the committer date, 2025-04-17T11:16:38+02:00. |
| Catalog | Eight rows: 1, 4, 7, 10, 14, 15, 16, 17. Checked against GitHub: those are exactly the issues and pull requests created before the cutoff and still open at it (16 and 17 closed later the same day; 18 was created the next day). No snapshot timestamp after the cutoff. Four were read and are described accurately as unrelated. |
| Source claims | Verified against the diff. One block of 1,024 threads, a shared integer histogram of at most 1,024 bins, the reference pass over all 65,536 states through `decode_3inst_f` and then the input pass, each normalised by its own sample count; the index mapping and end-bin clamping; the wrapper's device guard, current stream, float32 check on the input only, bin count from `ref_output` and the "Too many bins" check; the binding; the header declaration. `decode_pcb_f` selects 3INST with 2MAD commented out. No caller in the parent tree or the task tree. |
| Finding | Holds. The bin count comes from `ref_output` alone and both write loops use it, so a shorter `dist_output` is written past its end. Suspected, unexecuted, reach stated as direct callers only. |
| Scalar check | Re-ran: output identical. I compared the transcription with `decode_3inst` in `codebook.cuh`: same multiplier, addend, mask and xor constants, and the sum of the two half-precision halves. |
| Tests | 209 passed earlier in this session on the same implementation hashes. |

## Not verified

- No build or GPU run.
- The extrema (about plus and minus 3.97) come from the standard-library model of half-precision addition, not from CUDA.

## Must fix before canonical use

Reviewer-only.

1. The finding stops at capacity. The same wrapper also does not check that the two outputs are float32, on the input's device or contiguous, or that the input is contiguous or non-empty (an empty input divides by zero in the normalisation). A canonical entry should list the unchecked preconditions together.
2. The file-match hints named five ancestor entries for these files and none was read. Nothing in the entry depends on them, so this is a note, not a gap.

## Next

Record this approval and continue the walk from commit 63.
