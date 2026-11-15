# Verdict: commit-000103-reference-access-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/commit-000103-reference-access-001.md`
Upstream at walk position 103: `0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8` "Add Cohere2 architecture"
Reviewed: 2026-11-14, machine `exdev-314`

## Decision

**RESOLVED by the reviewer; no user decision needed.** Use the pre-cutoff ModelScope `config.json` for
`c4ai-command-r7b-12-2024` under a distinct, labelled status, with the conditions below. This is my ruling under the
user's mirror decision (`commit-000098-reference-mirrors.decision.md`); it refines points 2 and 7 of my own interpretation
there, not the user's words. The user is told and can overrule it.

Stopping was right, and so was refusing to label the model `no_eligible_revision` or to drop it.

## What I checked myself (no credential, from `exdev-314`)

- The official repository's current public file list: `config.json` blob `8bf71a2f…`, four safetensors files.
- `CohereForAI/c4ai-command-r7b-12-2024` on ModelScope, created 2024-12-14, and `AI-ModelScope/c4ai-command-r7b-12-2024`,
  created 2024-12-15. Two separate repositories.
- At their pre-cutoff revisions (`8e2f5049…`, config committed 2024-12-14; `714bfef4…`, config committed 2024-12-15) the
  two `config.json` files are byte-identical to each other, blob `43fd683c…`.
- At those same revisions every other reference file matches the official current hashes: all four safetensors files,
  `tokenizer_config.json`, `generation_config.json`, `special_tokens_map.json`, `tokenizer.json`.
- Both mirrors' current `config.json` (committed 2025-05-13, after the cutoff) matches the official current blob.
- The difference between the pre-cutoff and current config is one line, one field. **Reviewer-only: the field is
  `max_position_embeddings`; its later value must not reach any teacher.**

So the file the rule cannot verify is the historically correct one, and the file the rule can verify is hindsight.
The official config was edited sixteen days after the cutoff. Two independent mirrors captured the same earlier bytes
within a day of each other, alongside files that are all provably the official ones.

## Conditions

1. New status for a single file, for example `mirror_historical_unverified_identity`. It applies only when all of these
   hold, and the tool must check them, not a curator:
   - the official current hash for that path does not match, and the mirror's matching copy is dated after the cutoff;
   - at least two distinct mirror repositories hold a byte-identical copy at revisions whose file commit dates are at or
     before the cutoff;
   - at one of those revisions, every other reference file of the model passes the ordinary identity check against the
     official current hashes.
2. Only non-weight files may use it. A safetensors file never may.
3. The item's proof records both mirror repositories, both revisions and dates, the shared blob id, the official
   current blob id it does not match, and the date of the mirror's later matching copy.
4. The teacher-visible index row and object metadata say plainly: this file is the pre-cutoff mirror copy; its identity
   with the official file at that date could not be checked because the official history is gated. Nothing about what
   the file later became, and no post-cutoff date, appears in anything a teacher can read. The later date and the
   non-matching official blob id stay in the administrative report.
5. The model's selection report carries the status too, so a reviewer sees it without opening items.
6. This is an implementation change. File an implementation request with the rebuilt commit 103 bundle (all three
   models) before authoring. Name the affected file in that request and in commit 103's review request.
7. General rule from now on, replacing the last sentence of point 7 in the mirror decision: an unverifiable mirror file
   may stand in only under condition 1. Anything else unverifiable stays out.

## Other points in the request

- Command A (54 objects) and Command R7B Arabic (9 objects) recovered under the accepted rule: fine. I will recheck them
  with the bundle.
- The unsloth endpoints returning 401 are gated copies; not usable. Agreed.
- Trigger: `Cohere2ForCausalLM` derived from the new config class with no registry key detected is what I expected after
  commit 102.

## Next

1. Implement conditions 1 to 5, rebuild the commit 103 reference bundle, file the implementation request, wait.
2. Do not author commit 103 before that request is accepted.
