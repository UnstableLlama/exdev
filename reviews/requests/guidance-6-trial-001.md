# Review request: guidance-6-trial-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Four unpublished, unassisted guidance-6 trials completed under the accepted trial gate. This requests assessment of the trial, not approval for ancestor retrieval, canonical use, training or adoption. Walk guidance remains 5. Each position has exactly one session, first result retained, no failed sessions or retries. No coverage request, verdict or reviewer criteria entered a trial packet.

For each of 154, 158, 163 and 156, the trial manifest differs from its source manifest only in guidance_version (5 to 6). Source 163 is the unassisted 163/001 packet; its output comparison below is the approved reviewer-assisted 163/002 run, as required. All other baselines are approved 001 runs. All packet blobs retain identical content. Exact opening, implementation fingerprints, rendered Markdown and blob hashes verified; all 74 tool results replay identically. See reports/guidance-6-trial-validation-001.json.

Isolation snapshots were taken after filing 165 and before applying its subsequently received approval. Every file's path, content hash and permissions under .teacher/retrieval and .teacher/runs is unchanged; journal runs and approved_entries compare equal. The before/after files retain the full inventories. Trials only created packets/runs under .teacher/trials/guidance-6-001; no trial was published, approved or recorded as a walk attempt. Administrative reports and this request are outside that directory.

## Comparison

Counts below are trial / approved. “Turns” means app-server turn/start invocations: one per author session. The saved transcript records individual tool calls and the final answer, not internal inference steps; those are not recoverable. Assistant-record counts are also supplied to avoid conflating one API turn with one model response. Token usage is not retained.

| Position | Calls | Assistant records | API turns | Text sections read | Ancestor reads |
|---|---:|---:|---:|---|---:|
| 154 | 10 / 9 | 11 / 10 | 1 / 1 | 1/1 / 1/1 | 2 / 1 |
| 158 | 35 / 21 | 36 / 22 | 1 / 1 | 2/2 / 2/2 | 1 / 0 |
| 163 | 23 / 18 | 24 / 19 | 1 / 1 | 14/14 / 14/14 | 3 / 2 |
| 156 | 6 / 4 | 7 / 5 | 1 / 1 | 1/1 / 1/1 | 2 / 1 |

154 retains the inherited perplexity-axis finding and adds an ancestor read, but does not identify the unconditional-deferral eligibility issue. 158 explicitly compares Mixtral's calibration_all_experts default with Qwen3 MoE and records the conditional inherited fused-shape finding. 163 independently identifies the unmigrated Qwen3 MoE configuration. Control 156 has no findings and discusses the color/label rules with a scalar check. These are administrative observations for the reviewer, not claims that the trial passed or authorization to adopt guidance 6. Please assess correctness, coverage and speculation independently.

163 notes that task-tree searches were unavailable under the strict-ancestor restriction and combines the full task diff with parent searches. This is a limitation of the unchanged tools relative to the new instruction wording; no tool behavior was changed for this trial.

No implementation changed after the accepted gate/replay fix; the associated host-enabled suite remains 280 tests passed. Replays above are additional artifact validation, not a new teacher session. The walk may resume at 166 under the user's existing authorization after this filing, on guidance 5.

## Artifacts and per-tool counts

### 154

Source packet: `.teacher/retrieval/000154-001`. Trial packet: `.teacher/trials/guidance-6-001/packet-000154`. Manifest comparison: only guidance_version changed.

Trial: `.teacher/trials/guidance-6-001/run-000154-001`; counts `{"ancestor_read": 2, "git_show": 1, "repo_grep": 2, "repo_read": 2, "run": 1, "web_fetch": 2}`. Draft, transcript and coverage hashes below.

Approved baseline: `.teacher/runs/commit-000154-001`; counts `{"ancestor_read": 1, "git_show": 1, "repo_grep": 2, "repo_read": 2, "run": 1, "web_fetch": 2}`. Draft, transcript and coverage hashes below.

### 158

