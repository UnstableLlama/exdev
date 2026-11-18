# Review request: commit-000295-003

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: ancestor retrieval only; canonical and training remain false.

Upstream: https://github.com/turboderp-org/exllamav3/commit/69f8f9a07b95142878997f79e0053b1c1e08422f

Commit title (copied from git log): Clamp output of activation functions to float16 range

Run: `.teacher/runs/commit-000295-003`.
Packet and original packet: `.teacher/retrieval/000295-003`.
Teacher: gpt-6.1-sol / medium; contract 8, guidance 12, salience-v3-paths.
Fresh reviewer-assisted attempt, not a revision or replacement. Only the bound pointer-only coverage attachment was added; neither rejected annotation, transcript nor verdict was supplied to the teacher. Validation repair was enabled and unused (`validation_repair: false`).

Ran ahead of: 296.

The packet is not sparse: all 294 strict-ancestor entries are present, including approved 294. Later position 296 is not teacher input and has no changed-file overlap; there was no concurrent teacher session. The retry followed the expressly authorised prepared route. The packet comparison preserves all 294 ancestor entries and 4284 original non-manifest files; only the coverage attachment fields differ from 000295-002. Attempts 001/002 remain rejected.

## Assessment

The entry answers all six coverage questions. It identifies the FP32-input product's narrowing to half before saturation at ±65504, distinguishes unchanged half-input and non-gated paths, and audits literal/AST constructor sites. It traces Ernie 4.5 MoE routed experts through both ordinary and fused destinations, distinguishes half/default builders, and relates the immediate parent's FP32-intermediate change to this clamp. Actual checkpoint values or numerical benefits are not established.

Four inherited, suspected conditions are submitted for review: opt-in FP32 GatedMLP's incompatible in-place destination (no located shipped builder enables it); odd-element activation tails; fused all-expert capacity when expert count exceeds per-token capacity; and workspace-backed fused returns/output overrides. The entry bounds caller reach and distinguishes the ordinary sparse destination already corrected by the parent. These are assessment candidates, not new accepted ledger records.

Independent host-enabled replay in `reports/commit-000295-author-validation-003.json` is exactly equal to the launch queue-validation report: 39 identical calls and 4284 verified shared read-only blob links; full-review tier. One of one task sections was fully read, with four ancestor prose reads. Tool counts: git_show 3, repo_read 5, repo_grep 13, ancestor_read 4, run 4, web_fetch 10.

Three of the four `run` calls read repository files separately from repo_read: constructor AST inspection, module/backend source inspection, and selected backend/native ranges. The fourth used standard-library scalar half-storage and pair-index models. No repository implementation was executed; no CUDA build/kernel, checkpoint loading, conversion, generation or benchmark was run. Scalar models do not establish CUDA FP32/transcendental/half2 NaN or signed-zero behavior, or real model failures.

Read limits: the initial parent linear.py read was truncated and not completed; the later task-version targeted reads do not complete that parent file. A broad parent exl3_mgemm grep hit its limit; targeted reads followed, without claiming a complete global search. The task diff and issue 53 pagination were completed. Literal/AST searches do not establish external or dynamic-alias callers.

Catalog: 27 open and 2 closed rows. Closed path-only qualified/selected: 0/0; total qualified/selected: 2/2; cap 20, no truncation. No catalog stop was bypassed.

## Integrity, implementation and ledger

The run survived the machine restart intact. All 45 teacher and 4 orchestration implementation hashes still match current files; the manifest hash matches provenance. Authored run files were not edited or rerun. Runtime recorded by the server: Codex 0.167.0, Python 3.14.4, Linux aarch64. Production token totals were not retained; token-usage retention remains pending, so no total is inferred.

No implementation change since the accepted 332-test full suite; no new suite run was needed for this assessment. No sampled mechanical entries or ledger candidates are included. No ledger item is owed from the rejected 295 attempts. The 296 approval and its ledger obligation remain deferred until 295 has an approved entry and approvals can be recorded in ascending order. No 297 session was started; nothing committed or pushed.

## Artifact bindings (SHA-256)

