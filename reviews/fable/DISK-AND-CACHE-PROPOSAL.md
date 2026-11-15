# Proposal from the reviewer: packet storage and discussion recovery

From Fable, 2026-11-14, with the user's knowledge. This is a request for two implementation changes, each to come back
as an implementation request for review in the usual way. Nothing here changes what a teacher sees. Disk is the urgent
one.

## 1. Packets are full copies and the disk is nearly full (urgent)

Measured on `exdev-314` after commit 126:

- `.teacher/retrieval` holds 147 packets, about 31 GB. A packet was 36 MB at commit 10, 301 MB at 80, 526 MB at 122,
  and grows with every commit.
- The same blob in two packets has different inodes and different physical extents (checked with `ls -li` and
  `filefrag` on 121 and 122). Nothing is shared.
- Free space is 14 GB in the machine and about the same on the Mac that hosts it. That is roughly 25 more commits.

Request:

- Keep one content-addressed blob store and make each packet's `blobs/` entries links into it (hard links, or
  reflinks; the filesystem is btrfs). Blob names are already their sha256, so the packet's file names, contents,
  manifest and every recorded hash stay byte-identical.
- Convert the existing packets the same way, verifying each blob's hash before replacing a copy with a link.
- Shared storage means one stray write would damage every packet at once. Make the store and the links read-only,
  and confirm the teacher sandbox cannot write through its view of the packet.
- Evidence I will look for: before/after `du`, a full re-hash of every packet's blobs against their names, the
  manifest hashes of all approved runs unchanged, replay of a sample of old runs still identical, and the test suite.
- Until this lands: if free space falls below 5 GB, stop before starting the next commit and say so in the request.

## 2. Discussion recovery refetches everything on every commit

Timed from the session log for commit 122 (378 s from verdict to verdict): recovery plus graph indexing took about
145 s, the teacher session 68 s, my review 75 s, the rest under 45 s each.

- The preparation step calls `recover()` for every discussion that exists at the cutoff, every commit: about 31
  discussions and 132 s now. The repository has 576 discussions by the pinned tip, so at the same per-discussion cost
  this step grows to roughly 40 minutes per commit.
- The fetched history is the discussion's full history; the as-of-cutoff snapshot is derived from it locally. So a
  history fetched once can serve every later cutoff.

Request:

- Fetch each discussion's history once and reuse the stored file; fetch only discussions not yet stored. Keep
  `retrieved_at` honest (the time of the real fetch).
- Evidence I will look for: for positions 113 to 126, catalogs regenerated from the cache equal the recorded
  unreferenced, closed and eligible files apart from retrieval timestamps; the cutoff filter still excludes every
  event after the cutoff (126 and issue 33 is a good case: comments at 03:24:04Z in, 17:31:50Z out); the test suite.

## 3. Optional, smaller

The preparation, walk and validation steps are started as separate commands with 15 to 30 s sleeps between checks.
Running them as one command would save about half a minute per commit. Only if it is simple; not required.

## Not proposed

No change to the teacher session, its inputs, the review gate or the order of work. The next commit's teacher still
starts only after the current commit is approved.
