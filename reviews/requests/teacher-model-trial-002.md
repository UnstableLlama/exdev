# Review request: teacher-model-trial-002

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Author/orchestrator: gpt-6.1-sol, medium. Trial teacher: gpt-6.1-sol, medium, guidance11. Comparison teacher: gpt-6-astra, medium; guidance8 at185/197 and guidance9 at210/232/234.

Trial assessment only; no approval or replacement requested. Five fresh unassisted sessions used copies of the approved packets with only guidance_version changed. Original ancestor snapshots retained; no reviewer material, prior draft or ledger supplied. All five finished on their first attempt. Walk packet/run bytes and modes, journal runs and approved-entry selection compare equal before/after. Production code was unchanged during these sessions. Trials remain unapprovable; replacements stay held until assessment. Forward walk remains authorized on Sol.

## Findings side by side

| Position | Approved Astra | Sol trial |
|---|---|---|
| 185 | Settings overwritten; shared warp-sum store race; padded frequency/weight reads; optional-K and partial-width reference failures; all-expert workspace mismatch; persistent output ownership/dtype contract. | Same three new defect groups and all-expert mismatch. Splits the two reference failures into separate findings. Persistent output ownership/dtype remains explicitly in chapter prose, not a structured finding. |
| 197 | Draft cache not relocated; inherited unsafe vector boundaries; ineffective test dtype parameter. | Same three finding groups. Mentions recursive planning but does not identify recursion-limit failure; does not connect the vector-tail defect to quantized-cache scale tensor dimensions. No clear statement that orphan eviction-order changes survive a skipped movement pass. These reviewer conditions remain gaps, not teacher input. |
| 210 | Partial reconstruction width leaves unwritten storage after zeros becomes empty; example32x144 leaves512 elements. | Same identity with a16x144 example leaving256 elements. Adds explicit default128-padding reach limitation and scalar write-coverage checks. |
| 232 | Opting out of padding reaches inherited odd activation tail, consumed by down projection. | Same identity and explicit opt-in reach; existing model constructors retain padding. |
| 234 | New preprocessing reaches inherited floating-point resize overflow. | Same overflow and follows generated positions into spatial RoPE table bounds (112x8 grid, max index12217 versus12100 rows), under stated longest_edge1540 assumption. Reads the full first Base HF shard header, not every checkpoint/shard. Original packet lacks processor metadata; trial reports that limitation rather than using later backfill. |

These compare the retained entries, not independently approved new findings. Please assess accuracy and omissions. Scalar checks are not repository/GPU execution; no speed or numerical-equivalence claim. The changed guidance and one session per position confound model-only conclusions. Sol uses the cloned Astra catalog profile, not its native larger context.

## Coverage and calls

| Position | Astra calls | Sol calls | Astra full sections | Sol full sections |
|---|---:|---:|---|---|
| 185 | 45 | 41 | 7/7 | 7/7 |
| 197 | 25 | 23 | 8/8 | 8/8 |
| 210 | 9 | 15 | 1/1 | 1/1 |
| 232 | 16 | 20 | 1/1 | 1/1 |
| 234 | 35 | 49 | 3/3 | 3/3 |

All assigned sections were fully read in both sets. Per-tool counts, ancestor retrieval and coverage details are retained in the report. Total calls: Astra130, Sol148. One app-server turn/start per session; internal inference steps were not retained.

## Token totals

Final cumulative provider totals (not sums of cumulative events). Cached input is included in input; reasoning is included in output. Historical Astra totals are unavailable for all five runs; no estimate substituted. No account-quota measurement or quota saving established.

| Sol position | Input | Cached input | Output | Total |
|---|---:|---:|---:|---:|
| 185 | 2504584 | 2410496 | 8120 | 2512704 |
| 197 | 1083092 | 1020800 | 6143 | 1089235 |
| 210 | 584335 | 528768 | 3416 | 587751 |
| 232 | 929382 | 862720 | 4862 | 934244 |
| 234 | 4404444 | 4271616 | 8429 | 4412873 |
| Total | 9505837 | 9094400 | 30970 | 9536807 |

## Administrative follow-up

243's approval will now be recorded after isolation completion. Its three ledger items remain owed with244's request. Production token-usage-retention-001 is separately owed and nonblocking. No replacement103 before this assessment.

