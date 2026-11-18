# Recovery mechanics request for 336/004

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

The reviewed schema patch is live. All 355 host-enabled tests passed. The prepared preflight verified the original 336/002 packet, all 332 approved ancestors, 4,655 read-only blob links, and the bound artifacts from the three prior failed runs.

`recover --retry-position 336` refused before reservation because it requires the stopped run’s full literal path in the verdict. Recovery 004 identifies `-003` in a list that starts with `.teacher/runs/commit-000336-001`. Please issue a recovery verdict naming `.teacher/runs/commit-000336-003` in full and keeping the existing authorization for one fresh unassisted 336/004 using the unchanged 336/002 packet.

The journal matches the preflight snapshot byte for byte. It is stopped at 336 on 336/003, with no active session or 336/004 reservation. No teacher ran and no 336/004 diagnostic artifact exists.

## SHA256

- reviews/verdicts/commit-000336-recovery-004.md: `34aaf6b4eb248c9b1471871c52859efaa2d737715534cb1d44cd49e81308e059`
- reviews/verdicts/codex-output-schema-implementation-001.md: `a959832d5446275de2d66f8e86476aa7af699b1ac950a0f41994b8d3038593a3`
- reports/codex-output-schema-implementation-001.patch: `adcf1f27015b62ad90cf8368fac91c62c1be98733d283f5d71616470cfb91287`
- reports/codex-output-schema-implementation-001-live-suite.log: `bd2638c31d6e3e5c9f8f3d2b8ae4bcdc70ea163ef0b92b49bfbf1e41fa6404ae`
- reports/commit-000336-recovery-004-application.json: `7d19d92b8ffe0fff5e37bddf876af4f12050e15de87cf1adc564090ae09db33c`
- reports/commit-000336-prepared-004.result.json: `81931c7e6211ce8c958b421c0c5adb68285c1ae9382680dcba419b116cf5b240`
- reports/commit-000336-prepared-004.spec.json: `7c66e13b4c408ff2746d074d2afccb82b14097781a63283050cf6eba55790104`
- reports/commit-000336-before-prepared-004.json: `ee976ed2084c1af5f374489aee70b15ed6cfc2a3611eafdc5f5e0cc7715e6331`
