# Verdict: commit-000292-architecture-recovery-001

Reviewer: Fable. Date: 2026-11-17 (13:29 UTC). Upstream `47d83f56` "Add Ernie 4.5 model (text only)".
Stopped run: none exists (the reservation at 292 failed before any packet or run). New run: `.teacher/runs/commit-000292-001`.

## Decision

**The reference discovery is accepted and the proposed queue recovery is authorised, including first-packet
use.** No approval of any entry is given here.

## What I checked (my own queries to the official API)

- The publisher listing for `baidu` shows 39 repositories. For every one I took the latest commit at or
  before the cutoff 2025-07-07T02:18:07Z. All fifteen pins in the request equal that commit.
- Eight further repositories have an eligible revision and are not selected; all eight are the `VL`
  variants. I read two of their configurations at the eligible revision: both declare
  `Ernie4_5_VLMoeForConditionalGeneration`, which this commit does not register. Correctly left out.
- Bundle `data/evidence/github/000292-references.json`: triggers `Ernie4_5_ForCausalLM` and
  `Ernie4_5_MoeForCausalLM` from the two new class files, no unresolved files, fifteen selections (four
  dense, eleven MoE). Request hashes match.

## Mechanics

`recover --retry-position 292` bound to this verdict, recover the GitHub inputs, prepare
`.teacher/retrieval/000292-001` from the current approved selection (it must include 291), then the
prepared forward route with `original_packet` equal to that new packet. Allowed because no earlier packet
exists for 292. One teacher attempt, unassisted, guidance 12. If fetch or preparation fails, stop and file
a request.

## For the review request

State the catalog and path-only counts, sparse or complete, and the header preflight result over all 658
headers. Say which checkpoints' headers the teacher read. I will compare the branch-deciding tensors across
all fifteen checkpoints myself, including the Paddle, FP8, 2-bit and W4A8C8 variants.
