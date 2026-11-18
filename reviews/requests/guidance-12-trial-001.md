# Guidance 12 trial 001 — assessment request

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Author/orchestrator: gpt-6.1-sol, medium. Trial teachers: gpt-6.1-sol, medium, guidance 12.
Requested scope: assessment only, no ancestor approval or adoption. Walk default stays 11; replacements remain paused.

Six fresh unassisted sessions used copies of the specified packets differing only in guidance_version. No reviewer criteria, verdicts or ledger material reached teachers. Each ran once under .teacher/trials/guidance-12-001/ using author() with the accepted Sol default. All six approval-gate rejection checks passed. Walk files, journal runs and approved-entry snapshots remained equal. No implementation change since the accepted gate (287 host-enabled tests).

## Side-by-side observations

| Position | Guidance 11 comparison | Guidance 12 result |
|---|---|---|
| 98 | QK-normalization finding; generic alternate-head loading | Retains QK finding, adds bitsandbytes-storage and inherited partial-RoPE findings. Explains primary/alternate loading and absent optional groups, but output-head absence is scoped to sampled Aya23-8B shards, not all checkpoints. |
| 103 | Architecture diagnostic and partial-frequency-read findings | Diagnostic remains a formal finding; partial-frequency concern remains in ancestor prose, not a formal finding. Explicitly disclaims global absence of lm_head/biases after representative-shard inspection. Generic fallback does not meet the requested complete absence/path account. |
| 110 | Accurate architecture account but omitted tied-head mechanism; replacement rejected | Complete 0.6B header, explicit head before embedding alternate, optional biases/EXL3 absent. Adds FP8-storage, architecture-diagnostic and asymmetric-norm-validation findings. Does not establish the checkpoint-by-checkpoint stored-head/fallback split. |
| 214 | Prefixless names and sampled dimensions; no explicit head absence | Complete Gemma3-1B header establishes absent lm_head and embedding alternative, absent biases/FP8 scales/EXL3 groups. MedGemma remains first-shard sampling with remaining shards/output-head behavior unverified. |
| 243 control | Shared-list duplication, missing ordinal return, inherited EOS filtering | Same three conditions under different labels; no new architecture/header claim. |
| 245 control | No findings | No findings; no new architecture/header claim. |

These are author observations for independent checking, not a passing verdict or execution-equivalence claim. Coverage improves unevenly; I do not claim the targets meet all criteria or retain every detail. The wording was written with these targets in view; one run each. Comparisons 98 and 214 change both Astra to Sol and wording. The report calls its baseline field approved_metrics, but 110/002 is a rejected replacement and 214 is an unpublished guidance-11 trial, not approved production prose.

## Calls and tokens

Final cumulative transport-event totals; cached input is included in input. These are not quota or billing measurements. Historical baseline totals are unavailable except 214; no estimates. Report contains per-tool counts, coverage and exact run paths for both sides.

| Position | G11 calls | G12 calls | G12 input | Cached input | Output | Total | G11 total |
|---|---:|---:|---:|---:|---:|---:|---:|
| 98 | 44 | 71 | 4942744 | 4819456 | 12730 | 4955474 | unavailable |
| 103 | 53 | 49 | 3500512 | 3388544 | 10088 | 3510600 | unavailable |
| 110 | 63 | 71 | 4817341 | 4687616 | 12869 | 4830210 | unavailable |
| 214 | 18 | 34 | 2454170 | 2336128 | 5282 | 2459452 | 877463 |
| 243 | 20 | 23 | 1001875 | 947072 | 5047 | 1006922 | unavailable |
| 245 | 20 | 17 | 797983 | 734336 | 2975 | 800958 | unavailable |

Calls: 218 → 265 (+47, 21.6%). Trial total tokens: 17563616.

## Verified artifacts

