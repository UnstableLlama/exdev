# Verdict: reference-evidence-location-fix-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/reference-evidence-location-fix-001.md`
Scope: required fix 3 from `reviews/verdicts/reference-evidence-and-callee-implementation-001.md`
Reviewed: 2026-11-13, working tree on top of `dfebc8a`

## Decision

**ACCEPTED.** Required fix 3 is closed. Required fixes 1 and 2 remain open and are still due before position 100.

This approves no prose. Canonical and training remain false. The walk stays stopped before commit 44 until the user's answer on re-authoring commits 39 and 41 is recorded.

## Files reviewed (sha256)

All match the fix report (`cfee02eb1636cc0f85fa3be651e6365eeb186c70752f1cb4a79380319b4119b4`).

- teacher/architecture_evidence.py: `8cd711070cd3fb29399d2ef408e2e2d927f39d226be1468b4177407fedcb0768`
- tests/test_architecture_evidence.py: `27365580e90a8293cf5d359915d9df7380cb3d1e4ffc9b28142c7753357019fb`
- tests/test_walk_inputs.py: `3cac130aba5f8d5cf24355ad5d4377653ac2c7a14effc9b2fd6271e003773114`
- tests/test_teacher_packet.py: `c06e2b31dc2973751e322fec2ea7b2c46997ed9edc8ddd4c947086ff80ad8a34`
- docs/ancestor-context.md: `bc1d3d13567b45cb0bcf591c80531ea591e67ab889b85027c926cf416af3dc8f`

`teacher/walk_inputs.py` and `teacher/session.py` are unchanged since the previous verdict.

## Checks

| Check | Result |
|---|---|
| The change | `inventory` now lists both `exllamav3/models` and `exllamav3/architecture`. `trigger` raises "Architecture location unknown" for any non-root commit in which neither holds a model or config class. `load_bundle` calls `trigger` first, so preparation fails before anything is attached. Root commits are exempt. |
| Real history, full sweep | I re-ran the trigger over all 301 upstream commits that touch either directory, to the pinned tip. It fired on 84, with no parse errors and no false "location unknown". Architectures added after the August 2025 move are now detected (through `9d155a75`, 2026-10-29). Before this fix the sweep stopped firing after `0c441aaa` (2025-08-03). |
| Near positions | Commit 39 still returns `DeciLMForCausalLM` and `decilm.py`. Commit 41 and position 44 return no trigger. |
| Tests | Full suite: 197 passed with pinned Codex 0.167.0 first on PATH. `git diff --check` clean. New tests cover the moved directory, a new class in the new location, an unknown location failing at both trigger and loader, and the root exemption. |
| Legacy prompts | Rebuilt opening context for every run with a packet on disk: the same 9 reproduce and the same 37 do not, as before the change. |
| Fixture change | `tests/test_teacher_packet.py` adds a model class to the fixture repository only when a test class opts in. Other packet tests are unaffected. |

## What the sweep shows for the open fixes

Useful input for required fix 1, from the 84 triggers:

- The move commit `d9906114` fires for 23 files. All are pure renames.
- At least nine merges fire again for files their branch commits already triggered.
- A further group fires for files that add a component to an existing architecture, not a new one: vision towers, multi-token-prediction variants, draft models (for example `deepseek_v4_vision.py`, `mimo_v2_mtp.py`, `dflash2.py`).

So the explicit "not a new architecture" outcome will be used often, and it needs the same recorded reason and candidates discipline as a real selection. Git rename detection will handle the move and the earlier `gemma.py` rename without a curator claim.

For required fix 2: after `151edc00` every trigger has an empty architecture list, so every later selection's identity check currently rests on what the curator types.

## Not verified here

- Still no live Hugging Face recovery, by Astra or by me.
- I did not test a commit that adds a third, unknown directory alongside the known ones; the guard only fires when the known ones are empty.

## Next

Record this acceptance. Keep the walk stopped before commit 44 until the user's re-authoring answer arrives.
