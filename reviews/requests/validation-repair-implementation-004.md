# Validation repair implementation 004 — fixed keep-rest feedback

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please review the tested candidate implementing validation-repair-002.decision.md. The 298 request was published first. This change is developed and tested in /tmp/exdev-repair-004; its five exact candidate files are retained under reports/validation-repair-implementation-004-candidate/. Live teacher/ and tests/ files remain unchanged, byte-identical to the bound baseline copies. Run 299 was already active on accepted code; no teacher session has started for this change. No 300 will start before acceptance and application of the approved candidate. Nothing committed or pushed.

The proposed fixed sentence is exactly:

> Correct only the issue named in the validator message and return the rest of the annotation unchanged.

Policy validator-keep-rest-v2 sends precisely the verbatim validator message, one LF, then that constant sentence. The adapter stores and sends the same string. The recorded error remains verbatim; provenance hashes the complete actual feedback and identifies the new policy. No commit-specific, reviewer, author or earlier-attempt content is added. Historical validator-only-v1 transcripts retain their error-only verification and fingerprint; historical unrepaired runs retain their recorded policy in assessment disclosure.

The patch changes feedback construction, policy-specific provenance/verification, assessment disclosure, documentation and tests. Validator eligibility, annotation validation, approval eligibility, same-session behavior and the one-repair limit are unchanged. This instruction requests preservation; it does not mechanically enforce semantic equality of all remaining prose.

Twenty focused tests pass. Added tests bind the exact literal sentence and complete feedback hash, reject extra hints and policy/text mismatches, reject unknown policies, and replay legacy repaired/unrepaired records. Existing tests still exercise same-session transmission, one-repair limits, disabled repair, failed second finals and approval. The full host-enabled suite passes: 337 tests. An initial full-suite run exposed a legacy no-repair policy mismatch in the candidate; it was corrected before the bound passing runs. The patch and copies below are the exact tested final candidate.

After acceptance I will apply only these five candidate files after 299 exits, verify all candidate hashes, and retain the old run artifacts unchanged. Until then the live policy remains validator-only-v1. No orchestration files were changed.

## Bindings

- reports/validation-repair-implementation-004-baseline/validation_repair.py: `d6ce4f8944287bd1ef9cf42fbddba342597efa8122c19761e3ce66b4f44e27a4`
- reports/validation-repair-implementation-004-candidate/teacher/validation_repair.py: `dec32e1466f8ad2c1a40cc5205ed1ff7b0c701b7c26f4a481eebd0ac4ea37b19`
- reports/validation-repair-implementation-004-baseline/codex_adapter.py: `9540b6701d5ceb44c28af78ec9f38fa80038637a37e10563c181c0696b14e190`
- reports/validation-repair-implementation-004-candidate/teacher/codex_adapter.py: `cad6b72eda2880c399775538a473f8710c00923963e754f598d613daa7199c38`
- reports/validation-repair-implementation-004-baseline/cycle.py: `5c3768624cb16f134a5428a34687bea7eb70bc2626f909065d3676626a246e9e`
- reports/validation-repair-implementation-004-candidate/teacher/cycle.py: `9e6f7eb484cc727cebfc40b1e1c6d926ae29423b90e0fe31abfeadac4e9344de`
- reports/validation-repair-implementation-004-baseline/README.md: `4cf1c0ca435e8887734ec1d5b8281f928c4b194f39981c16e0e0bca514d442a3`
- reports/validation-repair-implementation-004-candidate/teacher/README.md: `260bf1d9ff50ca62fdf413a01609ef5d1aac2fa2633ddef74bf153cf311b8ee5`
- reports/validation-repair-implementation-004-baseline/test_validation_repair.py: `942d118c9fb550cee5e1c18c0b3956cca31070b6c63d809d4351bdda2b13b68a`
- reports/validation-repair-implementation-004-candidate/tests/test_validation_repair.py: `18ae769bcf82ffb2c7c9bd83348a20be169370560de294170ce9c15811d1a41d`
- reports/validation-repair-implementation-004.patch: `10beec58ff8b0b5faaff342af7a5593a89da5f115a5426967898375356931057`
- reports/validation-repair-implementation-004.json: `60c76215accabc10f1170335b333badecd03f54703ee8071de670fae0dc40ebb`
- reports/validation-repair-focused-004.log: `6d216dac0cd9076bb97c72f32b1ac95f41a2551d4fc05cc192145fb76763f3bd`
- reports/validation-repair-suite-004.log: `b11c8b5501cb8482f805a81423babc251846841389841a1733b9e6c53c6687b5`
- reviews/verdicts/validation-repair-002.decision.md: `c79b050871747a7cec7b24c402d21ace2a0dcd9b7599a34a95af8d1bd31a1e57`