| Path | SHA-256 |
|---|---|
| `reports/guidance-12-trial-001.json` | `b154f96b83e7a850e77f75a2948adf734961a9b212d8ceb84e3d675f6aa438d1` |
| `reports/guidance-12-trial-supervisor-001.py` | `f6716902bf9663896ae818391cd929b625458530f7d0491f842e2672cf3c7841` |
| `reviews/verdicts/guidance-12-trial.decision.md` | `f4b5a7d2c30dc4d67d656caa25a5aeec9007ea300bf79b3e5ff8f5d835ea9ece` |
| `reviews/verdicts/guidance-12-implementation-001.md` | `2ee45e2c257c7e3d0e4b9f52170d8b93e68d4daf9e0b1e20fbe09ebee68e2b58` |
| `.teacher/trials/guidance-12-001/walk-before.json` | `fcc483c1cd9b738c39a1dee2c1edd89eb68b9272a96ec1a78580c3b3d895e439` |
| `.teacher/trials/guidance-12-001/walk-after.json` | `fcc483c1cd9b738c39a1dee2c1edd89eb68b9272a96ec1a78580c3b3d895e439` |
| `.teacher/retrieval/000098-002/manifest.json` | `689f05c3c5ec59bb1409eb15077a4ccb9a483d2bae5cb5fb4e5640f5cc9a5bc8` |
| `.teacher/trials/guidance-12-001/packet-000098/manifest.json` | `b26373a3e36d442fbda90f4367b5a9d96e63b2669178804e540bb89cc25a0c0a` |
| `.teacher/trials/guidance-12-001/run-000098-001/draft.json` | `b0e68338638790fe7b8198799738a42d5fd6438fad0715c2c6530e72922e6ca0` |
| `.teacher/trials/guidance-12-001/run-000098-001/draft.md` | `4853d6a422e784c96a2f848091bf0d8ca01b56260b648e3db26ccbbe4b40bfd6` |
| `.teacher/trials/guidance-12-001/run-000098-001/raw-transcript.json` | `3253e02bd558952dde1ae5c2c5560bf18410b5eaf47b81970555118df65cbda8` |
| `.teacher/trials/guidance-12-001/run-000098-001/coverage.json` | `20e4817a79f1459e6d87660be8ea00ec8f878d233537e6079f37570997d6bbb3` |
| `.teacher/trials/guidance-12-001/run-000098-001/provenance.json` | `3e216ab977f82cd7f59b2739a6abcffa02a1f3f367ea96bbf3e4778ac7286eb2` |
| `.teacher/trials/guidance-12-001/run-000098-001/token-usage.json` | `cde893a61a3aa04e34d559f887d460b2fccbd975b20772b8167228b5fc249433` |
| `.teacher/runs/commit-000098-002/draft.json` | `d4c3ed86eb73f6f1575cf9952f7537282697777da4b8605b2d03008ddfb1628a` |
| `.teacher/runs/commit-000098-002/draft.md` | `5fbf8b7e0a26d77620ed890d734d64d2852dfbd862823918499573fa95dbbb1b` |
| `.teacher/runs/commit-000098-002/raw-transcript.json` | `f5b582e3487ef58382226f29c77ddd0a778ad21fd98cede7acde8487a96c5faa` |
| `.teacher/runs/commit-000098-002/coverage.json` | `e8eca53dee799ce8369237c96fd2a4fb2f5ce5245202c8648ba11ae36de31b69` |
| `.teacher/runs/commit-000098-002/provenance.json` | `fd6505ce693e4bc97f28cd49f1c4e4425da958a5e1cb6a45c675775b2a2cf719` |
| `.teacher/retrieval/000103-002/manifest.json` | `305ab6ff9b7d4003f82d658cbdb9c5233508c7b5682c051c5df282108647fdde` |
| `.teacher/trials/guidance-12-001/packet-000103/manifest.json` | `3241d55dca2c3cbf5b7385133a674576f1e2afc673bd64e24643bbbc7b458a8d` |
| `.teacher/trials/guidance-12-001/run-000103-001/draft.json` | `5711f891480acd216df10cb3ec585511131a0e5d6f671028bdf3391c7c85d5aa` |
| `.teacher/trials/guidance-12-001/run-000103-001/draft.md` | `93a37ee530ad2559aaec6c5e5c86d10bf7a68ff55b4703459c102ef139e26c40` |
| `.teacher/trials/guidance-12-001/run-000103-001/raw-transcript.json` | `47154a6c09d7f11d011e1edb661d9d552c99a73f98ff8474bf892aff47b22f41` |
| `.teacher/trials/guidance-12-001/run-000103-001/coverage.json` | `10d93cd4aac657e96c3975a3961b99350013def87b597b5d08f3ed7ec6e42ced` |
| `.teacher/trials/guidance-12-001/run-000103-001/provenance.json` | `33a4ffc45e829cd09f9a50a26a682cacbeb34b25ee2303c02ee16fd0c72be767` |
| `.teacher/trials/guidance-12-001/run-000103-001/token-usage.json` | `5631b5c63d3f292626c123a16a8bcae3346b3d99b7af70d0de23d2b829a53414` |
| `.teacher/runs/commit-000103-002/draft.json` | `4a5d8f0c1c54faa99abe044e1ceb25a243483a73bf189205d54b6f04e6360b33` |
| `.teacher/runs/commit-000103-002/draft.md` | `076795cca49a792617a14e87053643327514926642bad2f805794afa85d519a9` |
| `.teacher/runs/commit-000103-002/raw-transcript.json` | `099280d83c96885644a547605eebf5c90ae381f5bd2d92d4152bc48c38d31ce0` |
| `.teacher/runs/commit-000103-002/coverage.json` | `ba4f63fdcb86ddcb0ea94370468623ce26151b2331f37fe6cce2dc5ce5deb802` |
| `.teacher/runs/commit-000103-002/provenance.json` | `2a981f910c11a8468fc729990ecf50c81faea0cb017d6d2ffe802e5a5eb01e8f` |
| `.teacher/retrieval/000110-002/manifest.json` | `f422fc92772b0deaca973eb8cab374cc5faf41872536654d28a73db0ba5c3a30` |
| `.teacher/trials/guidance-12-001/packet-000110/manifest.json` | `39f622b14e79fc079434e236b420d568ae738e106856858ffe23686a4560cf33` |
| `.teacher/trials/guidance-12-001/run-000110-001/draft.json` | `afc80c6e2a56c421ba665d8912043ff15e5a4689507eae590d4bb26e1c551506` |
| `.teacher/trials/guidance-12-001/run-000110-001/draft.md` | `d4de7e96487bcadd7c81ccf04b273b4963579ffa27a92594677de10b6a251846` |
| `.teacher/trials/guidance-12-001/run-000110-001/raw-transcript.json` | `55bb8126227a77b71fdf78ed782be949f8390c2c119374e48d56b93bea904589` |
| `.teacher/trials/guidance-12-001/run-000110-001/coverage.json` | `16ed1e5f6723f3da2c17ea79d057057f9559c84ebf78c8253110497cd44fbbc4` |
| `.teacher/trials/guidance-12-001/run-000110-001/provenance.json` | `dca4670925d6f3b72aa6ec1f149154c3ad95ec468798bd4b2ce5a961c9213f16` |
| `.teacher/trials/guidance-12-001/run-000110-001/token-usage.json` | `8237eb07205bd01a93c1268c4c5fb971fdfeb788aba29c9ca22ca802425b73ed` |
| `.teacher/runs/commit-000110-002/draft.json` | `c2cf623a6bba875e5aff9cd878b7897c4184161c43bf551bb914aa062c068759` |
| `.teacher/runs/commit-000110-002/draft.md` | `a9eef1f37fe9bc456c75b9158069821848736131c2c4e67d26ab1a5e14d49827` |
| `.teacher/runs/commit-000110-002/raw-transcript.json` | `d0ca148c9c460f0331e28102261cdcfc683dd675dbdac16161ce1df1c035106d` |
| `.teacher/runs/commit-000110-002/coverage.json` | `f273fd093da756d1dec60aebf40f542d46ead7a395188261275b2310735a2c11` |
| `.teacher/runs/commit-000110-002/provenance.json` | `bb9a9d991496077ac639051a08fdbbd1728609ed572922013204a3424713af16` |
| `.teacher/trials/guidance-11-001/packet-000214/manifest.json` | `ade6f86d4b2b52fcfa5edec2ad3e0bc71c9b569546705457fbf655635c02a37e` |
| `.teacher/trials/guidance-12-001/packet-000214/manifest.json` | `c11586656e2e3745f140fb2960a77816a216f8ae1664618be7d9719c1f085cd1` |
| `.teacher/trials/guidance-12-001/run-000214-001/draft.json` | `812b013bb3463bcc29698427297dacb47cdc50aeb25c871495e6a5d7ad370cd3` |
| `.teacher/trials/guidance-12-001/run-000214-001/draft.md` | `af5475dcc1bc0d77a88e25d678179676c7aecbb54d4b575ae3867774df946533` |
| `.teacher/trials/guidance-12-001/run-000214-001/raw-transcript.json` | `7075d9e383d55100677f896d3bcabe32ac7f739280d8313c3edd92e9b643f412` |
| `.teacher/trials/guidance-12-001/run-000214-001/coverage.json` | `e338b28485af434a7c122bba9b6364a07077a18f4f1e7068a9d23b4aa1239c4e` |
| `.teacher/trials/guidance-12-001/run-000214-001/provenance.json` | `eaa57d3d6f6842476acd66004050fb3d20106840217864c108a6b50a0708915e` |
| `.teacher/trials/guidance-12-001/run-000214-001/token-usage.json` | `5575c9ddb323942a7b81b634cc4130bc38b9cba496bf1bfa817b770ef055adf4` |
| `.teacher/trials/guidance-11-001/run-000214-001/draft.json` | `4ffdb9cd22c0a4b25a81f6952f1b3b346d7382b69d95e6a7e9cf7b81c1c00f08` |
| `.teacher/trials/guidance-11-001/run-000214-001/draft.md` | `43d0d12c23bc33f4331e0581c09ec9b2d28d0b86ae88d45dde053f3ed061e071` |
| `.teacher/trials/guidance-11-001/run-000214-001/raw-transcript.json` | `9f5b991531ebdedffa241130aa3cdcdccaa53233f0a7c881bdfa6a3da3b3b4d7` |
| `.teacher/trials/guidance-11-001/run-000214-001/coverage.json` | `4fb31b7d50f52d507d295081645458c3db926954c7b590122496404d7cf8687a` |
| `.teacher/trials/guidance-11-001/run-000214-001/provenance.json` | `47876b9dabdc33afa82c3349fe03cd5655177ceac2909d9607923c04d16fa329` |
| `.teacher/trials/guidance-11-001/run-000214-001/token-usage.json` | `36f5251db2e8542e498ddd3b5e27520de312af756ccdd2cb73f1fd951d29c8dc` |
| `.teacher/retrieval/000243-001/manifest.json` | `358dd527e1f474c8be418b63615144dc3bad5ff7bd7979927640768959de74c3` |
| `.teacher/trials/guidance-12-001/packet-000243/manifest.json` | `616c1f4e555d950a4712240158efafe441c870ba51c695f4e15f3b64d71861f5` |
| `.teacher/trials/guidance-12-001/run-000243-001/draft.json` | `40a75e0ee53267596180b590260ee24e60c8dadd8824398a9908e259ca5d7d86` |
| `.teacher/trials/guidance-12-001/run-000243-001/draft.md` | `c46ce8da2e9edbdc1a877185aa773605f2f11c20c3d4e4e3d7db61ddd57587e7` |
| `.teacher/trials/guidance-12-001/run-000243-001/raw-transcript.json` | `ae65f228a443f79a215b830d26cbd715722e369afc11d67551e22372ba64a04c` |
| `.teacher/trials/guidance-12-001/run-000243-001/coverage.json` | `af9eb695db7c47a934d1e33aaea2126504e1597b24797771d7b5628f0f79c7cb` |
| `.teacher/trials/guidance-12-001/run-000243-001/provenance.json` | `1b811e0226b194da392e41a55998fcde88d0b02654a14b252e2263c210ec4407` |
| `.teacher/trials/guidance-12-001/run-000243-001/token-usage.json` | `57f3a841154b818d468ddf148cb2a9f9bc1b361f33049f2a8145de128ca3cd86` |
| `.teacher/runs/commit-000243-001/draft.json` | `36fae9d849e8d0a5c840f5d8e85e3891b930694ac2b443d9cf639450714f5fce` |
| `.teacher/runs/commit-000243-001/draft.md` | `f479daae45f64e985b8f28425b98cd12e1d54fae9a6b8551369c534b55c1bbec` |
| `.teacher/runs/commit-000243-001/raw-transcript.json` | `6c9cfcccbe839a57b1239cf057a1641cd6d1c31b9bdc7cca2eee2cce005d4697` |
| `.teacher/runs/commit-000243-001/coverage.json` | `ba69823e6e143835f0850f8476115966ae956a986cab7c230d76ff92026ac368` |
| `.teacher/runs/commit-000243-001/provenance.json` | `8c5fe502dec8d30b6d2c1ce6e29dfca04ec0b70a2a4a487ec0cc7f22fb159934` |
| `.teacher/retrieval/000245-001/manifest.json` | `e18c1d1412a429b5897db13e87ddc0169ef1bafdffb54a13988f0254219c12cd` |
| `.teacher/trials/guidance-12-001/packet-000245/manifest.json` | `d22ca626a2a0ee76659da7e9917710dd99e55b02bec10782dbc7acb55f8314be` |
| `.teacher/trials/guidance-12-001/run-000245-001/draft.json` | `d112c879a380de796bafb9fcb6b45d4db96ab376137c30399d242dd201049866` |
| `.teacher/trials/guidance-12-001/run-000245-001/draft.md` | `6a05d68f9781cd13883ab97424902b9e37783dcbfd24a96385fc1664af0517af` |
| `.teacher/trials/guidance-12-001/run-000245-001/raw-transcript.json` | `ca8979fd84e0bb1d42d1ebb3c5701c71477840e95740e18e20b3faa03804d7d6` |
| `.teacher/trials/guidance-12-001/run-000245-001/coverage.json` | `ff597a7647488a376bcb2d7bf0a8be9e7306d86bf62a8896c25b0ab5009a0f55` |
| `.teacher/trials/guidance-12-001/run-000245-001/provenance.json` | `3f3104760d0be94dcb5011e2e9d95bca0dd8a3e95f8cffdd827d3f6f0badcf84` |
| `.teacher/trials/guidance-12-001/run-000245-001/token-usage.json` | `7fc1443d655ff04618464f42ef7fb0ce4b5ac1864c54816746cbf4c24b25adcb` |
| `.teacher/runs/commit-000245-001/draft.json` | `5e685f8b95deb34e150887b3e6e30e3552c3b29261f4d33bfe0b9decba6ee2f7` |
| `.teacher/runs/commit-000245-001/draft.md` | `6f2de106b559d3fbfd52297bedc36b6f1c4dc98966382f9e5104eaa50ca2f9f7` |
| `.teacher/runs/commit-000245-001/raw-transcript.json` | `3b0eee0f3fca83b86d0080c29c326cc7a4f29251e102af926d8429da254f9525` |
| `.teacher/runs/commit-000245-001/coverage.json` | `b3b05ef6b63d5a761e026c2305e40c8e2f7d34bb5c760f0cad365adc1b41cf31` |
| `.teacher/runs/commit-000245-001/provenance.json` | `4fb435bd88770256b187574b0bb47c970c330e40c617f3275c62f8f7f5276dc6` |
