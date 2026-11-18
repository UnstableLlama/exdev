# Commit 297/001 — full review request

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Run: `.teacher/runs/commit-000297-001`  
Packet: `.teacher/retrieval/000297-001`  
Upstream: https://github.com/turboderp-org/exllamav3/commit/6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d  
Git title: **Loader: Add tensor override script**

Requested scope: ancestor retrieval only; canonical/training remain false. Fresh unassisted teacher: gpt-6.1-sol / medium, contract 8, guidance 12, salience-v3-paths. Runtime: Codex CLI 0.167.0, Python 3.14.4, Linux aarch64.

Independent author validation passed: all 43 calls replayed identically, 4302 shared read-only blob links verified, all 45 teacher implementation hashes verified. The four orchestration files match the recorded hashes. No implementation change; latest accepted full suite is 332 tests. No sampled mechanical run accompanies this request.

The entry explains YAML source grouping and reverse source-addition precedence, wildcard selection without missing-key fallback, forwarding of tensor options and deferred operations, main-only bulk enumeration, Config's removed st_variants branch, and the two consumers' installation timing. I checked the changed source against these mechanisms. Three suspected findings are submitted:

- New override-load-metrics: nonempty overrides plus load_metrics reaches a wrapper lacking the metrics attribute consumed by shared initialization. Conditional on successful loading through that block; source inspection only.
- Inherited model-metrics wrapper: Model.get_load_metrics calls absent stc.get_metrics. The new wrapper removes its former method; the ordinary collection already lacked it. API-level trigger; no external caller execution established.
- Inherited deferred BF16 odd tail: pair-only CUDA conversion leaves an odd final element unconverted when deferred loading disallows BF16. No affected checkpoint or GPU execution demonstrated; preserve the existing identity if accepted.

Coverage: all seven task sections fully read; three ancestor prose entries read from 34 matching targets (root loading/tokenization, metrics, and measures). Whole-parent-tree searches supplement the selected ancestor prose. Parent linear.py was read only at bytes 2700–9700; the broad parent override grep and model_diff ancestor search returned truncated selections. PR 22 pagination was completed; only initial 16000-byte pages of PR 26 and issue 33 were read. These do not establish motivation or exhaustive compatibility.

Report run file reads separately from repo_read: one standard-library tree-wide scan reads Python files and prints caller/API matches. The other run call transcribes fnmatch/grouped priority and BF16 pair-count arithmetic using synthetic inputs. Neither executes repository code, a YAML parser, checkpoint loading or GPU kernels. The nine repo_read calls are counted separately.

Validation repair was enabled and USED once (validator-only-v1). The sole feedback was verbatim `Source inspection requires source evidence`. The teacher then read parent examples/imgsearch.py and supplied a complete replacement annotation. It rewrote substantive prose and findings as well as evidence fields; this was the teacher's own same-session output. There were 42 tool calls before feedback and one after; selected final transcript index 91. Refused annotation SHA256 fa47bfb311c8eb12fde0962ed7a5fa1cea438ab618b67decb857777d09675b29; repair input SHA256 930db7cb1efcc501d1792dc662d7816afb9cbc671eb0e224a871b186b0fb3754. Replay verified repair provenance; this is not the first live repaired run.

Run-ahead disclosure: ran ahead of no positions; NOT sparse, 296 visible of 296 strict ancestors. Catalog: 28 open rows, seven closed rows; all seven closed selections qualify only by path overlap. Qualified/selected 7/7, cap 20, no truncation, no cut rows. No ledger item is owed from 296. Production token totals are unavailable in the retained artifacts; token-usage retention remains pending.

SHA-256 bindings:

- .teacher/runs/commit-000297-001/draft.json: `2bcf0a553781b59425bd5c32b3118535c32c3662579f5f5f19c303a3e29f6fc3`
- .teacher/runs/commit-000297-001/draft.md: `f530251eafbe637cafe53585c3d6a6da7e9c21f904d74c2595499c013d83885d`
- .teacher/runs/commit-000297-001/raw-transcript.json: `0ca31de0c43607231849aa077d663e8ba82d9ab1a437e79563552df0b81150cb`
- .teacher/runs/commit-000297-001/provenance.json: `bf47f00482b793447beeec324aef3e61fa4ad19712ee0c11cadfd91489beeae1`
- .teacher/runs/commit-000297-001/coverage.json: `f46e2dfa18c7d733e44dba64997f4dfa997893f0d13a73d65bfc2868addc8abb`
- .teacher/retrieval/000297-001/manifest.json: `884d808fdb5af579f9e6b69d46c5f2d4cd484e55e22f6c8e88aad94999bf2492`
- reports/commit-000297-validation-001.json: `fa620849d3b68cfa50ec57ee22728ba7dfb09e5955e6233aa07ab509ec52d364`
- reports/commit-000297-catalog-selection-001.json: `5a1172460421e92cb857c92fd386716fc9da871e5ec6da812ff8c2c8bb18c2e6`
- data/evidence/github/000297-unreferenced.json: `f9e97e1e5654cc127dffaee8f69e7c79f7580984b12b3a6595b447677e0e633a`
- data/evidence/github/000297-closed.json: `a61aa51ae87d318ec28ee9280fbbcd612559d59a8d5eb50217e47fc463a75fd0`
- reports/commit-000297-author-validation-001.json: `fa620849d3b68cfa50ec57ee22728ba7dfb09e5955e6233aa07ab509ec52d364`
- reports/commit-000297-cycle-001.json: `f1547efbedfa8faad5623f33a69aa2c07f5498d0e6f8b576c2b73f8daca5600d`
- reports/run-ahead-detached-000297-3ef127b423214d0492e6b75d76419d1e.json: `85018051b89efda4e8b61fac9e765a134b981855077b63e41f61082b19dc94c3`
- .teacher/admin/run-ahead/0c6ad421899840f9b74327d6e45218b0.json: `7c8b3f7694b4243267f6c7dffa0048c3327ba4b64210a10a2bc83d38c78458b2`
