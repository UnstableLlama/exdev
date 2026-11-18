# GPU test worker

A second, parallel worker that runs the code. The teacher walk explains each upstream commit from source and
records suspected defects in `reports/defect-ledger/`. Almost none of those findings has ever been executed:
on 18 November 2026 the ledger held 223 identities, 202 still `suspected`, and only 6 checks of 319 were
`repository_execution`. The walk machine has no GPU. This worker runs on a machine that does, and tries to
reproduce each finding against the real repository at the real commit.

It does not write explanations, does not touch the walk, and does not change the ledger. It produces
execution reports that the reviewer checks and the author then cites in a ledger revision.

## Roles

| Who | Where | Does | Never does |
| --- | --- | --- | --- |
| Teacher and author (Codex) | walk machine | explains commits, files ledger records | runs GPU code |
| Reviewer (Fable) | walk machine | reviews entries; reviews execution reports | edits prose or reports |
| **GPU worker (Opus)** | GPU machine | reproduces findings, writes execution reports | edits entries, ledger, reviews, teacher code; pushes to `main` |
| User | both | starts and stops workers, decides policy | |

## What a test is

One ledger identity at its latest revision gives a trigger, an expected behaviour and an actual behaviour,
plus the commits where it was introduced, where it is known to persist and where it was fixed. A test:

1. Checks out upstream `exllamav3` at one of those commits in its own worktree. The source is never edited.
2. Builds an environment that commit can run in (Python, Torch, FlashAttention, the native extension).
3. Runs the smallest script that performs the stated trigger and records what happened.
4. Compares that with the stated actual behaviour: same failure, at the same place, or not.

Where a fix commit is recorded, the strongest test is a pair: the same script at the fix's parent and at the
fix. Failing before and passing after confirms both the defect and the fix.

## Outcomes

- `reproduced`: the stated trigger produced the stated behaviour.
- `fix_confirmed`: reproduced at the fix's parent and absent at the fix, with the same script.
- `not_reproduced`: the trigger ran and the stated behaviour did not occur. This is as valuable as a
  reproduction; say exactly what happened instead.
- `inconclusive`: the script ran but does not settle it. Say why.
- `blocked`: could not build or reach the trigger in the time allowed. Say what stopped it.
- `not_testable_here`: needs something this machine cannot provide (GitHub Actions, Windows, a gated or
  very large checkpoint, a release upload). No script is forced.

A report never says more than its script did. A stub or monkeypatch used to reach the trigger is disclosed
and lowers the claim: `reproduced` requires the repository's own code path, unmodified.

## Queue

`gpu-tests/export_queue.py` reads the latest revision of every ledger identity and writes
`gpu-tests/queue.json`, ordered so the most informative tests come first:

1. suspected, with a recorded fix (pair test available);
2. suspected defects never executed;
3. other suspected findings;
4. confirmed findings without an execution check (lowest).

Each item carries the ledger file and its SHA-256, the texts above, the commits to test and a rough area
hint (`runtime`, `conversion`, `eval_script`, `packaging_ci`, `native_ext`). The hint is only a starting
point; the worker triages each item itself. Regenerate the queue after pulling `main`: the walk adds records
all day.

## Results

One directory per attempt: `gpu-tests/results/<defect_id>/<NNN>/` holding

- `result.json` (schema: `gpu-tests/result.schema.json`),
- `repro.py` (and any helper files), exactly as run,
- `stdout.txt`, `stderr.txt` for each commit tested,
- `env.json`: GPU, driver, CUDA, OS, Python, Torch, FlashAttention, whether the extension was built, pip freeze hash.

`result.json` names the ledger revision and file hash it tested, every commit tested with its role and
outcome, the model used (repository and pinned revision) if any, what ran, the limits, and the SHA-256 of
every file in the directory. A second attempt at the same finding gets a new number; nothing is overwritten.

## Environments

Historical commits need historical dependencies. The worker keeps

- one bare clone of upstream and a worktree per tested commit (`git worktree`, removed after the test);
- `uv` virtual environments keyed by Python version plus the commit's `requirements.txt` hash, reused across commits;
- a build cache for the native extension keyed by the hash of `exllamav3/exllamav3_ext/` at that commit.

Models are small public checkpoints only, pinned to a revision and recorded. An EXL3 model, when a test
needs one, is quantized with the repository itself at the tested commit; that conversion is evidence too,
and its log is kept. Nothing gated, nothing over a few gigabytes without the user's word.

## Rules that protect the walk

1. **Results never enter teacher input.** A test run in 2026 is later knowledge about a 2025 commit.
   Packets are built from pinned evidence and approved ancestor prose only; `gpu-tests/` is never a source.
2. **The worker never edits the ledger.** A reviewed report is cited by the author in a new ledger revision
   with a `repository_execution` check. Status changes stay in the existing author and reviewer flow.
3. **Separate branch.** The worker commits only under `gpu-tests/results/` and `gpu-tests/STATE.md`, on the
   branch `gpu-tests`, and never pushes `main`. The walk machine pushes `main`; the two cannot collide.
4. **Canonical and training stay false.** An execution report changes neither.
5. **No fixing.** The worker does not patch upstream code, open issues or contact maintainers.

## Review of a report

The reviewer cannot rerun GPU code, so the review is of the evidence: does `repro.py` perform the trigger
as the ledger states it, on unmodified code at the stated commit; do the logs show the stated behaviour; do
the hashes match; are the limits honest. A report that needed a stub to reach the trigger is accepted only
as `inconclusive`. Verdicts go in `reviews/verdicts/gpu-test-<defect_id>-<NNN>.md`.

## Owed before reports can change the ledger

- Ledger validator: accept an execution report as evidence, and decide how a `not_reproduced` finding is
  recorded (today the statuses are `suspected` and `confirmed` only).
- A merge routine for the `gpu-tests` branch into `main` that the reviewer runs after review.

Neither blocks starting the worker: reports accumulate on the branch.

## Starting it

On the GPU machine: clone this repository, check out `gpu-tests` (create it from `main` the first time),
and give the worker `gpu-tests/WORKER-PROMPT.md`.
