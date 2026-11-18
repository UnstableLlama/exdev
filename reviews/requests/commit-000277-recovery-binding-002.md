# Recovery binding request: 277/002

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

The authorised277/002 supervisor stopped before teacher startup: recover rejected the decision with `Recovery decision must identify stopped run`. The queue stop names `.teacher/runs/commit-000277-001`; the accepted recovery verdict names the new run but lacks that literal stopped-run path. No recovery or teacher session occurred; queue stop remains and278's request has now been published.

Please add the stopped run's exact path to reviews/verdicts/commit-000277-retry-recovery-002.md, confirming the existing recovery authorisation applies to it. After that correction, I will bind the updated verdict hash in the prepared spec, preserve this failed supervisor's result/log, and retry the same authorised recover/prepared sequence with a new supervisor/result path. No packet, teacher instruction, validator or orchestration change is proposed. No279 or other teacher launch pending resolution.

## SHA256

- reviews/verdicts/commit-000277-retry-recovery-002.md: `b0cc28955f808b840d24946a624e8107341d2d4bfb503e81edd695b55d0a16ca`

- reports/commit-000277-prepared-002.spec.json: `4f7460a863ff702e77ce58e81430f9e3778c1fa3da460998167d1240faadb058`

- reports/commit-000277-prepared-002.py: `c285412a5273a1a03f950d331677d886d5b82b1d52a6f6a1d97169d153175c69`

- reports/commit-000277-prepared-002.result.json: `451b6db756b8bf3d58c00326775b05f07c6f71816938cee49c2d7ae88b8b1512`

- reports/commit-000277-prepared-002.log: `201f35599a4a7fefb29f0f93a5e3485f0a3538a0df9680ed16efbd4f538e0d01`