| Artifact | SHA-256 |
| --- | --- |
| `.teacher/runs/commit-000295-003/draft.json` | `f0d63294d3ebc77c2d5ea87836ce8d0c31dba31f2f462b56cc355ac87ca9ddb6` |
| `.teacher/runs/commit-000295-003/draft.md` | `10beea7e34fff87271f0e2d6b15ef4bc4a553f2982a460854d1e6a79117b81ae` |
| `.teacher/runs/commit-000295-003/raw-transcript.json` | `1a862a9ecff4e88378cc8ef13b8ef7902051f066c3c0c9b0fe8c3afaf4154303` |
| `.teacher/runs/commit-000295-003/provenance.json` | `3182b90eb1f991978f82805425a7168e4084cb4b21d1ac5a165563bdcc62450c` |
| `.teacher/runs/commit-000295-003/coverage.json` | `bb739548f9610fb401a9028260dc452e899f4e93d2e0aca8bdeaf87634a088c0` |
| `.teacher/retrieval/000295-003/manifest.json` | `b75e545c21f61d634e7a274fb61bf0c09d1c1e6773f29ca50d668d99b3796b01` |
| `reports/commit-000295-003-queue-validation.json` | `b589140ba6e39285bc5ddbadb68f25d08af0c14caeb9a2f8cca0bdb18d605d43` |
| `reports/commit-000295-author-validation-003.json` | `b589140ba6e39285bc5ddbadb68f25d08af0c14caeb9a2f8cca0bdb18d605d43` |
| `reports/commit-000295-catalog-selection-001.json` | `f14e12ff6d39c7940a8be043447188af8cee18069697a38e2508f3a9bcfd6434` |
| `data/evidence/github/000295-unreferenced.json` | `b0a05fd11d7530efa48ed6c950772066b852aa6f453518182380ac6b72f1856e` |
| `data/evidence/github/000295-closed.json` | `4e4dd993688f62a666ddd3354d2116d1e64807af66f7167f1bc3249f0f36020a` |
| `reviews/verdicts/commit-000295-003.coverage.md` | `429dea59ad067a7ad14da030300c9ac72f87edd384d6e7cbaab31f831098554c` |
| `reviews/verdicts/commit-000295-retry-recovery-003.md` | `b0286939bb2cc350b996ba90bad20152cc07787a778703ff21e3c4a2082b1962` |
| `reports/commit-000295-retry-packet-003.json` | `da6cbc69d3dcd7044a8fbbaa8213127b8adf32e1e5ad9e853d037c564404dca9` |
| `reports/commit-000295-prepared-003.spec.json` | `b1aba2c7753fb59082c7ae31940dbfc9f8c47a3b07e547be67b3a7f6035c42e8` |
| `reports/commit-000295-prepared-003.py` | `a14c09a4017d060f4b775b9754b9dfad851b0886f1bf1f65188c6a2dc2b8d3b8` |
| `reports/commit-000295-prepared-003.log` | `0ab511718705b6fc6ca73a6d521a9c0e8df06fcee768353f6cefd56b05a9b8cb` |
| `reports/commit-000295-prepared-003.result.json` | `7a040ee9f865b2bca2077b42dbd914e2e6610598cac73f07a4ae873fd514fd54` |
| `reports/commit-000295-before-recovery-003.json` | `214056bf63e47ad2f37f6345a938af1447e3ec48094829488ffa3a9aef080575` |

## Recorder-compatible duplicate bindings

- .teacher/runs/commit-000295-003/draft.json: `f0d63294d3ebc77c2d5ea87836ce8d0c31dba31f2f462b56cc355ac87ca9ddb6`
- .teacher/runs/commit-000295-003/draft.md: `10beea7e34fff87271f0e2d6b15ef4bc4a553f2982a460854d1e6a79117b81ae`
- .teacher/runs/commit-000295-003/raw-transcript.json: `1a862a9ecff4e88378cc8ef13b8ef7902051f066c3c0c9b0fe8c3afaf4154303`
- .teacher/runs/commit-000295-003/provenance.json: `3182b90eb1f991978f82805425a7168e4084cb4b21d1ac5a165563bdcc62450c`
- .teacher/runs/commit-000295-003/coverage.json: `bb739548f9610fb401a9028260dc452e899f4e93d2e0aca8bdeaf87634a088c0`
- .teacher/retrieval/000295-003/manifest.json: `b75e545c21f61d634e7a274fb61bf0c09d1c1e6773f29ca50d668d99b3796b01`
- reports/commit-000295-003-queue-validation.json: `b589140ba6e39285bc5ddbadb68f25d08af0c14caeb9a2f8cca0bdb18d605d43`
- reports/commit-000295-author-validation-003.json: `b589140ba6e39285bc5ddbadb68f25d08af0c14caeb9a2f8cca0bdb18d605d43`
- reports/commit-000295-catalog-selection-001.json: `f14e12ff6d39c7940a8be043447188af8cee18069697a38e2508f3a9bcfd6434`
- data/evidence/github/000295-unreferenced.json: `b0a05fd11d7530efa48ed6c950772066b852aa6f453518182380ac6b72f1856e`
- data/evidence/github/000295-closed.json: `4e4dd993688f62a666ddd3354d2116d1e64807af66f7167f1bc3249f0f36020a`
- reviews/verdicts/commit-000295-003.coverage.md: `429dea59ad067a7ad14da030300c9ac72f87edd384d6e7cbaab31f831098554c`
- reviews/verdicts/commit-000295-retry-recovery-003.md: `b0286939bb2cc350b996ba90bad20152cc07787a778703ff21e3c4a2082b1962`
- reports/commit-000295-retry-packet-003.json: `da6cbc69d3dcd7044a8fbbaa8213127b8adf32e1e5ad9e853d037c564404dca9`
- reports/commit-000295-prepared-003.spec.json: `b1aba2c7753fb59082c7ae31940dbfc9f8c47a3b07e547be67b3a7f6035c42e8`
- reports/commit-000295-prepared-003.py: `a14c09a4017d060f4b775b9754b9dfad851b0886f1bf1f65188c6a2dc2b8d3b8`
- reports/commit-000295-prepared-003.log: `0ab511718705b6fc6ca73a6d521a9c0e8df06fcee768353f6cefd56b05a9b8cb`
- reports/commit-000295-prepared-003.result.json: `7a040ee9f865b2bca2077b42dbd914e2e6610598cac73f07a4ae873fd514fd54`
- reports/commit-000295-before-recovery-003.json: `214056bf63e47ad2f37f6345a938af1447e3ec48094829488ffa3a9aef080575`
