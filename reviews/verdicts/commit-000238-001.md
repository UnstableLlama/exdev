# Verdict: commit-000238-001

Reviewer: Fable. Date: 2026-11-16. Upstream `162f99ab` "compare_q.py: Add AnyPrecision models". First walk
commit authored at guidance 11.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`unconditional-anyprecision-import` (new requirement) is **accepted as true**, with the qualification under Run
checks. Both ledger revisions owed from 237 are **accepted**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 13 evidence
calls all cited, final equals annotation, 237 ancestors, 3263 blobs, nothing after the cutoff
(2025-06-05T00:26:00Z). Manifest guidance version 11; the system text equals 237's plus a blank line plus
paragraph F, nothing else.

## Run checks

- Replay: 13 of 13 identical.
- Diff read at parent and task. `compare_q.py` imports the new adapter at module scope and registers
  `anyprecision` in both tables. The adapter's storage accounting (packed weight plus the one table for the
  module's precision, logical element count as denominator, the 90%-of-vocabulary head test, unused scanner,
  unused `auto`/`bf16`, no device or dtype handling) is as the entry describes. Spec changes as described.
- The entry's arithmetic: 262144 + 8192 bytes over 1048576 weights is 2.0625 bits per weight. Correct.
- The finding: true. `compare_q_anyprecision.py` imports `any_precision` unguarded at the top, and
  `compare_q.py` imports that module unconditionally, so every comparison run and `compare_q_logits.py` now
  need the package. **Qualification:** this is the existing pattern, not a new kind of problem. At the same
  commit `compare_q_transformers.py` imports `gptqmodel`, `aqlm`, `awq`, `vptq` and `bitsandbytes` unguarded and
  `compare_q_exllamav2.py` imports `exllamav2`; only the llama.cpp adapter guards its imports. The teacher read
  the Transformers adapter and did not say so. A canonical entry should place the new requirement in that
  context. Classification "new requirement" is right.
- Paragraph F did not apply and was not forced: the commit names module attributes of an external library, no
  reference checkpoints or headers are in the evidence index, and the entry says no checkpoint tensors were
  inspected. No false header claim.

## Ledger (owed from 237)

- `exllamav3-llamacpp-embedding-order` r003, supersedes r002: fix `ab875ba7` recorded as source-supported.
- `exllamav3-llamacpp-cached-accounting` r003, supersedes r002: observation at `ab875ba7` added, no fix.
Both: flags false, status suspected. Accepted.

## Not verified

- Anything about the external AnyPrecision package (attribute names, device placement). The entry says the same.
- The "GiB under a GB label" remark; inherited from the root entry and not rechecked here.

## Follow-ups

- Ledger item for `unconditional-anyprecision-import` with the next request; say in it that the same pattern
  exists for the other backends named above.

## Next

Record the approval and proceed: replacement 72 per the accepted plan, and 239.
