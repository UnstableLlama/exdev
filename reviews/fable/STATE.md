# STATE: exdev (~/git/exdev)

Current picture, refreshed 2026-11-13 late afternoon (second session of the day). The repo's README, `docs/`, `reports/` and `reviews/verdicts/` are the
detailed record; this is the map. A copy of this file, my review script and the mailbox notes are in the repo under
`reviews/fable/` so another machine can pick the role up from a clone.

## What it is

Builds a historical Encyclopedia and code graph of exllamav3 (2,264 commits, pinned tip `bd1f519`), commit by commit with no
hindsight, to generate training data later. Source mirror in `.sources/exllamav3.git` (ignored). No training traces exist yet.

## Who does what

- **Astra** (OpenAI `gpt-6-astra`, in Codex, same checkout) writes all code, runs the teacher sessions, keeps the ledger and
  records approvals. Its handoff rules are in `reviews/AUTHOR-INSTRUCTIONS.md`, loaded through a root `AGENTS.md`.
- **I am Fable, the reviewer.** I write only under `reviews/verdicts/` (`commit-N-A.md` verdicts, `<topic>.decision.md` for
  user decisions quoting his words, `commit-N-A.coverage.md` coverage requests) and, since 2026-11-13 at the user's request,
  my own notes under `reviews/fable/`.
- Loop: a background shell loop waits for a file in `reviews/requests/` with no same-named verdict:
  `cd ~/git/exdev && while true; do for f in reviews/requests/*.md; do b=$(basename $f); [ -e reviews/verdicts/$b ] || { echo "PENDING $b"; exit 0; }; done; sleep 15; done`
  I review, write the verdict, then `codex queue --thread <uuid> --resume -C <repo> --message "Verdict ready: ..."`. Each
  request carries `Reply-to thread:`; the id is per Astra session and per machine (2026-11-13: `01a1d636-5761-7593-8e19-f8453a562b16`).
- Tests: pinned Codex first on PATH or two wire tests error:
  `PATH=/home/unstable/.codex/packages/standalone/releases/0.167.0-x86_64-unknown-linux-musl/bin:$PATH EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`
  (223 passing, about 14 s).

## Where the walk is

- Approved for ancestor retrieval only (never canonical or training): **commits 2-74**. The walk is **paused by the
  user** (2026-11-13, about 16:40 PST) with `next_position: 75`. Astra acknowledged in `reviews/PAUSE-ACK.md`.
- **Owed before 75: commit 39 attempt 006, unassisted**, with Deci's own repositories added to the reference evidence
  (user decision `commit-000039-deci-references.decision.md`). Astra's discovery found five complete Deci repositories
  and one GGUF repository with only a `config.json`; its validator refuses the incomplete one. My answer is in
  `reviews/verdicts/commit-000039-reference-scope.md` (attach the config, record what does not exist). Astra treats
  this as a user choice; the user has seen my answer and can overrule it. 39/005 stays in force until 006 is reviewed.
- Entries in force that are replacements: 17/003, 32/002, 39/005, 41/002, 44/003, 45/002, 55/002, 69/003, 71/002, 72/002.
  Reviewer-assisted: 39/005, 44/003, 45/002, 55/002, 71/002.
- Today's session (70-74): 70/001 approved; 71/001 rejected thin, 71/002 approved assisted; 72/001 rejected because
  the reference bundle missed three official GLM-Z1 models, 72/002 approved unassisted; 73/001 and 74/001 approved.
  `reference-discovery-implementation-001` accepted (enumerate the whole organisation, match on the pinned config's
  architecture string, no name filter).
- Findings recorded in drafts, not yet in Astra's ledger: `fp32-mlp-intermediate-contract` (71, I agree),
  `partial-rope-frequency-load` (72, confirmed at source level; introducing commit not yet established),
  `zero-block-scale` (74; real but harmless, an all-zero block still decodes to zeros). Older, still unrecorded: the
  empty-block division (39 to 45) and issue 16 / tokenizer truncation (fixed at 69).
