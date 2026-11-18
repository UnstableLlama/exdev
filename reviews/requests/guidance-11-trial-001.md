# Guidance 11 trial 001 — assessment request

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: assessment of six unpublished trials only; no ancestor approval or adoption. Walk default remains guidance 9.

Six fresh unassisted sessions used original approved cutoff packets, changing only guidance_version from 9 to 11. No reviewer pass criteria, ledger notes, coverage hints or processor-metadata backfill reached these sessions. All trials remain under `.teacher/trials/guidance-11-001/`; none is approved or eligible as ancestor context. Before/after snapshots confirm unchanged walk files (content and modes), journal runs and approved entries. No implementation change since the accepted gate; its 282-test result remains applicable.

Preflight confirmed bound and hash-verified headers in all targets, specifically Gemma3 references at 225 and both Mistral3 repositories at 234. The source/trial manifests and artifact hashes below were rechecked at filing.

## Observations for independent assessment

- 213 reads two headers and describes Q/K/V biases and unused `model.mtp_layers.0` tensors, with explicit attention/MLP dimensions. Sampling is not complete checkpoint equivalence.
- 214 establishes unprefixed names and sampled dimensions but does not explicitly establish absence of a stored output head. It mentions the output-head name and embedding alternative; this remains a gap against the proposed criterion.
- 225 describes tower tensors and projector dimensions 1152 by 2560/3840/5376, connecting input-by-output storage to `transposed_load=False`. Coverage is sampled, not every layer or quantized variant.
- 234 reads the Base vision/projector header and establishes 5120 projector width. It retains the resize overflow finding. It does not inspect every language shard; the original missing processor evidence remains missing.
- Controls 229 and 231 introduce no architecture/header claims. 229 has no finding; 231 retains the scalar resize-bound finding. Prose and tool paths vary, so this is not a claim of identical output.

These are source/header observations, not executed model equivalence. The wording was written with the four targets in view, and only one trial per position was run. Independent review should decide the result; adoption remains the user’s decision.

## Proposed paragraph F (verbatim)

> When the task adds or changes a model architecture, or code that names checkpoint tensors or depends on their
> shapes or orientation, and tensor headers for reference checkpoints are listed in the evidence index, read the
> headers of at least one reference checkpoint for each distinct configuration. Say which tensor names and shapes
> the changed code relies on and whether each exists with that shape, and name any stored tensors the code never
> reads. Do not describe tensor layout as unestablished while headers are available and unread.

## Usage comparison

Token columns are cumulative final transport-event totals (cached input is included in input), not context length or billed cost. Historical approved runs did not retain token events, so their token counts are unavailable; no estimate is substituted. Full tool breakdowns and coverage are in the report.

| Position | Approved calls | Trial calls | Header calls | Trial input | Cached input | Output | Approved tokens |
|---|---:|---:|---:|---:|---:|---:|---|
| 213 | 25 | 29 | 2 | 1597175 | 1513728 | 4063 | unavailable |
| 214 | 19 | 18 | 2 | 874379 | 812544 | 3084 | unavailable |
| 225 | 31 | 50 | 5 | 4345714 | 4192640 | 8263 | unavailable |
| 234 | 35 | 39 | 1 | 2993862 | 2888192 | 6423 | unavailable |
| 229 | 6 | 7 | 0 | 219267 | 185472 | 1486 | unavailable |
| 231 | 7 | 6 | 0 | 181089 | 153472 | 1818 | unavailable |

Total calls: 149 trial versus 123 approved (+26, 21.1%).

## Verified artifacts

