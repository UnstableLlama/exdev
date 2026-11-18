# Verdict: commit-000326-001 (teacher gpt-6.2-sol, guidance 12, unassisted; first run under validator v3)

Reviewer: Fable. Date: 2026-11-18 (05:41 UTC). Upstream `327d1f99` "Revert to flash_attn>=2.7.4.post1 until the wheel situation is sorted out".
Run: `.teacher/runs/commit-000326-001`. Packet: `.teacher/retrieval/000326-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 45 bad [], evidence 27 calls 27 bad [] uncited [], final==annotation
  True, anc 325 entries 325 True, blobs 4598 bad 0. Replay 27, mismatch 0. No repair.
- Diff read in full (`==` to `>=` for flash_attn in `requirements.txt` and `setup.py`).
- Central claims confirmed in source at the sha: both declarations changed and nothing else;
  `exllamav3/modules/attn.py:13` still imports FlashAttention at module load, so it stays required.
- The one finding is true at this commit: `setup.py` lists `exllamav3.generator` and
  `exllamav3.generator.sampler` (lines 73-74) but not `exllamav3.generator.filter`, while
  `exllamav3/generator/__init__.py:4` imports it eagerly. Correctly presented as carried over and conditional.
- The entry made the central check itself and kept the motive ("wheel situation") as unestablished.
- 325 ledger: `unconditional-anyprecision-import--r003` (partial fix `1f7f3e94` added) and
  `optional-class-sentinels--r002`; both suspected, training false, earlier observations byte-equal. Accepted.

## For the ledger

Check the filter-package finding against existing identities before opening a new one (see the list my grep
printed in the state file bullet); if an earlier entry already records it, extend that identity.

## Must fix before canonical

- Four Source Notes paragraphs cover unrelated issues (#2, #21, #7, #16, #49); cut to one sentence.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
