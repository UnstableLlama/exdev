# Verdict: commit-000296-001 (teacher Sol, guidance 12, unassisted; ran ahead of 295)

Reviewer: Fable. Date: 2026-11-17 (15:05 UTC). Upstream `86753399` "Loader: Tweak default reserve_per_device".
Run: `.teacher/runs/commit-000296-001`. Packet: `.teacher/retrieval/000296-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`stale-reserve-docstring` is accepted as true as stated (a documentation discrepancy, as the entry says).
The entry states both changed defaults, who takes them and who does not, and what the reserve does in the
memory helper.

It stands without a rerun: 295 changes an activation kernel and has no bearing on loader reserves.

**Record this approval only after 295 is approved**, so approvals stay in ascending order.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 294 of 295 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 13 evidence
calls all cited and none bad, final equals annotation, 4287 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 294 of 295, as disclosed. Repair enabled, unused.

## Run checks (mine, tree at `86753399`)

The two defaults are 0.5 and are converted with `1024**3`; the docstring in the same file still says
0.25. As stated.

## Ledger

File `stale-reserve-docstring` as a new identity with the next request after this is recorded.
