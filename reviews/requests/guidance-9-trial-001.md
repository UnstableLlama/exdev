# Review request: guidance-9-trial-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Five fresh unassisted guidance-9 trial sessions completed at 184, 188, 190 and controls 189, 178, one invocation each, no retries. Requested scope is trial assessment only: no ancestor approval, canonical use, training or adoption. The walk remains on guidance 8.

Each scratch packet under .teacher/trials/guidance-9-001 differs from the original approved guidance-8 packet only in guidance_version. Cutoff evidence and ancestor selection are unchanged. No coverage request, verdict, ledger or reviewer criteria reached a teacher. This comparison isolates the fifth paragraph against guidance 8. All walk retrieval/run file hashes and modes and journal runs/approved_entries match across the before/after snapshots. The 193 approval was held outside the snapshots. Trials are not journal attempts and have no approval.

Token capture observes existing transport events without changing sends. Counts below use the final cumulative event, not sums of cumulative events; cached input is a subset of input. Baseline token counts were not retained, so no token ratio is claimed. Each session uses one app-server turn/start, not one inference step. Tool calls total 83 versus 69 (20.3% more).

| Position | Trial / baseline calls | Input | Cached input | Output | Total |
|---|---:|---:|---:|---:|---:|
| 184 | 24 / 23 | 1176660 | 1098240 | 5072 | 1181732 |
| 188 | 20 / 16 | 889916 | 827648 | 4140 | 894056 |
| 190 | 18 / 11 | 699926 | 647040 | 3758 | 703684 |
| 189 | 9 / 10 | 267517 | 232448 | 1551 | 269068 |
| 178 | 12 / 9 | 479009 | 428160 | 2722 | 481731 |

All assigned task sections were read fully: 5/5, 2/2, 2/2, 1/1, 1/1 respectively. Full per-tool and retrieval coverage details are in the report; this is not a claim of whole-repository coverage.

184 reports routing-bias bypass, the per-call fused output dtype override and inherited all-expert shape mismatch. Its bypass discussion does not report a dtype-conversion finding. 188 reports unchecked native buffers but retains the device-key omission under uncertainty. 190 reports the removed flattening view's stride rejection as a suspected finding, with a public-wrapper input and scalar offset check; it also retains the test-arity finding. Control 189 has no findings and explains overwrite semantics. Control 178 adds no assertion-removal finding; it retains the inherited optional-output failure and explains scheduler readiness. These are observations of the drafts, not independently approved findings or a pass verdict.

184 has two run-tool file-reading calls (the first stops at a nonexistent linear_fp16.py path; the second reads fp16.py and other requested files) and one scalar indexing/half-rounding check. The other executed run calls at 188, 190 and 178 are scalar transcriptions; 189 executes none. No GPU, model, native extension or performance execution occurred. The trial drafts retain their limits. All 83 tool results replay identically, including the failed file read, and all packet blobs verify read-only by hash. No teacher was rerun for validation. Implementation is the accepted guidance-9 gate; no further implementation change is submitted here.

## SHA256