- Reviewer-only knowledge to carry: at commit 71's parent a packed-scale EXL3 layer got no input sign flips in forward
  and `get_weight_tensor` would raise on a tensor truth test; 71 repairs both in passing and no entry says so. GLM4
  checkpoints store only the fused `gate_up_proj`; 9B has q/k/v biases; all BF16 (72's headers, unread by the teacher).
  The paged cache encoder's launch geometry may overrun a token when groups per token exceed 32 and do not divide
  evenly (74, not worked out).

## Rules in force (user decisions; files in `reviews/verdicts/`)

- `commit-000017-001` + `catalog-hints`: titles-only catalog of discussions open at the cutoff, with path hints and a reading rule.
- `reference-evidence-and-callee`: attach reference model configs and headers when a commit adds an architecture; read the
  callee when dispatch changes.
- `evidence-index-and-config-reading` + `config-reading-amendment`: all ancestor-attached evidence offered through a compact
  index; read the config.json of every listed model of the architecture the task adds or changes, no opt-out.
- `thin-entries-and-retroactive`: I may issue `REJECTED: thin` with a coverage request (pointers and questions only, no
  conclusions, nothing past the cutoff); such runs are flagged `reviewer_assisted`. I allow one assisted attempt per commit.
- `closed-discussion-salience` (2026-11-13 evening): a second catalog of closed discussions, gated by term overlap with the
  task, no time window. Accepted implementation: a row qualifies only on **commit-message** terms (score sum of 1/df² ≥ 1).
  The mechanical definition is mine; a time window must go back to the user.
- `commit-000039-deci-references` (2026-11-13): re-author 39 with Deci's repositories. From now on reference discovery
  covers every organisation that officially publishes the registered architecture, the original publisher included.

## How I review a run

`python3 reviews/fable/check.py NNNNNN AAA` from the repo root (same file as in my continuity folder): artifact hashes,
evidence hashes against the transcript, final message equals annotation, render equals draft.md, policy assess,
implementation hashes, packet ancestry, blob hashes, opening context against Git, no timestamp after the cutoff. Its
"system same as 32-002" line is stale; diff the system prompt against the previous run by hand (nothing, or exactly one
sentence). Then by hand: catalog against GitHub (`gh api`), every claim against upstream at parent and task, replay the
`run` call, findings traced independently, hindsight grep of the packet (search for ledger ids and `reviews/verdicts`;
the bare word "hindsight" matches tokenizer vocabularies). Verdict sections: Decision, Artifacts, Run checks, Not verified,
Must fix before canonical use, Follow-ups, Next.

## Open threads

- Astra's required fixes 1 and 2 to the new-architecture trigger, due before position 100.
- Five older ledger files have origin `reviewer_observation`, which the validator rejects. Inherited findings must stay one
  defect with several observations.
- Whether `run` output that prints repository files should count as a read. Astra now reports such calls separately.
- Expectation to check later: issues 99 and 233 should be listed by the closed catalog at positions 560 and 1100.
- Undecided by the user: whether reviewer-assisted entries qualify for canonical use or training.
- Discovery tool follow-ups: a missing root `config.json` should be its own status, not `unavailable`; the validator
  should tell "file never published" from "could not fetch".
- Validation marks a run incomplete when a binary diff section (an image) is unread; it should be "unreadable". The
  teacher cannot read images, so 74's only quality evidence (`doc/cq_humaneval.png`) is described by nobody.
- When a commit adds an architecture, check the reference list myself against the publisher's organisation before
  reading the entry. At 72 the list was half complete and only an outside check showed it.
- Pace today: five commits, two rejections and one implementation review in about 75 minutes.

## Git and other machines

- Pushed to `main` twice on 2026-11-13 at the user's request; the second push carries everything through the 74/001
  verdict and the pause. Straight to main,
  because Astra works live in the checkout.
- **Not in Git** (ignored): `store/` (35 GB: code graphs, logs, timeline database), `data/` (1.1 GB, includes the hash-bound evidence bundles), `.sources/` (upstream mirror),
  `.teacher/retrieval` and `.teacher/validation` (about 14 GB of packets). A clone can read every draft, verdict and
  report, but cannot build or validate packets until those are copied from the work machine. The evidence bundles carry
  retrieval timestamps and are bound by hash, so they must be copied, not re-fetched.
- On 2026-11-13 the user asked for the folder zipped for Google Drive. Two archives in the home directory, which
  together are the whole folder: `~/exdev-2026-11-13-core.zip` (repository with `.git`, `data/`, `.sources/`,
  `.teacher/`: everything the review loop needs) and `~/exdev-2026-11-13-store.zip` (`store/`, `.tools/`, `worktrees/`,
  `.graph-work/`).
