# Verdict: commit-000214-reference-access-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/commit-000214-reference-access-001.md` (sha256 `8f6fb0b14a50033a73e918758c763a2973ce0487d44e16dfc14ae814096104b2`)
Upstream at walk position 214: `42afcd7e6cd361b2be9aef1072f26ffccffb92db` "Support Gemma3ForCausalLM"
Reviewed: 2026-11-16, machine `exdev-314`

## Decision

**RESOLVED by the reviewer under an existing rule; no user decision needed.** Record `google/medgemma-4b-it` in
the discovery report as "not inspected at the pin; current public metadata declares
Gemma3ForConditionalGeneration", exactly as point 5 of `commit-000098-reference-mirrors.decision.md` prescribes.
It is not a proved non-match, not absent, and not inspected. No file from it is attached. Discovery is then
complete for the purpose of authoring 214. The user is told and can overrule this.

Stopping was right, and so was declining to assert the two-witness historical exception with one witness.

## Why point 5 applies and no new exception is needed

- Point 5 covers a gated repository created before the cutoff whose public metadata shows a different
  architecture string. All three hold here. The request asks only how to classify the repository; it does not
  ask to use any of its files as evidence, which is what the 103 exception (two witnesses) governs.
- The classification makes no claim about the pin, so it needs no proof about the pin. The one pre-cutoff
  mirror config may be recorded beside it as an administrative note. It agrees with the current metadata, which
  makes the residual risk small, but it is not what the classification rests on.

## What I checked myself (no credential, from `exdev-314`)

- Hugging Face public metadata for `google/medgemma-4b-it`: gated; created 2025-05-19T20:52:44Z, before the
  cutoff (2025-06-01T15:13:26Z); declares `Gemma3ForConditionalGeneration`; `config.json` blob `cf0df746…`, the
  value in the request.
- Every hash listed in the request matches the file on disk.

## Conditions

1. The discovery report row carries the exact status text above, the public creation date, and, as an
   administrative note only, the single pre-cutoff mirror witness (revision `f987c345…`, 2025-05-21, blob
   `ac44fe0d…`, same architecture string). The post-cutoff mirror date and the differing fields stay in the
   administrative report and reach no teacher.
2. 214's review request names this repository and its status, and 214 gets a full review. I will check the
   five-model bundle (45 objects, 15 tensor headers), the reuse of the 164 proofs and the two `gemma-3n`
   absences there.
3. No implementation change is needed for this. If the tool cannot express the status without one, file an
   implementation request first.

## Residual risk (stated for the user)

If the repository had declared `Gemma3ForCausalLM` at the pin, one reference model would be missing from 214's
evidence. Everything recovered says otherwise: the current official metadata and the only pre-cutoff copy both
declare the multimodal class.

## Next

1. Update the discovery report as in condition 1, then prepare and author 214 in the usual way.
