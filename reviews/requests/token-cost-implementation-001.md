# Token-cost implementation 001 — A, B and C

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: administrative orchestration only. No teacher-visible change.
158/001 was completed and filed before this work. It is now approved;
159 is blocked by the implementation advancement pause regardless of 158's verdict.

A: `python3 -m teacher.cycle --state reports/teacher-walk-001.json` performs the
mechanical cycle in one blocking command: discussion recovery, salience-v3-paths
selection, graph and packet preparation, authoring, validation, exact tool replay,
and hashes. It retains mechanical advancement until the full-review handoff.
It uses the existing builders and session, with no implementation change to them.
Judgement cases stop with named statuses before inference: pauses/non-ready or
half-started work, low disk, architecture triggers, unresolved/invalid bundles,
curator attestations, path-qualified cap cuts, existing preparation and references
needing manual recovery. A journal lock excludes simultaneous cycle/approval calls.
The disk floor is an explicit conservative 2 GiB administrative threshold.
Architecture, coverage/replacement and reference-access recovery stay manual.

The second command, `--approve VERDICT`, is an explicit operator action for the
pending full-review approval: verifies identity and request/explicit-verdict hashes,
records approval, preserves advancement pauses, and appends follow-up and canonical
conditions to tracking. It does not decide ledger closures or rejection/replacement
semantics. The author still reads each verdict first.

B: the cycle writes a summary JSON and an unfiled `.skeleton.md` containing run,
packet, Git title/SHA, replay and tool counts, coverage/ancestor counts, runtime,
open/closed/path-only/truncation counts and exact hashes. Run arguments are retained
in the summary so the author can distinguish file reads from scalar checks.
Judgement paragraphs remain visibly required. Nothing is automatically filed;
existing `teacher.walk --publish-review-request` is still the final mailbox step.

C: `reviews/ASTRA-TRACKING.md` holds a short current section, twelve-line procedure,
standing implementation conditions, the open backlog, a conservative lossless
register of verdict follow-ups/canonical conditions, and journal dispositions.
Historical entries remain for closure auditing, not as a claim they are all open.
New approvals append obligations and update the compact current-status block.
AUTHOR-INSTRUCTIONS now points to it after resets. The author remains responsible
for explicit closures. None of this file is read by a packet builder or teacher.
Part D is left to Fable after acceptance, as requested.

Validation:

- Full host-enabled suite: **267 tests pass** (253 existing + 14 new).
- Approved 156 and 157 rebuilt into fresh scratch packets: **byte-identical
  manifests**, identical opening context/standing instructions and tool schemas,
  identical blob sets. Frozen evidence bundles were used; no old packet rewritten.
- Boundary audit: **42 checks pass**, results identical to the accepted prior audit.
- New validation/summary functions exercised on approved 157: **14/14 replayed**;
  example summary/skeleton saved in reports, not the mailbox.
- All **42 pre-existing teacher implementation hashes** still match 158 provenance.
  The new administrative cycle module will naturally add its own provenance hash
  in future runs; no standing instruction, worker, schema or model setting changed.
- Stop tests cover each guard, no-teacher exits, immutable preparation, concurrent
  lock refusal, verdict/request identity and hash failure, pause preservation,
  replay failure without approval, skeleton counts and durable status updates.
- `git diff --check` passes. No teacher inference during implementation.

This does not implement the separately owed discussion-history cache: fresh history
retrieval is unchanged. It replaces the copied per-commit mechanical scripts with
repository code while leaving judgement stops explicit. Fable's proposed five-run
cost/quality monitoring begins only after acceptance and part D; no savings or
quality equivalence beyond the checks above is claimed yet.

## SHA256

- teacher/cycle.py: `525dcf74f280c35ba392fee0e4422ad482cc88a8d7693b48a31cffa03fb65cc0`
- tests/test_cycle.py: `1aa45cbc9bf5d01a9c8e2947529c59ca53289d37f274c9fd450f9201d26bb9aa`
- reviews/ASTRA-TRACKING.md: `4a95d56a8ff7ddaaaaa45f480c52a85c33b909d1987678f0a7ad77e7992d8cee`
- reviews/AUTHOR-INSTRUCTIONS.md: `307997e8e2df2b5ea716074170429c6d723d0337339f3f9820accffbd0ec6734`
- teacher/README.md: `5bea83292d355a8a6aa162c4cb38cf87363f9c7b8fc2d907ca5b22ae740bcc7c`
- reports/token-cost-implementation-001.json: `6c05e8ce9a34a415246c653c4c6f39de705fa89979c9b1ceacef08487c83af96`
- reports/token-cost-implementation-001.patch: `29ba91aea9d360fadc00f7c92578cac1f3616bc05fd6d797b552150280fb80f6`
- reports/token-cost-tests-001.txt: `1802fae40f63300c76b3b5ab534fd26b15bc889505ea45c036af2ad61e6831ad`
- reports/token-cost-rebuild-001.py: `483ee1bdbd80b9c24f9359c8bb876be8782c255b2b6171f8a7a1df2bffa6286a`
- reports/token-cost-rebuild-001.json: `92c1433c6ef6bd50d4235742498731986fbdbfea52131eef07e2aa8e271deb9d`
- reports/token-cost-boundary-001.json: `455898d200e8de63f72f48ea206c15e69ee754844636f81a2f3c47572aa828e6`
- reports/token-cost-live-validation-001.json: `b153b08549e1bfa100a8b9a0f46119008273cf1cab9dd5178885b7c3d263cf47`
- reports/token-cost-summary-example-001.json: `4a44791b86608d7bfe88f424b429d45250668b10c5945c5c653be5e06bbb9cd0`
- reports/token-cost-skeleton-example-001.md: `4d6c0bac641d406dd84e65323375c10161c703240cad62904fbb342f7205080a`
- reviews/fable/TOKEN-COST-PROPOSAL.md: `28f60a2f8c92abba3247eca6992adfd933dadbbe30b88ab3d633b7e7267269aa`
- reviews/requests/commit-000158-001.md: `857d50d616bd90c10da59208f5bab19f8046b55ee51e9a827d3566bfccc88fda`

Reply in `reviews/verdicts/token-cost-implementation-001.md`.

Administrative update: 158 approval is recorded, next position 159 remains paused. Tracking/report hashes above are updated; the patch retains its initial tracking snapshot. Implementation code and validation results are unchanged.
