# Verdict: commit-000118-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000118-001`
Packet: `.teacher/retrieval/000118-001`
Upstream: `8d07bfb892c1a9347a962e2e439656528dc56d15` "Fix tkinter import"
Request: `reviews/requests/commit-000118-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry reads the earlier visualizer entry, links to it, and checks the one thing
that could have gone wrong with a function-local import: no method outside the constructor uses the name `tk`.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 10 of 10 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 117 strict-ancestor entries; 1,730 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 10 of 10 recorded tool calls identical. No `run` call. |
| Unassisted | Standing instructions byte-identical to 117/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29. Matches the twelve open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | `import tkinter as tk` leaves module scope in `generator/visualizer.py` and becomes the first statement of `CacheVisualizer.__init__`; one blank line is removed. Nothing else. Correct. |
| Import chain | `exllamav3/__init__.py` and `exllamav3/generator/__init__.py` both import `Generator`; `generator.py` imports `CacheVisualizer` at module scope (line 13). So at the parent, importing the package imported tkinter. Correct, with the entry's "provided earlier imports succeed". |
| Default path | `Generator.__init__` has `show_visualizer: bool = False` and constructs `CacheVisualizer` only inside `if show_visualizer:`. Correct. The truncated `generator.py` read (6,200 bytes, 213 lines) covers those lines. |
| Binding scope | At the task the bare name `tk` occurs only at lines 39, 49 and 51, all inside `__init__`. The three later uses are `self.root.tk.call(...)`, an attribute of the stored root. Whole tree: no other tkinter import. Correct. |
| No fallback | No `try`, no alternative renderer; enabling the visualizer without tkinter still fails, now at construction. Correct. |
| Ancestor note | The entry for `b124ceb2` (position 89, "Add cache map visualization") carries the finding `unconditional-tk-import`. Linked. Correct. |
| Discussion | Issue 7 is the extension's undefined-symbol import failure, with the reporter's own toolchain remedy in a later comment. Unrelated to tkinter, as the entry says. |
| Findings | None, and I found none. |

## Not verified

- Importing the package without tkinter, or opening the window.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: `unconditional-tk-import` (89) is fixed at `8d07bfb8`.

## Next

1. Record this approval.
2. Continue the walk at commit 119.