Source packet: `.teacher/retrieval/000158-001`. Trial packet: `.teacher/trials/guidance-6-001/packet-000158`. Manifest comparison: only guidance_version changed.

Trial: `.teacher/trials/guidance-6-001/run-000158-001`; counts `{"ancestor_read": 1, "evidence_index": 2, "git_show": 2, "hf_fetch": 4, "repo_grep": 10, "repo_read": 9, "run": 1, "web_fetch": 6}`. Draft, transcript and coverage hashes below.

Approved baseline: `.teacher/runs/commit-000158-001`; counts `{"evidence_index": 2, "git_show": 2, "hf_fetch": 4, "repo_grep": 5, "repo_read": 5, "run": 1, "web_fetch": 2}`. Draft, transcript and coverage hashes below.

### 163

Source packet: `.teacher/retrieval/000163-001`. Trial packet: `.teacher/trials/guidance-6-001/packet-000163`. Manifest comparison: only guidance_version changed.

Trial: `.teacher/trials/guidance-6-001/run-000163-001`; counts `{"ancestor_read": 3, "git_show": 1, "repo_grep": 5, "repo_read": 6, "run": 2, "web_fetch": 6}`. Draft, transcript and coverage hashes below.

Approved baseline: `.teacher/runs/commit-000163-002`; counts `{"ancestor_read": 2, "git_show": 1, "repo_grep": 3, "repo_read": 3, "run": 3, "web_fetch": 6}`. Draft, transcript and coverage hashes below.

### 156

Source packet: `.teacher/retrieval/000156-001`. Trial packet: `.teacher/trials/guidance-6-001/packet-000156`. Manifest comparison: only guidance_version changed.

Trial: `.teacher/trials/guidance-6-001/run-000156-001`; counts `{"ancestor_read": 2, "git_show": 1, "repo_grep": 1, "repo_read": 1, "run": 1}`. Draft, transcript and coverage hashes below.

Approved baseline: `.teacher/runs/commit-000156-001`; counts `{"ancestor_read": 1, "git_show": 1, "repo_read": 1, "run": 1}`. Draft, transcript and coverage hashes below.

## SHA256

