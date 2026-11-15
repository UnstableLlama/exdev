# Verdict: architecture-trigger-fixes-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/architecture-trigger-fixes-implementation-001.md`
Closes: required fixes 1 and 2 (and confirms 3) of `reviews/verdicts/reference-evidence-and-callee-implementation-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**ACCEPTED.** The walk may continue at commit 100.

## Artifacts reviewed (sha256)

All nine hashes in the request match the files on disk.

## What I checked

| Check | Result |
|---|---|
| Code read | `teacher/architecture_evidence.py` in full. |
| Tests | 237 passed with the pinned Codex first on PATH and sandbox tests enabled (9.5 s), run by me. |
| Fix 1 | `administrative_outcome` returns `not_new_architecture` on three bases. `git_renames` is automatic and needs every new class file to be a Git-detected rename whose class list and derived identities equal the old file's. `covered_merge` needs a merge, hash-checked bundles for commits on the merged side that themselves validate and are not administrative, a cutoff no later than the merge's, the expected identities covered and the relevant files byte-identical. `curator_attestation` needs a reason. A registry-key trigger refuses all three; a source-derived new identity refuses everything except `covered_merge`. `load_bundle` recomputes the outcome and rejects a bundle whose stored outcome differs or that also carries items or selections. |
| Fix 2 | Identities are read from the syntax tree of `*Config` classes: an `arch_string` assignment, or the second positional or `arch_string` keyword argument of `super().__init__`, including the `kwargs.get("arch_string", "<literal>")` form the tree uses. Nothing is executed. A new class file with no derivable identity is listed as unresolved and the bundle must say so. |
| Fix 3 | A non-root commit with no model or config classes under `exllamav3/models` or `exllamav3/architecture` raises. |
| History unchanged | I ran the new trigger over walk positions 2 to 99. It fires at 39, 72 and 98 and nowhere else, with the same architecture strings and class files as before. The reference bundles in force for 39, 72 and 98 still validate. |
| The three future cases | `151edc00` "Simplify architecture definitions": one class file, one recognised rename, outcome `git_renames`. `d9906114` "Refactor": 22 class files, 22 recognised renames, outcome `git_renames`. `b2d05c0b` (merge of the Arcee branch): derived identity `ArceeForCausalLM`, refused with or without a bare reason. All as the request says. |

## Things to carry

- At `b2d05c0b` the registry-key detector finds nothing and only the derived identity fires. After `151edc00` the registry
  no longer has the dictionary shape the detector looks for, so from there on the derived identity and the unresolved
  list are the whole guard. That is what fix 2 was for; it works on the one case I could try.
- `curator_attestation` is the one path where a reason alone is enough: a new `*Config` or `*Model` class file with no
  registry key and no derivable identity. It is the right outcome for a helper class and the wrong one for an
  architecture written in a style the parser does not recognise. **Condition:** every bundle whose outcome basis is
  `curator_attestation`, and every bundle with a non-empty unresolved list, must be named in that commit's review
  request with the reason, and that commit gets a full review whatever the mechanical policy says.
- A merge that brings in a branch which added a registry key cannot use `covered_merge` and needs its own recovery at
  the merge. Stricter than necessary, and on the safe side. Leave it.

## Not verified

- The `covered_merge` path on a real merge. No such case exists before position 100; the first real use should be
  flagged in its request.
- The earlier verdict's three minor items (guidance-version comparison, cache file overwrite, binding the history file
  for `no_eligible_revision`) are not part of this request and remain open.

## Next

1. Record this acceptance.
2. Continue the walk at commit 100.
