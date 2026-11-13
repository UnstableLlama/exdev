# How Fable and Astra exchange reviews

Set up on 2026-11-11 so the user no longer carries messages between the two agents.

- Astra requests a review by writing `reviews/requests/<run-name>.md`. Each request has a `Reply-to thread: <uuid>` line and
  a SHA256 list of the artifacts under review.
- Fable writes one verdict per request to `reviews/verdicts/<same-name>.md`: decision first, artifact hashes, a checks table,
  what was not verified, reviewer-only items for canonical use, follow-ups, next step.
- Fable wakes on a background shell loop, not a timer:
  `while true; do for f in reviews/requests/*.md; do b=$(basename $f); [ -e reviews/verdicts/$b ] || { echo "PENDING $b"; exit 0; }; done; sleep 15; done`
- After each verdict Fable notifies Astra:
  `codex queue --thread <uuid> --resume -C <repo path> --message "Verdict ready: reviews/verdicts/<name>.md — <one line>"`
- Approvals are for ancestor retrieval only. Canonical and training stay false.
- Verdict kinds: APPROVED, REJECTED (incorrect claim), REJECTED: thin (with a `commit-N-A.coverage.md` request for one
  assisted attempt), HELD (needs a user decision), and for implementation requests ACCEPTED or NOT ACCEPTED.
- User decisions are recorded by Fable as `reviews/verdicts/<topic>.decision.md`, quoting his words and saying which parts
  are Fable's interpretation.
- Coverage requests are pointers and questions only: no conclusions, nothing after the commit's cutoff, no length quota.
- Reviewer knowledge from later history stays in a verdict's reviewer-only section. It never goes into a coverage request
  or a packet.
- Committing: only when the user asks, straight to `main`, with a note to Astra first because both agents write in the
  same checkout.
