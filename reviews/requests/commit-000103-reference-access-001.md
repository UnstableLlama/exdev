# Reference-access review: commit 103 Cohere2

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Task: `0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8` — "Add Cohere2 architecture"
Cutoff: 2025-04-28T04:22:35+02:00.
No teacher run or packet has started. This requests resolution of a reference
access blocker, not prose approval. Canonical and training remain false.

Commit 102 approval and the first live git_renames outcome are recorded. The
commit 103 trigger correctly derives Cohere2ForCausalLM from the new config
class; no registry literal key is detected and there are no unresolved files.

Official discovery enumerated CohereForAI, CohereLabs and Cohere (original,
current publisher and company namespaces, with the same documented sources as
98). CohereLabs has 55 visible repositories. Three pre-cutoff gated candidates
currently advertise Cohere2ForCausalLM: c4ai-command-a-03-2025,
c4ai-command-r7b-12-2024 and c4ai-command-r7b-arabic-02-2025. Their historical
configs were not accessible from Hugging Face. Current metadata is administrative.

Under the general mirror rule in `reviews/verdicts/commit-000098-reference-mirrors.decision.md` point 7, accepted tooling successfully
recovered Command A (54 objects) and Command R7B Arabic (9 objects) from
CohereForAI ModelScope mirrors. These are retained in the cache with per-file
identity and cutoff proofs, not attached as a partial final bundle. Only metadata,
small files and bounded safetensors headers were downloaded; no weight payloads.

Command R7B recovery failed closed at config.json. Both located ModelScope
mirrors have the current config committed on 2025-05-13, after the task cutoff.
At known pre-cutoff mirror revisions, both configs have Git blob id
`43fd683cd8fc1b67dcac6743694d5c954cbcf736`; the official current config publishes
`8bf71a2f9acdcf6e9d2aec5607717a6860385de6`. These do not match. The checked unsloth
base and two quantized-name endpoints return 401, not usable identity proofs.
The alternatives report records exact revisions and metadata.

I have neither omitted Command R7B nor labeled it no_eligible_revision. Its
historical existence is not in doubt; the available evidence cannot meet the
current official-identity plus historical-availability rule. Please resolve
whether another verifiable source is available or a user decision is needed to
accept the older mirror under a different evidence status or exclude this model.
No credential request is assumed; the prior user said no token is coming.

Discussion catalogs (10 open, 0 qualifying closed) and parent snapshot 102 are
ready. No implementation changed. The walk is stopped before commit 103.

## SHA256

- reports/commit-000103-reference-access-blocker-001.json: `ee4e4d22234e79b9ed29f9cd18053a9a7f3e5a69a81b977635474d247431d57d`
- reports/commit-000103-reference-discovery-002.json: `55c762be3a1ad3e19d9617495258547d91f3789c160d2e51f3d6064ebb88fa1f`
- reports/commit-000103-reference-discovery-001.json: `ac0a91683c6089d16c184ba6446ffd6d88481e2fe20a0d2992d159e1167e9084`
- reports/commit-000103-reference-selection-002.json: `3eed8139ec69be2135cfa80bca381d0f24216baa0ff2832895a18ce5f1933fe1`
- reports/commit-000103-mirror-discovery-001.json: `08da283c90fd77f473df02914889e920b6d1d362a75b3a6641f8690336964e9a`
- reports/commit-000103-reference-alternatives-001.json: `13b61661b001ad8d4d8a4ade58e543e5b41c5c63c77e8c3c5fe43723e35457b4`
- reports/commit-000103-mirror-recovery-001.json: `cd20ce12173301ac7140b433fef2de79bad2272a93f5a2f00d881462b75ddbf4`
- reviews/verdicts/commit-000098-reference-mirrors.decision.md: `d1415f21051a32872ab7b9d9504e5f446f38f8019163c65d7d5c0c315638f26c`
- data/evidence/modelscope/000103-001/0/recovered.json: `365c5fbcbfa5ac450c98ec2d5dc1ed5eebbdb5228e962d3f557c46eda20c9bfc`
- data/evidence/modelscope/000103-001/2/recovered.json: `6155940693f4bdd236011aae30c9162e52a3187cb309c8a22bfb491049b28a9a`

Reply in `reviews/verdicts/commit-000103-reference-access-001.md`.
