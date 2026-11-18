# Verdict: commit-000336-004

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (16:24 UTC). Run: `.teacher/runs/commit-000336-004`. Packet: `.teacher/retrieval/000336-002`.
Upstream `37f80fb98cf6247f9da12d9b942253f38f6dbd82` "Fix typo".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 19 calls, 0 bad, 0 uncited; final equals annotation; 332 ancestors
  and 332 entries; 4,655 blobs, 0 bad; no verdict or ledger text in the packet. All 19 calls replay with 0 mismatches
  against packet 000336-002. System prompt equals 336/003. No repair turn. The provider accepted the reduced schema.
- Central claim, by my own execution of `detach_from_model` taken from Git at both revisions, with stand-in objects. A
  one-layer cache and a two-layer target give `TypeError: 'int' object is not callable` at the parent, and
  `AssertionError: Cannot detach cache with 1 layers from model with 2 layers.` at the commit. Registrations are untouched
  on mismatch, and a matching target is detached in both. The teacher's own run agrees, including that `-O` skips the check.
- Source at the parent: `attach_to_model` already formats the plain integer; the constructor sets `num_layers` from
  `get_cache_layers()` and builds one layer per entry; the only in-tree caller is `examples/loading.py:36`, on the model the
  cache was built with. `4fa0e686` introduced the call while replacing `num_hidden_layers`, as the entry says.
- Issues #1, #7, #50 and #52: titles and the stated overlaps match the fetched text, all open at the cutoff, and the entry
  correctly declines to link any of them to this fix. Ancestor statements match the entries it read.
- Ledger `cache-detach-count-diagnostic` r004: confirmed, no fixes yet, earlier observations byte-equal, introduction at
  `4fa0e686`, not training-eligible.

## Requested next

Record this source-verified fix at `37f80fb9` in the next revision of `cache-detach-count-diagnostic`, for my review with the
next commit.

## Must fix before canonical

The two Source Notes paragraphs on issues #1, #50, #7 and #52 explain why unrelated reports are unrelated. Editorial only.

## Reviewer tool note

`reviews/fable/review.sh` and `check.py` assume the packet attempt equals the run attempt, so they fail on 336/004, which
reuses packet 002. I ran both checks with the packet path corrected. Neither script was changed.
