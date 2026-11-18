# Proposal: identify the claim and evidence ID in validator feedback

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

For 324/001 the teacher received exactly:

```text
Unknown or unsuccessful evidence call
Correct only the issue named in the validator message and return the rest of the annotation unchanged.
```

For 322/001 it received:

```text
Source inspection requires source evidence
Correct only the issue named in the validator message and return the rest of the annotation unchanged.
```

Proposed first change: for an unknown, failed or catalog-only claim anchor, add the claim location and a bounded rendering of the exact rejected reference to the single repair message. For 324 this would identify `source_notes[2].evidence` and `call_50832e5bd8be469ba24c813982789a2`. Keep the one-turn rule and the existing instruction to preserve the rest. Generate the details from validation of the candidate and current transcript. The message supplies no suggested replacement, reviewer text or new evidence.

Use a versioned feedback policy and retain replay compatibility for recorded refusals under the earlier policies. Keep refusal eligibility tied to the existing category and verify the recorded feedback against the refused annotation. Scope this proposal to claim anchors. The 322 example illustrates the same precision gap for a different refusal class.

This request seeks a decision on the proposal. Production files are unchanged. For an implementation submission I would bind the changed files, tests and replay checks for existing repairs as well as the focused regressions and the host-enabled suite.

## Artifact bindings

- .teacher/runs/commit-000322-001/raw-transcript.json: `ca846a3eeb58be4b648a38bb8885661a4847e8fdbbdfb2259ebac991e00b15d8`
- .teacher/runs/commit-000324-001/raw-transcript.json: `3e80a40c7a590641cccc02bf769a858a3fed275bcfd48d50dad78bb83aeb9345`
- reviews/verdicts/commit-000324-recovery-001.md: `9b66023424c774380ed35688c81cc7ef26f97363f12eb06ed1bf72637b9744c2`
- teacher/editorial.py: `92d39a4364126b5a39f3436267dda1ffff6c007b5a9830d9a7f003d0a29b8316`
- teacher/validation_repair.py: `dec32e1466f8ad2c1a40cc5205ed1ff7b0c701b7c26f4a481eebd0ac4ea37b19`
- teacher/codex_adapter.py: `14172b70b8c08acd31d9118dd243d4b5bb788344af834fb2fdbf5033910d353b`
