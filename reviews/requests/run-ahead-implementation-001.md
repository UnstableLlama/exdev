# Run-ahead implementation 001 — design and current blocker

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

The current tooling cannot implement the user's run-ahead decision safely. This is a design request, not a claim of completed or tested implementation, and does not request permission to use run-ahead yet. No runner code, packet, authored run, approval or journal state was changed for this request. Assisted 255/003 continues under the existing sequential procedure. Work order remains 255/003, replacement 234, then 256 onward. Nothing is committed or pushed.

## Blocker

`teacher.walk.publish_review_request` maintains one `handover.full_review` and changes the global state to `awaiting_full_review`. Both `teacher.walk.resume` and `teacher.cycle.guard_state` require `ready`. `teacher.cycle.approval` selects that single handover and resets `next_position` to the approved position plus one. The cycle holds the journal lock throughout the teacher session. Existing replacement supervisors also assume a single ready journal. Clearing these stops by hand would lose review state and would not enforce the cap or ordered approval.

## Proposed implementation

Introduce a durable review queue separate from the active-session record and the next unstarted forward position. Preserve legacy journals through an explicit, tested migration of the current handover. Keep rejected, held, failed and recovery states as explicit stops requiring judgement; queue capacity is not authorization to bypass them.

At launch, reserve the single teacher session and a review slot under a short journal lock. Count outstanding requests and reservations across forward and replacement work, with a maximum of three; conservatively reserve capacity for any run that could require full review. Capture the unresolved earlier positions at launch in an administrative run record. Prepare packets exclusively from approved strict ancestors, never pending prose. Bind the resulting approved-entry selection; report “ran ahead of N, M” in each applicable request without passing reviewer information to the teacher.

Separate the session lock from short journal-update locks so a verdict can be recorded during a teacher session without concurrent teachers or lost state writes. Publishing a request appends to the durable queue rather than replacing a handover. Requests are filed immediately when ready. Detached notifications identify the exact run/request; replacement work uses the same session reservation and queue accounting.

Select approvals by exact run and request hashes. Record forward approvals in ascending position order and reject attempts to record a later position while an earlier position remains unresolved, including mechanical approvals. Do not rewind the next unstarted position when recording an older approval. Keep later completed runs immutable if an earlier run is rejected; expose the dependency gap and stop advancement for reviewer judgement/rerun instructions. Replacement approvals retain their explicit supersession path and existing plan conditions.

## Validation required before live use

Implementation review must include the full host-enabled suite and focused cases for legacy migration; three-request capacity and an active reservation; mixed replacement/forward requests; omitted pending ancestor prose; launch-time ahead-position reporting; ordered approvals and mechanical handling; concurrent publication/approval without lost writes; duplicate/stale notifications; failure/rejection/hold recovery; and unchanged packets/prompts when no run-ahead is used. No live teacher smoke run before acceptance. The existing 255/003 session is not a test of this change.

Until completed implementation and validation receive acceptance, continue one request at a time under the existing gates. The decision is recorded as pending implementation; no new teacher is launched by this request.

## Decision binding

- reviews/verdicts/run-ahead-001.decision.md: `0fbb5b4728164d65bd51a5e883831e2bac825d7fcf64ddb4f0095ce0fbeeedb0`

Reply in `reviews/verdicts/run-ahead-implementation-001.md`.
