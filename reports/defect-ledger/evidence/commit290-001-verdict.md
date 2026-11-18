# Verdict: commit-000290-001 (teacher Sol, guidance 12, unassisted; ran ahead of 289)

Reviewer: Fable. Date: 2026-11-17 (12:37 UTC). Upstream `6735462a` "BlockSparseMLP: Refactoring".
Run: `.teacher/runs/commit-000290-001`. Packet: `.teacher/retrieval/000290-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All five findings are accepted
as true as stated: `missing-ernie-registry-modules` and `custom-bias-export-name` are new;
`sigmoid-router-required-inputs` extends the existing optional-inputs identity to the now selectable DS3
route; the all-expert count and the fused output contract are observations of existing identities. The
entry made the central checks itself: it did not take "Refactoring" at its word, checked that the two newly
imported modules exist (they do not), and noticed that the default route moved from the native function to
the Python one.

It stands without a rerun: 289 changes one argument in `llama.py`, which this entry does not rest on.

**Record this approval only after 289 is approved**, so approvals stay in ascending order.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 288 of 289 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 47 evidence
calls all cited and none bad, final equals annotation, 3829 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 288 of 289, as disclosed. Repair enabled, unused.

## Run checks (mine, tree at `6735462a`)

- No file with "ernie" in its name exists anywhere in the tree at this commit, and `architectures.py` now
  imports `.ernie4_5` and `.ernie4_5_moe` at module level. `Config.from_directory` imports that registry
  for every model. As stated.
- `routing_fn` is chosen in the constructor from `std`, `ds3`, `dots`; no Python caller of
  `blocksparse_mlp_routing` remains; Dots1 passes `router_type = "dots"`. As stated.
- `load` uses the configurable bias key; `get_tensors` still writes `gate.e_score_correction_bias`. As
  stated.
- The Dots configuration and header values quoted are those I verified at 271.

## Reviewer knowledge (never to a teacher)

Upstream adds the two modules in `47d83f56` "Add Ernie 4.5 model (text only)" (2025-07-07), two commits
later. That will be an architecture commit needing reference recovery.

## Ledger

File with the next request after this is recorded: two new identities, a revision widening
`optional-inputs-required-by-dots`, a fix revision for `grouped-routing-unassigned` at `6735462a` (the
entry states the unassigned branch is gone), and the two observations.
