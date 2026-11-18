# Opt-in walk orchestration

Administrative code only. Do not enable this driver until Fable accepts
`reviews/verdicts/run-ahead-implementation-002.md`. Ordinary `teacher.cycle`
and its packet, prompt and implementation fingerprints are unchanged.

After acceptance, migrate an inactive journal once:

```
python3 -m orchestration.run_ahead enable --state reports/teacher-walk-001.json --verdict reviews/verdicts/run-ahead-implementation-002.md
```

Migration preserves stops and pauses. It moves the single handover and pending
replacement reviews into `review_queue`; it does not record an approval or
resolve a failure. Back up the journal before the one-time migration. Do not mix
the legacy state-mutating approval/publication commands with the migrated driver.

## Queue operations

* `cycle --state STATE` reserves one forward session and runs the legacy cycle
  against a private journal. Every completion requests full review, including
  work formerly eligible for mechanical approval. It runs only one position.
* `publish --state STATE --run RUN --request PATH` binds a completed request.
  File it immediately. A completed unpublished draft prevents another launch.
* `approve --state STATE --run RUN --verdict PATH` verifies the exact request,
  artifact hashes and decision, replays validation, and records ancestor-only
  approval. Forward approvals must be in ascending position order. An older
  approval never changes the next unstarted position or another active session.
* `stop --state STATE --run RUN --verdict PATH --outcome rejected` (or `held`)
  records a stop. The active session may finish; no new session may start.
* `recover --state STATE --verdict AUTHORIZATION [--retry-position N]` is an
  explicit operator recovery, not an automatic interpretation of a verdict.
  Check the decision's authorization before invoking it. A retry is prepared
  separately, preserves the original packet and blocks other launches until its
  verdict. Rejected forward work needs an approved retry before resuming.
* `prepared --state STATE --spec SPEC` runs a replacement or authorized retry.
  The JSON spec binds `kind`, `position`, `run`, `packet`, `original_packet` and
  `authorization` (`path`, `sha256`). Replacements also bind `supersedes_run`
  and `preflight` (`path`, `sha256`). The existing header preflight must pass;
  only the guidance field may differ from the original replacement manifest.
  An attempted replacement consumes its queue slot in history; a further
  attempt needs a new reviewed plan, not an automatic retry.

Use `python3 -m orchestration.run_ahead ACTION ...` for those operations.
For a detached forward cycle use `setsid -f python3 -m orchestration.notify
--state STATE --notify-thread THREAD`, redirect its launch output, confirm its
log and end the turn. The supervisor sends one completion notification using
the existing queue transport. Notifications grant no advancement permission.

## State and evidence

The legacy `.cycle.lock` covers the entire teacher session. A separate short
`.queue.lock` serializes atomic journal updates, allowing verdict recording
during a session. `active_session` identifies the reserved session;
`status == running` remains true through preparation and execution. The watch
script's stall check and request-without-verdict rule continue to apply. Its
process check also recognizes the new modules.

The combined cap is three reserved, unpublished or pending forward/replacement
items. `next_position` means next unstarted forward position. Each reservation
captures approved entries and pending positions with changed-file overlap.
Requests must include `Ran ahead of: N, M.` when applicable, plus the overlap
details from `review_queue[].ran_ahead_of`. These records and implementation
hashes stay administrative; they are not teacher input.

Sparse ancestor packets retain complete Git ancestry but export prose only for
approved strict ancestors. `approved_ancestor_selection` binds that subset;
the isolated reader exposes the corresponding catalog. Approved artifacts are
checked against their review hashes and source identity. When the selection is
complete, the original attachment and worker paths are used byte for byte.

## Recovery limits

Architecture/discovery stops, failed validation, worker crashes and interrupted
reservations stop the queue. Inspect the private snapshot/log and preserve all
outputs; do not clear a reservation merely because a process disappeared.
Later completed runs remain immutable. Dependency gaps require reviewer
judgement before a rerun or resumption. The driver does not decide policy.

An interruption between writing a run's `review.json` and committing its
journal approval can leave those two artifacts inconsistent. Stop and reconcile
them against the bound verdict before another operation; never infer approval
from queue capacity. Reaching the end of history also stops for administrative
review instead of silently advancing. Prepared sessions use the same session
lock but require an operator-managed detached supervisor if run in background.
