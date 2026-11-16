# Verdict: header-budget-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/header-budget-implementation-001.md`
Patch: `reports/header-budget-implementation-001.patch`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED.** The header budget for official Hugging Face safetensors headers may be 16 MiB, in recovery and in the
runtime tool. Authoring of commit 141 may proceed, unassisted, on the complete bundle. Canonical and training
remain false.

The need is real and I confirmed it at the source: five official files have headers above 4 MiB. The change is
seven lines, raises one number in two places, adds a check on the normalised size, and leaves every other bound
alone. Failing closed on the first attempt and asking, rather than dropping the two repositories or marking them
absent, was the right call.

All three ledger candidates are **accepted**.

## Artifacts reviewed (sha256)

All twenty-eight hashes in the request match the files on disk. `git diff -- teacher` hashes to the patch's hash.

## Checks

| Check | Result |
|---|---|
| The patch | `MAX_HEADER_BYTES = 16*1024**2` in `root_evidence.py` and `worker.py`; the length test in `recover_hf` and the size test in the `safetensors_header` tool use it; `recover_hf` now also rejects a normalised header above the bound; one README paragraph. Nothing else in `teacher/` changes. |
| Other 4 MiB bounds | Still present and untouched: the provider request and buffer limits in `codex_transport.py` (lines 86, 101) and both ModelScope header tests in `mirror_evidence.py` (lines 110, 183). As stated. |
| Recovery shape | Still two ranged requests per file, bytes 0 to 7 and then exactly 8 to 7 + length; a length below 2 or above the bound fails before the second request. The new test asserts the exact ranges. |
| Runtime shape | The tool still parses the cached header, validates each entry and returns one page; the bound is checked before parsing. |
| Tests | I ran the full suite: 247 tests, all pass, with `EXDEV_SANDBOX_TESTS=1` and the pinned Codex on the path. (Without Codex on the path two wire tests error at process spawn; that is my shell, not the patch.) The three new tests cover the upper bound and both rejections, normalised expansion, paging of a header above 9 MB through the sandboxed runner, and refusal above the bound. |
| Header lengths, from Hugging Face | I read the eight-byte prefixes myself at the pinned revisions. `Qwen3-30B-A3B-GPTQ-Int4/model.safetensors`: 9,080,000. `Qwen3-235B-A22B-GPTQ-Int4` shards 1 to 5: 4,223,256; 4,427,128; 4,426,888; 4,426,888; 480,000. Equal to the request. |
| Publisher listing | Hugging Face lists 469 Qwen repositories today. Equal to the request. |
| The seven | Today 27 Qwen repositories declare `Qwen3MoeForCausalLM`. Twenty are later products (the 2507 releases, the MLX conversions, the Coder models). The seven selected are the ones that existed with that class before the cutoff. |
| Pins | For each of the seven I listed the full commit history and took the latest commit at or before 2025-05-11T13:35:38Z. All seven equal the pinned revision. The two GPTQ repositories were last changed about seventy minutes before the cutoff (12:24:37Z and 12:29:01Z) and next changed after it (16:27:20Z; 12 May). |
| Bundle | 239 items: 211 headers and 28 non-weight files, four per repository. Largest stored item 10,635,788 bytes, below the bound. Not yet bound to a packet; no teacher run exists for 141. |
| Boundary and live audits | Reports say 42 of 42 and 12 of 12; I read the reports, I did not rerun them. |
| Ledger `deferred-bf16-odd-tail--r001` | Accepted. One identity, introduced `647bb7d5`, observed at 119 and 140. |
| Ledger `single-load-missing-deferred-abort--r001` | Accepted. Reviewer observation introduced at `c6aa83f7`; no induced failure claimed. |
| Ledger `variant-collection-loader-api--r002` | Accepted. Adds 140 and the explicit-device reach. |

## Why 16 MiB is acceptable

The largest header seen is 9.08 MB raw and 10.6 MB normalised. 16 MiB covers it with margin and is still a small,
fixed bound on a metadata-only fetch. The teacher's view does not widen: it still receives one bounded page per
call. The bound does not affect what is fetched beyond the header range, and no weight bytes are read.

## Conditions

1. If a later architecture needs more than 16 MiB, stop and ask again; do not raise it in passing.
2. The ModelScope bound stays at 4 MiB until a case needs it and is reviewed.

## For the 141 review (reviewer-only; never to a teacher)

I will compare the constructor's declared tensors with these headers myself, as at 98, 103 and 110. The GPTQ and
FP8 repositories are unlikely to be loadable as they stand; I will look rather than assume.

## Next

1. Record this acceptance and the three ledger acceptances.
2. Author 141 unassisted and file its request.
