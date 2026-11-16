# Verdict: commit-000089-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000089-001`
Packet: `.teacher/retrieval/000089-001`
Upstream: `b124ceb2d598902e5a084fc06c1b378be1dfb6a3` "Add cache map visualization"
Request: `reviews/requests/commit-000089-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and the finding is the important thing about this commit: an optional debug window
makes `tkinter` a hard import for the whole package.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 88 strict-ancestor entries; 1,222 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 13 of 13 recorded tool calls identical, including the `run` call. |
| Diff read in full | The upstream diff is 14,242 bytes; the three `git_show` calls cover offsets 161 to 14,410. |
| Unassisted | Standing instructions byte-identical to 88/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15 (pull request 20 closed since 88). Matches the six open rows. |
| Generator claims | `show_visualizer: bool = False`; a `CacheVisualizer(self.pagetable.max_pages)` only when set; `update_visualizer` builds `(job.serial_number, [page.page_index …])` per sequence of each active job and `page.kv_position / PAGE_SIZE` per page; it is called in `iterate` after both the draft-model and the plain generation branches. Correct. |
| Visualiser claims | `import tkinter as tk` at module scope. Fourteen entries in `job_colors`, indexed `index % len(job_colors)`. Defaults 800 x 600, gap 0.75, margin 25. Grid width `ceil(sqrt(pages * ratio))` capped at the page count, height `ceil(pages / width)`. Overlays deleted and rebuilt each update, followed by `root.update()`. The module docstring calls it "horribly slow" and suggests a bitmap. Correct. |
| Demo claims | New `show_visualization = False` passed as `show_visualizer`; `total_context` 32768 to 16384; model path changed; prompts replaced with long repeated sequences. Correct. |
| Finding | `unconditional-tk-import`: correct. `generator.py` imports `.visualizer` at module scope; `exllamav3/generator/__init__.py` imports `Generator`; `exllamav3/__init__.py` imports from `.generator`. So `import exllamav3` now needs `tkinter` whether or not the window is used. Suspected is right, since nobody ran it without `tkinter`. |

## Not verified

- The window itself. Nobody opened it; the entry says so.
- The teacher's read of `generator.py` at the parent was cut at 13,500 bytes. Every claim about that file is supported
  by the diff, which was read in full.

## Must fix before canonical use

Reviewer-only.

1. `new_requirement` understates the finding for the common case: a headless Linux Python without the `tkinter`
   package cannot import the library at all after this commit. A canonical entry should say that in plain words.

## Next

1. Record this approval.
2. Continue the walk at commit 90.
