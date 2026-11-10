# Ancestor approval policy v1

Policy identity: `exdev-mechanical-ancestor/v1`. This is an administrative policy, never a teacher instruction. Both mechanical and reviewed approvals grant ancestor retrieval only; canonical and training approval remain false. Commit 3 was explicitly accepted by the user-supplied Fable review and is recorded as a reviewed approval, not retroactively labeled mechanical.

## Retrieval metrics

New runs write a coverage object even when there is no chapter assignment. `retrieval_usage` reports the number and identities of distinct ancestor entry/chapter targets indexed for the task's exact changed file paths, plus every ancestor content-read call, its target and whether it succeeded. Multiple page reads count as multiple calls. Catalog/search calls do not count as prose reads. Missing legacy index/path metadata is labeled unavailable. Existing historical reports are not silently rewritten.

The metric is report-only: zero retrieval calls never fail authoring, coverage or approval. The metric is not sent back to the teacher and does not generate instructions to retrieve more.

## Tier decision

Trusted code checks changed paths against the Git diff with rename detection disabled, so both sides of a rename are included. The teacher's type label or self-assessment cannot select a tier. Mechanical approval requires all of:

- Exactly one parent.
- Every changed path is Markdown (`*.md`), under `doc/`, an image (`png`, `jpg`, `jpeg`, `gif`, `svg`, `webp`, `ico`, `bmp`, `tif`, `tiff`, `avif`), `.gitignore`, under `.github/`, or exactly `LICENSE` or `NOTICE`.
- No requirements file (basename starting with `requirements`), `setup.py`, or file ending in `.py`, `.cu`, `.cuh`, `.cpp`, `.h`, `.json`, even inside an otherwise allowed directory. A mixed doc/code commit is full review.
- An explicitly empty findings list and no execution-basis claim, including chapter claims.
- Schema and recorded-transcript replay pass, saved Markdown matches, the saved coverage report recomputes exactly, and every task-diff section was fully read. Original manifest and artifact hashes are rechecked by approval.

Anything else is full review. Validation errors stop the walk rather than manufacturing an approved draft. A missing/incomplete diff read selects full review; the retrieval usage count does not. Empty changes are conservatively full review.

Mechanical approvals identify the policy name/version as reviewer and record `approval_kind: mechanical`, tier reasons, changed paths and sampling status in `review.json`. Human/Fable approvals use `approval_kind: reviewed` and their actual attribution. Neither is a claim of formal certification.

## Sampling, handover and rejection

A mechanical draft is sampled exactly when the first byte of its full commit SHA is below `0x1A` (26/256). A sampled mechanical draft is approved provisionally for ancestor use without waiting for Fable. Sampling is deterministic and no model decides it.

`teacher.walk` journals each run before authoring, proceeds sequentially through mechanical approvals, and stops after authoring the first full-review draft. Its handover includes that draft and all sampled mechanical drafts since the last handover. Stops and failures require explicit review/recovery; rerunning the command does not bypass them. The history tip is pinned in the journal. There is no task-specific reviewer steering of the teacher.

```sh
python3 -m teacher.walk --state reports/teacher-walk-001.json
python3 -m teacher.approval_policy --state reports/teacher-walk-001.json --reject-sample RUN_DIRECTORY --note 'User-supplied rejection rationale'
```

On a sampled rejection, trusted code first persists a stopped state. It marks the rejected run rejected and **every later run in the chronological journal** `needs_reauthoring`, even if no actual retrieval is visible. Their ancestor eligibility is revoked; exports already require approved status and therefore reject them. Immutable drafts/transcripts are retained. The rejection command is idempotently repeatable after interruption. Existing prepared packets are retained as invalidated historical artifacts, not reused by the stopped walk. Before any restart, rebuild affected packets and author fresh run directories; do not repair old authored prose.

The initial journal starts at commit 4 with the reviewed root, commit 2 and commit 3 as its approved baseline. Earlier runs predate the new mechanical policy and are not part of its sample population. The journal is local trusted administrative state, not a provider tool.