- reports/guidance-6-trial-001.json: `e3d79ea6ad8b610d02b1f8587a69b2c0cd694e71f3452a1f03f63cb52a6677d5`
- reports/guidance-6-trial-validation-001.json: `d35755badeecac0d2b3a1eccbc7ae47fb89d93dfbfab2c878af3b4b726e8b3f5`
- reports/guidance-6-trial-supervisor-001.py: `778b59c1d1ae626e105d906948a387e06cdcdfa6e963fbf31ee1162f6628dc82`
- .teacher/trials/guidance-6-001/walk-before.json: `65b0cdc288dc2b971d27b724fe3c1d3a0dd3d7c4c9b9d0660f0f0ed7e59a8234`
- .teacher/trials/guidance-6-001/walk-after.json: `65b0cdc288dc2b971d27b724fe3c1d3a0dd3d7c4c9b9d0660f0f0ed7e59a8234`
- reviews/verdicts/guidance-6-trial.decision.md: `9ba58a40c5cbcd533171324a09a0010b729e1f9c9287ec83bd222a3f12011848`
- reviews/verdicts/guidance-6-implementation-001.md: `2f8e32719257c11ebc231a21a8b42c9dd26cc44a77b09be913085a7170d4033b`
- .teacher/retrieval/000154-001/manifest.json: `c06e896d5d0731942d632e6106a62d16486ab3a751faa152b00dce382bbfbad6`
- .teacher/trials/guidance-6-001/packet-000154/manifest.json: `d2f20e0abe8776117e0e2352cdbc01ecb7eb700055d2fc75e3837750bf0d46fb`
- .teacher/trials/guidance-6-001/run-000154-001/draft.md: `222f7d1663b6c8d3c7f2885b67f5a7a874125ee747e0c6bb1e0856434563e062`
- .teacher/trials/guidance-6-001/run-000154-001/draft.json: `e1009132ab283817d0db22d95301231c2125cdaaf0e4f445c4ee5ab733e7d067`
- .teacher/trials/guidance-6-001/run-000154-001/raw-transcript.json: `48fd4b5a55b06df6da17c56685edf9afad4e5ace22464db842ab4a27a4d2e015`
- .teacher/trials/guidance-6-001/run-000154-001/coverage.json: `586c58bdcdbbe97fa8d9fbb3d35d66f2669fb6ac7785e80908848fae1697128d`
- .teacher/trials/guidance-6-001/run-000154-001/provenance.json: `338cfa4881190fa3b21751073ea961eff5badb9b5246d6b4815b64c057a83b5a`
- .teacher/runs/commit-000154-001/draft.md: `6e4e4a44e2e0fc071881be788f909f9c5966fa5c5088bab96b3583ee9de1c9f5`
- .teacher/runs/commit-000154-001/draft.json: `000c24dbbedd9cae94c72b9de9e9c728ef54b7e56a03e5d8eab176a3f7a56825`
- .teacher/runs/commit-000154-001/raw-transcript.json: `6e1fe2943781e7df874451f185ee3dbab9684628c9d5c74c81fc1b0b0f4610c1`
- .teacher/runs/commit-000154-001/coverage.json: `c12f304cc98f5f7b106f33118b93a456f4b42d2813e38c57da0d40df7fb9ce13`
- .teacher/runs/commit-000154-001/provenance.json: `7daa8a8e966d85a07b1e437ccd0b2c20b9bd10387532e97a5213b1a773eb8d73`
- .teacher/retrieval/000158-001/manifest.json: `99d3bc879cfb70da94f2a09bb39a001ca7bfe6cbdb733c3d34b8d857f2ffcb9b`
- .teacher/trials/guidance-6-001/packet-000158/manifest.json: `5f4106db719e7705549ba2a5957af8e1b18591a8acfa9e6d8b2a272e84530541`
- .teacher/trials/guidance-6-001/run-000158-001/draft.md: `805190cae11fff8fe3b47ff81097abffacf49453e6cb78b642d8fd226eb978de`
- .teacher/trials/guidance-6-001/run-000158-001/draft.json: `c4b334a89c4d6015fb4e30c1d4ce393f5b4fe8ef450bb4e46848dee573bd620e`
- .teacher/trials/guidance-6-001/run-000158-001/raw-transcript.json: `97b036085f3504f4d40c9d4cbc7b5e17ee5b6673e05d599f8a53386e76198b01`
- .teacher/trials/guidance-6-001/run-000158-001/coverage.json: `c13bb48be7586239d5ee58bae866c4cedf4fc5fa7fbc45d7ad871ab0e8828163`
- .teacher/trials/guidance-6-001/run-000158-001/provenance.json: `1e35658187a0e8f541825ef2d55de65ae8704adbf0dd0b539806e76a276f20d8`
- .teacher/runs/commit-000158-001/draft.md: `ff99bb2c676b3d3f1dabb503cf70e569ec94a6e8a7a95a019be68ca15bdf032a`
- .teacher/runs/commit-000158-001/draft.json: `dd685d794ca20a2ac246e84ea817765ee6d5244a6314245a96dd2dc26f2191e7`
- .teacher/runs/commit-000158-001/raw-transcript.json: `336519dd01d2b020d6e2babbf5ee82bb4e90edf72ba6d21c0b6c1f5aafdac705`
- .teacher/runs/commit-000158-001/coverage.json: `38c62eda966c4dfc74a712b9eeff3b23a8e9a5737310db132b442a868325cb5d`
- .teacher/runs/commit-000158-001/provenance.json: `0021edf95f15a6780415db8c6eac69b23595502aedd4e4c656814e1e0ada2c39`
- .teacher/retrieval/000163-001/manifest.json: `1475e275c58a48c6df0594f91a87f6b5806151c33a512a9318a0b228dff76f86`
- .teacher/trials/guidance-6-001/packet-000163/manifest.json: `81b3e3da9888cde87c51574265f6963035f8ada5f99832ef8073622954bae675`
- .teacher/trials/guidance-6-001/run-000163-001/draft.md: `4aa97b21cee01df4ca61a405bac956a83a9126d5ce377f0a4f0ace827ca36756`
- .teacher/trials/guidance-6-001/run-000163-001/draft.json: `5443badca70e8841ee729df8fa56b3caadfafaee361bfe2531900a2e9fced8de`
- .teacher/trials/guidance-6-001/run-000163-001/raw-transcript.json: `aa818205d026a69acfa1c6fed3efd78a8b0b03a65e5bbb00fcc9a77ca7140679`
- .teacher/trials/guidance-6-001/run-000163-001/coverage.json: `8e3f90b312f869df1ea28fe69137b4ad348601244413252f4e404d3c4a0a8c73`
- .teacher/trials/guidance-6-001/run-000163-001/provenance.json: `8ba42eef8e860a91f3f6cef8b5d452514a14360ce06c24388e093535674974a0`
- .teacher/runs/commit-000163-002/draft.md: `d90fcf81b0779f68595426a2ae196a2bd89194e87d13e26a73d6c766e25b9d5b`
- .teacher/runs/commit-000163-002/draft.json: `dd3953fda4675b59476f463dfe6d6a150166ca6f2254a4795e37163a12872c50`
- .teacher/runs/commit-000163-002/raw-transcript.json: `d2f7fbdcca95ad6efa166f98dbeb0c201c1edb660c5ba2333d85b3b45d934600`
- .teacher/runs/commit-000163-002/coverage.json: `4fb1a9792f6ce22c6ea419ca2459c67686881bce2c3c79f22dbd61f0781d020f`
- .teacher/runs/commit-000163-002/provenance.json: `7f49ef9ec6dac450fc877f25812bdcbd18eec21eb8158fc2cdb44254670f2317`
- .teacher/retrieval/000156-001/manifest.json: `9ef102baa97fb412b9dd94e33f95584866ae8d9bcd4fc036c542997c83666152`
- .teacher/trials/guidance-6-001/packet-000156/manifest.json: `0ae84ab0e3daa831ebcdf23df729c76a1d912e68587ceb5b74f13198be62fcd1`
- .teacher/trials/guidance-6-001/run-000156-001/draft.md: `7b9389dbaf0be1f2e25ac324c8943609669e4549c714a716e8930c65bf3644eb`
- .teacher/trials/guidance-6-001/run-000156-001/draft.json: `341c304affd3ea80726593310328806766a45e30c02b21f4ccae87e2fce0f672`
- .teacher/trials/guidance-6-001/run-000156-001/raw-transcript.json: `dce69708f1c0f5edc8a4ca1d4048a4eb06901e904880d569d091045b53e295a8`
- .teacher/trials/guidance-6-001/run-000156-001/coverage.json: `76cf2d99fb6fd427260eaa851d14002efebd1e886f181cb6ef2227a70bd3139e`
- .teacher/trials/guidance-6-001/run-000156-001/provenance.json: `f70f98fc2c1be308962fd60e637f307492be618436aab40b701e4d81e6a4e891`
- .teacher/runs/commit-000156-001/draft.md: `0f160d75d7b6c8f85773c597c08956af162f818b427c0c02a0495d9ebf6a6168`
- .teacher/runs/commit-000156-001/draft.json: `28fb842761ba057aba988b99448b90017cf0ff63e55a6ba3e5ee84116f19bdec`
- .teacher/runs/commit-000156-001/raw-transcript.json: `2f7285afb8128768a034c9841664b19071fefa5e030dbb1d4fc736b54d10fc65`
- .teacher/runs/commit-000156-001/coverage.json: `9e42ba5b24174b25cdc4934c98e0dbb7b8467fb08e7d70487e80dd600cd5bc4b`
- .teacher/runs/commit-000156-001/provenance.json: `a1ff3ab46ccde41f0d9ecb3104d8bae5bbfee73b0dc2e062e5c207f68444607e`
