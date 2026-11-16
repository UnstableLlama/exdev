# Review request: guidance-8-trial-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Four fresh unassisted guidance-8 trial sessions completed at 154, 140, 157 and 156, one invocation each, no retries. This requests trial assessment only, not approval of these outputs for ancestor retrieval, canonical use or training, and not adoption. The walk stays on guidance 7.

Each scratch packet under .teacher/trials/guidance-8-001 uses the approved run's original packet with only guidance_version changed from 5 to 8. Cutoff evidence and ancestor selection are unchanged. No coverage requests, verdict text, ledger material or reviewer pass criteria were supplied. Consequently the comparison with historical approved runs includes the three adopted paragraphs as well as the new fourth paragraph; it does not isolate paragraph D against guidance 7.

Both snapshots of .teacher/retrieval and .teacher/runs (hashes and modes), and journal runs/approved_entries, are identical. The trials are not journal attempts, have no ancestor approval and were not published. The 176 approval was held outside these snapshots until trial completion. Token capture is an administrative transport observer of existing thread/tokenUsage/updated events; it changes no sends, model settings or teacher inputs.

| Position | Trial / baseline calls | Input tokens | Cached input | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|
| 154 | 23 / 9 | 1091585 | 1022848 | 3619 | 1095204 |
| 140 | 23 / 17 | 881829 | 826368 | 4376 | 886205 |
| 157 | 22 / 14 | 1217334 | 1116928 | 2933 | 1220267 |
| 156 | 6 / 4 | 172609 | 143488 | 1691 | 174300 |

Counts use the final cumulative usage event, not the sum of cumulative events. Cached input is a subset of input. Historical baseline token usage was not retained; no token-cost ratio is claimed. Each session is one app-server turn/start, not one inference step. Tool counts total 74 versus 44 baseline (about 68% more); per-tool counts and raw usage events are in the report. All four read their sole task section fully.

154 reports the omitted sliced-module deferral guard and retains the perplexity-axis finding. 140 reports the missing exception abort, inherited BF16 odd tail and inherited single-device progress behavior. The two controls report no findings: 157 describes the additional close and its preconditions without claiming measured handle savings; 156 describes color tags and grouping. These are the trial drafts' observations submitted for independent assessment, not findings approved by this request.

Execution is limited to scalar transcriptions at 154, 140 and 156; 157 executes no run tool. No model, GPU, native loader or plotting execution occurred. Drafts retain their individual limits. No teacher statement reports inability to follow instructions with available tools. Exact replay validation is recorded separately; no teacher was rerun for validation.

## SHA256

