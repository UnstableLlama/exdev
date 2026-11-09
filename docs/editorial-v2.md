# Editorial v2 candidate

The [annotation schema](../schema/editorial-annotation-v2.json) keeps problem, reasoning, impact and source notes as lists of claims. Each claim contains text, an evidence basis (`source`, `execution` or `inference`) and recorded tool-call IDs or approved `ancestor:<sha>` context IDs. Concrete uncertainty belongs in `limitations`; pipeline status and reviewer bookkeeping belong in the separate review record.

The validator rejects missing or fabricated call IDs, failed evidence calls and execution claims without a successful `run` result. This establishes provenance, not the truth of the prose: reviewers must still check that the cited output supports the claim and that a successful program actually measured what the prose says. Source reports of benchmarks should be labeled source, not execution. Inferences retain their evidence anchors and are explicitly labeled.

Identity, cutoff, model and implementation provenance come from trusted preparation. The model cannot provide SHA, approval, merge-policy or training-eligibility fields. Every output starts as a draft with a separate `review.json` containing pending status and `training_eligible: false`. Merge promotion and independent-example decisions remain administrative review responsibilities; the new draft writer cannot promote any entry or training example.

A canonical root commit may contain subsystem chapters with unique IDs, titles and evidence-bearing claims. The renderer links those chapters within the one root entry. It preserves upstream credit and links to the source commit and JSON evidence ledger. This is Markdown preparation for the later human-facing wiki, not a new website.

Links to earlier prose require both Git ancestry and inclusion in the packet's approved `ancestor_entries`. Current packets contain no old drafts. [Approved replacement prose export](ancestor-context.md) is implemented, with exact artifact checksums and an inline context budget. The first 25 existing entries are unchanged; there is no automatic migration that could mistake an old draft for freshly authored work.

## Generation and preservation

The selected teacher is **Codex `gpt-6-astra`, medium reasoning**. Each task gets a new provider process and ephemeral thread with no inherited authoring context. The model-tool profile is pinned alongside the adapter; the provider's default profile exposes tools beyond this project's contract, so feature flags alone are insufficient.

The draft command preserves raw assistant output and tool results before schema validation. Successful validation writes `draft.json`, `draft.md` and a separate pending `review.json`; failures retain raw output and a failed status. `provenance.json` records packet and implementation hashes. The command never overwrites an existing run or publishes into `encyclopedia/`.

Tests use explicitly labeled fixtures. The real installed Codex binary is tested against a loopback fake Responses endpoint with a dummy key, including its WebSocket prewarm, generation and tool-result continuation. The test checks Astra/medium, the exact 14-tool inventory, absence of prior repository context and built-in skill/delegation instructions, and one real sandboxed historical tool call. These fixture responses are not authored corpus or training traces. The initial live draft is a separate review candidate; these fixture checks do not establish editorial quality.

Protocol references: [official Codex app-server documentation](https://learn.chatgpt.com/docs/app-server) and [official configuration schema](https://learn.chatgpt.com/docs/config-schema.json). The adapter is pinned to the locally generated 0.167.0 protocol; upgrades require rerunning the wire and boundary checks.

The provider-facing output schema also restricts `links` to supplied ancestor SHAs (an empty array at the root). Local chapter anchors are a separate field. This restriction was added after the first live root attempt confused chapter IDs with ancestor links; that response was rejected and preserved rather than repaired by the administrative session.
