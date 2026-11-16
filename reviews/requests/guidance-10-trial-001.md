# Review request: guidance-10-trial-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Three fresh unassisted guidance-10 trials completed at 188 and controls 189, 178, one invocation each, no retries. Requested scope is trial assessment only; no ancestor approval, canonical use, training or adoption. The walk remains on guidance 8.

Each scratch packet differs from its original approved guidance-8 packet only in guidance_version. Cutoff evidence and ancestor selection are unchanged. No coverage request, verdict, ledger or reviewer criteria reached a teacher. Walk retrieval/run hashes and modes and journal runs/approved_entries match across the snapshots. Approval of 196/002 was held outside these snapshots. These trials are not journal attempts and have no approval.

Token capture observes transport events without altering sends. Counts use the final cumulative event; cached input is a subset of input. Historical baseline token counts were not retained, so no token ratio is claimed. Each session uses one app-server turn/start, not one inference step. Tool calls total 44 versus 35 (25.7% more).

| Position | Trial / baseline calls | Input | Cached input | Output | Total |
|---|---:|---:|---:|---:|---:|
| 188 | 22 / 16 | 1029916 | 964992 | 4625 | 1034541 |
| 189 | 10 / 10 | 298023 | 262656 | 1638 | 299661 |
| 178 | 12 / 9 | 477184 | 424704 | 2620 | 479804 |

All task sections were fully read: 2/2, 1/1, 1/1 respectively. Detailed per-tool and ancestor retrieval coverage is in the report; this does not imply complete repository coverage.

188 reports removed transform validation and inherited zero-grid and Boolean-selector findings. It still places the device-less kernel-address cache concern under uncertainty, not findings; cross-device/context correctness is not established. Control 189 reports no findings and explains overwrite semantics. Control 178 retains the inherited optional-sampling-output finding and adds no assertion-removal finding. These describe the drafts, not independently approved findings or a pass verdict.

188 executes one scalar shape/integer calculation; 178 executes one scalar transcription of optional-output assignment. Neither run call reads repository files. 189 executes no run call. No GPU, model, native extension or performance execution occurred. All 44 recorded tool results replay identically; all packet blobs verify read-only by hash and shared-store link, all provenance implementation hashes match, and cutoff bundles validate. No teacher was rerun for validation. Two administrative validator invocations failed before replay because of an incorrect import and omitted argument; the corrected invocation completed all checks. No implementation changes beyond the accepted guidance-10 gate are submitted.

## SHA256