## SHA256

- reports/teacher-model-trial-002.json: `72410a77e0fc83c39ad92ed5739fd2f495d74a6841edda664db5bcef08369d5e`
- reports/teacher-model-trial-supervisor-002.py: `abbde0331ea80510f83de491ce421160106d4293af2bd880415b5979631bafc7`
- reviews/verdicts/teacher-model-trial-2.decision.md: `2e0c93122c5b29037ce9080c0b498847673a08a8f641a2fe178f61b451be7854`
- .teacher/trials/teacher-model-001/walk-before-002.json: `2fc629bca5e2874c7ee2c1ce736e8cb59c17d0a5b1f165acff7aa1d599d89fc8`
- .teacher/trials/teacher-model-001/walk-after-002.json: `2fc629bca5e2874c7ee2c1ce736e8cb59c17d0a5b1f165acff7aa1d599d89fc8`
- .teacher/runs/commit-000185-001/draft.json: `5f49b515f8f347e0d5749f847dbd89319353011db5fc4b0bd4f49b6d389c064f`
- .teacher/runs/commit-000185-001/draft.md: `ba7f79f1ea7c09d324ddce398edc3d286897fa3c73e3538e8676c85f1b23e697`
- .teacher/runs/commit-000185-001/raw-transcript.json: `be80bd80474b28b0a864e1bdbc812c448991909736bd5510eb9038b374fcaed6`
- .teacher/runs/commit-000185-001/coverage.json: `46567a5d4a0f344b4bf06d685b8ed9dd8859955e20e94510dc47cefec95a0870`
- .teacher/runs/commit-000185-001/provenance.json: `bc68740331e6d23c40aeb6aefaad107e04eb169f9b85f206465802906aa18f94`
- .teacher/trials/teacher-model-001/run-000185-002/draft.json: `4d0680e22c8ccd6201a4bb7806fa407581b200218ce8297ed670790f1ad59bce`
- .teacher/trials/teacher-model-001/run-000185-002/draft.md: `c02af1c76bad535a6ff8895e680b5c37cb2eeaf4b0b6e79ae9c73858f85dcabe`
- .teacher/trials/teacher-model-001/run-000185-002/raw-transcript.json: `94a17d82e23b687853b6d157c588050781e2638cb828ca662953c126364b1937`
- .teacher/trials/teacher-model-001/run-000185-002/coverage.json: `b4a0069ad14cc2f95664f21c53414913286b053336665f03b003fee2b7d6d9cb`
- .teacher/trials/teacher-model-001/run-000185-002/provenance.json: `5aab03984e2ad23d2f291760eca81f435e128e28450d054c962845a172651797`
- .teacher/retrieval/000185-001/manifest.json: `b14c3813253ca50b00347cee47d48c71d65f8c4e26e591740daae24218fa5d15`
- .teacher/trials/teacher-model-001/packet-000185-002/manifest.json: `0a1493e28826597bd06c910bce4192811d3460b0dd230e9a30a750a3175b022d`
- .teacher/trials/teacher-model-001/run-000185-002/token-usage.json: `43f70d9f0a35c7fc680f6c61a4cd63d65eb93fcf4d8684bf056afe894c2818bd`
- .teacher/runs/commit-000197-001/draft.json: `0799b0ec0bced86e8eaf0c167080acb28452d998d58bc69b85ccbaf1f4934321`
- .teacher/runs/commit-000197-001/draft.md: `d3552e8c05ce8facc514620cb2a40d0ff01355947de9fe853db02be80a91d562`
- .teacher/runs/commit-000197-001/raw-transcript.json: `fb57f945a9da5f82e46ae8b3e4d1dd24f561e64ab3180b37d0afe21a2d75f58c`
- .teacher/runs/commit-000197-001/coverage.json: `e7461dc4aef95aed75b19ff2d2ba2b77f183b948c4e33103f3ac2c899a2d0c98`
- .teacher/runs/commit-000197-001/provenance.json: `f529f4fef2a35324131999ab75ce9c84b33b7be6ec489921c5c939717990be8a`
- .teacher/trials/teacher-model-001/run-000197-002/draft.json: `3b1b4266526677ea901551c52e87ec016290586fb70534b8c5c9fd0c25481c8b`
- .teacher/trials/teacher-model-001/run-000197-002/draft.md: `00b8748f5a695fe69827531c113ae8753d151fff313ec635164a62afa58e6ff7`
- .teacher/trials/teacher-model-001/run-000197-002/raw-transcript.json: `54b2104beec4296509f4f6d1729ba610f3882633bd4bb81e1537cac8427d075f`
- .teacher/trials/teacher-model-001/run-000197-002/coverage.json: `d7c272c420b01730cbd779df2c94a3a35b6ba417975f93522af339625f45d18a`
- .teacher/trials/teacher-model-001/run-000197-002/provenance.json: `d64e5606aecda4d4ce99e855fe770cda05e0940a531bb5839c728adbe8754de6`
- .teacher/retrieval/000197-001/manifest.json: `490cc4a20c571ab2f1165d49290db4f5a22eb491b1ba3909446210b8c272f4bb`
- .teacher/trials/teacher-model-001/packet-000197-002/manifest.json: `19dc6cff8ea2e7fa5ece5be6643c95c25ee1dc20610215d228c878b540bb38e0`
- .teacher/trials/teacher-model-001/run-000197-002/token-usage.json: `89e9f4bf0abd18e941b7dba834d7c4f1998a6b7bc39e34efa59b947aa9d655d5`
- .teacher/runs/commit-000210-001/draft.json: `e123d9a88847f15b1872bda61cc4c8c318590422bdd093db474fb8326453ebac`
- .teacher/runs/commit-000210-001/draft.md: `a3f77ba7e392a80f32275a38a2db3eee2ef4d6bdd19a295694d69b50e6a143bb`
- .teacher/runs/commit-000210-001/raw-transcript.json: `19c57f983525419bb745d31de32fe4cea011ee07b6a8fcd12f91c9e8c0780161`
- .teacher/runs/commit-000210-001/coverage.json: `249695f30e773b47395d79460e8494b8ea6d6cf801caf740643ae218b92d669f`
- .teacher/runs/commit-000210-001/provenance.json: `cc6f3e8dbff4c3aa9e993e44ca27b6b454e9ac8d9c2dcc42df0181184039ba9b`
- .teacher/trials/teacher-model-001/run-000210-002/draft.json: `7c4934af1737c9eb4301acd67e91b9a0a969635449c0aee061a154a9f57f63c2`
- .teacher/trials/teacher-model-001/run-000210-002/draft.md: `9b5b8e405e1ebda2004fcbcb1bddf1d20497b0be29bc50432fca9501ad49d32f`
- .teacher/trials/teacher-model-001/run-000210-002/raw-transcript.json: `ecdf9a39132a78756305bc079e47241fb02e84cbd3a0233714ffcf8009c69f5b`
- .teacher/trials/teacher-model-001/run-000210-002/coverage.json: `a010a16ce57ed89e62c70e6cbea5e1c88983363f2daf02c9f1cd2dbf342987fe`
- .teacher/trials/teacher-model-001/run-000210-002/provenance.json: `890b71245816c796e8fb179d2ee634e81c4165c4bb3ef67c2034b1132e5438e3`
- .teacher/retrieval/000210-001/manifest.json: `921fa3af350433256c5a809f94fe81ca98aac9782d6f1f25a5c7e398b26304ca`
- .teacher/trials/teacher-model-001/packet-000210-002/manifest.json: `709efe780e503f13d62a8368c3c3a3d533a5da2f8f43f553e0e4a0d410514a76`
- .teacher/trials/teacher-model-001/run-000210-002/token-usage.json: `d0d247058418cd5fe2055ef8fa3c20922a288bd4eae17322016d533b425c8f01`
- .teacher/runs/commit-000232-001/draft.json: `d43c25b0e17772da2dd9d30d9aa2757f4dd0f4b5e51407ef29ed32c605df9485`
- .teacher/runs/commit-000232-001/draft.md: `8733d056771ce335b4ab5f4257626b310d287702941c0bd6f584bfca1b686a75`
- .teacher/runs/commit-000232-001/raw-transcript.json: `7b145006e914d0aef4d29b16fa56be3188696db1599fd42f2006ae0a05ec3708`
- .teacher/runs/commit-000232-001/coverage.json: `c4423c8082bb1edeb706ff48c6fd174773373967416fa560308bde51ac448080`
- .teacher/runs/commit-000232-001/provenance.json: `9f0f182cfc99c109bd3322234bb649623ad3f6a87d83ed86708f15f63668027c`
- .teacher/trials/teacher-model-001/run-000232-002/draft.json: `a26f71d9dd91a4b7f0b785ab1b0cd931e018f5a493aea5797b50d193c6d53b19`
- .teacher/trials/teacher-model-001/run-000232-002/draft.md: `e3558793806011f1776416da7032ecd15a400c586a30005c4f3a5f53857b3d5b`
- .teacher/trials/teacher-model-001/run-000232-002/raw-transcript.json: `8860150de83cc9a6148c756cdcdc5c8276a2123c85dd864e62113112b9e9a528`
- .teacher/trials/teacher-model-001/run-000232-002/coverage.json: `5058642b84e1508ca2b4db1a01caf6695a91be4be3950d6806d3fed77e749d22`
- .teacher/trials/teacher-model-001/run-000232-002/provenance.json: `8c0a5b3fee6515034fcac58c3f0ae42dfaa72ee513f7cd1e636562da59529f02`
- .teacher/retrieval/000232-001/manifest.json: `6ac5728ac8923fcd533a9d46c2dea9ec7a02875c191387abae2d97f13a5ebc60`
- .teacher/trials/teacher-model-001/packet-000232-002/manifest.json: `a3bbaa954fbaa8156bcbd6722eb94cb1907d95eebcc497e94c947d306a79f6ef`
- .teacher/trials/teacher-model-001/run-000232-002/token-usage.json: `7b4cbdfdae0aa93e124cdb62f78f43cfd840947f962075023f19e8e19ee766ee`
- .teacher/runs/commit-000234-001/draft.json: `0b3d02722fd4fe928fd64a2e5413d0bd296df32d5bb40e0208f31d909d06e43a`
- .teacher/runs/commit-000234-001/draft.md: `0c9f0933ea292ff1ea8966820615416c03868f8888ae7b7dbc281ec6d0efe612`
- .teacher/runs/commit-000234-001/raw-transcript.json: `063a9a2504553a3cb4a676650282dfb5e4f17d6600dc78fb8a490520ecdbf7b2`
- .teacher/runs/commit-000234-001/coverage.json: `a3a5f913cc1483fe36f31c7c6b479cea7f2278d55ed3b1403436acc01e05d898`
- .teacher/runs/commit-000234-001/provenance.json: `4ef0db73011fa2293e447bf8d038717f52ebed3c73c3113dc7d25c0603858161`
- .teacher/trials/teacher-model-001/run-000234-002/draft.json: `d48ca60bcc0280f47d7376503eb1f36ee4c5bc2e7164951a6068c1c86e7a12a7`
- .teacher/trials/teacher-model-001/run-000234-002/draft.md: `b78c88b83a07a7ca91b6f63a6d05b5a9a9a22bdcc12dae8ecd9fa7cdde3d8e49`
- .teacher/trials/teacher-model-001/run-000234-002/raw-transcript.json: `ccfb600d45682891c73036bf82d78ce7d5f5b0980324ef3a127ea751d46f6a7e`
- .teacher/trials/teacher-model-001/run-000234-002/coverage.json: `e42ea732066677c98fbb9bf030a91e9d863e2895b69ce01126f0f3786c72d6c1`
- .teacher/trials/teacher-model-001/run-000234-002/provenance.json: `722a2e50039f7fe098a73df21b5ccb47375bbb17d9b1d5d79e9b92b58e27d94e`
- .teacher/retrieval/000234-001/manifest.json: `9922afb48d86d8895dabe708e67eca7d00cbc5e7891050e42496f26344be43d2`
- .teacher/trials/teacher-model-001/packet-000234-002/manifest.json: `101e7a6378ba5c0b1a4b2e27f57db237415845a19492f68fa7cf8a2ee1637dc1`
- .teacher/trials/teacher-model-001/run-000234-002/token-usage.json: `1a843bf102ec6bf8284e5c4e707d5cffc2ff587ee78ba118071bfa2a40c5aed7`
