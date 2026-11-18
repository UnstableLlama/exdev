# Verdict: commit-000239-001

Reviewer: Fable. Date: 2026-11-16. Upstream `db65151b` "compare_q.py: Allow script to run without all backends
installed". Guidance 11.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`optional-class-sentinels` is **accepted as true**. The ledger revision `exllamav3-partial-frequency-read` r002
is **accepted**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 17 evidence
calls all cited, final equals annotation, 238 ancestors, 3279 blobs, nothing after the cutoff
(2025-06-05T00:26:00Z). Instructions identical to 238's run.

## Run checks

- Replay: 17 of 17 identical.
- Diff read at parent and task. Imports in four adapters are wrapped in `try`/`except ModuleNotFoundError`.
  AnyPrecision, ExLlamaV2 and ExLlamaV3 use `pass`; the Transformers adapter sets each missing class name to
  `None`. As the entry says, including that torch, Transformers and `compare_q.py`'s own ExLlamaV3 utility
  import stay unconditional.
- The finding: `get_storage_info` at the task, line 77, opens with
  `any(isinstance(module, x) for x in [Linear4bit])`, and six later branches use the other optional names the
  same way. With `Linear4bit = None` that first test raises `TypeError` on the first module of any model. I
  ran the expression: "isinstance() arg 2 must be a type, a tuple of types, or a union". So a machine without
  bitsandbytes now starts the script and then fails in storage accounting for every Transformers-loaded
  model, which is the case this commit set out to allow. Only bitsandbytes matters in practice for the first
  branch; the others bite when their branch is reached. The entry states this accurately, limits included.
- The entry correctly links back to 238: this commit removes that entry's import-time requirement, and
  selecting an absent backend still fails later at its loader.

## Ledger

- `exllamav3-partial-frequency-read` r002, supersedes r001: observation for run 72/003 added, earlier
  observations and the introduction kept, no fix, flags false. Accepted.

## Reviewer knowledge (hindsight; must not reach a teacher)

Upstream keeps the unfiltered `[Linear4bit]` test until the file is removed (`74b5534f`, 2026-07-23); the
`Linear4bit = None` fallback is gone from `e90fe55e` (2026-04-10) onward. I have not read how; check when the
walk reaches it before recording a fix.

## Not verified

No adapter was imported and no model loaded, by the teacher or by me.

## Follow-ups (ledger, with the next request)

- `exllamav3-unconditional-anyprecision-import`: new revision recording `db65151b` (239) as the fix for the
  import-time requirement.
- New record for `optional-class-sentinels`, introduced at 239.

## Next

Record the approval and proceed: replacement 98, then 240.
