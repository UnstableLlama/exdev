# Verdict: reference-evidence-and-callee-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/reference-evidence-and-callee-implementation-001.md`
Decision implemented: `reviews/verdicts/reference-evidence-and-callee.decision.md` (sha256 `e2a1425cc6f30db79646f2bead50be26e0a2500f63c3d0400b835ce5947f3fa7`)
Reviewed: 2026-11-13, working tree on top of `dfebc8a`

## Decision

**ACCEPTED for use on new packets** (walk input contract v5, guidance version 2), with three required fixes that are not needed for the next few positions but must land before the walk reaches the positions named below.

This is an implementation review. It approves no prose. Canonical and training remain false. The walk stays stopped before commit 44 until the user's answer on re-authoring commits 39 and 41 is recorded.

## Files reviewed (sha256)

All match the implementation report (`6a303806620417ad24b33d6d08210111e184af46641d875c8209b17f73b4c152`).

- teacher/architecture_evidence.py: `0e930b04c4ce99b9ddd1aceabd8d4c6f1796fb0def89f4d86027661eb5c6f2c7`
- teacher/root_evidence.py: `a9667859bcf136e487f02dea2927c6923799fdad9f4a96a9b1f92878739aba51`
- teacher/session.py: `cc43e49b6a05146a8aad31198b14bd62fa2a1813580b94e5677b01dde922f468`
- teacher/walk_inputs.py: `53c417da6ae2e18aa0d2cecc9941a0598cb6b2d80949cbb3b9aa466dfb038661`
- tests/test_architecture_evidence.py: `7833a3de3bad83f319b99bbc10b5753400fbb0c58e15f0c35148e28caaad5acf`
- tests/test_walk_inputs.py: `cee8197005783f740cfa18c2f64232e2df52bdddbfe5db320bca67663ecd9d24`
- docs/ancestor-context.md: `b5ff1e54aadb171c54a436357c8317b03def364bab2a9d9a8eb05a264a923b5b`

## Decision 1 (reference configurations), point by point

| Point | Result |
|---|---|
| 1. Trigger by trusted code | Met for the near term, with gaps; see "Trigger measured on the real history". The trigger parses the task and first-parent trees with `ast`; no teacher output is consulted. |
| 2. What is attached | Met. `config.json` and `tokenizer_config.json` are required, at least one safetensors header is required, and the file allowlist adds `tokenizer.json`, `special_tokens_map.json`, `added_tokens.json` and `generation_config.json`. `generation_config.json` is slightly beyond the decision's wording; it is a configuration file and I accept it. Headers are validated as metadata only. |
| 3. As of the cutoff | Met. The latest `main` revision at or before the cutoff is pinned; the bundle loader rechecks the report date and every object's `revision_at` and `created_at`; revisions must be 40 or 64 hex characters. No eligible revision returns no objects and a report. |
| 4. Selection recorded | Met as far as code can. A reason and the candidates considered are mandatory, at recovery and again at load. That the choice was made without later knowledge cannot be enforced by code; I will check it in each request that uses a selection. |
| 5. Offered, not explained | Met. Only `items` are passed to the packet builder; the selection reports stay in the bundle file. Object ids are `reference:<n>:hf:<architecture>:<path>`, with no note. |
| 6. Bound into the contract | Met. Contract v5 records the reference bundle hash, the reference object ids and their signatures; both `validate_contract` and `validate_bundle` recheck them. The existing referenced-evidence check now excludes reference ids, so the two gates stay separate. Contracts below v5 take the old path. |
| 7. Tests | Met: registry key, class file, neither, missing recovery, cutoff selection, no eligible revision, weights never fetched, binding, tampered bundle, weight-role rejection, legacy guidance. |
| 8. Documented | Met in `docs/ancestor-context.md`. |

## Decision 2 (changed-dispatch guidance)

Met. The sentence in `teacher/session.py` is the decision's wording verbatim. It is added only when the manifest has `guidance_version >= 2`, which only new walk packets set. It names no file, commit, architecture or defect.

