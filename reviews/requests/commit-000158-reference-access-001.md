# Commit 158 reference discovery access gap

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

157 approval recorded. No 158 teacher run or packet exists. Upstream
`9665ba99989955593d2fb148323c9a96c77d1bea`, "Add Mixtral architecture", triggers
MixtralForCausalLM. Exact cutoff: 2025-05-14T17:53:33+02:00.

Official-publisher discovery enumerated all 83 currently visible mistralai
repositories. Four match the pre-cutoff architecture and all four configs/header
sets are recovered and pass load_bundle: 176 evidence objects, no weights.
Four root-config 404 cases were checked against immutable repository trees and
confirmed absent. One candidate remains unreadable:
`mistralai/Mistral-Large-Instruct-2407` returns HTTP 401 on repository history.
It therefore has no inspected pre-cutoff config or pin. Its name cannot establish
that it does not match. Discovery remains incomplete even though recovery for the
four known matches is complete.

I have stopped before authoring under the existing exhaustive-discovery rule.
Please review the access gap and route any evidence-policy exception or alternate
source authorization to the user. Existing ModelScope authorization was scoped
to the ten Cohere repositories; I have not extended it to Mistral or guessed a
mirror. No new token request is made here. No implementation changed.

The first discovery command mistakenly used a cutoff nine minutes later. That
administrative output is retained and explicitly excluded. Discovery was rerun
at the exact recorded cutoff; only selection 002 fed recovery, and discovery 003
records the pinned-tree absence checks. Neither report nor reviewer material
was supplied to a teacher.

GitHub recovery and parent indexing completed. Salience-v3-paths: thirteen open
rows, zero qualifying closed rows, zero by path alone, no truncation or cut rows.
No historical packet or run was rewritten. Older ledger follow-ups remain tracked.

## SHA256

- reports/commit-000158-reference-access-blocker-001.json: `bd06cdf7e3dc12fbe056dc3a56e529f6d00db00e445279674aa32b470f632119`
- reports/commit-000158-reference-discovery-001.json: `bedef0dea419ebf1b27b10578c9f2c09f33791e81bb97ad2f55a040fd0a010fe`
- reports/commit-000158-reference-discovery-002.json: `011973b18ba95e17e61a16912e82a9cce47c153d8b1eaa7cdd160e22d938a144`
- reports/commit-000158-reference-discovery-003.json: `5d3c0df314215fe5220e303671a10b7e0c546f4355ddf1f8779711977c344dad`
- reports/commit-000158-reference-selection-002.json: `92c442b3def8ed87d2d7d1a48dbe812e28a1362bf927d7186e093cd722ddb13a`
- reports/commit-000158-reference-recovery-001.json: `d4cbd5a5663419b5684d3a6324635216f509eaa2aa2a5a2a3fc1d44907a96c97`
- reports/commit-000158-catalog-selection-001.json: `929fa8624e183a34b17c8326e273606de36c706b604181beeae407bd23380315`
- data/evidence/github/000158-unreferenced.json: `d70b278347f8647eb77703569db9b75ae8beb040667b42d89a1f484952946e48`
- data/evidence/github/000158-closed.json: `a0d17fad2db38e130208a98bb139fd5e430f5870db2f2ed954a635673fb4ffe1`
- data/evidence/github/000158-references.json: `a3d321355661e5b8dfc88081d54c9f8cb2e78ce5485db46d6ad0e8d9a96f9707`
- reviews/verdicts/commit-000157-001.md: `9a11568d7622543ae9413b4926ece64ed952f70bd7b85b6d2a6b3ecec78f4a28`

Reply in `reviews/verdicts/commit-000158-reference-access-001.md`.
