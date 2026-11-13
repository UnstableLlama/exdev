# STATE: exdev (~/git/exdev)

Current picture, rewritten 2026-11-13 evening. The repo's README, `docs/`, `reports/` and `reviews/verdicts/` are the
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
  (221 passing, about 13 s).

## Where the walk is

- Approved for ancestor retrieval only (never canonical or training): **commits 2-69**. Next is **commit 70**, under
  contract 8 / guidance 5 / closed-catalog rule `salience-v2`. Astra was asked to pause before 70 on 2026-11-13 evening
  because the user was changing machines.
- Entries in force that are replacements: 17/003, 32/002, 39/005, 41/002, 44/003, 45/002, 55/002, 69/003.
  Reviewer-assisted (written with a coverage request from me): 39/005, 44/003, 45/002, 55/002. 69/002 is assisted,
  approved and superseded by the unassisted 69/003.
- Commit 67 passed Astra's mechanical tier (README only); I glanced at it and agreed.
- Defect ledger: `exllamav3-decilm-kv-head-count` r002 confirmed (introduced 39, fixed 44). Not yet recorded by Astra:
  the empty-block division (found at 39, fixed at 45) and issue 16 / tokenizer truncation (fixed at 69).

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
- Whether `run` output that prints repository files should count as a read (first seen at 69/002).
- Expectation to check later: issues 99 and 233 should be listed by the closed catalog at positions 560 and 1100.
- Undecided by the user: whether reviewer-assisted entries qualify for canonical use or training.
- Pace: about ten commits an hour when unblocked.

## Git and other machines

- Pushed to `main` on 2026-11-13 evening at the user's request (everything through the 69/003 verdict). Straight to main,
  because Astra works live in the checkout.
- **Not in Git** (ignored): `data/` (854 MB, includes the hash-bound evidence bundles), `.sources/` (upstream mirror),
  `.teacher/retrieval` and `.teacher/validation` (about 9.5 GB of packets). A clone can read every draft, verdict and
  report, but cannot build or validate packets until those are copied from the work machine. The evidence bundles carry
  retrieval timestamps and are bound by hash, so they must be copied, not re-fetched.
