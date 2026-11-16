# Verdict: commit-000158-reference-access-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/commit-000158-reference-access-001.md`
Upstream: `9665ba99989955593d2fb148323c9a96c77d1bea` "Add Mixtral architecture"
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**RESOLVED under the existing decision; no new question for the user.** Stopping was right. The gap can be
closed with evidence the standing rule already allows, so discovery can be completed and 158 authored unassisted.

`mistralai/Mistral-Large-Instruct-2407` is **not a match**: its configuration declares `MistralForCausalLM`, and
that is shown by a hash-verified mirror copy dated ten months before the cutoff.

## Why no new authorization is needed

`reviews/verdicts/commit-000098-reference-mirrors.decision.md`, point 7: "General rule from now on: when an official
repository is gated and no credential is configured, a hash-verified mirror may stand in, under points 2 to 4."
The table of ten Cohere repositories in that file is what was checked at 98, not the limit of the rule. This is
the same situation with a different publisher. Points 2 to 4 are met, as follows.

## What I checked (from `exdev-314`, no credential)

| Check | Result |
|---|---|
| Official public metadata | `https://huggingface.co/api/models/mistralai/Mistral-Large-Instruct-2407?blobs=true` answers without a login: created 2024-07-24T11:27:22Z, gated, last modified 2025-07-28. `config.architectures` is `["MistralForCausalLM"]`, `model_type` `mistral`. `config.json` is 598 bytes with Git blob id `38970e71536e08b5870344f15698dc17e40dc72e`. |
| Mirror 1 | ModelScope `AI-ModelScope/Mistral-Large-Instruct-2407`, created 2024-07-25. Its `config.json` was committed 2024-07-26T15:52:10Z (revision `c591542258…`), is 598 bytes, and hashes to Git blob id `38970e71536e08b5870344f15698dc17e40dc72e`. |
| Mirror 2 | ModelScope `mistralai/Mistral-Large-Instruct-2407`, created 2024-07-24. Its `config.json` was committed 2024-07-29T04:20:52Z (revision `db035f89aa…`), same 598 bytes, same blob id. |
| Identity (point 2) | Both mirror files equal the blob id Hugging Face publishes for the official file. |
| Availability (point 3) | Both mirror commits are in July 2024; the cutoff is 2025-05-14T15:53:33Z. |
| Content | `architectures: ["MistralForCausalLM"]`, `model_type: "mistral"`, 88 layers, hidden size 12,288. No expert fields. Not `MixtralForCausalLM`. |
| The request's own account | 83 repositories enumerated, four matches recovered, four root-config absences confirmed against pinned trees, one unresolved. I have not re-checked those here; I will at the 158 review, as for every architecture commit. |
| The wrong cutoff in the first run | Disclosed, excluded, rerun at the exact cutoff. Accepted; keep the discarded report as it is. |

One limit, stated plainly: the official history is gated, so this shows the file as it was on two mirrors in July
2024 and as it is officially now, and those are the same bytes. It does not show the official file at the instant
of the cutoff. That is the same limit point 3 of the decision already accepts.

## What to do

1. Record the repository in the discovery report as inspected through a hash-verified mirror, not as absent and
   not as uninspected: official name, official blob id, the ModelScope repository and revision used, its commit
   date, the declared architecture, and the outcome "not a match". Use mirror 1; note mirror 2 as agreeing.
2. If the accepted ModelScope tooling can express that with data only, proceed: mark discovery complete and
   author 158 unassisted on the four recovered bundles. If it needs a code change, file an implementation
   request first.
3. Name this mirror-resolved repository in the 158 request. That request gets a full review, including my own
   comparison of the four bundles' headers with the builder.
4. This repository contributes nothing to the teacher's packet: it is a non-match. Nothing about it should
   appear there beyond what a discovery report normally exposes.

## Note to the user (informational)

No gate was accepted and no token was used. I applied the mirror rule you set at commit 98 to a Mistral
repository. Say so if you want that rule kept to Cohere.

## Next

Complete discovery as above and continue with commit 158. The token-cost work in
`reviews/fable/TOKEN-COST-PROPOSAL.md` still comes after 158's request is filed.
