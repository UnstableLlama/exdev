# Commit 255/004 — pre-launch coverage gate blocker

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

No 255/004 teacher has started and no output directory was created. The journal remains stopped_failure at 255. The recovery verdict authorizes one fresh assisted 004 using the unchanged 003 packet, coverage and instructions. I have not changed that packet or bypassed its gate.

`teacher.author._author` checks that output.name equals the coverage path basename with `.coverage.md` removed (teacher/author.py lines 43–46). The immutable `.teacher/retrieval/000255-003` manifest binds `commit-000255-003.coverage.md`; a `commit-000255-004` output therefore raises `ValueError('Coverage request belongs to another attempt')` before creating the run. The recovery supervisor's unchanged-packet check is consistent with the verdict, but the author's attempt gate cannot represent this recovery. Please resolve the mechanics explicitly; I have made no validator exception or packet rewrite.

Separately, automatic approval review rejected the escalated detached 004 launch because it requires direct user authorization beyond the tool-read recovery verdict. No teacher started in that rejected launch. A direct authorization question is pending; reviewer acceptance of a code or packet change does not by itself remove that execution restriction.

This request contains no proposed annotation and supplies no reviewer material to any teacher. Replacement 234 and position 256 remain unstarted. Run-ahead implementation is separately filed as run-ahead-implementation-002; live run-ahead remains disabled pending acceptance. Nothing is committed or pushed.

## Bindings

- reviews/verdicts/commit-000255-003.md: `3df8a893059565d28bff8d54a15d92d63154a0ac894d79901d36c2d195a2ac14`
- .teacher/retrieval/000255-003/manifest.json: `e2664de81740d341a15448295db04fd44c24444105833c8b8a9663817180cbe6`
- teacher/author.py: `70db8a88568c1db016b80e75313c3c75f784fdcd203c4abb1bdbd072893999d2`
- reports/commit-000255-assisted-004.py: `691b55b7e339dc785cf008f003ccc6ede0073bd6d7a16baaf18c1bb9377fe1d6`