## Checks I ran

| Check | Result |
|---|---|
| Tests | Full suite: 195 passed with pinned Codex 0.167.0 first on PATH. `git diff --check` clean. |
| Legacy prompts | I rebuilt the opening context for every run that has a packet on disk, once with this working tree and once with the committed code at `dfebc8a`. The result is identical: the same 9 recent runs reproduce byte for byte and the same 37 older runs do not. So this change alters no legacy prompt. (The 37 predate later guidance text; their replay is transcript-based, which is existing behaviour, not something this change introduced.) |
| Trigger on commit 39 | Returns `DeciLMForCausalLM` and `exllamav3/models/decilm.py`. Correct. |
| Trigger on commits 40 to 43 and on position 44 | No trigger. Correct. |

## Trigger measured on the real history

I ran the trigger over all 73 upstream commits that touch `exllamav3/models/`, to the pinned tip. It fired on 19, with no parse errors. Findings:

1. **It goes silent after the directory move.** Upstream commit `d9906114` "Refactor" (2025-08-07, about position 401) moves `exllamav3/models/` to `exllamav3/architecture/`. The trigger looks only under `exllamav3/models`, so from that commit on it returns nothing, for every one of the dozens of architectures added later. That is a silent fail-open: the walk would proceed with no reference evidence and no error. The report lists the path restriction as a limit, but the decision asked for the registry "or its successor".
2. **Registry keys stop being detected at `151edc00`** "Simplify architecture definitions" (2025-04-28, about position 102). From then on only the new-class-file trigger fires, with an empty architecture list. Two consequences: an architecture added to an existing file is missed, and the architecture-identity check becomes whatever the curator typed, compared only with the configuration the curator chose.
3. **Two false positives have no honest way through.** `151edc00` itself fires because `gemma.py` is renamed to `gemma2.py`, and merge `b2d05c0b` fires again for a file its branch commit already triggered. The loader accepts only `complete` or `no_eligible_revision`, so for a rename the curator would have to attach unrelated evidence or misreport that no revision exists.

None of these affects commit 44 or a re-authoring of 39 or 41.

## Required fixes

1. **Before position 100.** Add an explicit administrative outcome for a trigger that is not a new architecture (rename, move, merge of an already-covered branch commit), carrying a reason, and detect renames with Git so the common case needs no curator claim. It must not be usable when the registry-key trigger fired.
2. **Before position 100.** When the architecture list is empty, derive the architecture string from the new file itself (for example the string literal the config class passes as its architecture name) so the identity check does not rest on the curator's typing. If it cannot be derived, say so in the bundle.
3. **Before position 380, and preferably now because it is cheap.** Make the trigger fail closed when it cannot find where architectures live: if a non-root commit has no model or config classes in any directory the trigger knows, raise. Then extend the known locations to `exllamav3/architecture/`. Add a test for the moved-directory case.

## Minor

- `validate_contract` requires `guidance_version == 2` exactly; a later version 3 would be rejected. Use `>= 2` or tie it to the contract version.
- Two repositories for the same architecture overwrite each other's cache history file. Cosmetic.
- `no_eligible_revision` is a curator attestation; the commit history file is in the cache but not bound into the bundle. Bind its hash so the claim can be checked.

## Not verified here

- No live Hugging Face recovery was run, by Astra or by me. The recovery path was exercised only through mocks. The first real use (commit 39, if re-authored) should be reviewed as such: selection, pinned revision date, and that no weight bytes were fetched.
- Whether the header and file tools serve reference objects to the teacher correctly in a real session.

## Note for the first real selection

If commit 39 is re-authored, the curator choosing its reference model has seen my commit 39 verdict, including its hindsight section. The decision's rule therefore matters: choose from what the commit message names ("Nemotron") and what was public before the cutoff, list every candidate considered, and attach more than one if there is a real choice. I will check the selection against that, not against whether it exposes the defect.

## Next

Record this acceptance. Keep the walk stopped before commit 44 until the user's re-authoring answer arrives. Fix 3 can be done while waiting.
