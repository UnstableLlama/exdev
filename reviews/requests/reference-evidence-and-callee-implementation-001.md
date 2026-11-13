# Implementation review: architecture references and changed dispatch

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Decision: `reviews/verdicts/reference-evidence-and-callee.decision.md`, SHA256
`e2a1425cc6f30db79646f2bead50be26e0a2500f63c3d0400b835ce5947f3fa7`.
Implementation report: `reports/reference-evidence-and-callee-implementation-001.json`, SHA256 `6a303806620417ad24b33d6d08210111e184af46641d875c8209b17f73b4c152`.

Commit 43 approval is recorded, bound to your verdict path and hash. The walk
is stopped before commit 44 awaiting the user's decision about replacements
for 39 and 41. None of those runs has been started. This is an implementation
review, not a request to approve any new prose; canonical and training remain false.

## Changes

- Trusted first-parent trigger detects newly registered keys and new model/config
  class files. It inspects registry dictionary structure across model Python
  files, including renamed registries with that structure.
- Recovery takes an explicit curator selection with architecture, repository,
  reason and candidates considered. It uses the root HF recovery/range tools,
  selects the latest cutoff-eligible immutable revision, retrieves configuration
  and tokenizer JSON plus safetensors headers, and skips weight payloads.
- No eligible revision yields no objects and a report. Missing required roles,
  incomplete recovery, mismatched architecture, task or cutoff block preparation.
  Selection reasoning stays administrative; only evidence objects reach teachers.
- Contract v5 separately binds reference bundle bytes and object signatures.
  Referenced GitHub evidence retains its separate fail-closed gate. Legacy
  contracts and prompts remain unchanged.
- Guidance version 2 adds the general changed-dispatch rule only on new walk
  packets. No commit-specific instruction or reviewer hindsight was added.

## Validation and requested checks

Full pinned host-enabled suite: **195 tests passed**. Coverage includes registry
and class-file triggers, neither case, missing recovery, cutoff selection,
no eligible revision, header-only requests and skipped weights, object binding,
architecture roles and legacy/new guidance behavior. `git diff --check` passed.
Please inspect trigger coverage, recovery roles, cutoff handling, selection
provenance, separation from issue bundles, validation and prompt compatibility.
The report lists exact implementation hashes and known limits. No live HF
reference repository was selected or recovered in this session.

Write only `reviews/verdicts/reference-evidence-and-callee-implementation-001.md`.
The walk remains stopped regardless of this implementation verdict until the
user's replacement-order decision arrives.
