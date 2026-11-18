# Review request: teacher-model-trial-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Trial assessment only; no adoption, ancestor approval or replacement. Forward walk stays Astra/medium, guidance 11. Further replacements remain held.

Three fresh unassisted Sol/medium sessions completed under .teacher/trials/teacher-model-001, using copied packets with guidance 11. No reviewer material, prior drafts or ledger text supplied. Walk packet/run bytes and modes, journal runs and approved selection compare equal before/after.

Sol used the cloned Astra catalog profile (272k configured window; provider reports 258400 effective), not its native larger context. Position 231 compares guidance 9 Astra against guidance 11 Sol; 213 compares the earlier guidance-11 trial, not the original walk entry. Three positions, one session each cannot establish general accuracy or quota savings.

## Comparison

| Position | Astra calls | Sol calls | Astra full sections | Sol full sections |
|---|---:|---:|---|---|
| 213 | 29 | 40 | 2/2 | 2/2 |
| 231 | 7 | 9 | 1/1 | 1/1 |
| 239 | 17 | 22 | 4/4 | 4/4 |

213 describes MiMo dispatch, all five configs, sampled Base/RL-0530 tensor layouts and unused MTP tensors, with no finding. 231 reports floating-point bound overshoot with a scalar example and no repository caller. 239 traces missing optional classes into unchanged isinstance consumers and reports the resulting TypeError with synthetic execution. These appear to cover the comparison targets; independent source/accuracy judgement is requested, not asserted as an approval. All three distinguish scalar checks from model/GPU execution.

## Usage

Totals below are final cumulative provider events, not sums of successive cumulative events. Cached input is included in input. Reasoning is included in output. These are token counts, not billed cost or account-quota measurements. The transport retained no account-wide quota meter; no quota saving is claimed.

| Position/model | Input | Cached input | Output | Total |
|---|---:|---:|---:|---:|
| 213/Astra | 1597175 | 1513728 | 4063 | 1601238 |
| 213/Sol | 2520900 | 2411392 | 5718 | 2526618 |
| 231/Astra | unavailable | unavailable | unavailable | unavailable |
| 231/Sol | 265004 | 235776 | 2323 | 267327 |
| 239/Astra | unavailable | unavailable | unavailable | unavailable |
| 239/Sol | 853756 | 801408 | 4721 | 858477 |

Historical token totals for Astra 231/239 were not retained. Tool counts rose from 53 to 71 overall; the only retained paired token comparison, 213, also increased. Per-tool counts, full coverage objects and raw usage events are in the report. One app-server turn/start per session; internal inference-step counts are not retained.

## Implementation follow-up

teacher/codex_transport.py restores the exact catalog byte copy for Astra; Sol alone reserializes the cloned profile. Applied after 240 validation, before these trials; three isolated host wire tests passed. Its current hash is bound below as requested by the 240 verdict. The accepted gate full-suite result remains 285 tests; this follow-up used the targeted three-test suite.

## SHA256

