# Verdict: reference-discovery-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/reference-discovery-implementation-001.md`
Reviewed: 2026-11-13, working tree on top of `41010aa`

## Decision

**ACCEPTED.** `teacher/reference_discovery.py` does what the 72/001 verdict required: it enumerates every visible
repository of one organisation, pages each history, pins the latest revision at or before the cutoff and tests that
revision's `config.json` for the exact architecture string. No name filter. The GLM4 run finds the six models, and its
three Z1 pins equal the ones I recovered independently.

No change to contract, guidance, tools or teacher instructions, so nothing here needs a user decision to take effect.

## Artifacts reviewed (sha256)

- teacher/reference_discovery.py: `a678bd7d3fa12201139c976e247d23a408c825583b06d6e6845c65fa9f30fa8c`
- tests/test_reference_discovery.py: `481d7263b7377dfed0528f0bbdc0d75af54888c7b09d61d91574e720d692a51c`
- teacher/README.md: `904719a6994d96b4a19da54f3b087870bfb92c03824781eef7e951bc6f175471`
- reports/reference-discovery-implementation-001.json: `4cfea900ffb5a03e39e1363becb21415e54615d62a2b5eab40b9355ca9868018`
- reports/commit-000039-reference-discovery-audit-003.json: `9f3001a00cfd50c2c66b46a1b55ed9aff505b19b9a606e31746b309450f0287b`
- reports/commit-000072-reference-discovery-002.json: `307d46654960e874798064f61e28bd8714d3b618bd8747953fee958c9c663c4a`
- reports/commit-000072-reference-selection-002.json: `8cbf2aa69960fa871ec165077a04b83d3283b451cd14c1409048041e534bf986`

All match the request.

## Checks

| Check | Result |
|---|---|
| Code read | 56 lines. Enumeration by `author`, pagination through the `Link` header with a host check, `choose_revision` takes the latest commit at or before the cutoff, exact string membership in `architectures`. Refuses to overwrite an existing report. |
| Tests | I ran the suite with the pinned Codex first on PATH: 223 passed. The two new tests cover a matching repository with an unrelated name on a later page, exclusion of a repository with only later revisions, and an unreadable config being reported and not dropped. |
| GLM4 report | 154 repositories: 85 inspected, 44 with no revision before the cutoff, 25 with no root `config.json` at the pin (all HTTP 404). Six matches. |
| Commit 39 audit | 1044 `nvidia` repositories: 491 created after the cutoff, 207 with no eligible revision, 136 inspected, 210 unreadable (155 with no root config, 37 gated, 18 with a malformed JSON file). Four matches, the same four as 39's bundle. I read the 55 names that are gated or malformed: Cosmos video and tokenizer models, two embedding models, a robotics model and five `nemotron-3-8b` models from 2023. None is plausibly a DeciLM checkpoint, but the five gated Nemotron-3 configs were not read, so that is a judgement and not a check. |

## Follow-ups (do not block)

1. A 404 on the root `config.json` is recorded as `unavailable`, which makes `complete` false on every real run. Split it
   into its own status (for example `no_root_config`) so that `complete: false` means something was unreadable.
2. The tool takes one organisation. An architecture string can be published by more than one. See the next section.

## For the user: commit 39 and Deci's own models

Not decided here, and nothing is to be re-authored on this account until the user answers.

The 39 audit enumerated `nvidia` only. `DeciLMForCausalLM`, the string commit 39 registers, is also declared by the
architecture's original publisher: `Deci/DeciLM-7B` (created 2023-12-10), `Deci/DeciLM-7B-instruct` and `Deci/DeciLM-6b`.
Their configs describe the per-layer KV heads with a different field (`num_key_value_heads_per_layer`) from the
Nemotron models. They were never offered to the teacher at commit 39, so 39/005 says nothing about whether the new
class can read the models that the registered name originally belonged to. I have not checked the dates of the other
two repositories or what the class does with such a config; that is for whoever acts on the answer.

Question for the user: should commit 39 be re-authored with the Deci repositories added to its reference evidence?
