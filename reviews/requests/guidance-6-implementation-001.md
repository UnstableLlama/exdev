# Implementation request: guidance-6-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements the user decision in reviews/verdicts/guidance-6-trial.decision.md after filing 164/001. Please accept the trial gate; this does not request walk adoption or approve any trial output.

teacher/session.py appends exactly the three approved paragraphs (including their recorded line breaks) when guidance_version >= 6. Existing instructions retain their order. Contract-8 validation now accepts guidance 5 or 6 so fresh trial packets can use the gate; older contract-version requirements and all evidence checks remain intact. The walk prepare() builder still writes guidance_version=5. No existing packet, run, or approval was edited.

For the actual 164 packet, version-5 system instructions and the entire opening messages serialize byte-identically before and after (6,366 system bytes). The comparison report also verifies the three paragraphs verbatim against the decision. Fixture tests verify opt-in, unchanged task message/tools/reasoning effort, default 5, and that altered evidence still fails validation.

Full host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — **280 tests passed**, 22.344 seconds. This shared suite also includes the separately submitted tool-replay-errors-implementation-001 fix; its patch is separate. ResourceWarnings were emitted but no test failed. Version-5 instruction bytes remain identical with both changes installed.

No trial has started. After acceptance, the four fresh unassisted sessions at 154, 158, 163 and control 156 will use the same approved cutoff evidence in scratch packets/runs under .teacher/trials/, with guidance 6 and no coverage request or reviewer material. They will not become journal attempts, approvals, ancestor context, or published entries. Isolation is an administrative obligation, not a new approval-system feature in this patch. The four results will be filed in guidance-6-trial-001. Walk guidance remains 5 unless the user later adopts 6.

164/001 is awaiting its own verdict; no 165 session has started. The reviewer-only trial criteria were not included in the instruction text.
## SHA256

- reviews/verdicts/guidance-6-trial.decision.md: `9ba58a40c5cbcd533171324a09a0010b729e1f9c9287ec83bd222a3f12011848`
- teacher/session.py: `82afcce1f0675e46a524570d81a93377b18b2c8e38fd15dfdaff25812c6d6ad6`
- teacher/walk_inputs.py: `267ad3e29b4ac86e911d854c7c7c786adf2437508bfdfa03982a18a1eb80f668`
- tests/test_walk_inputs.py: `cb20c141ca5ad5341d329ef2f0bec9f75a48f1bca23cb94937d3f282e9cb24f9`
- reports/guidance-6-implementation-001.patch: `132940d3e76b83becd43832297f2a2742ccf951091490c9bd762613d79cfc540`
- reports/guidance-6-implementation-001.json: `7540e2fed34f18f8862d6942c12e39aa92371ddb205955b58f29a94d13ca3014`
- reports/guidance-6-v5-before-system.txt: `3c2c01e372ee31c9084e55d3f762ec8e0e529522a6609546098571b309c7a168`
- reports/guidance-6-v5-before-opening.json: `75b3f2588946d9bedc83cc758452e9b50180d5068d70e045c74005197207d741`
- reports/guidance-6-tests-001.txt: `a46bbc93b31520018ac48a1e42778ed3c0d4838cdfd8c8402953e0070cab7598`