- `.teacher/retrieval/000140-001/manifest.json`: `a7bc1946b75d332414db6af598d73f79d9718a2b40ffdc2b270a7d3c334ee455`
- `.teacher/retrieval/000154-001/manifest.json`: `c06e896d5d0731942d632e6106a62d16486ab3a751faa152b00dce382bbfbad6`
- `.teacher/retrieval/000156-001/manifest.json`: `9ef102baa97fb412b9dd94e33f95584866ae8d9bcd4fc036c542997c83666152`
- `.teacher/retrieval/000157-001/manifest.json`: `4a9d24c594fcc3e2e34c4413cc8090689c9a97c11084c6f6155c50219a0ec70f`
- `.teacher/runs/commit-000140-001/coverage.json`: `693229d655e3a44e45560b7cc0e064a25f647bf808c0ffc014d85d3f0ef3938a`
- `.teacher/runs/commit-000140-001/draft.json`: `73c6cfb246e2f136326a7c6a44638aee140731867aa4867cd7c9473fd2088427`
- `.teacher/runs/commit-000140-001/draft.md`: `71ba60e88e6b75e9725e22476a715a1669aece103c1a8bb1c90f6c45de833a3b`
- `.teacher/runs/commit-000140-001/provenance.json`: `ab1ec8d2a8b94af897ef152a4f7bac62e0ff1d06c5fe1a30d0020bb80b04e777`
- `.teacher/runs/commit-000140-001/raw-transcript.json`: `442bc674e5b63b37010a48efe55b23b9c49d90471739dd0647968c91e0fc7b3a`
- `.teacher/runs/commit-000154-001/coverage.json`: `c12f304cc98f5f7b106f33118b93a456f4b42d2813e38c57da0d40df7fb9ce13`
- `.teacher/runs/commit-000154-001/draft.json`: `000c24dbbedd9cae94c72b9de9e9c728ef54b7e56a03e5d8eab176a3f7a56825`
- `.teacher/runs/commit-000154-001/draft.md`: `6e4e4a44e2e0fc071881be788f909f9c5966fa5c5088bab96b3583ee9de1c9f5`
- `.teacher/runs/commit-000154-001/provenance.json`: `7daa8a8e966d85a07b1e437ccd0b2c20b9bd10387532e97a5213b1a773eb8d73`
- `.teacher/runs/commit-000154-001/raw-transcript.json`: `6e1fe2943781e7df874451f185ee3dbab9684628c9d5c74c81fc1b0b0f4610c1`
- `.teacher/runs/commit-000156-001/coverage.json`: `9e42ba5b24174b25cdc4934c98e0dbb7b8467fb08e7d70487e80dd600cd5bc4b`
- `.teacher/runs/commit-000156-001/draft.json`: `28fb842761ba057aba988b99448b90017cf0ff63e55a6ba3e5ee84116f19bdec`
- `.teacher/runs/commit-000156-001/draft.md`: `0f160d75d7b6c8f85773c597c08956af162f818b427c0c02a0495d9ebf6a6168`
- `.teacher/runs/commit-000156-001/provenance.json`: `a1ff3ab46ccde41f0d9ecb3104d8bae5bbfee73b0dc2e062e5c207f68444607e`
- `.teacher/runs/commit-000156-001/raw-transcript.json`: `2f7285afb8128768a034c9841664b19071fefa5e030dbb1d4fc736b54d10fc65`
- `.teacher/runs/commit-000157-001/coverage.json`: `8b2fd580ba50cea067a0531369d5c8af1063637657bb26b0a6fdfa6ee14cbee4`
- `.teacher/runs/commit-000157-001/draft.json`: `de5a4429600079fe3c8c3781a5573efa0d449286c24ebb021b7ddc5c09475486`
- `.teacher/runs/commit-000157-001/draft.md`: `d6b646c8d72023ffa081c8cdc6238ddf5b84602d6d5f2781f986f02db1442ca6`
- `.teacher/runs/commit-000157-001/provenance.json`: `e5e533ebcb90c464c2659cee8b6fc96a72ab2edbedb508857ce95e7a263e4f9e`
- `.teacher/runs/commit-000157-001/raw-transcript.json`: `793c70626a0511248789f1bc4a5ed80e8667af8651057b463548cade566384c4`
- `.teacher/trials/guidance-8-001/packet-000140/manifest.json`: `0543309226fc5b7a961900e5ccaba78bfd84336df11dbad91a58698fc11d3684`
- `.teacher/trials/guidance-8-001/packet-000154/manifest.json`: `e6a1d5e95e08aaba81c853cb19df319a986aefa8f79e20c00df77e13e9b7e351`
- `.teacher/trials/guidance-8-001/packet-000156/manifest.json`: `ea0c20e5f1c48acfc877a95b408c67c3fffb5c34e95de1f44ea9d47b80b00646`
- `.teacher/trials/guidance-8-001/packet-000157/manifest.json`: `234eaf422c89ac9c4dba7fcccfffc2332bf2e71b334db8620ec21a46fb09e72b`
- `.teacher/trials/guidance-8-001/run-000140-001/coverage.json`: `e715e0ef0428faf716600bebff2f9e4594305ae805f80284f7034f5f1d78be48`
- `.teacher/trials/guidance-8-001/run-000140-001/draft.json`: `492405116f7cb59a854c77218033013ac4e0ad61efc6aa77f23e110a2428b6de`
- `.teacher/trials/guidance-8-001/run-000140-001/draft.md`: `58a57a730fa07c7d4d9fbb6507745f7f73e92e9dfec755894308dcc17c0dca85`
- `.teacher/trials/guidance-8-001/run-000140-001/provenance.json`: `c186e7421007e362260b6a491884dd64105bfb410b5fad9033741c0955e668ec`
- `.teacher/trials/guidance-8-001/run-000140-001/raw-transcript.json`: `d2903e12a7d35c282317c0b09e97429ab2529f93fef795a0fda8bd9ac4a7d733`
- `.teacher/trials/guidance-8-001/run-000140-001/token-usage.json`: `cfcb9bb95e0b13f63de53c13667023dc8b468ba00094bc8d1645a0a8840bce8d`
- `.teacher/trials/guidance-8-001/run-000154-001/coverage.json`: `937de78fd5fcedb0f7322034c17c77c8ad689dbfe2cb6da8dcdae3b9776bc3b2`
- `.teacher/trials/guidance-8-001/run-000154-001/draft.json`: `1ddc91410fb4d891b321a66e772e20101c3554c3fc736ac76651b7b937b69502`
- `.teacher/trials/guidance-8-001/run-000154-001/draft.md`: `51467c9c54da0397951f08092a347ef217a3602009f4c1dac8a42898033c5d01`
- `.teacher/trials/guidance-8-001/run-000154-001/provenance.json`: `900744e71cae68424113e353586c8304cac29bc6980935f3eae4074cc92fa9b9`
- `.teacher/trials/guidance-8-001/run-000154-001/raw-transcript.json`: `fec873c8a033babf774076548f007f43af04421a6d1425f78552280b07b6176f`
- `.teacher/trials/guidance-8-001/run-000154-001/token-usage.json`: `1bbe844f35a5301321ad379ae6bc27ebc371c300286f8b935ceffff6aafe188b`
- `.teacher/trials/guidance-8-001/run-000156-001/coverage.json`: `a530a20fc2429dd9c7b11dc1718488c270675532b4b39dab0b6a1343e13c769c`
- `.teacher/trials/guidance-8-001/run-000156-001/draft.json`: `a4fd8b36ada51a2b20b12f10ae709b3749ae5e5ca802863888eaa28d2bc5e11c`
- `.teacher/trials/guidance-8-001/run-000156-001/draft.md`: `d45b9b328a1b50a09c04710c0cbd3b278b7f564d7b8b587cf43946ece56031bc`
- `.teacher/trials/guidance-8-001/run-000156-001/provenance.json`: `94b0f2e5da4693bdb04b815d79199086b606bd28a5786296ade3338f38163657`
- `.teacher/trials/guidance-8-001/run-000156-001/raw-transcript.json`: `b80d885fb39abf9df50db4c242549acb9c5943c461f6cb789ea45bec3596a508`
- `.teacher/trials/guidance-8-001/run-000156-001/token-usage.json`: `9ca558992d931301fdb496637dfd833ed5872661efc1a1453e59a62dada91e4c`
- `.teacher/trials/guidance-8-001/run-000157-001/coverage.json`: `cedfdd5f9e140be35784aa0710e90952e3ce67912d9d7e09a977cc25a57e711e`
- `.teacher/trials/guidance-8-001/run-000157-001/draft.json`: `b5dd5d4809af82b00a650a7e16e74bb74acb7dbdbbc6010915c99007e8f67d44`
- `.teacher/trials/guidance-8-001/run-000157-001/draft.md`: `41944369f0739946f677a3c0ac7725ec25b919692eabf25ac6b4cda91f029120`
- `.teacher/trials/guidance-8-001/run-000157-001/provenance.json`: `e25e5cded489f7d10637a876f1a8ca37c28c43070254c26e5150c4ab7a160535`
- `.teacher/trials/guidance-8-001/run-000157-001/raw-transcript.json`: `f0efc37f9c174556e9f7e42d24358fb146c4f7455407d4ce13b4fbc503603047`
- `.teacher/trials/guidance-8-001/run-000157-001/token-usage.json`: `9095a4b39b127fa132b492117195332e09d7a46cfa29e1f343683d89dc803dc2`
- `.teacher/trials/guidance-8-001/walk-after.json`: `34f85d85bc96584a17620a9f36bd2d5aa9269cc735e92704db79ce7faa4992be`
- `.teacher/trials/guidance-8-001/walk-before.json`: `34f85d85bc96584a17620a9f36bd2d5aa9269cc735e92704db79ce7faa4992be`
- `reports/guidance-8-trial-001.json`: `458855f068de0471132e1aa44ccba8c98966d70082748f8d0eac3fadb39f8aee`
- `reports/guidance-8-trial-supervisor-001.py`: `6eaea73123320174fcdc7a80511ee828443f63e3594ea34c64374a6dda4c9d9a`
- `reports/guidance-8-trial-validation-001.json`: `000f0d5a4ca08666ed1de8514c5211d732e818c0dd8c999fa8920b6bec5a0868`
- `reviews/verdicts/guidance-8-implementation-001.md`: `f07371b2fbe5abd2c0d89cb69939394659731f102e4647e72a00adfbc9d952c3`
- `reviews/verdicts/guidance-8-trial.decision.md`: `941c51728fcf206d1757fbb943fdeaf852919139f9d2718caeaac37e2bef97b5`