- `.teacher/retrieval/000178-001/manifest.json`: `996717db472963ef1e8743c03f8f26f8dadd6fad5dcf3a5cc6da2a46058d5eb9`
- `.teacher/retrieval/000188-001/manifest.json`: `e12eff0dca4d55e389f4e62b2a4ea10c94fcbbe33e5d4fcc38f98e48557dd435`
- `.teacher/retrieval/000189-001/manifest.json`: `b67a353b655108e6b4d834ec3327149b310b128b5260f9afe1d842ba8347a3a4`
- `.teacher/runs/commit-000178-001/coverage.json`: `cf20cbd28ea563908fe7910d5eb0dfd27bdf2d1473530a32b5dbafe13740a018`
- `.teacher/runs/commit-000178-001/draft.json`: `14235a9af7ed232c592cb1eb45a6ec580e866c84fb5cbae4d37433e9b0b552b4`
- `.teacher/runs/commit-000178-001/draft.md`: `e76c77f1a246117773a0e3aade1ed88d8d8f4b64c300f656080d243233e0b636`
- `.teacher/runs/commit-000178-001/provenance.json`: `ec821b4b614f871601448399441b0e32690de73025f05372ab8b532cd42e8d85`
- `.teacher/runs/commit-000178-001/raw-transcript.json`: `c105da0dfb3878c86880acb331c05609d99f3398aa281af2489e8272e29156e0`
- `.teacher/runs/commit-000188-001/coverage.json`: `3889a183193cd876d54d02841edb755a3f172bd4ae562716978baa2d7dbab681`
- `.teacher/runs/commit-000188-001/draft.json`: `1a0d0b6fb3fb9980fdcd9fbd269e704b692ce8cee6f0644d2d355f288db854b3`
- `.teacher/runs/commit-000188-001/draft.md`: `ace74ca1a8fcdd412fcd8ee8254efc3bea680740b9072eabb20a787ee1ac78b7`
- `.teacher/runs/commit-000188-001/provenance.json`: `91df893efad6d565bb9dabc6b119242c192c49d78f2dab27ffddbe8fc1077748`
- `.teacher/runs/commit-000188-001/raw-transcript.json`: `0cee855b62ed0a61f5fcaa89d08177917d67bf4558dbaee30816855606179425`
- `.teacher/runs/commit-000189-001/coverage.json`: `06eb44041510efcf9a65cddb3dcf6af87eeca1229ba1fcafcba69a7b67002605`
- `.teacher/runs/commit-000189-001/draft.json`: `d99fb38bb5bdb49ae230f893a7b3f26480bd107389951d67d1b890e730d2e509`
- `.teacher/runs/commit-000189-001/draft.md`: `871238c7526b296728088efb969406931c79da05d5b5e3a8f114a1514ccf96fa`
- `.teacher/runs/commit-000189-001/provenance.json`: `b706b5c6d3dbab1fb5d6138f34dcdb5f5f1fd412574c3a1cd979f8dca32b85dd`
- `.teacher/runs/commit-000189-001/raw-transcript.json`: `a13833adc65735a621e5424dc7a93410feb0f34eb27923e391a4faadfdca36cd`
- `.teacher/trials/guidance-10-001/packet-000178/manifest.json`: `a1c82385e8e98c7f0348239c3b65fef5d9339c403abaa7d358c3738255644d4c`
- `.teacher/trials/guidance-10-001/packet-000188/manifest.json`: `2fe952ba53fbd664a6b8e693c787d5b1aaa723f196f97a917c863a04a1dffca9`
- `.teacher/trials/guidance-10-001/packet-000189/manifest.json`: `23f9ca69d5aedc7acdad439feab8e7ad170666d563b514435f2580af87f2730b`
- `.teacher/trials/guidance-10-001/run-000178-001/coverage.json`: `88c089d9f290b860da58b957aa20d38a121d32b075dfa1d7bc3e573c970f2128`
- `.teacher/trials/guidance-10-001/run-000178-001/draft.json`: `74086dcdf7aea35d44b86940cd8b48253b1ff75e8428d143833a87408750d6b6`
- `.teacher/trials/guidance-10-001/run-000178-001/draft.md`: `fdffc17f50782543593f4c9d52495996c394a13ada67e7b1a5a4bc80f832813d`
- `.teacher/trials/guidance-10-001/run-000178-001/provenance.json`: `7fe2e2ee47fc147ade929737786c65e7c420c27c4a99e988ae31f69cce938b16`
- `.teacher/trials/guidance-10-001/run-000178-001/raw-transcript.json`: `b4524df5a2d62cc932bfb4060b8b5a8e4046866fa5a38445ecbd89e2b3b2bc38`
- `.teacher/trials/guidance-10-001/run-000178-001/token-usage.json`: `5688f7f8721ac6ef816caed047410b5725a728a579b93c9678de7b6dfb0c7df0`
- `.teacher/trials/guidance-10-001/run-000188-001/coverage.json`: `466734f7cb9c9eabb0c145a2470426ef3d0318ab9ba39f41d16d083a2e129103`
- `.teacher/trials/guidance-10-001/run-000188-001/draft.json`: `34a7103a6acb59d0bbab2a060575e6fd92be5612b957a52a4cc2fe018953662f`
- `.teacher/trials/guidance-10-001/run-000188-001/draft.md`: `623619146eac49c24b958c7de0d9edcfda34904226e7975229085035fefca579`
- `.teacher/trials/guidance-10-001/run-000188-001/provenance.json`: `d12af720ed61ba14c346bde9c8fee589ef22e177b034ae859cd46025d3be6fd7`
- `.teacher/trials/guidance-10-001/run-000188-001/raw-transcript.json`: `ba9b94d5c142cc9805ebd1a46deeb20ed77c0b38881ad6dd17db93bf75872f40`
- `.teacher/trials/guidance-10-001/run-000188-001/token-usage.json`: `ced00a75e395af49b1653cdff6fbcc1617bbb71ba5d5960fa3346262a582f2f0`
- `.teacher/trials/guidance-10-001/run-000189-001/coverage.json`: `252a84088b5d297ff9b3b4297bc267f929b307059f60c94445c2fbc23aa79832`
- `.teacher/trials/guidance-10-001/run-000189-001/draft.json`: `bece6902479f2e803ecfd9a79d2f7dd9f73984130fb534963a03ea2234a24972`
- `.teacher/trials/guidance-10-001/run-000189-001/draft.md`: `07c2d479932d15579b7b37850c825558f6b6516229a67146b624036d35725e35`
- `.teacher/trials/guidance-10-001/run-000189-001/provenance.json`: `7fb8278c826f7956631f9419987b473c328c0e2d2a20b214fcc687081488ebf6`
- `.teacher/trials/guidance-10-001/run-000189-001/raw-transcript.json`: `951a1cc2d878de9d9f4af0495b587a8b3580a9dc607d2925ac88de3979d999f3`
- `.teacher/trials/guidance-10-001/run-000189-001/token-usage.json`: `3eaa52fad13ceba1fad3a539b2ba0eb70bd8e01d20a2b6757fa7f31c49b5d68e`
- `.teacher/trials/guidance-10-001/walk-after.json`: `081b35f91f38c4442a27a245e06f1065075c1adaad825dd9d3859a30ae9ed3d0`
- `.teacher/trials/guidance-10-001/walk-before.json`: `081b35f91f38c4442a27a245e06f1065075c1adaad825dd9d3859a30ae9ed3d0`
- `reports/guidance-10-trial-001.json`: `b071a7ddb829029cebda806310e1723c6e6f0e71ec2ee339564e55e83b74c36d`
- `reports/guidance-10-trial-supervisor-001.py`: `fc2180dfdc781fd32491524fd9bfb8541050c567a6e139d1be2fbfeacd2e450c`
- `reports/guidance-10-trial-validation-001.json`: `9dfcc2dd26bf8d86ceb59d51f8ec79592479184455c78811d2fcd364d3e5dbb7`
- `reviews/verdicts/guidance-10-implementation-001.md`: `b4cb18c07c361c7c4eb04d5af2117b0585903da1c78f0dd6cc60ea21a70e1ff0`
- `reviews/verdicts/guidance-10-trial.decision.md`: `9d1dcc4ec73d6465424184fe490b32f8f830ff3ca6a785ed6757f3fd7741c5fb`
