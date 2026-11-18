# Verdict: commit-000336-recovery-002

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (08:02 UTC). Stopped run: `.teacher/runs/commit-000336-001` (failed before any tool call; recovery
authorised by `reviews/verdicts/commit-000336-recovery-001.md`). New run: `.teacher/runs/commit-000336-002`.

## Decision

**The mechanics are authorised for this rerun.** No approval of any entry is given here.

## What I checked (my own comparison of the two packets)

- Request hashes: 7 checked, 0 bad. The stop is as described: `existing_preparation`, no 336/002 run directory.
- `.teacher/retrieval/000336-002` against `000336-001`: the manifests differ only in `ancestor_entries`,
  `ancestor_catalog_blob`, `ancestor_search_blob` and `ancestor_search_graph_commits`, and 002 drops
  `approved_ancestor_selection`. Cutoff and guidance are equal.
- Ancestor entries: 331 become 332. The only addition is direct parent `3be1ea10` (335); none is removed or changed. The
  332 entries are exactly the strict ancestors of `37f80fb9` in Git.
- Packet files: 4,654 become 4,656. Two blobs leave, the old ancestor catalog and search index. Four arrive: their
  replacements, plus the 335 prose and its quantizer chapter. The 335 prose blob matches its hash. Every other file is
  present with the same size.
- `orchestration/run_ahead.py` requires this decision file to name the stopped run, and requires `packet` and
  `original_packet` manifests to be byte-identical on the prepared forward route, so using 002 for both is the way to
  run this packet.

## Mechanics

Once no cycle process remains: `recover --retry-position 336` bound to this verdict, then the prepared forward route for
`.teacher/runs/commit-000336-002` with `packet` and `original_packet` both `.teacher/retrieval/000336-002`, binding the
comparison audit `reports/commit-000336-002-packet-verification.json` and this verdict. One fresh unassisted attempt,
contract 8, guidance 12, gpt-6.2-sol medium. Nothing from 336/001, either recovery request or either verdict reaches the
teacher. Keep the 336/001 artifacts as they are.

If this attempt stops with the same Codex error, stop and file both failures; no third attempt without the user.
