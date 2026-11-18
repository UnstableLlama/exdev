# Verdict: commit-000258-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-17 (05:55 UTC). Upstream `afa7f1e5` "Remove default imports for HF integration".
Run: `.teacher/runs/commit-000258-001`. Packet: `.teacher/retrieval/000258-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`integration-example-stale-import` is accepted as true as stated. The entry made the commit's central
check itself: it looked for remaining users of the removed export.

The pre-run recovery was carried out as authorised: `retry_only` is gone, the earlier failed item is kept,
257 approved entries are selected, and this run saw 257 of 257 ancestors.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 13 evidence calls all cited and none bad, final equals annotation, 3447 blobs,
nothing after the cutoff. Orchestration hashes equal the accepted files; complete packet; ran ahead of none.

## Run checks (mine, tree at `afa7f1e5`)

- The only in-tree references to `patch_transformers` are its definition, and the example's
  `from exllamav3.integration import patch_transformers` and call. The initializer is now empty, so that
  import fails. As stated.
- `setup.py` still does not list `exllamav3.integration`; the adapter is unchanged. As stated.

## Ledger

- New identity `integration-example-stale-import`, introduced here: file with the next request.
- This commit fixes `eager-undeclared-transformers` (introduced at 255): file a revision recording the fix
  at `afa7f1e5`. `integration-not-packaged` stays open; note there that after this commit it is reached
  only by an explicit import of the integration package.
- `exllamav3-invalid-70b-qtip-spec` r001: accepted.

## Reviewer knowledge (never to a teacher)

Upstream `72bdf5a3` "Fix example" (2025-06-12, same day) is the next commit to touch the example.
