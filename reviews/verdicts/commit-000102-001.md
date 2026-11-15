# Verdict: commit-000102-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000102-001`
Packet: `.teacher/retrieval/000102-001`
Upstream: `151edc00b202b645fcfa2cc2c679d7ef381916fb` "Simplify architecture definitions"
Request: `reviews/requests/commit-000102-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry shows the refactor keeps the same eight registrations, and it found the
one thing the refactor broke: the mismatch assertion's message still names the removed `expect_arch` parameter.

The `git_renames` administrative outcome for this commit is **accepted**. First live use.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 48 of 48 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 40 of 40 implementation hashes; exactly 101 strict-ancestor entries; 1,451 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 48 of 48 recorded tool calls return the same result. One of them is a recorded tool error (`max_bytes` of 80,000 refused); it replays as the same error. |
| Diff read in full | The upstream diff is 9,590 bytes; the one `git_show` call asked for 16,000 from offset 0. |
| Unassisted | Standing instructions byte-identical to 101/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path, or the administrative reason text. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22, 24. Matches the nine open rows. |
| Administrative outcome | The bundle has trigger `class_files: [exllamav3/models/gemma2.py]`, no architectures, no items, no selections, and the automatic `git_renames` outcome. Git reports `gemma.py` renamed to `gemma2.py` at 98 % similarity; the class list and the derived identity `Gemma2ForCausalLM` are unchanged. I had run the new trigger on this commit myself when reviewing the implementation and got the same outcome. |
| Diff claims | Each `*Config` gains a class attribute `arch_string` and each `*Model` a `config_class`; the registry becomes a comprehension over eight model classes keyed by `m.config_class.arch_string`; `Config.__init__` loses the `expect_arch` parameter and compares against `self.arch_string`. The eight keys are the same eight as before. Correct. |
| Finding | `architecture-mismatch-diagnostic`: correct. `config.py` line 46 still formats `{expect_arch}` in the assertion message, and line 28 still documents the parameter. On a mismatch the message expression raises `NameError`. `Config.from_directory` picks the class from the file's own architecture string, so the ordinary route cannot reach a mismatch; a direct `SomeConfig(directory)` on the wrong model can. Suspected is right, since the only execution was a stand-in. |
| Reference checks | The entry reads a config for every architecture and claims only that the identifier matches. I did not recheck all 34; the reads replay, and the identifiers for the Deci, NVIDIA and Cohere sets were verified in earlier reviews. |

## Not verified

- Any import of the refactored package.
- Whether anything outside the repository imports `exllamav3.models.gemma`. The entry says the tree has no other user and
  no compatibility module was left.

## Must fix before canonical use

None.

## Follow-ups

- After this commit the registry no longer has the dictionary-literal shape the registry-key detector reads. From
  position 103 on, new architectures are caught by the derived identity and the unresolved list only (see my note in
  `architecture-trigger-fixes-implementation-001`).

## Next

1. Record this approval and the accepted administrative outcome.
2. Continue the walk at commit 103.
