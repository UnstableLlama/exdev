# Verdict: blob-store-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/blob-store-implementation-001.md`
Proposal: `reviews/fable/DISK-AND-CACHE-PROPOSAL.md` (request 1)
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**ACCEPTED.** The walk may continue at commit 128. Canonical and training remain false.

The change does what was asked and no more: one content-addressed store, packets hold read-only hard links into it,
every existing packet converted. I re-verified the result myself and did not rely on the report's numbers.

## Artifacts reviewed (sha256)

All nineteen hashes in the request match the files on disk.

## What I checked

| Check | Result |
|---|---|
| Every packet blob | Walked all 199 packet directories under `.teacher/`: 136,560 entries, 2,171 distinct inodes. I hashed each inode once: every entry's content hashes to its file name. No entry is writable, none is a symlink or other non-regular file, and every entry is the same inode as the store object of that name. |
| Store | 2,171 objects, 618,806,974 bytes, each hashing to its name, none writable, none unreferenced; the only other entry is `.lock`. |
| Manifests | For 144 of 145 runs that record a manifest hash and still have their packet, the packet's `manifest.json` hashes to the recorded value. The exception, `commit-000002-001`, predates this change: its manifest is dated 2026-11-10 12:17 and has not been touched since. |
| Recorded hashes | Every hash that any request file records for a path under `.teacher/` or `data/evidence/`: 676 lines, 675 match. The exception, `data/evidence/github/000069-closed.json` in an old implementation request, is dated 2026-11-13 and is outside this change. |
| Tracked run files | `git diff -- .teacher` is empty across the 741 tracked files. |
| Space | `du -s -B1`: `.teacher/retrieval` 993,390,592 bytes; all of `.teacher` 1,041,518,592. Free space 49.7 GB, up from 14 GB. Matches the report. |
| Replay | Six runs not in the author's sample (17/003, 39/005, 71/002, 110/001, 119/001, 123/001): 121 recorded tool calls replayed through `teacher.runner.Runner`, 121 identical. |
| Host writes | On a real shared blob (mode 444, 111 links): opening for append or update is refused. |
| Sandbox | With the packet bound read-only as `runner.py` does: write, chmod, unlink and create are all refused, and the store is not visible. |
| Tests | `python3 -m unittest discover -s tests`: 244 run, none failed, 12 skipped in my non-interactive shell. |
| Code | `put()` hashes the data, verifies an existing store object before reuse, writes a new object to a temporary inode, fsyncs, sets 0444 and renames; links by creating the link under a temporary name and renaming; an existing packet copy is verified before being replaced; a failed link raises and leaves the old copy. Under a store-wide lock. Six writers call it; no other code writes into a packet's `blobs/`. |

## Notes

1. **Copying.** The saving exists only while the hard links are preserved. Copying `.teacher/` to another disk or
   machine with a tool that does not preserve hard links turns it back into about 38 GB. Say so wherever moving the
   checkout is documented.
2. `teacher/root_tasks.py` still builds chapter packets with `shutil.copytree`, which makes full copies. It is not on
   the walk's path. Worth converting when that code is next touched; not required now.
3. Nothing removes store objects. That is right for now, since no packet is ever deleted.
4. The request says all 244 tests passed; here 12 were skipped. Tell me in the next request which twelve skip
   outside your shell and why.
5. The request says 127 was awaiting its verdict. It was approved before this review
   (`reviews/verdicts/commit-000127-001.md`, sha256 `41e9cbc032b12f73476081b2c8674f0497d4d0d0d48d7428c8992430faeb1cc7`).

## Not verified

- A live teacher session on a linked packet. Commit 128 will be the first; its review covers it.
- Behaviour when the store and a packet are on different filesystems, beyond reading the code path and its test.

## Next

1. Record this acceptance and lift the pause.
2. Continue the walk at commit 128.
3. File the discussion-history cache (proposal request 2) as its own implementation request when ready. It does not
   block the walk.
