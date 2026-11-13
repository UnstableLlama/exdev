# Verdict: config-reading-amendment-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/config-reading-amendment-implementation-001.md`
Decision implemented: `reviews/verdicts/config-reading-amendment.decision.md` (sha256 `a8ed9a5a101d2578d1ee1168d0528a7b72a52addf028094702a99b1a9d513a34`)
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**ACCEPTED for new packets** (walk input contract v7, guidance version 4).

This approves no prose; canonical and training remain false. Proceed with `commit-000039-004`, unassisted, then stop for full review.

## Artifacts (sha256)

- implementation report: `0d08c42f36221fe7d5ac5255caf5f094337de8937a89c3a4b0b618554ffc6645`
- test log: `a429adeb3b8a2d1abea9fc8623827b272997a2d05e675a329d3da6af0a32dfd0`
- preview report: `5ccb81dcb84f2293a0f464fb653fc8fa0b57c5ec78ad30de6855a453d7d9e7d4`

All match the request. All 7 files the report binds match the working tree.

## Checks

| Check | Result |
|---|---|
| Index field | Met. For contract v7, each model row gains `architectures`, read from that model's pinned `config.json` in the packet; an absent key gives an empty list; a non-list value or two configurations that disagree fail closed. The field is inside the hashed index, and validation recomputes it from the blob. |
| Guidance sentence | Met. For guidance version 4 the old sentence is replaced by the amendment's wording, with its two clarifications appended ("adds or changes" defined; configuration files only). There is no opt-out. Guidance version 3 packets keep the old sentence. |
| Dry run, position 39 | Built in my scratch directory. Contract 7, guidance 4. The index names all nine models with their architecture: four `DeciLMForCausalLM` (attached by this commit) and one each for Qwen2, Llama, Phi3, Mistral and Gemma2 (attached at the root). Opening page 6,117 bytes, not truncated. A teacher can now tell which four the rule covers without opening anything. |
| Dry run, position 44 | Same nine models offered, the four DeciLM ones marked as attached by commit 39. Opening page 6,485 bytes. |
| Older packets | Commit 39 attempt 003 (contract v6) still reproduces its opening context byte for byte and passes assessment; so do 39/002 and 61/001. Across all runs with packets, 30 reproduce and the same 37 oldest do not, as before. |
| Tests | Full suite: 209 passed with pinned Codex 0.167.0 first on PATH. `git diff --check` clean. |
| Rejection recorded | The request states 39/003 is recorded rejected and 39/002 stays approved. |

## Not verified here

- No teacher run under guidance version 4 yet; 39/004 is the first.

## Still open

- Required fixes 1 and 2 from the reference-evidence implementation verdict, due before position 100.
- The guidance version check in `validate_contract` is still an exact match per contract version; harmless, but each new guidance version needs a new branch there.

## Next

Author `commit-000039-004` with no coverage request and stop for full review.
