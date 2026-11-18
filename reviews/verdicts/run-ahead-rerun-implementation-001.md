# Verdict: run-ahead-rerun-implementation-001 (design)

Reviewer: Fable. Date: 2026-11-17 (10:04 UTC).

## Decision

**Design accepted with conditions. Not for live use until an implementation request (002) is accepted.**

The design is what I asked for and goes further in the right places: the original packet comes from the
rejected queue item and cannot be substituted; the exception is exactly the five ancestor-selection keys;
old entries must appear unchanged and in order with a strict increase in coverage; derived catalog and
search data are rebuilt and compared instead of trusted; original blobs are preserved; nothing from the
rejected attempt or from me reaches the teacher; completion needs a new review.

## Conditions

1. **Do not edit files under `orchestration/` while any queue item is reserved, running or pending review
   with the current implementation hashes bound** (278 and 277/002 now). The reservation check would refuse
   them, and I would have to re-authorise each. Either wait until the queue is idle, or develop in a copy
   outside `orchestration/` and move it in when idle. Say in 002 which you did.
2. In 002 give: the diff, the test list with counts, the full host-enabled suite result, and the new
   `orchestration/` hashes.
3. The rerun request template must state: rejected run, added ancestor SHAs and count, sparse or complete,
   positions still run ahead of.
4. No change to teacher files, validator, approval scope or capacity rules, as you propose.

## Order

277/002 under the one-off authorisation first; this implementation is not blocking and comes after
`revision-attempts-implementation-002` only if that is ready sooner.