- reports/teacher-model-trial-001.json: `723b7b1361ab895e50d762dff2cd619947fd43720dd7dcecd164adfbaadc3f04`
- reports/teacher-model-trial-supervisor-001.py: `59b6a301f9d034dc2149ad419001fb3afe7ac322dba187e301e31d636138ffd9`
- teacher/codex_transport.py: `f0f1c6e12e5d38de781ea125bd5ea25ee795afad1cd1c4152ed31519e854ad19`
- reports/teacher-model-catalog-followup-tests-001.log: `7855d195fcb8019c93cf2d5ee81a840b14f650bfa8c29b4c3778ffaaee11a819`
- reviews/verdicts/teacher-model-trial.decision.md: `8156830a9e1a178c810527d72bf5529f32c17b993b8b24789618d82b0a5c43de`
- reviews/verdicts/teacher-model-trial-implementation-001.md: `6c9078513e8cc8037291d8c20639654fd976e1fcdd3facbc515bad0367cfaf74`
- .teacher/trials/guidance-11-001/run-000213-001/draft.json: `a3229380a3736fe27e883b4baec71ea31273f3d91f47de8d6f2bd36fec7c0754`
- .teacher/trials/guidance-11-001/run-000213-001/draft.md: `d2e493b63651786f6dbeca332e5c2875890cb9f3048494178d7d23809ae22107`
- .teacher/trials/guidance-11-001/run-000213-001/raw-transcript.json: `3dc945ec00e4ac36d29c2fbda010b4bf64aebce3182e6665b653bd4b06a76f26`
- .teacher/trials/guidance-11-001/run-000213-001/coverage.json: `473a6e7b86534c3f0a3c9729f46bc91d277c88976a6f731227fa50c6470e2fd9`
- .teacher/trials/guidance-11-001/run-000213-001/provenance.json: `2994f8f571302232df276e85f8a3a5bee67ceeb1d7a44f9e83992e3ff3445587`
- .teacher/trials/guidance-11-001/run-000213-001/token-usage.json: `ee6a2f5b37e66938590984520322272e86bf651db7a939cc24e2f99b8da839d5`
- .teacher/trials/teacher-model-001/run-000213-001/draft.json: `3e314e28e24a3772d5e3a2e6c158add1942330aa86279fda2fdd945f2b9245c9`
- .teacher/trials/teacher-model-001/run-000213-001/draft.md: `f2eea5a326eaec02a7a85ed40a2fbda82de1bf3bc5efb2a55e272a70f316d6a8`
- .teacher/trials/teacher-model-001/run-000213-001/raw-transcript.json: `502eeab5fcc8ac44f0c6959f705949ded5d2de2c591836a4f8b2cb9bb91cbcd9`
- .teacher/trials/teacher-model-001/run-000213-001/coverage.json: `171aae4750b4f13d1eb04cffdb0ad07914cca449588c0912456e913b524ae096`
- .teacher/trials/teacher-model-001/run-000213-001/provenance.json: `82dcb1f41370843ca1b30d04caf1cd2ebbdc6d84ff991eec9c443d9447424991`
- .teacher/trials/teacher-model-001/run-000213-001/token-usage.json: `56af3ef5ba5b4da56c086b5cc013d425ca1cd9e1100743495a116c08fc9a4e3b`
- .teacher/trials/guidance-11-001/packet-000213/manifest.json: `341996d2ecfebf4c674484424ae3884ef7c71bf711b9beb848a784c1e5f613fb`
- .teacher/trials/teacher-model-001/packet-000213/manifest.json: `341996d2ecfebf4c674484424ae3884ef7c71bf711b9beb848a784c1e5f613fb`
- .teacher/runs/commit-000231-001/draft.json: `00f4a6d598335f9abaf67da5030281abdbe3eac2a8bdb5408455764f14e27d9b`
- .teacher/runs/commit-000231-001/draft.md: `fca5772adc8841f21d40fc04078be399919c517914d9038863b32b9044492134`
- .teacher/runs/commit-000231-001/raw-transcript.json: `9cadcee31a5a753ee3d4495c3bee98a54131a0ecd47ae9da5211cd2c743eebff`
- .teacher/runs/commit-000231-001/coverage.json: `f6fe5414c5d03838da381b13b758d04f824b60214f6bc04aaa00c66f3a2e285a`
- .teacher/runs/commit-000231-001/provenance.json: `431743ff49ce2271724efe184cf2afd9f26d1b0088ade33129a6878bcc9d0a7d`
- .teacher/trials/teacher-model-001/run-000231-001/draft.json: `95d976a8ab3dddb6fc14fbd7d5b33fe4377142d3d9f6aeaac81b8edd6718e5b0`
- .teacher/trials/teacher-model-001/run-000231-001/draft.md: `903b9038c66555d8c78509be8c4f175c28f2487ec3ce55d5f2c7f8bbc1c481b4`
- .teacher/trials/teacher-model-001/run-000231-001/raw-transcript.json: `2a4868e28294834d30027bb22f67fd87f83ba6805e920ff3f173e3517f50f0a1`
- .teacher/trials/teacher-model-001/run-000231-001/coverage.json: `0798e27fc9f3cc3833f9b1b9b01a0f2f3a0bfe8435ca253dcc0654c8dea284f0`
- .teacher/trials/teacher-model-001/run-000231-001/provenance.json: `b4a3d28681cc20823f46507237b3d973872b9fa4baa01c13b4827bbba5686e35`
- .teacher/trials/teacher-model-001/run-000231-001/token-usage.json: `7881aca4f7ef85af13772c697d45316fe92a6ad68619a0d0914f7afd6182cf2f`
- .teacher/retrieval/000231-001/manifest.json: `7aec3619261d58d734eb2e61ba236a40069925d78f90917c92b96a6f0d5f941a`
- .teacher/trials/teacher-model-001/packet-000231/manifest.json: `d216b730cde480c89f966915b666f111a1d782053dfd5df38b4f24a96cd39e71`
- .teacher/runs/commit-000239-001/draft.json: `4c827262187bec74666ade7ce937478421a46deea11ef34b36e49b178e4d0464`
- .teacher/runs/commit-000239-001/draft.md: `1d8ff0684a43b1aa4803c7da38c7ca67d53f05196227056268157c02d2979690`
- .teacher/runs/commit-000239-001/raw-transcript.json: `7bd7db22a1496a52783dd668314cacfb0155a518035e6abe2a96db5a926dcd9c`
- .teacher/runs/commit-000239-001/coverage.json: `bcfadaef804b304f3bd902d9c4fd83c04f9da99e6993e964488c4bcb816e89c0`
- .teacher/runs/commit-000239-001/provenance.json: `9d668c55139e474998148cd4b2fc1cce28d3362d84c337812cf2475fef21e27a`
- .teacher/trials/teacher-model-001/run-000239-001/draft.json: `83c875422dac2c9e2421fa3be7f9b70e1334ee8780934dbfc1458bbd951499e7`
- .teacher/trials/teacher-model-001/run-000239-001/draft.md: `e3373e59b4a64965616f7e609a2f5d1aaabbbf36f189c1d0c6363f5fea31c617`
- .teacher/trials/teacher-model-001/run-000239-001/raw-transcript.json: `c88febf3444296e77db060cab6da94357218c2cc0edbc607f5f1a6836568d222`
- .teacher/trials/teacher-model-001/run-000239-001/coverage.json: `98dc7ac049a75809bc4b3ca026797833534c6862afceea68706bc81a8b068525`
- .teacher/trials/teacher-model-001/run-000239-001/provenance.json: `b5f5a54b204b39fc2986c60d6bf216001988a05557f2b7b3b43191311eddb52b`
- .teacher/trials/teacher-model-001/run-000239-001/token-usage.json: `0146c5819e0bd4f382d178013fad50b7317f91f161c83684df03009ac8fec233`
- .teacher/retrieval/000239-001/manifest.json: `beecddf58a8ee639d773a785936fc11e41aea353ad0155dc3507093d11eae05d`
- .teacher/trials/teacher-model-001/packet-000239/manifest.json: `beecddf58a8ee639d773a785936fc11e41aea353ad0155dc3507093d11eae05d`
