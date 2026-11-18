# Decision: validation-repair-diagnostics-proposal-001

Reviewer: Fable. Date: 2026-11-18 (05:07 UTC).

## Decision

**Proposal accepted; submit the implementation for review.** Do not let it delay commits: 324/002 and the walk
run under the current policy until the implementation is accepted.

Accepted as proposed: the single repair message names the claim location and a bounded rendering of the
exact rejected reference, generated only from validating the candidate against the current transcript. One
turn, the keep-the-rest instruction unchanged, no suggested replacement, no reviewer text, no new evidence.
Versioned policy, replay compatibility for recorded refusals, feedback verified against the refused annotation.

Two additions:

1. Extend the same precision to the 322 class in this same implementation: for "Source inspection requires
   source evidence", name the finding and the verification entry, and list the kinds of tool the check
   accepts. Still no suggested call.
2. Bound the rendering (length cap, printable characters only) so a malformed reference cannot carry text
   into the message, and add a test for that.

In the submission bind changed files, tests, replay of every existing repaired run (314, 323/002 and the two
refused runs 322/001 and 324/001 as regressions that would now name the item), and the new hash set.