- `.teacher/retrieval/000178-001/manifest.json`: `996717db472963ef1e8743c03f8f26f8dadd6fad5dcf3a5cc6da2a46058d5eb9`
- `.teacher/retrieval/000184-001/manifest.json`: `8125d2ec9534ad59803789335607cb86cc6ac09deaf6f0b1e844a0dad4e77211`
- `.teacher/retrieval/000188-001/manifest.json`: `e12eff0dca4d55e389f4e62b2a4ea10c94fcbbe33e5d4fcc38f98e48557dd435`
- `.teacher/retrieval/000189-001/manifest.json`: `b67a353b655108e6b4d834ec3327149b310b128b5260f9afe1d842ba8347a3a4`
- `.teacher/retrieval/000190-001/manifest.json`: `1b539fad4c62a1c58e8a1a9c45875f74112520a6589ee909a369851363e60de6`
- `.teacher/runs/commit-000178-001/coverage.json`: `cf20cbd28ea563908fe7910d5eb0dfd27bdf2d1473530a32b5dbafe13740a018`
- `.teacher/runs/commit-000178-001/draft.json`: `14235a9af7ed232c592cb1eb45a6ec580e866c84fb5cbae4d37433e9b0b552b4`
- `.teacher/runs/commit-000178-001/draft.md`: `e76c77f1a246117773a0e3aade1ed88d8d8f4b64c300f656080d243233e0b636`
- `.teacher/runs/commit-000178-001/provenance.json`: `ec821b4b614f871601448399441b0e32690de73025f05372ab8b532cd42e8d85`
- `.teacher/runs/commit-000178-001/raw-transcript.json`: `c105da0dfb3878c86880acb331c05609d99f3398aa281af2489e8272e29156e0`
- `.teacher/runs/commit-000184-001/coverage.json`: `7e5367533f8000ebb682e4964e75729d6d92e32082aaefb397588a480130aaf8`
- `.teacher/runs/commit-000184-001/draft.json`: `eaad2613f8075456b0277e156f05467b446027027a18c9a88da75a40bd25b7d2`
- `.teacher/runs/commit-000184-001/draft.md`: `6ff073174347a6453e524ad8721300712fbc3b33f1e6f7588f48b68892831627`
- `.teacher/runs/commit-000184-001/provenance.json`: `e0225f6c7a9952be81cd747caf0830e4918f44f2270cd2837d0a5d087b321ce6`
- `.teacher/runs/commit-000184-001/raw-transcript.json`: `ad6d11a9a013e5b5618951404bea017be993a1e8a6d1e78924610ea0f5d8fda3`
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
- `.teacher/runs/commit-000190-001/coverage.json`: `aafea9253a67544ea66343e13efe999d1883373dc40a82a2129a492f14599285`
- `.teacher/runs/commit-000190-001/draft.json`: `bbef0d5de38d15b435f6024f950e7f6c4c7194f2b15ec22c5a4c74e407edaa6a`
- `.teacher/runs/commit-000190-001/draft.md`: `e61ad724a5baa58fe97260fa934c679a65202ec5a2ba6677687b36d6ac172275`
- `.teacher/runs/commit-000190-001/provenance.json`: `3d5c46beab6ea40fef71fa4c8eee6f70a7e75b54f350ee8b16e40943f5ca34e1`
- `.teacher/runs/commit-000190-001/raw-transcript.json`: `dcc263504bd0a28f34dc8ca1f7fa8002b5362aae3bb7d5b98096e90dbce146ee`
- `.teacher/trials/guidance-9-001/packet-000178/manifest.json`: `0dd955fda8dede3dffa8a45e47a7fb5bcd54a2d2ee798be0078a800aa723ffe1`
- `.teacher/trials/guidance-9-001/packet-000184/manifest.json`: `126fb2618f87a944aac7ac6f343efe2a26774d06fcac93476e7a41bb97e155e7`
- `.teacher/trials/guidance-9-001/packet-000188/manifest.json`: `b674e11a1f1f630fde17aa42080aaf90f08359a2346a670a4d9d9087a18f14c8`
- `.teacher/trials/guidance-9-001/packet-000189/manifest.json`: `40f535618fa696441c5bda4cd451c78168361b91ff9ca604c516ea44829bd2cc`
- `.teacher/trials/guidance-9-001/packet-000190/manifest.json`: `727a8ec97c5f3cf85337ed217da06effe5053edc6f0dcf5af8cf2e808a953906`
- `.teacher/trials/guidance-9-001/run-000178-001/coverage.json`: `c367ad57c8ce26544965857e7b0b40f6a09e4d4acde497d76866a87c98434575`
- `.teacher/trials/guidance-9-001/run-000178-001/draft.json`: `0880ae8a9efcc96f7d5afb13a71206606f0bd8e06bd3d030a98278ad7324f25a`
- `.teacher/trials/guidance-9-001/run-000178-001/draft.md`: `cde6c12a476889fa129d8316b33d8a33957ed47357f93d9a48dd2794817c049a`
- `.teacher/trials/guidance-9-001/run-000178-001/provenance.json`: `574aa2ab4f0a6c3b993095119242df16137ecdf72d4d094b788cd0d58de298fd`
- `.teacher/trials/guidance-9-001/run-000178-001/raw-transcript.json`: `e19eed38b0c848280fcbc814138375501b054cdd5567f2342ba53747a3fccbe9`
- `.teacher/trials/guidance-9-001/run-000178-001/token-usage.json`: `c7d494e9124f7e0df126472d86e46958555364d95104a795b47807fddae7dbe3`
- `.teacher/trials/guidance-9-001/run-000184-001/coverage.json`: `3d88db50a02c669efa596d942cce02ed45efa7760a77000452a04826ed813f1a`
- `.teacher/trials/guidance-9-001/run-000184-001/draft.json`: `8c06e66f39a890db35c8703753bf14ad33a7031c3b6cb63241a11d9f81d2b908`
- `.teacher/trials/guidance-9-001/run-000184-001/draft.md`: `3d4079cb49a558b15a36f9bd47b76e3e0dc6e56ffb0c859bb20669b9ef095cbc`
- `.teacher/trials/guidance-9-001/run-000184-001/provenance.json`: `336869852238945a24d0dd119ca57c06c942b9f928d4dcab1ca98bbe24b9664f`
- `.teacher/trials/guidance-9-001/run-000184-001/raw-transcript.json`: `8220d707c8bd6ecf995a70f82a81e1eece0a5f75976a2b08d57efa6c7833226c`
- `.teacher/trials/guidance-9-001/run-000184-001/token-usage.json`: `c0f19f61d446057671020ccbdf1e06b1e34164d4da0d50791a41dfb611b9a886`
- `.teacher/trials/guidance-9-001/run-000188-001/coverage.json`: `6c5c00928511f55742da00b01c1e9b1e17cba116c85d97ac84c5ec4e8b42d8b8`
- `.teacher/trials/guidance-9-001/run-000188-001/draft.json`: `c04bf42511759a5ec2c1bb85b863abc7912945136b0f20acca21979e8af19966`
- `.teacher/trials/guidance-9-001/run-000188-001/draft.md`: `9410205d80564ad15e19c6f56982e78106a0c0fd838c9073269a1f21c6ad177b`
- `.teacher/trials/guidance-9-001/run-000188-001/provenance.json`: `ca592856cbadc4153ec4351e578d1dde3e1615950dec3f7c878b9ac281fc548f`
- `.teacher/trials/guidance-9-001/run-000188-001/raw-transcript.json`: `fb87cf3d8cbdd185fca7a4e0e459360305eb8caab4b8da752880fc6989ff2a93`
- `.teacher/trials/guidance-9-001/run-000188-001/token-usage.json`: `13804ab9512f9bdfe065341ea0c84218c7f3c7ade59e7a74a4950100c078684e`
- `.teacher/trials/guidance-9-001/run-000189-001/coverage.json`: `d2a4719cc3bbbb90dd522804a09472edca71ae3728aa1a37994aec94c54be6f4`
- `.teacher/trials/guidance-9-001/run-000189-001/draft.json`: `4004fd0e65f36d4c280d0144729a037eb910174bcfcf568a5e8f3c37a0d0c51b`
- `.teacher/trials/guidance-9-001/run-000189-001/draft.md`: `a9aeec59a7409681d7ebda11c3204637ffd8763c00bc5626cea8669ad703ed56`
- `.teacher/trials/guidance-9-001/run-000189-001/provenance.json`: `3142734be724ec898d77d479ca0c7c14c5bf08f1480aec138aa9a2c4f213f64b`
- `.teacher/trials/guidance-9-001/run-000189-001/raw-transcript.json`: `a74557f3e80f6211298f8ae494e4f21e4b0e0ea03ddca5e5d2430fe2a544728f`
- `.teacher/trials/guidance-9-001/run-000189-001/token-usage.json`: `6b75af0be6fd70f4916729d6f89f1d6118be08a4a91f4412bc447b811b8198d6`
- `.teacher/trials/guidance-9-001/run-000190-001/coverage.json`: `4fb02cd6eb26f6bf456e6589a614720f817c99f7908409d03d57c6dc2c386e57`
- `.teacher/trials/guidance-9-001/run-000190-001/draft.json`: `abab35856244830f4980ead9b12c2ebbbe596a2d904ae0c1e0566dee7d358402`
- `.teacher/trials/guidance-9-001/run-000190-001/draft.md`: `f0818187ca8f092fac0f71861ce2b01448896c823e706d3984251e61a1571c39`
- `.teacher/trials/guidance-9-001/run-000190-001/provenance.json`: `b73e5cf5d3028e5a50ac51083fc97523d48a60736b1e02e4f347697ae3fa0743`
- `.teacher/trials/guidance-9-001/run-000190-001/raw-transcript.json`: `de99547c65caa30c520673d30c8822f8598c3249adfe602a1af0a9f53cc62b88`
- `.teacher/trials/guidance-9-001/run-000190-001/token-usage.json`: `cf8b600ca8530884508f187ea5f586c0c43577c223906376f4a03f5b53cdc0ce`
- `.teacher/trials/guidance-9-001/walk-after.json`: `1fc76c5f2a85c5dde6eb116611bde1327761c2dd7a60bb520e334dbb3a609694`
- `.teacher/trials/guidance-9-001/walk-before.json`: `1fc76c5f2a85c5dde6eb116611bde1327761c2dd7a60bb520e334dbb3a609694`
- `reports/guidance-9-trial-001.json`: `3f8e7a6c603a09aa20de8781d132920a50a440a22f9529a73392e3050d6aaf3a`
- `reports/guidance-9-trial-supervisor-001.py`: `1ee9d0ebff64b807e688ed10c9c5263c16b3ccb476a73e341f04659c7a5313ad`
- `reports/guidance-9-trial-validation-001.json`: `3ec137999881237376ad6e9547dc4b14d36ef5135efab7bf6ac4b794357d374c`
- `reviews/verdicts/guidance-9-implementation-001.md`: `7c57c8c7bd79414079cd371945b13f8d43e632c728b07fa9aa6269f421c81a0c`
- `reviews/verdicts/guidance-9-trial.decision.md`: `ba117a6eebe3c2d002ef2cf722de75d632b653f346f72c7db52336b121025373`