| Path | SHA-256 |
|---|---|
| `reports/guidance-11-trial-001.json` | `307451466ebe9abff65d80b0fad7553a209646c97c71b7a05f0bfa34781bb728` |
| `reports/guidance-11-preflight-001.json` | `3de9afe471784c434cf3f2c6301df4d75535578b5c0ff5e210a202d80b71db89` |
| `reports/guidance-11-trial-supervisor-001.py` | `8d6e8a7e248f99ca088db939660429cc904d6bb9611764870c025731a5b64d33` |
| `reviews/verdicts/guidance-11-trial.decision.md` | `9caadd17b4d29ae33e582d088dcb1fee6aa3d437decb6425ca9e7fa1616de4a5` |
| `reviews/verdicts/guidance-11-implementation-001.md` | `fe9a73d6ace193d163b3773844e4343581414eb3739c0e7516b9b13afd48b24b` |
| `.teacher/trials/guidance-11-001/walk-before.json` | `d9b5a3253348700aff78e6b8b2edb5be06ffa9c118ab48715b0767b9c5f24674` |
| `.teacher/trials/guidance-11-001/walk-after.json` | `d9b5a3253348700aff78e6b8b2edb5be06ffa9c118ab48715b0767b9c5f24674` |
| `.teacher/retrieval/000213-001/manifest.json` | `17b14e2052cbbb562636c4590d5184b59272f1fef5dd89e3619c7dd32693ff49` |
| `.teacher/trials/guidance-11-001/packet-000213/manifest.json` | `341996d2ecfebf4c674484424ae3884ef7c71bf711b9beb848a784c1e5f613fb` |
| `.teacher/trials/guidance-11-001/run-000213-001/draft.json` | `a3229380a3736fe27e883b4baec71ea31273f3d91f47de8d6f2bd36fec7c0754` |
| `.teacher/trials/guidance-11-001/run-000213-001/draft.md` | `d2e493b63651786f6dbeca332e5c2875890cb9f3048494178d7d23809ae22107` |
| `.teacher/trials/guidance-11-001/run-000213-001/raw-transcript.json` | `3dc945ec00e4ac36d29c2fbda010b4bf64aebce3182e6665b653bd4b06a76f26` |
| `.teacher/trials/guidance-11-001/run-000213-001/coverage.json` | `473a6e7b86534c3f0a3c9729f46bc91d277c88976a6f731227fa50c6470e2fd9` |
| `.teacher/trials/guidance-11-001/run-000213-001/provenance.json` | `2994f8f571302232df276e85f8a3a5bee67ceeb1d7a44f9e83992e3ff3445587` |
| `.teacher/runs/commit-000213-001/draft.json` | `25282e819d73d20e3e528e06e27e0f7b56b613de90d8c2b46176124a1d3e329b` |
| `.teacher/runs/commit-000213-001/draft.md` | `e3ef61d33d3e60bc3194e428e8ab7f01a2974bf44dde44e0ec3fe72ac929c68e` |
| `.teacher/runs/commit-000213-001/raw-transcript.json` | `5be1fd9c82841211f17385a1d218c41f7ce8fc8f8d9c48feee10c98e8cbbd690` |
| `.teacher/runs/commit-000213-001/coverage.json` | `fcafd646a84af5c0a58555e19fb3c245e53f5e57a9cac9864789e27a8686f5af` |
| `.teacher/runs/commit-000213-001/provenance.json` | `b5b79829dc05f959913f0519f62f77a9df9a93b9bb838f879f4d918fc18521a9` |
| `.teacher/trials/guidance-11-001/run-000213-001/token-usage.json` | `ee6a2f5b37e66938590984520322272e86bf651db7a939cc24e2f99b8da839d5` |
| `.teacher/retrieval/000214-001/manifest.json` | `5ce1579eb29f513e291457602a2f65a989d860d02f0747176f85c08c61de63ef` |
| `.teacher/trials/guidance-11-001/packet-000214/manifest.json` | `ade6f86d4b2b52fcfa5edec2ad3e0bc71c9b569546705457fbf655635c02a37e` |
| `.teacher/trials/guidance-11-001/run-000214-001/draft.json` | `4ffdb9cd22c0a4b25a81f6952f1b3b346d7382b69d95e6a7e9cf7b81c1c00f08` |
| `.teacher/trials/guidance-11-001/run-000214-001/draft.md` | `43d0d12c23bc33f4331e0581c09ec9b2d28d0b86ae88d45dde053f3ed061e071` |
| `.teacher/trials/guidance-11-001/run-000214-001/raw-transcript.json` | `9f5b991531ebdedffa241130aa3cdcdccaa53233f0a7c881bdfa6a3da3b3b4d7` |
| `.teacher/trials/guidance-11-001/run-000214-001/coverage.json` | `4fb31b7d50f52d507d295081645458c3db926954c7b590122496404d7cf8687a` |
| `.teacher/trials/guidance-11-001/run-000214-001/provenance.json` | `47876b9dabdc33afa82c3349fe03cd5655177ceac2909d9607923c04d16fa329` |
| `.teacher/runs/commit-000214-001/draft.json` | `fd83770d4fc4fdf5d7003752bf4dead4459620bfc611b9ab33976cf6099057a1` |
| `.teacher/runs/commit-000214-001/draft.md` | `310b5724c8948aef0f33f7668f6a8aff4955bc28280291f78121cdd6c4b4ac84` |
| `.teacher/runs/commit-000214-001/raw-transcript.json` | `78dc1622d9460e5c89a43df643ef37f7c6dda686e326f3a5ec60e7455d8d4180` |
| `.teacher/runs/commit-000214-001/coverage.json` | `320ca04a3d76b57971e5bf39d33d6f53b69f167e7088a481d2ec451497230516` |
| `.teacher/runs/commit-000214-001/provenance.json` | `e9717264ff63949040e77be529c7344881fbb1d51b047c88c3f40ca877701421` |
| `.teacher/trials/guidance-11-001/run-000214-001/token-usage.json` | `36f5251db2e8542e498ddd3b5e27520de312af756ccdd2cb73f1fd951d29c8dc` |
| `.teacher/retrieval/000225-001/manifest.json` | `7ae08616390ccdb9caf3e930ce0caf8e1b607e6f2f73a473076ff9f8ebb8c668` |
| `.teacher/trials/guidance-11-001/packet-000225/manifest.json` | `ba4cf9bb16e9104df638424443f43084608dfb08a2239cb41f01de1fd7bb791b` |
| `.teacher/trials/guidance-11-001/run-000225-001/draft.json` | `d7fffc951aae1b43569036fdaf7935a43353abad1ba9d9ed8c436a47501d1503` |
| `.teacher/trials/guidance-11-001/run-000225-001/draft.md` | `d490e911c7e3d25867256a673fba7b178a97148b3ff6a4efd31fefc3056e5011` |
| `.teacher/trials/guidance-11-001/run-000225-001/raw-transcript.json` | `9f2db2bd050512d0c9bc6ae6ca200f90dfa0f087aa4b17d965c397fc93418813` |
| `.teacher/trials/guidance-11-001/run-000225-001/coverage.json` | `f6b5375fdc5234d94057f76d0232ea454421055efb4a6a93ef33dc2f1fa48fda` |
| `.teacher/trials/guidance-11-001/run-000225-001/provenance.json` | `93e9230d021ffc9f5d28d30e91a02dba95a193d688d08bef095a1560f2dbd99f` |
| `.teacher/runs/commit-000225-001/draft.json` | `24788f44fc28ff2f427f05a1a6436f4d8e9bff1795305bfb8f508d5d325c9070` |
| `.teacher/runs/commit-000225-001/draft.md` | `ffdb90a3c9d3ef1664f5ff3065fe5b75174fbc54d115aaf61690621529a5873f` |
| `.teacher/runs/commit-000225-001/raw-transcript.json` | `30d266e44bcd9eac783eb2692b57658343455bf97589fd6a93a7e1d11db7254a` |
| `.teacher/runs/commit-000225-001/coverage.json` | `cd020c3496188301987a3a5996a2671e744076ff4e9984b42d9b2c3a0c62a848` |
| `.teacher/runs/commit-000225-001/provenance.json` | `1215a0073c135a39a3f3e95883a5bcedea2e6615f370001187765cde68621707` |
| `.teacher/trials/guidance-11-001/run-000225-001/token-usage.json` | `629757b5526cd6279cbea8489dc280b710aa09d63c30f2e71838df7d975fcef5` |
| `.teacher/retrieval/000234-001/manifest.json` | `9922afb48d86d8895dabe708e67eca7d00cbc5e7891050e42496f26344be43d2` |
| `.teacher/trials/guidance-11-001/packet-000234/manifest.json` | `101e7a6378ba5c0b1a4b2e27f57db237415845a19492f68fa7cf8a2ee1637dc1` |
| `.teacher/trials/guidance-11-001/run-000234-001/draft.json` | `55615b2857b6afc7a731d2d07b30c1e0330c846111cf481e73215595d66fff77` |
| `.teacher/trials/guidance-11-001/run-000234-001/draft.md` | `4fbaa6f63666425e75a12280849ef511baa2b0cf253a91b8cef1189993bc64e3` |
| `.teacher/trials/guidance-11-001/run-000234-001/raw-transcript.json` | `c1e5cf9d05120b879085c413d137418276779fae1960922cefe8f69e0028b154` |
| `.teacher/trials/guidance-11-001/run-000234-001/coverage.json` | `4dabee9033eb742922e9b617653062e1c4a52731e3b3f71c9d209099f23f6bdd` |
| `.teacher/trials/guidance-11-001/run-000234-001/provenance.json` | `092aac20c134236cbe08f0e0f2aa0b7cc1130b7d030566b0311c969610cb62f4` |
| `.teacher/runs/commit-000234-001/draft.json` | `0b3d02722fd4fe928fd64a2e5413d0bd296df32d5bb40e0208f31d909d06e43a` |
| `.teacher/runs/commit-000234-001/draft.md` | `0c9f0933ea292ff1ea8966820615416c03868f8888ae7b7dbc281ec6d0efe612` |
| `.teacher/runs/commit-000234-001/raw-transcript.json` | `063a9a2504553a3cb4a676650282dfb5e4f17d6600dc78fb8a490520ecdbf7b2` |
| `.teacher/runs/commit-000234-001/coverage.json` | `a3a5f913cc1483fe36f31c7c6b479cea7f2278d55ed3b1403436acc01e05d898` |
| `.teacher/runs/commit-000234-001/provenance.json` | `4ef0db73011fa2293e447bf8d038717f52ebed3c73c3113dc7d25c0603858161` |
| `.teacher/trials/guidance-11-001/run-000234-001/token-usage.json` | `07a646b1b843a8803a40dbfc2fd6926c3c14c4618aca7c1ea1eca45cc8b950cf` |
| `.teacher/retrieval/000229-001/manifest.json` | `af05a51a1e669c4479007aa354b22f11960c691c14ad25d0fe693e1af793cefb` |
| `.teacher/trials/guidance-11-001/packet-000229/manifest.json` | `cdef749fa496cb4d8a36549af0376c13d5aa2d072cca245170f592f5d95ad65a` |
| `.teacher/trials/guidance-11-001/run-000229-001/draft.json` | `4c224eb893ae6a2ed14efefc1eae5b6bbc0dc1eca0c8c065165f93e2e760c1c0` |
| `.teacher/trials/guidance-11-001/run-000229-001/draft.md` | `7971139f8be7264ece6a023dd51c8da08659a7e77412b7ad838115d83225671a` |
| `.teacher/trials/guidance-11-001/run-000229-001/raw-transcript.json` | `7ff411aff48d5105a5453bdb03fb4efad061a229b5584aa2bbf83f921f09549d` |
| `.teacher/trials/guidance-11-001/run-000229-001/coverage.json` | `4c154e122c09c349cb5f32bf88519edd10edc314c3d826776c2a7de5b85e31da` |
| `.teacher/trials/guidance-11-001/run-000229-001/provenance.json` | `51facba48fa2310beeae9733449e537872d5ea58eece2cb1f9ab006d07e63c47` |
| `.teacher/runs/commit-000229-001/draft.json` | `560cd4b88148abb4d869a2b2ac020a62a66ab43cfe148c9fe008dc1f89115be8` |
| `.teacher/runs/commit-000229-001/draft.md` | `27a351742da0403bb9b487baa385a8cb6b164d2a1f92b9658b7c6142bbad38c7` |
| `.teacher/runs/commit-000229-001/raw-transcript.json` | `6d6eea009e3d848ded9a551ae3ed7c5fa05a41b3742565f5119a47b1b8d9c112` |
| `.teacher/runs/commit-000229-001/coverage.json` | `a2739143eaa796f91839e1dc72969289243a5d2a6712ffa1168a29a12653f4ab` |
| `.teacher/runs/commit-000229-001/provenance.json` | `b9f8f9bf79b7c3f744ecb69b67fbd98b2751a75745332b05311806a111a7066e` |
| `.teacher/trials/guidance-11-001/run-000229-001/token-usage.json` | `124bb949fc657876396481f77294b32ee40584fad0cc374a2594a0f12aaeb444` |
| `.teacher/retrieval/000231-001/manifest.json` | `7aec3619261d58d734eb2e61ba236a40069925d78f90917c92b96a6f0d5f941a` |
| `.teacher/trials/guidance-11-001/packet-000231/manifest.json` | `d216b730cde480c89f966915b666f111a1d782053dfd5df38b4f24a96cd39e71` |
| `.teacher/trials/guidance-11-001/run-000231-001/draft.json` | `3b6cbe6df7b9fd6170b4ed423050fea81000622ed7cad561c3803a009f04915d` |
| `.teacher/trials/guidance-11-001/run-000231-001/draft.md` | `116a55f4e4ce8c526033c4ab6ea3263ca02041d8f5b48c400310a52df32bc4d6` |
| `.teacher/trials/guidance-11-001/run-000231-001/raw-transcript.json` | `bccc21a42034eb57c8f859fb352c696874eff4fdf6e4b8405442156851063c82` |
| `.teacher/trials/guidance-11-001/run-000231-001/coverage.json` | `5cabe0f8f63f4b9df07be01e23dafe70e8f7a6448c9ef39be638b20cd65ea283` |
| `.teacher/trials/guidance-11-001/run-000231-001/provenance.json` | `951616f1095f749089ac6bbad45726acc20bcc6486b29bc900f9f6f7bdfd5e49` |
| `.teacher/runs/commit-000231-001/draft.json` | `00f4a6d598335f9abaf67da5030281abdbe3eac2a8bdb5408455764f14e27d9b` |
| `.teacher/runs/commit-000231-001/draft.md` | `fca5772adc8841f21d40fc04078be399919c517914d9038863b32b9044492134` |
| `.teacher/runs/commit-000231-001/raw-transcript.json` | `9cadcee31a5a753ee3d4495c3bee98a54131a0ecd47ae9da5211cd2c743eebff` |
| `.teacher/runs/commit-000231-001/coverage.json` | `f6fe5414c5d03838da381b13b758d04f824b60214f6bc04aaa00c66f3a2e285a` |
| `.teacher/runs/commit-000231-001/provenance.json` | `431743ff49ce2271724efe184cf2afd9f26d1b0088ade33129a6878bcc9d0a7d` |
| `.teacher/trials/guidance-11-001/run-000231-001/token-usage.json` | `f71e20a3d4da78a1d56a0906e20d27c15c8d0f945087c120e6680d123adf20a4` |
