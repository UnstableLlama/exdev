# Commit 214 reference discovery gap

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

213 is approved. No 214 packet or teacher run exists. Upstream `42afcd7e6cd361b2be9aef1072f26ffccffb92db`, "Support Gemma3ForCausalLM", cutoff 2025-06-01T17:13:26+02:00. Walk remains stopped at architecture_trigger, guidance 9.

Full original-publisher Google enumeration covers 1,136 visible repositories. Discovery 002 has five matches and one unresolved candidate. It reuses accepted 164 config/absence proofs only where the fresh official repository SHA is unchanged and either the proof was mirror-verified or the latest repository revision predates 164's cutoff. Changed/new candidates were examined afresh. Counts: 657 pinned configs, 151 mirror-inspected configs, three mirror-inspected non-JSON configs, 183 pinned root-config absences, 141 repositories created after cutoff, one unavailable. All five matching configs have been read.

The unresolved candidate is `google/medgemma-4b-it`. Current official public metadata and both recovered mirror config versions declare Gemma3ForConditionalGeneration, not the triggered Gemma3ForCausalLM. But the current mirror config's date is July 9, after cutoff. Its blob `cf0df7460f46b6470769ea9ebf40fb602a0792e8` matches the current official hash. The May 21 mirror config at `f987c345ce10b4c6b09357625cfc1bf4de1e075b` instead has blob `ac44fe0dc956cf40ee4466e48b8dd1346c282ba4`. The July edit changes text config fields, not the architecture string. Only one pre-cutoff witness was recovered; LLM-Research and AI-ModelScope names returned 404. I have not asserted the two-witness historical exception or treated current metadata as a pinned inspection.

Please resolve whether the existing decision 98 point 5 permits retaining this as "not inspected at the pin; current public metadata declares Gemma3ForConditionalGeneration", or whether more historical evidence is required. Any new policy exception goes to the user. Nothing about this candidate or the review goes to the teacher; it has not been excluded as a proved pinned non-match.

Fresh mirror checks resolve medgemma-4b-pt as a non-match and medgemma-27b-text-it as the fifth match. The two gemma-3n litert-preview repositories have no root config in their complete public sibling lists at latest revisions before cutoff. First-pass probe output is preserved; its final console-print KeyError happened after saving the results and was not a retrieval failure. Discovery 002 explicitly records the remaining gap.

GitHub recovery and parent indexing completed. Catalog: one qualifying and selected closed row, zero path-only rows, no truncation. No implementation change, historical packet rewrite, teacher run, or ledger obligation from 213. Ancestor retrieval only; canonical/training remain false.

Five known matching bundles are complete: four Gemma 3 1B variants plus medgemma-27b-text-it. The combined candidate bundle is `reports/commit-000214-references-combined-002.json` (45 objects, 15 tensor headers, zero weight payload bytes); `load_bundle` passes. This does not resolve exhaustive discovery. The original four-model bundle remains untouched. Build 002 completed retrieval but failed at the no-overwrite guard; build 003 saved the fifth separately, then the combined bundle was validated. No teacher saw any partial bundle.

## SHA256

- `reports/commit-000214-reference-access-artifacts-001.json`: `17c75d237bb239ae4f9252c107566b19b88077e4acb65b8db579fe1c975b8319`
- `reports/commit-000214-reference-discovery-002.json`: `62bc860f383aec7d498fab84a77c5ad0c53fcecb23ebdf24f443c7da8d5714b4`
- `reports/commit-000214-reference-access-blocker-001.json`: `af55e25a388391a1211c86dd496451f286137957319432b2bd0cecc6b41d5a4b`
- `reports/commit-000214-reference-recovery-002.json`: `5dcd8bc1e0f13a4c37a6382e407180221b917eaa2cfb90aaad81cd6e4c8da5f9`
- `reports/commit-000214-references-combined-002.json`: `e824e1e4584cae9ad80f7fa3a9b428b7604ddb708799b25890b024de8807a197`
- `reports/commit-000214-catalog-selection-001.json`: `c1607e0e908f6b61da67dcd5793b8466d01d559ca446949e080bbfb4dbe3fcf8`
- `reviews/verdicts/commit-000098-reference-mirrors.decision.md`: `33adbd76861e8bc4fd7c2d1e0eaca96ccde628572e1f403b92218c3b67487584`

The artifact manifest includes all discovery/probe/build reports and source snapshots. Administrative files only, never teacher input. Reply in `reviews/verdicts/commit-000214-reference-access-001.md`.
