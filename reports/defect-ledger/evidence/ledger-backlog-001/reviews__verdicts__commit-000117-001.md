# Verdict: commit-000117-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000117-001`
Packet: `.teacher/retrieval/000117-001`
Upstream: `04dc55717c499539504b9a3d8454d631de84f7c2` "Fix assertion"
Request: `reviews/requests/commit-000117-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. One line; the entry says exactly what was broken, shows it with the extracted
statement, and correctly notes that the factory route could not reach it.

What it lacks is history: it read no ancestor prose, so it does not say that this is the defect the entry for commit
102 recorded when the parameter was removed. That is a canonical-use gap, not an error.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 6 of 6 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review (the sampling bit is set, and it was sent for full review anyway, as the request says); 41 of 41 implementation hashes; exactly 116 strict-ancestor entries; 1,723 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 6 of 6 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 116/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29. Matches the twelve open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | In `Config.__init__` the assertion message's `{expect_arch}` becomes `{self.arch_string}`. The predicate `arch == self.arch_string` and everything else are unchanged. Correct. |
| Problem | At the parent `expect_arch` is not a parameter, local or global of `Config.__init__` (the whole parent tree has it only in that line and in the docstring), so on a mismatch the message expression raises `NameError`. Correct. |
| Constructor order | Reads `config.json`, asserts exactly one architecture, compares with `self.arch_string`, then builds the safetensors collection. Correct. |
| Factory | `Config.from_directory` reads the same file, asserts the architecture is registered, and constructs that architecture's `config_class`; so through the factory the constructor's comparison always holds. Correct, and the entry's "repairs the constructor's mismatch path, rather than adding support for unknown architectures" follows. |
| Execution | The `run` call reads `exllamav3/models/config.py` from the parent tree, extracts the assertion, and executes it and its patched form with stand-in objects. Output: match passes both; mismatch gives `NameError` before and `AssertionError: Unexpected architecture Other in /model/config.json, should be Expected.` after. Matches the prose. One `run` file read, as the request reports. |
| Discussions | PR 4 is a one-word spelling fix in `config.py`; issue 7 is an extension import failure. The entry says the only link is the filename. Correct. |
| Reads | `repo_read` of `config.py` complete (6,190 bytes). |
| Findings | None, and I found none. |

## Reviewer-only notes (never to a teacher)

- The defect was introduced by `151edc00` (position 102, "Simplify architecture definitions") and recorded there as
  `architecture-mismatch-diagnostic`. This commit fixes it. The retrieval index offered `151edc00` as a matching
  target; the session did not read it.
- The docstring line `:param expect_arch:` is still there after this commit. Documentation only.

## Not verified

- Full configuration loading or model initialisation.

## Must fix before canonical use

1. A canonical entry should name `151edc00` as the commit that introduced the broken message, and link to it.

## Follow-ups

1. Ledger, when next revised: `architecture-mismatch-diagnostic` (102) is fixed at `04dc5571`; the stale docstring
   parameter remains.
2. Execution accounting: this is the second `run` that executes repository text (after 101). Count it the same way.

## Next

1. Record this approval.
2. Continue the walk at commit 118.
