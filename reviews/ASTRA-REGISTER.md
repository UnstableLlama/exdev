# Astra historical register — administrative only

Search this file for a specific obligation or verdict; do not read it whole after a reset.
Never provide it to a teacher.

## Durable register

The following is a lossless administrative carry-forward of verdict follow-up and
canonical-use sections plus journal dispositions as of implementation filing.
It includes historical/closed items so no obligation is lost: explicit later
acceptance/closure takes precedence. Entries without a closure remain for audit;
this register is not teacher evidence. New approvals append current follow-ups.

### architecture-trigger-fixes-implementation-001.md

Source: `reviews/verdicts/architecture-trigger-fixes-implementation-001.md` (sha256 `af76941abf69a669421f49d582fae781f0aa180a7185c8775a60d18c9d455835`).

**Things to carry**

- At `b2d05c0b` the registry-key detector finds nothing and only the derived identity fires. After `151edc00` the registry
  no longer has the dictionary shape the detector looks for, so from there on the derived identity and the unresolved
  list are the whole guard. That is what fix 2 was for; it works on the one case I could try.
- `curator_attestation` is the one path where a reason alone is enough: a new `*Config` or `*Model` class file with no
  registry key and no derivable identity. It is the right outcome for a helper class and the wrong one for an
  architecture written in a style the parser does not recognise. **Condition:** every bundle whose outcome basis is
  `curator_attestation`, and every bundle with a non-empty unresolved list, must be named in that commit's review
  request with the reason, and that commit gets a full review whatever the mechanical policy says.
- A merge that brings in a branch which added a registry key cannot use `covered_merge` and needs its own recovery at
  the merge. Stricter than necessary, and on the safe side. Leave it.

### closed-path-overlap-implementation-001.md

Source: `reviews/verdicts/closed-path-overlap-implementation-001.md` (sha256 `3cb4af9b7b1800145b5c2138c7f5adae421ac6585168cdc4397d20010f35ff99`).

**Conditions**

1. **Report it.** Each request for a commit authored under the new rule states how many catalog rows qualified by
   path alone and whether the cap truncated.
2. **Stop at the first truncation.** Ties among path-only rows are ordered by kind and then by rising number, so
   when more than 20 qualify, the newest discussions and all pull requests after the issues are the ones cut. With
   576 discussions by the tip that will happen. At the first position where a path-qualified row is cut, stop and
   propose an ordering before authoring that commit.
3. **No rewriting.** Bound bundles, packets and runs up to 151 are not regenerated, and the canonical-use condition
   on 150 stays as recorded.

### commit-000012-001.md

Source: `reviews/verdicts/commit-000012-001.md` (sha256 `1a74b12961c201b6481933e93f71d793ab788fa204fdb34ea003bb1bec91ee4f`).

**Follow-ups**

4. Record the `proxy_err` finding in the defect ledger from the commit 12 tree only, source-verified, not executed. No later history.
5. Add standing guidance: when recording a finding in a function, grep the parent tree for its callers and state the reach.
6. Tabulate r002: add an impact field (low; narrow trigger).
7. Note in the run record that the root quantizer chapter matched but was not read.
8. The scalar check used a symmetric H, so it does not exercise the draft's remark that symmetry is not required (the remark is algebraically true).

### commit-000013-001.md

Source: `reviews/verdicts/commit-000013-001.md` (sha256 `8be1c3365b70efd46271d5247353d1aec628dc758bf9e155d47dc1d8dc18b56f`).

**Follow-ups**

3. **New observation, reviewer-identified, pre-existing since the root commit.** In the tile-sampling loop (`for w in range(width):`), the loop variable `w` is never used; the column index is `((i + width) % tiles_n)`. By source inspection each sampled tile is appended `width` (3) times and the diagonal is shifted by a constant, not widened. Present at `543c4b2` line 335 and unchanged here. Consider a ledger candidate from the root tree, status suspected, effect on the search unassessed (duplicates do not change a mean; they do triple the work per evaluation). No later history.
4. Proxy-error ledger: add a revision recording that commit 13 (`08166e3`) is still affected, verified from that tree only.
5. Add standing guidance: when an ancestor entry read in the session records a defect in a file the task touches, check by source whether it persists at the task commit and say so either way.
6. The two commits are one minute apart with the same author (02:03:55 and 02:04:57 +02:00). That is a fact the entry may state; it supports no conclusion about intent.

### commit-000015-001.md

Source: `reviews/verdicts/commit-000015-001.md` (sha256 `8bf63b1b03f21ca236ae96530d9d2432ca9c208274d7ebc3e9e1aea8457c781b`).

**Follow-ups**

3. Ledger candidate for the double-prefix path defect: introduced at the root (`543c4b2`), fixed at `2591348`, source-verified, relative `work_dir` only, write outcome unestablished.
4. Ledger candidate for the checkpoint-rotation gap from the root tree, status suspected, recording that it is unchanged at commit 15. No later history.
5. Consider standing guidance: when a change corrects where something is written, grep for the code that reads it back.

### commit-000016-001.md

Source: `reviews/verdicts/commit-000016-001.md` (sha256 `8b64bfd25998b5c85fce8c6d56d176928307c5061981a3eb045cabbab75201f6`).

**Follow-ups**

4. Ledger candidate: `from typing import override` in the two sampler modules, present in the parent tree (check the root for introduction), fixed at `271c921`. Source-verified import chain; the Python-version fact cited to the Python docs as external evidence; not executed on 3.11. No `python_requires` is declared in `setup.py` at this commit, so the supported interpreter range is itself unestablished.
5. Consider standing guidance: when a change fixes an import, grep for what imports the affected module and state how far the failure reaches; and when a claim rests on a language or library version fact, cite its documentation or mark it unestablished.

### commit-000017-002.md

Source: `reviews/verdicts/commit-000017-002.md` (sha256 `eae5ef407a53bea243759d31d582e4ac08bf012f2cf64b1a6b16f148cb09dcc1`).

**Follow-ups**

1. **Truncation keeps the wrong end.** Items are sorted oldest first and cut with `items[:100]`, so once more than 100 are open the newest, which are the likeliest to concern the current commit, are the ones dropped. Keep the newest, or paginate.
2. **Hard-coded report name.** `recover_unreferenced_catalogs` always writes `reports/unreferenced-discussion-retrospective-002-016.json` with `report[:-1]`. Running it for a later position will overwrite the accepted audit with different contents under the same name. Derive the name from the range or stop rewriting it.
3. **Undocumented limit.** A comment that existed at the cutoff and was deleted later cannot be recovered and leaves no trace, so "available" means "everything still recoverable", not "everything that was visible". Say so in `docs/ancestor-context.md`.
4. The unreferenced-discussion guidance sits in the static system text, so it is sent even when a packet has no catalog. Gate it on the field, as was done for merge facts.
5. Recovery fetches full history for every issue up to the cutoff on each run unless `--reuse` is passed; note the cost before the walk reaches commits with hundreds of issues.

### commit-000017-003.md

Source: `reviews/verdicts/commit-000017-003.md` (sha256 `2b4f4297004a00fe66535fde0b3a50ea033e406ecf931b43145d066b3c39f6a7`).

**Follow-ups**

1. **Request file names the wrong commit message.** It gives the upstream title as "Fix compile from JIT install". The actual message, and the one the teacher received, is "Explicitly include extension sources for JIT install". The run is unaffected; correct the request text in a follow-up note rather than editing history silently.
2. **Bare file names over-match.** A path from an unrelated project hints a same-named root file: `File "/opt/other/project/setup.py"` yields `setup.py`, and `flash-attn/README.md` yields `README.md`. Suffix matching is what resolves checkout paths, so keep it for paths with a directory component, and require a stricter match for single-component paths (for example, drop them when the candidate has a different parent directory after prefix stripping). Navigation only, so not blocking.
3. **`teacher/walk.py` changed after authoring.** Its hash no longer matches this run's provenance. That is consistent with the later change to when walk stops publish status, and `walk.py` is not on the authoring path, but the local approval should confirm that its implementation check accepts or explains the difference rather than skipping it.
4. The teacher did not read the root usage-evaluation chapter this time (attempt 002 did). Report-only under policy; noted because the entry now has no ancestor link.

### commit-000018-001.md

Source: `reviews/verdicts/commit-000018-001.md` (sha256 `2dd6f118eee77c517fc2b4c1eada21b2de3b88a6b76d43a0f3ebf3bead0ec33d`).

**Follow-ups**

3. Ledger candidate, status suspected: `update_config` key-name mismatch introduced at `b73e159`, source-verified against the three model classes; the author's intent is unknown, so it may be a typo or a deliberately different key. No later history.
4. Consider standing guidance: when a change reads or writes a named configuration key, grep the tree for other reads and writes of that key and of near spellings.
5. `list_tensors` goes through `convert_dtype`, which raises on any dtype outside its five; whether a model directory can hold other dtypes under a leaf module's key was not assessed by the draft or by me.

### commit-000019-001.md

Source: `reviews/verdicts/commit-000019-001.md` (sha256 `8b057a73c8442329913d18be0b84ee709d990a8cb138467cb17a40512a2f3eeb`).

**Follow-ups**

3. Ledger candidate for `format-identifier-consumer-mismatch`: introduced at `c8b4bd5`, source-verified from that tree only, reach through `compile_model` and `util/add_quant_config.py`, not executed.
4. The two commits are four and a half minutes apart with the same author (15:27:17 and 15:31:51 +02:00); the entry may state that as a fact.

### commit-000022-001.md

Source: `reviews/verdicts/commit-000022-001.md` (sha256 `4f117caadfad4a9dfe0267481402fe5a35a731a02290a8123ad0561f99075cf7`).

**Follow-ups**

3. Ledger candidate for `negative-remaining-minutes`: introduced at `e0f26ed`, reviewer-executed against the function text from the diff (plain Python, no repository import), reach limited to the one print in `convert_model.main`. Display only; no effect on quantized output.
4. **Tier policy gap.** `approval_policy` flags `execution_claim` only when an annotation item has basis `execution`. This draft's only executed check sits inside a finding's verification (`scalar_transcription`), so the flag was not raised. It made no difference here because findings already force full review, but the reason list under-reports. Detect executed verification methods inside findings too.
5. The singular/plural logic prints "0 minute" and "-30 minute"; cosmetic, same function.

### commit-000023-001.md

Source: `reviews/verdicts/commit-000023-001.md` (sha256 `2d6a81656818fbd8189c37fe967b10022a1a8b9d61954a8d7a2210e58756aecf`).

**Follow-ups**

3. This commit is 67 seconds after commit 22 with the same author (02:42:52 and 02:43:59 +02:00); the entry may state that as a fact.

### commit-000024-001.md

Source: `reviews/verdicts/commit-000024-001.md` (sha256 `b4b7cfb78a6e7fff2772110c2efeefaf2af95910584e91577a8a63e1c09b1936`).

**Follow-ups**

5. Ledger candidate for the missing `devices` key: introduced at `72e88ae`, source-verified, reach limited to `tests/test_quant_fn.py` and any external caller of `Linear.convert_exl3`; not executed.
6. Ledger candidate for `scale-progress-premature-completion`: introduced at `72e88ae`, source-verified, display only.
7. Consider recording the resume behaviour (an omitted `--devices` resets a stored multi-device list to `"0"` with a warning) as an observation; whether it is a defect depends on intent, which is unknown.
8. Standing guidance: when a change makes a dictionary key or argument required, grep the whole tree, including `tests/`, for every place that builds that dictionary or calls that function. This run's search was restricted by path.
9. The tile-sampling observation from commit 13 is still present: the sampling loop in `g_scale_gss` is unchanged by this diff.

### commit-000026-001.md

Source: `reviews/verdicts/commit-000026-001.md` (sha256 `504979e633ba31f6408034444cefc29ecc6900c88442304cab7e3a9d4b631b9b`).

**Follow-ups**

4. Tabulate ledger: add a revision recording that the defect persists at `08cf8e9` and that the import now sits at `exllamav3/util/memory.py:67`, at function entry, verified from that tree only.

### commit-000028-001.md

Source: `reviews/verdicts/commit-000028-001.md` (sha256 `a14da6a19cea6fb6f1214064202d70163557a4716b37132a7fa28191392a80e9`).

**Follow-ups**

5. Ledger candidate for `negative-final-share`: introduced at `4d82aab`, reviewer-executed against the formula text (plain Python), exception type unobserved, reach conditional on tile count and ratios.
6. Ledger: the required-`devices` record should gain a revision noting it persists at `4d82aab`. `tests/test_quant_fn.py:139` still builds `quant_args` without `devices`; the new key is read with `.get`, so it adds no second failure.
7. Consider recording the silent ratio reset on resume as an observation alongside the devices one from commit 24; intent is unknown.
8. This commit is 74 seconds after commit 27 with the same author (10:41:12 and 10:42:26 +02:00); a fact the entry may state.

### commit-000029-001.md

Source: `reviews/verdicts/commit-000029-001.md` (sha256 `dbc48b0db738f5569d6f2dec1365db7c22b4fa234d244bd332ff11926a5630d9`).

**Follow-ups**

4. Ledger candidate for `shard-size-documentation`: introduced at `ae9f910` as a documentation defect; the underlying `type = int` and zero-threshold behaviour predate it (verify the introduction of the latter from the root tree). Source-verified, not executed.
5. Consider one ledger observation covering the resume resets (devices with a warning from commit 24, ratios silently from commit 28, checkpoint interval from earlier), now that the guide documents resume as restoring arguments.
6. Standing guidance for documentation commits: when a change documents options or defaults, check every documented statement against the parser and its consumers, not only the ones that look suspicious.

### commit-000030-001.md

Source: `reviews/verdicts/commit-000030-001.md` (sha256 `dbc623c864593811f8c09ed509694ac38fce9913dc8de1f5005824005cf1452a`).

**Follow-ups**

5. Standing guidance: when a commit message names a platform, product or error, grep the parent tree for that term before concluding nothing in scope bears on it.

### commit-000031-001.md

Source: `reviews/verdicts/commit-000031-001.md` (sha256 `597e1b8430a584ba0d5d8ec7421e4bf8c599ac7a85be3b69a19e8e9109a68bae`).

**Follow-ups**

4. Ledger candidates for the two decode findings: verify the introduction from the root tree, record as source-verified with this commit as a persistence point. No execution.
5. `self.special_delimiters` is now assigned in `__init__` and never used; `encode_unspecial` still does its own regex splitting. Facts for the entry, not defects.
6. This commit is 146 seconds after commit 30 with the same author (01:47:08 and 01:49:34 +02:00).

### commit-000032-001.md

Source: `reviews/verdicts/commit-000032-001.md` (sha256 `273d637ef1ba5c1ce36dc3981c866727fc8dc9ba4346eb6162599ed83fea4048`).

**Follow-ups**

6. **Guidance, pending the user's decision on catalog hints:** before finalizing, the teacher should compare catalog titles against the diff for shared numbers, identifiers and error text, and read any item that shares one. With eight items, reading all of them would have cost little. This is guidance only and does not change what the packet contains.
7. Ledger candidate for the fused-branch bias ordering: introduced at `1d77c05`, suspected, source-verified, reach conditional on a per-layer bias existing for a fused layer.
8. Ledger observation for the 32-versus-128 logits width: introduced at `1d77c05`, source-verified inconsistency, effect on `SeqTensor.append` unassessed.
9. Narrow the inherited-defect guidance so it applies to defects in the code the task diff touches, not to any defect ever recorded in the same file.

### commit-000032-002.md

Source: `reviews/verdicts/commit-000032-002.md` (sha256 `4e92800ceea5ff4310c92a94bddae9237d2b1656a6aae495ebc76c3c72aebeef`).

**Follow-ups**

1. **Two wire tests depend on whichever `codex` is first on PATH.** `test_codex_wire` errors with "Codex version has not been boundary-tested: codex-cli 0.169.0" now that the default CLI has updated. Failing closed is correct, but the tests should locate the pinned binary the way authoring does, or skip with a clear reason.
2. **`AGENTS.md` now exists at the repository root** (added by me at the user's request, pointing to `reviews/AUTHOR-INSTRUCTIONS.md`). The teacher sandbox does not mount the repository and this run's preflight shows no instruction sources, so it does not reach the teacher. Keep it that way: if authoring ever runs with the repository mounted, the adapter's inherited-instruction check will, correctly, abort.
3. The teacher read one ancestor entry (`c8b4bd54`) and recorded no link. Report-only under policy.
4. Carried from the commit 17 verdict and still open: bare file names over-match in path hints; `exllamav3_ext` packaging blocker.

### commit-000035-001.md

Source: `reviews/verdicts/commit-000035-001.md` (sha256 `7a39344c09a85853b7ea96b4ea74b67f95c5d93d2706405e6efdef04b51694b7`).

**Follow-ups**

3. Ledger candidate for `detach-count-diagnostic`: introduced at `4fa0e68`, source-verified; reviewer-level reach: no in-tree caller; the wrong exception type appears only when counts already mismatch.
4. This commit is authored two and a half minutes after commit 34's commit time and committed 100 minutes after it (34 at 00:38:31, this one authored 00:41:08 and committed 02:18:35 +02:00). Facts only.

### commit-000037-001.md

Source: `reviews/verdicts/commit-000037-001.md` (sha256 `c634399106f87dce4e83761a94485d4e571a7e57494d213bf87836f6deaceefd`).

**Follow-ups**

1. The teacher's ancestor search for "remaining" in `convert_model.py` returned no matches, and it did not read the entry that introduced the estimate (`e0f26ed1`, "More feedback from conversion"), linking the time-formatting entry instead. Report-only under policy, but it is a second example of search by symbol missing the obviously relevant ancestor. Worth a look at what the search indexes.
2. Carried and still open: wire tests depend on the default `codex` on PATH; bare file names over-match in path hints; commit 17 packaging blocker; commit 32 canonical items.

### commit-000038-001.md

Source: `reviews/verdicts/commit-000038-001.md` (sha256 `067c602831a044983ec4e8ecb35834fea2e169db4298bdea7f35991e786ab201`).

**Follow-ups**

1. **Reading rule, borderline case.** The teacher read the two error-titled issues (7, 12) but not PR 13 ("Fix a tokenizer issue while converting models..."). Its path hints do not match this task, so the only question is whether that title "reports an error or failure". I read it as a fix title, not a report, so I do not count this as a miss. If the user wants fix-titled PRs read under the ten-item rule, that is a wording change for a decision file.
2. The items read (7, 12) are in the ledger but not mentioned in the prose. That is fine for unrelated items; noting it because the commit 37 draft handled the same two items by describing them, so the two entries are inconsistent in style.
3. Carried and still open: wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000039-001.md

Source: `reviews/verdicts/commit-000039-001.md` (sha256 `3ebc1c674fbd04e28f0732bc7e56f4015d4d3a6cdbf65ac4882e9e59338d9f50`).

**Follow-ups**

1. **For the user, not decided here: reference evidence for new-architecture commits.** The root entry was authored with pinned Hugging Face configurations and tensor headers. This commit, which adds a new architecture, was authored with an empty evidence catalog, and the draft's main limit is exactly that. If a Nemotron configuration dated before the cutoff had been attached, the head-count mismatch would probably have been visible. Whether the curator should attach cutoff-eligible reference configurations when a commit registers a new architecture is a policy question. I am raising it, not holding the walk for it.
2. When the walk reaches position 44, check that the fix's entry names this commit as the introduction and that the ledger record is extracted then.
3. Carried and still open: wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000039-002.md

Source: `reviews/verdicts/commit-000039-002.md` (sha256 `7853c45af864843e3ce639e0f5a3f7c71dc4dd9d581799219671e42bc996ce33`).

**Follow-ups**

1. **For the user, forward-looking only, no action needed now.** When several reference models are attached, the teacher may read just one. A general rule could say: read every attached `config.json` before stating that a mapping is corroborated, and say which were read. I am not recommending it be applied to commit 39, for the reason above. If the user wants it for future new-architecture commits, it is a one-sentence guidance change and a decision file.
2. Required fixes 1 and 2 from the implementation verdict remain due before position 100.
3. Carried and still open: wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000039-005.md

Source: `reviews/verdicts/commit-000039-005.md` (sha256 `ead08fe973e3b31b1812a7e9607f4f925f60593b1f3d49e529f4d0a10c13935a`).

**Follow-ups**

- Defect ledger `exllamav3-decilm-kv-head-count`: this entry is an authoring-time observation at the introducing commit. Record it as another observation on the same defect, not a new one.
- The empty-block finding is the same hazard attempt 004 reported; one defect, two observations.

**Must fix before canonical use**

Reviewer-only. None of this goes to a teacher.

1. The entry is reviewer-assisted. Whoever selects entries for canonical use or training decides whether assisted entries qualify.
2. The head-count finding says the declared widths disagree with the headers and stops there. It does not say what `n_heads_in_group` means. The stored widths in the sampled blocks equal query heads divided by that field, times the head dimension. A canonical entry should say so or say it was not established.
3. The finding's trigger names "block 1 of the inspected 51B model". True as a statement about the declaration, but that model fails the block 11 assertion during construction and never reaches a load. One clause would make that clear.
4. The 51B comparison covers blocks 0 and 1. That model has other group sizes on later blocks which the entry did not sample.
5. The failed fetch of the Ultra safetensors index is in the transcript and not mentioned in the entry. It was not a configuration read, so the guidance did not require it.

### commit-000040-001.md

Source: `reviews/verdicts/commit-000040-001.md` (sha256 `4a052f0d6c41de21c58a1e873e3008333967a7403acd67ac1613fc15532e0aa3`).

**Follow-ups**

1. Carried and still open: the user's pending question on reference evidence for new-architecture commits; the position 44 ledger check; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000041-001.md

Source: `reviews/verdicts/commit-000041-001.md` (sha256 `0612d55613a87a4f3b7181eec4193a9e1d0554f313f98135b3c242b9f2b84c76`).

**Follow-ups**

1. **Pattern worth watching, no action requested.** This is the third recent draft whose stated limit was "the source does not explain why", where a nearby file in the parent tree did bear on it (commit 37: the entry that introduced the estimate; commit 39: the head-count naming; here: the kernel selector). The standing guidance has targeted rules for dependencies, callers, keys and message terms, but nothing that says to follow a changed dispatch into its callee. Whether to add one is a guidance change and therefore a user decision.
2. Carried and still open: the user's pending question on reference evidence for new-architecture commits; the position 44 ledger check; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000041-002.md

Source: `reviews/verdicts/commit-000041-002.md` (sha256 `1d2397adea42322688ac99887c28612a5f1ba22f3ebe62fc40ddf10dfec818ba`).

**Follow-ups**

1. The teacher read ancestor `897e20a2` again and this time recorded no link or note. Report-only.
2. Required fixes 1 and 2 from the implementation verdict remain due before position 100.
3. At position 44, the administrative ledger check from the commit 39 verdicts applies. It is not teacher input.
4. Carried and still open: the future-only "read every attached configuration" question for the user; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000042-001.md

Source: `reviews/verdicts/commit-000042-001.md` (sha256 `cb64919a751cf707a8eb13785a52e5f53ed46f463386a77e57a906470ba930f3`).

**Follow-ups**

1. **For the walk, next two positions.** Position 43 is the merge of PR 13 and position 44 is the DeciLM fix. At 43, PR 13 becomes eligible evidence (it was open before the merge) and the merge policy applies. At 44, the administrative ledger check from the commit 39 verdict applies. Neither is to be signalled to the teacher.
2. The teacher made no ancestor read and recorded no link. Report-only.
3. Carried and still open: the user's two pending guidance questions (reference evidence for new architectures; following a changed dispatch into its callee); wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000043-001.md

Source: `reviews/verdicts/commit-000043-001.md` (sha256 `29632c9c2934a193130263cf3620adec7eb8d4dded0400ccfbd46c843bc3d7bb`).

**Follow-ups**

1. Carried and still open: wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; the position 44 ledger check; earlier canonical items.

### commit-000044-001.md

Source: `reviews/verdicts/commit-000044-001.md` (sha256 `a80590ee6a884c6b6c7c7af4e0b987b63a6e1a86cacb838feb187fa99620740b`).

**Follow-ups**

1. **Evidence does not carry forward.** Reference objects attached at commit 39 were not offered to this teacher, although they are older than this commit's cutoff and directly relevant. Whether reference evidence attached at an ancestor should be re-offered to later commits that touch the same architecture file is a design question for the user. Not urgent.
2. **Existing ledger files.** Five older files under `reports/defect-ledger/` have origin `reviewer_observation`, which `validate` rejects ("Unknown origin"), so `eligible_revisions` fails if it is given the whole directory. This predates today's work. Either the validator should know that origin or those files belong elsewhere.
3. Required fixes 1 and 2 from the implementation verdict remain due before position 100.
4. Carried and still open: the future-only "read every attached configuration" question; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000044-003.md

Source: `reviews/verdicts/commit-000044-003.md` (sha256 `dc8ee756455157d226e18bcf2bf1d2ce8d59574a923ca2fa5f6328208daf782f`).

**Follow-ups**

- Defect ledger: the two findings are observations of defects first reported at commit 39 (the empty-block division) or of a limitation stated there (51B linear attention). One record each, several observations; no new defect.
- Ledger `exllamav3-decilm-kv-head-count` r002 can cite this entry as the fix's own corroboration from cutoff-eligible evidence.

**Must fix before canonical use**

Reviewer-only.

1. Reviewer-assisted; the selection of assisted entries for canonical use is undecided.
2. The Problem line says the checkpoints "require" the quotient, labelled source. The evidence is sampled blocks, as the limits section says. A canonical entry should carry that bound in the sentence.

### commit-000045-001.md

Source: `reviews/verdicts/commit-000045-001.md` (sha256 `bedee88d122fc790d400d6ae29e3bd6289d23c7323cac091bba7cce2214e2da6`).

**Follow-ups**

1. This is another case for the carry-forward question raised at commit 44: the DeciLM reference configurations attached at commit 39 would answer item 2 directly, and were not offered here. Still a design question for the user, still not urgent.
2. Required fixes 1 and 2 from the implementation verdict remain due before position 100.
3. Carried and still open: the future-only "read every attached configuration" question; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000045-002.md

Source: `reviews/verdicts/commit-000045-002.md` (sha256 `b64db4aa76f32df33e7b13f1893628a3d41953b3b87aae3fc92c61a6ce3c6251`).

**Follow-ups**

- Defect ledger: this is the fix for the empty-block division first reported at commit 39 (attempts 004 and 005) and carried in 44/003. One defect, with introduction at 39 and fix here. A fix-derived record is not needed for discovery, since the introducing entry found it from eligible evidence; record it as authoring-time with this commit as the fix.

**Must fix before canonical use**

Reviewer-only.

1. Reviewer-assisted; selection of assisted entries is undecided.
2. The entry says the compiler "skips modules whose tensor-size list is empty", from source. Whether the collection can open a file with no tensors at all is the same unexecuted question as the save, and a canonical entry should join the two.

### commit-000046-001.md

Source: `reviews/verdicts/commit-000046-001.md` (sha256 `b91167e441558f90e4292726555177ad94513ebca865876b20fa071a03f51d17`).

**Follow-ups**

1. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward question and the future-only "read every attached configuration" question for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000047-001.md

Source: `reviews/verdicts/commit-000047-001.md` (sha256 `3e2b217ad396eaee2b9821188c01164d2e8857d9e92c584e83b789b74ee701b9`).

**Follow-ups**

1. The teacher made no ancestor read and recorded no link, although commit 45 and earlier entries describe the same converter loop. Report-only.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000048-001.md

Source: `reviews/verdicts/commit-000048-001.md` (sha256 `04e9a360de794f7eaac2d3bbcef69bb00f109d9127023ea377cb3682b088b6a5`).

**Follow-ups**

1. Good example of ancestor search working: a search by file found the right earlier entry. Contrast with the commit 37 miss, which was a search by symbol word. Useful for whoever looks at the search-indexing follow-up.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; bare file names over-match in path hints; earlier canonical items.

### commit-000049-001.md

Source: `reviews/verdicts/commit-000049-001.md` (sha256 `87ad4e303ba0bcc383a70bdb30b1243238fbdfdfeeb6e1299f9af2cee840c10f`).

**Follow-ups**

1. The teacher made no ancestor read and recorded no link, although commit 47 two positions earlier is another VRAM change in the same function. Report-only.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000050-001.md

Source: `reviews/verdicts/commit-000050-001.md` (sha256 `26d61e568e1bc62593f202f89405d2b51b0cae24c0e035d4c2eeaa2f025fa1c7`).

**Follow-ups**

1. **Validation reports carry no run identity.** Two different runs produced byte-identical reports, so the hash in a request no longer shows which run was validated. Add the run directory and the draft hash to the report.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000051-001.md

Source: `reviews/verdicts/commit-000051-001.md` (sha256 `4ac5e7e3a5efa650235a59220c938d009a481e2562fbd6edc9d97c9abba35ce4`).

**Follow-ups**

1. Four consecutive commits (47, 49, 50, 51) are one VRAM series in the same function. Each draft links at most its immediate parent. Report-only, but a canonical pass will want the series stated once.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000052-001.md

Source: `reviews/verdicts/commit-000052-001.md` (sha256 `ec66afcf99abf7a42a1cb130af96c085270f4f5198c9cb47f4d9ed2e91ed9642`).

**Follow-ups**

1. **Ledger handling of inherited findings.** The read-wait observation now exists in the root chapter's prose and as a structured finding here. If it is extracted to the defect ledger, it should be one defect with two observations and an introduction at the root, not a new defect introduced at this commit. The finding's own location (the parent tree's `stloader.cpp`) supports that.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000053-001.md

Source: `reviews/verdicts/commit-000053-001.md` (sha256 `ff3f96f491da995fe8888a05853ca038cb941a2fd481acd1962845073c9a0110`).

**Follow-ups**

1. **The inherited finding will keep recurring.** It now appears in the root chapter, commit 52 and commit 53, and the rule will repeat it in every later entry that reads one of those and touches the loader's data flow. That is the rule working, but for the ledger it must stay one defect with several observations. Worth deciding how the ledger extraction de-duplicates before the count grows.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000054-001.md

Source: `reviews/verdicts/commit-000054-001.md` (sha256 `c48b100abbd70952cd2ef0565080645568701e2f4d0eb28fa97dee999d1544f8`).

**Follow-ups**

1. The teacher read one ancestor entry (`41717916`, the reconstruct-threshold change in the same file) and recorded no link. It did not read commit 47's entry, which is the one that bears on item 1. Report-only.
2. Carried and still open: required fixes 1 and 2 before position 100; ledger de-duplication of the inherited read-wait finding; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000055-001.md

Source: `reviews/verdicts/commit-000055-001.md` (sha256 `96860481f622da61d2ed2dcf168b7345524f39f3c2988c18d4014c3134535995`).

**Follow-ups**

1. **Retrieval is the weak point of this entry.** The policy keeps retrieval report-only, and I am not asking for that to change. But this is the clearest case so far where reading nothing produced a correct yet incomplete entry: four direct ancestors, three live findings, none consulted. It is also a third case for the reference carry-forward question, since the Nemotron configurations would show which models this commit is for. Both remain questions for the user.
2. Carried and still open: required fixes 1 and 2 before position 100; ledger de-duplication of the inherited read-wait finding; the "read every attached configuration" question; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000055-002.md

Source: `reviews/verdicts/commit-000055-002.md` (sha256 `b25a2ab46c220f7c20e4d1ba1446e0e26e1e9c9b13185f031b255bc42da37f50`).

**Follow-ups**

- Defect ledger: `inherited-native-read-wait` and `inherited-split-source-group` are further observations of existing defects (root and commit 52). `unaligned-tail-padding` is a further observation of commit 53's finding with a new caller. Only the two allocation findings originate here, and attempt 001 already reported them.
- Still open and unchanged: required architecture fixes 1 and 2 before position 100; the five older ledger files with an origin the validator rejects.

**Must fix before canonical use**

Reviewer-only.

1. Reviewer-assisted; selection of assisted entries is undecided.
2. The tail-padding trigger is a synthetic width (55,297). Every DeciLM width is a multiple of 256, so the last slice of each over-threshold layer in the reference models is aligned (I checked all four). A canonical entry should say the finding is not reached by the models this change serves.
3. Execute the per-slice pass once and confirm that attention is quantised N times, or keep it as source reading.

### commit-000056-001.md

Source: `reviews/verdicts/commit-000056-001.md` (sha256 `2f88b04c4098bf6870e75e983098171ab0fd289c2948378c87a7be762bd8860f`).

**Follow-ups**

1. Carried and still open: required fixes 1 and 2 before position 100; the commit 55 canonical items; ledger de-duplication of the inherited read-wait finding; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000057-001.md

Source: `reviews/verdicts/commit-000057-001.md` (sha256 `3021688569e99bca149fa731e376e1597bcca78b14323c3fd29cfa26cb8b1776`).

**Follow-ups**

1. This commit changes one string literal in a `.py` file and still takes a full review, by the policy's rule that any `.py` path is non-mechanical. That rule is doing its job; I mention it only because a run of such commits will set the pace of the walk.
2. Carried and still open: required fixes 1 and 2 before position 100; the commit 55 canonical items; ledger de-duplication of the inherited read-wait finding; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000058-001.md

Source: `reviews/verdicts/commit-000058-001.md` (sha256 `f21f118c0f1ad66034efbab3ab485f1192336afa3b02665b44b088003e2d207a`).

**Follow-ups**

1. Carried and still open: required fixes 1 and 2 before position 100; the commit 55 canonical items; ledger de-duplication of the inherited read-wait finding; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000059-001.md

Source: `reviews/verdicts/commit-000059-001.md` (sha256 `75c50448b9cd99c2649fc138ffe021bdbfd435c340b4eecfca35faae3acdd045`).

**Follow-ups**

1. Carried and still open: required fixes 1 and 2 before position 100; the commit 55 canonical items; ledger de-duplication of inherited findings (now two: the read-wait risk and the reasoning-boundary loss); the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000060-001.md

Source: `reviews/verdicts/commit-000060-001.md` (sha256 `7884281d7ab5301edf57e9d2b5b930e0d3fb54a78912a925f01f973f6b19479c`).

**Follow-ups**

1. **Is re-recording this finding here within the rule?** The inherited-defect rule covers "code directly touched by the task diff or its changed data flow". This diff touches a different class in the same file and does not change the flow through `Streamer_rich.stream`. The teacher re-recorded the finding anyway. It is harmless and accurate, but it shows the rule being applied by file proximity, which will multiply duplicates. For the ledger it remains one defect (introduced at commit 58) with observations at 58, 59 and 60.
2. Carried and still open: required fixes 1 and 2 before position 100; the commit 55 canonical items; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000061-001.md

Source: `reviews/verdicts/commit-000061-001.md` (sha256 `437317d688d41bb360e3fee1184aba9e19e9c3416d43dd1116f310f212d4c950`).

**Follow-ups**

1. Carried and still open: required fixes 1 and 2 before position 100; the commit 55 canonical items; ledger de-duplication of inherited findings; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

### commit-000062-001.md

Source: `reviews/verdicts/commit-000062-001.md` (sha256 `dec7514ebcce70e4fe2668d61c5618009ec9d209150160ea561bfc8666eacf0c`).

**Must fix before canonical use**

Reviewer-only.

1. The finding stops at capacity. The same wrapper also does not check that the two outputs are float32, on the input's device or contiguous, or that the input is contiguous or non-empty (an empty input divides by zero in the normalisation). A canonical entry should list the unchecked preconditions together.
2. The file-match hints named five ancestor entries for these files and none was read. Nothing in the entry depends on them, so this is a note, not a gap.

### commit-000063-001.md

Source: `reviews/verdicts/commit-000063-001.md` (sha256 `d7b6f2bee59636b020254dd0e96aed2f1f16aa463e999a075c37b366606c11e1`).

**Must fix before canonical use**

Reviewer-only.

1. The entry does not say when the constant index was introduced. Git shows it in the initial commit, so every conversion before this one sampled a single wrapped diagonal three times over. A canonical entry should say so and link the root entry's quantizer chapter, which the file-match hints named.
2. The inherited progress finding is a further observation of commit 24's finding, not a new defect.

### commit-000064-001.md

Source: `reviews/verdicts/commit-000064-001.md` (sha256 `a1d38487733ccc203142c9d02be4953b372d6ee810c26509d5c2878e45b52e7b`).

**Must fix before canonical use**

Reviewer-only.

1. Four issues were fetched and the entry says nothing about them. Nothing needed saying, but earlier entries note that the open discussions were inspected and found unrelated; a canonical entry should be consistent about that.

### commit-000065-001.md

Source: `reviews/verdicts/commit-000065-001.md` (sha256 `d591a347af99cda24206ff75355c273a99743368379e3304f3f5265b5c057bef`).

**Must fix before canonical use**

Reviewer-only.

1. The Source Notes sentence about the ancestor entry is labelled inference and cites the ancestor read; other entries use the `ancestor` label for what an entry reports and a separate source sentence for what this commit does to it. Split it the same way.
2. The partial-frequency read is a further observation of a root finding, not a new defect.

### commit-000066-001.md

Source: `reviews/verdicts/commit-000066-001.md` (sha256 `73ae32f1a5c9eb4ef1a99b1e7cde3cb5545b985a00f409b1adb44f87e62febaf`).

**Must fix before canonical use**

Reviewer-only.

1. The entry says the converter "prints the actual decision" but not how it gets it: `quantize_exl3` writes the decision and the global scale back into the caller's `quant_args` dictionary. The converter builds a fresh dictionary per layer, so nothing leaks, but a caller that reused one dictionary would turn the first layer's automatic decision into a forced policy for the rest. A canonical entry should state the write-back.
2. Following from the resume behaviour the entry describes: a job started with a forced policy and finished after a resume without the switch records `auto` in its metadata. The entry has both halves and does not join them.
3. `g_scale_gss` is now always called with verbose off, so its own final message can no longer print; `regularize` prints the equivalent.
4. The progress finding is a further observation of commit 24's defect, not a new one.

### commit-000068-001.md

Source: `reviews/verdicts/commit-000068-001.md` (sha256 `2277284e35f1b41425860c7c133779580dbd27b147a9a7a036235b25550e66d2`).

**Must fix before canonical use**

Reviewer-only.

1. The run read commit 53's entry and four issues, and uses none of them in the text. Harmless; a canonical entry would drop the unused evidence or say why it was consulted.

### commit-000069-002.md

Source: `reviews/verdicts/commit-000069-002.md` (sha256 `87f680619291552efc74bb6379e22a8a0ef66f3cc3e36d23868a2d477fe3253c`).

**Follow-ups**

1. **`run` as a file reader.** This is the first run that used `run` to print parent-tree files, eleven at once and then by line range. The content is legitimate and the calls are in the ledger, but they bypass `repo_read`: no paging record, the claims they support are labelled source while citing an execution call, and anything that counts files read from `repo_read` calls will miss them. Astra should decide whether that is acceptable or whether `run` output that reproduces repository files should be detected and reported. Not blocking.
2. Commit 69's third attempt, under the salience catalog, should be unassisted, as the decision file says. Whichever approved attempt is fuller will be in force.

**Must fix before canonical use**

Reviewer-only.

1. Reviewer-assisted; selection of assisted entries is undecided.
2. The entry is long for a one-line change because it lists every caller, including the ones with short fixed prompts. A canonical entry can keep the callers that matter (calibration, evaluation, chat, generator) and summarise the rest.
3. The motivating discussion exists and was not offered. That is the subject of the pending re-authoring, not a fault of this entry.

### commit-000069-003.md

Source: `reviews/verdicts/commit-000069-003.md` (sha256 `1996e9dfaa8111f96e4d24112c1b07dc603cb9120566c8ba7012fd4e7315b5b7`).

**Follow-ups**

- Defect ledger: issue 16 is a reported failure with a maintainer diagnosis and this commit as its remedy, all before the cutoff. It can be recorded without hindsight.
- The audit expectation stands: issues 99 and 233 should appear at positions 560 and 1100.

**Must fix before canonical use**

Reviewer-only.

1. The entry covers `split_raw` only. Attempt 002 found that the article-based path and both evaluation scripts are affected in the same way. A canonical entry should take one sentence from 002 for them.
2. `num_tokens` is listed under what the override covers. True, and it has no caller, as 002 established.

### commit-000070-001.md

Source: `reviews/verdicts/commit-000070-001.md` (sha256 `a9cabe97c545eae198314712ef3e7d2efc0d1f66639a0a51a48f78942dd03316`).

**Must fix before canonical use**

Reviewer-only.

1. The entry says the 1e-10 offset cancels "in exact arithmetic". A canonical entry could add the plainer fact that 1e-10
   is far below float32 resolution for logits of ordinary size, so the addition changes no stored value at all there. Not an
   error in the entry.
2. Issues 7 and 15 were read and reported as unrelated. Accurate; a canonical entry would likely drop the paragraph.

### commit-000071-001.md

Source: `reviews/verdicts/commit-000071-001.md` (sha256 `b183c268c5b14d64b276b3b12486ebee84928dcca9b4f24455fe515cc72a19d8`).

**Must fix before canonical use**

Nothing beyond the points above.

### commit-000071-002.md

Source: `reviews/verdicts/commit-000071-002.md` (sha256 `5ad9bfdfaeec6003368657487476d692bba986e1ba59c96d820a68a447fe559b`).

**Follow-ups**

- Open thread, unchanged: whether `run` calls that print repository files should be counted as reads. Four of five here.
- The finding is recorded in the draft only; no ledger revision was submitted.

**Must fix before canonical use**

Reviewer-only.

1. The entry says the parent forward "passed only suh to the input transform, including when packed su was retained",
   and stops there. For a packed-only layer `suh` was None at the parent, so its forward applied no input sign flips at
   all, while `get_weight_tensor` (had it not raised on the tensor truth test) would have applied them. That looks like
   a parent defect for packed-scale models, present since the initial commit and repaired here by the constructor
   conversion. The entry has both facts and not the consequence. A canonical entry should state it, and it is a
   candidate for the defect ledger once someone establishes whether packed-scale models were ever published.
2. Likewise `if self.su` on a multi-element tensor raises; the entry calls it a "tensor truth test" without saying so.
3. This entry is reviewer-assisted. Its use beyond ancestor retrieval waits on the user's decision.

### commit-000072-002.md

Source: `reviews/verdicts/commit-000072-002.md` (sha256 `014fd6b931e3dec4c2ba4cfc9dd98048a70bb3eafd9ad34460a2ebd9eebb2ffa`).

**Follow-ups**

- The finding is in the draft only. When it goes to the ledger, establish the introducing commit (the kernel has two
  commits of history: the initial commit and `bcc09666` "RoPE kernel: Add GPTJ mode") and keep it one defect.
- Open thread, unchanged: `run` calls that read repository files.

**Must fix before canonical use**

Reviewer-only.

1. The headers of the three models I examined at 72/001 show only the fused `gate_up_proj` in every layer, with no
   separate gate or up tensors. The entry calls the fused key a "fallback", which is right about the code and
   understates the fact that it is the only form these checkpoints use. The same headers show `q_proj`, `k_proj` and
   `v_proj` biases in the 9B and none in the 32B, which settles what the entry leaves to "by their presence"; and that
   all tensors are BF16. A canonical entry should read the headers.
2. This is the first model definition to use what commit 71 added: the MLP's FP32 output now reaches the down
   projection's GEMM destination, and `interm_dtype = torch.half` is the value 71/002's finding says works. The entry
   reports the dtypes without the link; it read commit 39's entry and not commit 71's.
3. I held back the one assisted attempt for these two points. They are omissions of corroboration that the entry
   declares, not gaps that mislead a reader, and an unassisted entry with its own confirmed finding is worth more than an
   assisted one that adds them.

### commit-000073-001.md

Source: `reviews/verdicts/commit-000073-001.md` (sha256 `99052b35466d358b614258fa9f9ee65d50615ca2ba0390388a3df277b12108dc`).

**Must fix before canonical use**

Reviewer-only.

1. Issue 19 ("Any chance of a single model file?") is new in the catalog and is neither read nor mentioned. Its title
   reports no failure, so the rule did not require it. A canonical entry need not mention it.
2. The request text should give the catalog count from the bundle, not from memory.

### commit-000074-001.md

Source: `reviews/verdicts/commit-000074-001.md` (sha256 `aaed45c7429f06b6a1f4022de87c658b02c2162647f038ede9ee1733f84be12b`).

**Follow-ups**

- Validation marks a run incomplete when a binary section is unread. A binary section should be recorded as unreadable
  so that "incomplete" keeps its meaning.

**Must fix before canonical use**

Reviewer-only.

1. The figure is the only quality evidence the commit carries and no entry can describe it. A canonical entry needs a
   human or an image-capable pass to say what `cq_humaneval.png` shows.
2. The README hunk (cache quantization removed from the two to-do lists) is read and not mentioned.
3. The launch geometry of the paged encoder uses `ceil(warps / ceil(warps / 32))` warps per block. When the number of
   32-value groups per token is above 32 and not a multiple of the block count, the last block of a token runs one or
   more warps past the token. I did not work out whether any supported model has such a width; the test's dimensions
   would show it only if one of them does. Worth a look by whoever next reads this file.

### commit-000076-001.md

Source: `reviews/verdicts/commit-000076-001.md` (sha256 `570c27fce971d8e48f6439fdbc65b4973ee2c01ec76ccbdd579bf6cca25c3248`).

**Must fix before canonical use**

Reviewer-only.

1. `single-device-progress` is classed `behavior_change`. Nothing that worked before changed; a new interface is
   incomplete on one branch. A canonical entry or ledger record should class it accordingly.
2. The `load_gen` docstring added here ends mid-sentence ("Don't specify a callback function when using the"). The
   entry does not mention it.

### commit-000077-001.md

Source: `reviews/verdicts/commit-000077-001.md` (sha256 `f1f7748fd4963093dd51037917b465ac55ba98bfacb3a6ba6ee5ec7f2d700616`).

**Follow-ups**

- The finding is another observation on `exllamav3-cache-detach-count-diagnostic`, not a new defect.

### commit-000079-001.md

Source: `reviews/verdicts/commit-000079-001.md` (sha256 `eee4ec398cbbcd3970f16e19816db7854d1a89d133ed6081b3b58512096def68`).

**Follow-ups**

- When this finding goes to the defect ledger, record it as one defect covering the four `K - 1` sites, introduced at
  this commit, with this run as the observation for two of them and this verdict as the pointer to the other two.

**Must fix before canonical use**

Reviewer-only. None of this goes to a teacher.

1. The finding names two of the four sites. `reconstruct` and `quantize_tiles` index their tables with `K - 1` in the same
   way and have no range check on K either (`reconstruct` checks only the packed width; `quantize_tiles` derives
   `edges = 65536 >> K` and checks tensor shapes against it). `reconstruct` is the one on the model-loading path:
   `exllamav3/modules/quant/exl3.py` calls `ext.reconstruct(w, self.trellis, self.K)`. A canonical entry should state
   the finding for all four, and say where `self.K` comes from.
2. The finding gives K = 9 as the trigger. K = 0 or negative indexes before the array in the same way.

### commit-000080-001.md

Source: `reviews/verdicts/commit-000080-001.md` (sha256 `5c370be828374bdd27db8488aa730dfe0a32ccee508258aed75bf933e8bf514b`).

**Must fix before canonical use**

Reviewer-only.

1. The equality example (threshold exactly 0.04 keeps the 0.04 token) is binary64 arithmetic. The repository computes in
   float32, where a boundary token may fall either side. The entry labels the check as binary64 but a canonical entry
   should not present the boundary case as the sampler's behaviour.

### commit-000081-001.md

Source: `reviews/verdicts/commit-000081-001.md` (sha256 `a6e3baf4b4b17cf87dbaa8647b009ed842c0e3a0ea556143ab4c7430db35ecd4`).

**Must fix before canonical use**

Reviewer-only.

1. `top-p-description-mismatch` is classed `defect`. It is a documentation mismatch: the code did not change and matches
   its older description. The ledger classification should say so, and should not imply which of the two is intended.

### commit-000082-001.md

Source: `reviews/verdicts/commit-000082-001.md` (sha256 `6afe0d531efa38f7c63c7dd98171a93ff599e1d01d8285871f6a5deea82448a3`).

**Must fix before canonical use**

Reviewer-only.

1. The entry does not say that `torch.multinomial` returns shape `(rows, 1)` where the other sampling branches produce
   `(rows,)`, nor that `expect_sample`, if a case ever used it, is built as a float tensor. Both are small; neither is
   wrong in the entry.

### commit-000084-001.md

Source: `reviews/verdicts/commit-000084-001.md` (sha256 `5f3252977a5b1cf712f532157ac0ef06bd5d95ddd7b465a070851cf1fc658644`).

**Must fix before canonical use**

Reviewer-only. None of this goes to a teacher.

1. The entry says compatible activation widths "remain a caller-side requirement" and stops. It does not look for a
   caller that pads activations. After this commit a layer whose input width is not a multiple of 128 holds a wider
   weight than the activations it is given, and `capture_H` allocates its matrix at the padded width. A canonical entry
   should say whether anything in the tree widens the activations, or say that nothing was found.
2. The same padded width is passed to `load_exl3`, so an already converted model with such a layer is asked for a
   different input width than it was converted with. Not mentioned.

### commit-000086-001.md

Source: `reviews/verdicts/commit-000086-001.md` (sha256 `a58dc0a27ad59c8f43aeae8925286d6d6842b36a88a29806c67c9cc945142994`).

**Must fix before canonical use**

Reviewer-only. None of this goes to a teacher.

1. The both-axes observation is `simultaneous-axis-padding (defect)` in 84/001 and
   `simultaneous-padding-restriction (new_requirement)` here. It is one identity. The reclassification is defensible:
   the discussion shows the authors chose to leave it an error. The ledger should carry one record with both
   observations and say that the limitation was accepted in pull request 20, not two records.
2. The pull request says Reka Flash 3 "has both output and input sizes that are not divisible by 128". The entry does
   not ask whether the accepted one-axis restriction then stops that very model from loading, or whether its two
   unaligned sizes fall on different layers. Worth a sentence in a canonical entry.
3. The activation-width gap noted in my 84/001 verdict applies here unchanged.

### commit-000088-001.md

Source: `reviews/verdicts/commit-000088-001.md` (sha256 `dfa23a8cb8e5b939709c911aaf8637e938cd2efb4b292a5bf6ef2ceb8ce83eb7`).

**Must fix before canonical use**

Reviewer-only.

1. Ledger identities: the two findings are further observations on the records that 84/001 and 86/001 feed, not new
   defects. This is the third name for the both-axes observation; keep one record.

### commit-000089-001.md

Source: `reviews/verdicts/commit-000089-001.md` (sha256 `efac1756afa9e24ca05e80ef3c9ae81eb6bd0686a5e484c9f0b0d22789f4b7a3`).

**Must fix before canonical use**

Reviewer-only.

1. `new_requirement` understates the finding for the common case: a headless Linux Python without the `tkinter`
   package cannot import the library at all after this commit. A canonical entry should say that in plain words.

### commit-000090-001.md

Source: `reviews/verdicts/commit-000090-001.md` (sha256 `4e2ac572fa7e588f26e43947ffc2645bb8c9a864a115dc4496cfd6d58dafc27e`).

**Follow-ups**

- Ledger: `missing-combo-sampler` is a new defect introduced at this commit. The NaN boundary is a separate one with
  origin reviewer observation; file it the way the validator accepts.

**Must fix before canonical use**

1. The NaN case above is absent from the entry. A canonical entry needs it or an equivalent statement of what the
   presence/frequency kernel does at the window boundary with zero decay.

### commit-000092-001.md

Source: `reviews/verdicts/commit-000092-001.md` (sha256 `e3056f06f00498bbbdc9ad0aaea46c395a78ea584d5ad7fee8a7e39fff86e66a`).

**Must fix before canonical use**

1. `chat-min-p-disable` and 91's `combo-default-min-p` are one defect (`SS_MinP` rejects 0 and has no no-op
   alternative) seen from two callers. One ledger record, two observations.

### commit-000096-001.md

Source: `reviews/verdicts/commit-000096-001.md` (sha256 `dae7969eadddc197612da50bb8a332340e31d932ffd98a2c20ecf2a5f502e9bc`).

**Must fix before canonical use**

Reviewer-only.

1. `plain-mlp-allocation` has two sites, one new here and one older in `TransformerBlock`. The ledger should hold one
   defect with both, and the older site needs its introducing commit established; this run does not establish it.

### commit-000098-001.md

Source: `reviews/verdicts/commit-000098-001.md` (sha256 `ceb937d61cb326dbbb323e476b66cd33355dc59f447ec229beca6060d240c1a3`).

**Follow-ups**

- Ledger: `cohere-qk-normalization` as a new suspected external-compatibility record at this commit. The unused
  `q_norm` / `k_norm` tensors are a reviewer observation on the same record.

**Must fix before canonical use**

1. The entry reads no header. A canonical entry should state the tensor comparison above in its own words from its own
   reads: that the eight full-precision checkpoints match, that the Plus checkpoints carry unused `q_norm` / `k_norm`
   weights, and that the two 4bit repositories are a different storage format.
2. It says tied embeddings are explicit in v01 and defaulted in v01-4bit, and is silent on the other eight, which are
   all defaulted.

### commit-000099-001.md

Source: `reviews/verdicts/commit-000099-001.md` (sha256 `b42b6df0ce650090e06c0f80f3156eb7f2a7f301ebf9fa77eff8be133d0571c9`).

**Must fix before canonical use**

1. `inherited-single-device-progress` is still classed `behavior_change`; see my note on 76/001.

### commit-000102-001.md

Source: `reviews/verdicts/commit-000102-001.md` (sha256 `3ec253a0c1f136f27ba3e874b3fd9c375202dd77449e2036c635cf376ab8c723`).

**Follow-ups**

- After this commit the registry no longer has the dictionary-literal shape the registry-key detector reads. From
  position 103 on, new architectures are caught by the derived identity and the unresolved list only (see my note in
  `architecture-trigger-fixes-implementation-001`).

### commit-000103-001.md

Source: `reviews/verdicts/commit-000103-001.md` (sha256 `853564e10bd59136466ecf0fb2f6d64d9d380e53e3febc6692c915c6099a8810`).

**Must fix before canonical use**

1. As at 98: the entry reads no header. A canonical entry should state the tensor comparison from its own reads.

### commit-000103-reference-access-001.md

Source: `reviews/verdicts/commit-000103-reference-access-001.md` (sha256 `154cd6c6cac60803ba4566f2f45b44d403617973e426b2d5a61ce50dbbc9c76f`).

**Conditions**

1. New status for a single file, for example `mirror_historical_unverified_identity`. It applies only when all of these
   hold, and the tool must check them, not a curator:
   - the official current hash for that path does not match, and the mirror's matching copy is dated after the cutoff;
   - at least two distinct mirror repositories hold a byte-identical copy at revisions whose file commit dates are at or
     before the cutoff;
   - at one of those revisions, every other reference file of the model passes the ordinary identity check against the
     official current hashes.
2. Only non-weight files may use it. A safetensors file never may.
3. The item's proof records both mirror repositories, both revisions and dates, the shared blob id, the official
   current blob id it does not match, and the date of the mirror's later matching copy.
4. The teacher-visible index row and object metadata say plainly: this file is the pre-cutoff mirror copy; its identity
   with the official file at that date could not be checked because the official history is gated. Nothing about what
   the file later became, and no post-cutoff date, appears in anything a teacher can read. The later date and the
   non-matching official blob id stay in the administrative report.
5. The model's selection report carries the status too, so a reviewer sees it without opening items.
6. This is an implementation change. File an implementation request with the rebuilt commit 103 bundle (all three
   models) before authoring. Name the affected file in that request and in commit 103's review request.
7. General rule from now on, replacing the last sentence of point 7 in the mirror decision: an unverifiable mirror file
   may stand in only under condition 1. Anything else unverifiable stays out.

### commit-000104-001.md

Source: `reviews/verdicts/commit-000104-001.md` (sha256 `ff5b0841fe7ee5935a83f6fdc5dac91fcf23b471f6454f62887fb420d52d8c35`).

**Must fix before canonical use**

1. `documentation-dump-scope` is classed `defect`. It is a documentation inaccuracy of the smallest kind; the ledger
   classification should say documentation.

### commit-000105-001.md

Source: `reviews/verdicts/commit-000105-001.md` (sha256 `9ecacb0ccb351c9ac4cee30ff76b4e860faea53d9a6f85ab00df4e1f9c143ea0`).

**Follow-ups**

- Ledger: `stream-argument-mismatch` as a new defect introduced at this commit, in the chat example only.

### commit-000106-001.md

Source: `reviews/verdicts/commit-000106-001.md` (sha256 `eaa224b432c5908de49c98e4d081b9eb961b802fcfcc7471544ac32df925a655`).

**Must fix before canonical use**

1. The entry rewrites the description of the rich streamer's thinking branch and does not carry the inherited
   `reasoning-boundary-answer-loss` finding that 73/001 and 78/001 record. It still holds at this commit: when the
   closing tag arrives in the same chunk as the start of the answer, the whole chunk is added to `think_text` and the
   answer part never reaches `all_text`. The entry read only 105's ancestor entry. Not false, but a canonical entry
   for a commit that edits this exact branch should say the defect survives.

### commit-000110-001.md

Source: `reviews/verdicts/commit-000110-001.md` (sha256 `49388233a3ec882aff469ddc45175ec7a08d0e96bb17b3cdac4d4e95b0ddd090`).

**Must fix before canonical use**

1. As at 98 and 103: no header read. A canonical entry should state the tensor comparison, the two tied-embedding
   storage patterns and the FP8 storage format from its own reads.

### commit-000111-001.md

Source: `reviews/verdicts/commit-000111-001.md` (sha256 `c06488d9cef4293421349f69ceb4c016e8534f5f58f76408ba68a74dd230c857`).

**Must fix before canonical use**

1. Ledger identity: this is a fourth observation on the `SS_MinP` zero defect, not a new record. One side effect worth
   recording there: at temperature 0 the defect is now unreachable through `ComboSampler`.

### commit-000112-001.md

Source: `reviews/verdicts/commit-000112-001.md` (sha256 `3bf123024513936c7cd1c8a5016b65175207edcda73751d5a28972e8f79f0805`).

**Must fix before canonical use**

1. A canonical entry should state that the residual stream is float32 (the embedding's default output dtype), since
   that is why the float32 MLP output matters. The entry says the change does not establish that the whole block runs
   in float32, which is true, but it never says what the residual is.

### commit-000113-001.md

Source: `reviews/verdicts/commit-000113-001.md` (sha256 `f4e372b092b9c058f3a194cea5d271cf29eca5bfc3ceee0dc31cad5478e0200f`).

**Follow-ups**

1. This is the first recorded failure of this kind (a corrupted call id in otherwise ordinary output). If it recurs,
   a fresh unassisted attempt on the same packet is the right recovery and does not need a separate request; say so in
   the next request and keep the failed run.

### commit-000113-002.md

Source: `reviews/verdicts/commit-000113-002.md` (sha256 `6ce2b9e1984e8d88c94f6cdf56f12c727397dc8a7f36e1ab6c5a44bc9bd01c9f`).

**Follow-ups**

1. Ledger: the `SS_MinP` zero defect seen at 91, 92 and 111 under three names is one identity and is **fixed at 113**.
   Merge and close it when the ledger is next revised.
2. Ledger: file the `SS_TopP` zero assertion as a new record (reviewer finding, this verdict).
3. Behaviour change worth a row when the ledger is revised: `min_p = 1.0`, valid before, now fails the assertion.

**Must fix before canonical use**

1. A canonical entry should say that zero `top_p`, the other case in PR 30, still fails after this commit.

### commit-000114-001.md

Source: `reviews/verdicts/commit-000114-001.md` (sha256 `f3a3844cda0923adf3f661608a52dcd707e6e6b0254e80d02306ef3a9b0a55ca`).

**Follow-ups**

1. Ledger, when next revised: add `86ee10b6` to the top-p record's verified revisions (still present at 114).
2. Ledger, when next revised: the min-p identity (91, 92, 111) is fixed at 113; the 1.0 endpoint was rejected at 113
   only and accepted again at 114, one minute later. Record that as a one-commit regression, not a standing behaviour
   change. This replaces follow-up 3 of the 113/002 verdict.
3. Validator: teaching `ledger/retrospectives.py` the `reviewer_observation` origin is an implementation change and
   needs its own request. Not urgent; nothing reads these records yet.

### commit-000115-001.md

Source: `reviews/verdicts/commit-000115-001.md` (sha256 `a3bd6b9f8f3e0b6eddef295164756d39f1a4780e92b2768238156744fb3a37c5`).

**Follow-ups**

1. Ledger, when next revised: mark the top-p record fixed at `a7a6681e` (affected at 113 and 114 at least; introduction
   still not established), origin of the fix `fix_derived` from this entry, and note the semantics chosen.

### commit-000117-001.md

Source: `reviews/verdicts/commit-000117-001.md` (sha256 `6a63a2e6dbe02c93eff1d4289581c0e2742df3ffa1947ba84a779041499d2fb8`).

**Follow-ups**

1. Ledger, when next revised: `architecture-mismatch-diagnostic` (102) is fixed at `04dc5571`; the stale docstring
   parameter remains.
2. Execution accounting: this is the second `run` that executes repository text (after 101). Count it the same way.

**Must fix before canonical use**

1. A canonical entry should name `151edc00` as the commit that introduced the broken message, and link to it.

### commit-000118-001.md

Source: `reviews/verdicts/commit-000118-001.md` (sha256 `75db19ffa161a6489e13ec120ef87ba4f1ff5b922ee66b9fcc04b39c012a3d3d`).

**Follow-ups**

1. Ledger, when next revised: `unconditional-tk-import` (89) is fixed at `8d07bfb8`.

### commit-000119-001.md

Source: `reviews/verdicts/commit-000119-001.md` (sha256 `c4815cd7a5d1d8f9ca89ed8188b3b51907761616b6927a75c22a9ebd56a9fdf8`).

**Follow-ups**

1. Ledger: file three reviewer-origin candidates from findings 1 to 3 (suspected, source inspection, introduced at
   `647bb7d5`), excluded from historical context and training like the top-p record. Send them with the next request.
2. Ledger: `deferred-bf16-odd-tail` is approved as drafted.

**Must fix before canonical use**

1. A canonical entry must cover the eager-path consequences of moving the transforms into `get_tensor`: the variant
   collection, sliced FP16 loading and fused FP32 weights (findings 1 to 3).

### commit-000120-001.md

Source: `reviews/verdicts/commit-000120-001.md` (sha256 `f6d5b6ee4edb430f0cb260c9559b93ef61399ac7e4dd4f6fd1bf02e84b9c31bc`).

**Follow-ups**

1. Ledger, when next revised: add `8d347764` to the affected revisions of the three accepted records and of the
   odd-tail record; add the `-lm` and `get_metrics` gaps to the variant record or link the entry's finding to it.

### commit-000121-001.md

Source: `reviews/verdicts/commit-000121-001.md` (sha256 `cdce80827a6f116e47c6e37d06783b15fb2f85cff0228c0d8f62a373ef434845`).

**Follow-ups**

1. Ledger, when next revised: one record for the same-directory same-stem object conflict, introduced at `647bb7d5`,
   fixed at `3c801c61` (fix-derived from this commit; suspected, since no build was run). It also belongs in 119's
   canonical-use list alongside the three findings already there.

**Must fix before canonical use**

1. A canonical entry should name `647bb7d5` as the commit that created the same-stem pair, and link to it.

### commit-000122-001.md

Source: `reviews/verdicts/commit-000122-001.md` (sha256 `27c70aaf49a52f60bd0fc73fc9b2da5af7d93852474f3a91a5bbaa89e334497e`).

**Follow-ups**

1. Ledger, when next revised: one identity, "repetition penalty turns masked logits into NaN", introduced at
   `40863d06` (90). Its factor-zero case is fixed at `a6538654` (fix-derived from this commit); its factor-one case
   remains open (this entry's finding). Record it as partially fixed, not as two defects.

### commit-000123-001.md

Source: `reviews/verdicts/commit-000123-001.md` (sha256 `d2c0355fb7bd13790849dff3bb279a5e9c09866ae1e634feab2bfc28ade3e78a`).

**Follow-ups**

1. Ledger: file one reviewer-origin candidate from the finding above (suspected, source inspection, introduced at
   `5d470a29`), excluded from historical context and training. Send it with the next request.
2. Ledger: `boolean-dimension-threshold` is approved as drafted.

**Must fix before canonical use**

1. A canonical entry must cover the selector's unguarded shape-3 returns together with the removed launch-time
   divisibility check.
2. Say that `DevCtx` moves to its own file, not that state moves into it.

### commit-000124-001.md

Source: `reviews/verdicts/commit-000124-001.md` (sha256 `7bf2d1f2a7cccb91e14931c62e2f53416baf1ce9cf68c088d67d71b0fe79afb5`).

**Follow-ups**

1. Ledger, when next revised: record `humaneval-top-k-float` as a second site of the 92 identity, not a new defect.

### commit-000125-001.md

Source: `reviews/verdicts/commit-000125-001.md` (sha256 `05abb6b7e86cb1d1e9e0a544b5706b179192327376865cfb0e47be826ff229b9`).

**Follow-ups**

1. Ledger: no new record for this commit. When the top-k identity is next revised, list `57a37f26` as affected.

### commit-000126-001.md

Source: `reviews/verdicts/commit-000126-001.md` (sha256 `298459c39ccd7a9d76b96cf5d7294bc39b0b4ce0e128ffeee15b7cc9d4794b00`).

**Follow-ups**

1. Ledger: `deferred-cuda-error-number` is approved as drafted. The deferred CPU half (number captured, never
   reported) is the same oversight and belongs in the same record.

### commit-000127-001.md

Source: `reviews/verdicts/commit-000127-001.md` (sha256 `41e9cbc032b12f73476081b2c8674f0497d4d0d0d48d7428c8992430faeb1cc7`).

**Follow-ups**

1. Ledger: `ppl-vocabulary-bound` is approved as drafted; record it as having no effect for vocabularies of 2,047
   or more.

**Must fix before canonical use**

1. Name the direction of each printed KL value.

### commit-000128-001.md

Source: `reviews/verdicts/commit-000128-001.md` (sha256 `1a456adfc82783706ac740a5f6ebd24b55ee3d13d63d5cdce581553fe17c83a0`).

**Follow-ups**

1. Ledger, when next revised: a fix-derived record for handle accumulation during conversion and compilation, fixed
   at `4710c012`. Introduction: per-file caching at the first commit, made worse at `647bb7d5` (five to eight handles
   per file). Suspected; no execution.

### commit-000129-001.md

Source: `reviews/verdicts/commit-000129-001.md` (sha256 `d63398c35666f232531115d28d547f0e8b2370e68112ee949ef21e5c1a574f3b`).

**Follow-ups**

1. Ledger: `scalar-codebook-double-transform` and `missing-gemv-header` approved as drafted, both introduced at
   `c4867edd`. Keep the header record separate from the first-commit one.
2. Ledger: no new record for the Boolean threshold; add `c4867edd` to the 123 identity's affected revisions, and to
   `exllamav3-gemm-selector-divisibility`.

### commit-000130-001.md

Source: `reviews/verdicts/commit-000130-001.md` (sha256 `44bba3cca2dbf5ef9bded2c4de5a20ad946c0473d61fd7b4dbf59a1f7d925a40`).

**Follow-ups**

1. Ledger: `unicode-flush-bypasses-string-checks` approved as drafted, introduced at `2e7b00d3`.
2. Ledger: the checkpoint attribute and the terminal bypass are one record each, introduced at `543c4b27`, with
   `2e7b00d3` among the affected revisions. Do not file them as introduced here.
3. The earlier ledger revisions owed (listed in the 129 verdict and your journal) are still owed.

### commit-000131-001.md

Source: `reviews/verdicts/commit-000131-001.md` (sha256 `8fb043f749520d23b11690c118d5b62d96375a9823df3f228c5dd91f1cf08d34`).

**Follow-ups**

1. The earlier ledger revisions owed (min-p, top-p, mismatch diagnostic, tk import, object-name conflict,
   repetition-penalty NaN, handle accumulation, 119 affected revisions, humaneval top-k, 126's errno pair) are still
   owed.

### commit-000132-001.md

Source: `reviews/verdicts/commit-000132-001.md` (sha256 `12f6d2bf0a3350eecb388433973f7513174b44423f84d5c7647db0eb4ac3fbba`).

**Follow-ups**

1. Check whether `exllamav3-missing-exl3-gemv-header` records its fix; if not, find the removing commit and revise.
2. The earlier ledger revisions owed are still owed.

### commit-000133-001.md

Source: `reviews/verdicts/commit-000133-001.md` (sha256 `1151b69aa52459792255048dc48b581e5bcc736c3f3d11ecbff4e3525c31884f`).

**Follow-ups**

1. Ledger: `multi-gemm-leading-dimension-validation` approved as drafted, introduced at `b73d0739`.
2. Ledger: add `b73d0739` to the affected revisions of `exllamav3-boolean-dimension-threshold` and of
   `exllamav3-gemm-selector-divisibility`; no new record for either.
3. The earlier ledger revisions owed are still owed.

### commit-000134-001.md

Source: `reviews/verdicts/commit-000134-001.md` (sha256 `de98cbc650b536e2f46d833b7c059f4e93969f1a7a6c3ea4e2ad9a972ff8d43d`).

**Follow-ups**

1. The earlier ledger revisions owed are still owed.

### commit-000135-001.md

Source: `reviews/verdicts/commit-000135-001.md` (sha256 `a6314835ff4e73ab581d715e6b7c205ca1f89d694612819750de32ea4e267557`).

**Follow-ups**

1. Ledger: `zero-slice-division` approved. File it so the root is visible: the zero cap introduced at `5d470a29`
   (zero-block launch in `exl3_gemm`), carried into `exl3_mgemm` at `b73d0739`, division by zero added at
   `edafdd1f`. One record, not three.
2. Ledger: `broadcast-scratch-capacity` approved as drafted, a new requirement introduced at `edafdd1f`.
3. Ledger: add `edafdd1f` to the affected revisions of `exllamav3-multi-gemm-leading-dimension-validation`, with
   the changed consequence (write past the output).
4. The remaining older ledger revisions are still owed.

### commit-000136-001.md

Source: `reviews/verdicts/commit-000136-001.md` (sha256 `6eeba01d95f73fa417401f4362e63d7b52407e14fdb4f6df14e00171ff6215e3`).

**Follow-ups**

1. Ledger: file a reviewer-observation record for the integer check, introduced at `a027848d`, with the reach
   listed above and no fix entry yet. Like the selector-divisibility record it stays out of historical context
   and training.
2. The remaining older ledger revisions are still owed.

**Must fix before canonical use**

1. The entry needs the Python 3.12 finding, or a later attempt that states it. For ancestor retrieval the present
   text is acceptable because its limits section already tells a later reader the point is open.

### commit-000137-001.md

Source: `reviews/verdicts/commit-000137-001.md` (sha256 `abee5ae42288ff1c2e26be6c14ccccb8053e2623da9a51c235b8d0f4c23fc668`).

**Follow-ups**

1. Ledger: `empty-codeblock-feedback` approved as drafted, introduced at `e0cfb2e9`.
2. The remaining older ledger revisions are still owed.

### commit-000138-001.md

Source: `reviews/verdicts/commit-000138-001.md` (sha256 `63eadf95a7ba1db1a57fc3ef7ef55cdf12a4fe67195ff17948959f754c301cf0`).

**Follow-ups**

1. Ledger: a fix-derived record for the ignored transpose on in-memory tensors: introduced at `647bb7d5`, fixed at
   `538dcae3`, with the two consequences above stated as source reading only.
2. The remaining older ledger revisions are still owed.

### commit-000139-001.md

Source: `reviews/verdicts/commit-000139-001.md` (sha256 `5c7282f76a8ea8dc1cb28495334368787efe253a65190f567e06f7d84636febb`).

**Follow-ups**

1. Ledger: `all-expert-fused-shape` approved as drafted, introduced at `6fc153d7`.
2. Ledger: a reviewer-observation record for the fused path's intermediate dtype, introduced at `6fc153d7`,
   conditional on a caller leaving `interm_dtype` unset or not half. Excluded from historical context and training
   like the other reviewer records.
3. The remaining older ledger revisions are still owed.

### commit-000140-001.md

Source: `reviews/verdicts/commit-000140-001.md` (sha256 `8d2148d666b0bbb2786668cd9f416fc3a9f7b8c257643d172b671922d2de27e7`).

**Follow-ups**

1. Ledger: file the BF16 odd-tail record: introduced at `647bb7d5` (119), with `c6aa83f7` as affected and the
   wider reach. One identity for the 119 and 140 findings.
2. Ledger: a reviewer-observation record for the missing abort in `_load_single`, introduced at `c6aa83f7`.
3. Ledger: add `c6aa83f7` to the affected revisions of `exllamav3-variant-collection-loader-api`.
4. The remaining older ledger revisions are still owed.

### commit-000141-001.md

Source: `reviews/verdicts/commit-000141-001.md` (sha256 `ac8212ce237944cd159421451f42d3b586d7d7e7cc522c302a47d804c4690f2e`).

**Follow-ups**

1. Ledger: add `a5caa423` to the affected revisions of `exllamav3-all-expert-fused-shape`, with the concrete
   128 against 8; no new record.
2. The remaining older ledger revisions are still owed.

**Must fix before canonical use**

1. As for 98, 103 and 110: a canonical entry for an architecture commit should state what the headers show,
   including which published variants cannot load.

### commit-000142-001.md

Source: `reviews/verdicts/commit-000142-001.md` (sha256 `6620739a76739b9bfa58e309cb85773bf159c47e6773a61bcf50097960145b62`).

**Follow-ups**

1. Ledger: the repetition-penalty NaN record is now complete and can be filed as one identity: introduced at
   `40863d06` (90), half fixed at `a6538654` (122), fixed at `43383ebd` (142).
2. The remaining older ledger revisions are still owed.

### commit-000143-001.md

Source: `reviews/verdicts/commit-000143-001.md` (sha256 `f4aeb9c4ebcd10a85a02f6df61f81730d4fd41944185a55cca51b40ce191dc2f`).

**Follow-ups**

1. Ledger, when the walk reaches the merge `10222646`: add the wheel matrix as evidence to
   `exllamav3-top-k-int-is-integer-compatibility` (Python 3.10 and 3.11 are build targets).
2. The remaining older ledger revisions are still owed.

### commit-000144-001.md

Source: `reviews/verdicts/commit-000144-001.md` (sha256 `3bb1950975ca0185c35f550b0607420ea84a0452fb0400bcc3ade23e5320fbb5`).

**Follow-ups**

1. The remaining older ledger revisions are still owed.

### commit-000145-001.md

Source: `reviews/verdicts/commit-000145-001.md` (sha256 `c4e752aed10e1a65511550113a9cd095fb933b7799b2a8680f0ff0922a6b09c6`).

**Follow-ups**

1. Ledger: a fix-derived record for the unset `max_total_tokens`: introduced at `543c4b27`, fixed at `809b0dab`;
   consequence, the wrong exception type for an oversized job.
2. Ledger: `empty-utf32-return-annotation` approved, introduced at `809b0dab`, as an annotation mismatch with no
   run-time effect.
3. The remaining older ledger revisions are still owed.

### commit-000146-001.md

Source: `reviews/verdicts/commit-000146-001.md` (sha256 `f6399bef02d6695c90fd6c9ac1dd7a892d9b35b8d4bd5f67d674a760cca3df24`).

**Follow-ups**

1. Ledger, at the next revision of `exllamav3-unset-max-total-tokens`: add `9c31971b` as the merge that brings the
   fix to the development line, and the pull request's traceback as an observation.
2. The remaining older ledger revisions are still owed.

### commit-000147-001.md

Source: `reviews/verdicts/commit-000147-001.md` (sha256 `150a43b07c1b62c73606ee297a7f22b02969cf15aa2b22a8a152e8efc0dd5c5b`).

**Follow-ups**

1. Ledger: at the next revision of `exllamav3-repetition-penalty-masked-nan`, add the maintainer's explanation as an
   external observation, marked as eligible only from 144 on.
2. Ledger: the `humaneval-top-k-float` site (second site of 92's record) is fixed here at `beb7bcd9`; record it when
   that revision is written.
3. The remaining older ledger revisions are still owed.

### commit-000148-001.md

Source: `reviews/verdicts/commit-000148-001.md` (sha256 `1f936e5ef25407ec3ecc52258d1033a75e0460b8666f7aeeee1270fb76e47e36`).

**Follow-ups**

1. Ledger: the pending revision of `exllamav3-repetition-penalty-masked-nan` may now cite this entry as the first
   position at which the maintainer's explanation is eligible on the master line (144 on the development line).
2. The remaining older ledger revisions are still owed.

### commit-000149-001.md

Source: `reviews/verdicts/commit-000149-001.md` (sha256 `815b7e557174b9d693294db1a4e97f9303fd0c5bc2cefff29a3de0808d08a666`).

**Follow-ups**

1. Ledger: revise `exllamav3-top-k-int-is-integer-compatibility`: add `f5127e87` as affected, with the new reach
   (the HumanEval script's default invocation) and the note that it arises from the merge. Reviewer observation;
   excluded from historical context and training.
2. The remaining older ledger revisions are still owed.

**Must fix before canonical use**

1. As at 136: the entry names the integer check as unestablished; a canonical entry should state it as a finding,
   here with the merge-specific reach.

### commit-000150-001.md

Source: `reviews/verdicts/commit-000150-001.md` (sha256 `79368fab71da8d5724b9b1c7679c12e1c74632eb59e14290d34aacce6a9336c2`).

**Follow-ups**

1. Catalog rule: as described above.
2. Ledger: a fix-derived record for the script's unconditional BOS (double for Gemma, unwanted for ChatML/Qwen3):
   introduced `543c4b27`, fixed `1e175478`, with the limit that marker recognition was not run.
3. The remaining older ledger revisions are still owed.

**Must fix before canonical use**

1. A canonical entry should have the pull request 35 comment available. That depends on the catalog question above.

### commit-000151-001.md

Source: `reviews/verdicts/commit-000151-001.md` (sha256 `1ddafa816d7722e0837efadfd47a58a17d4b541673fcd0f3bb9418e59318763a`).

**Follow-ups**

1. Ledger: revise `exllamav3-top-k-int-is-integer-compatibility` with the fix at `95cfa726` and the commit title as
   upstream confirmation.
2. The remaining older ledger revisions are still owed.

### commit-000152-001.md

Source: `reviews/verdicts/commit-000152-001.md` (sha256 `70e49d928e4abd9ffffeba23cd9a6de650c04266e0590cfd3bc81d687cafc311`).

**Follow-ups**

1. The remaining older ledger revisions are still owed.

### commit-000153-002.md

Source: `reviews/verdicts/commit-000153-002.md` (sha256 `1ed558b6edb6c31262812a5466b9162561d82f24cc183ea72278ffc055814815`).

**Follow-ups**

1. Record 153/002 as approved and reviewer-assisted, and 153/001 as rejected and superseded.
2. Ledger: the eight retained conditions are existing identities, not new records. Add this commit as the point
   where each reaches the first-parent line, when the owed ledger revision is done.
3. Two location fields name `70056fef` rather than the task commit. The trees are identical, so this is harmless;
   no change needed.

**Must fix before canonical use**

- This entry is reviewer-assisted. It joins 39/005, 44/003, 45/002, 55/002 and 71/002 under whatever the
  assisted-entry policy for canonical use turns out to be.
- The recurring note: no tensor headers were read (the entry says so).

### commit-000154-001.md

Source: `reviews/verdicts/commit-000154-001.md` (sha256 `f390c6e559ce02c60cdd9a7d1c23dee0f1f0d103d72ba7f72b203b023adf6944`).

**Follow-ups**

1. Ledger: file `ppl-axis-bound` as one identity introduced at `9575f7d8`, with `5c3ff204` as an affected
   revision; note that it changes results only for a vocabulary smaller than the sequence.
2. Ledger: a reviewer-observation record for the unconditional deferral in `model_diff.py`, introduced at
   `5c3ff204`, conditional on a module that cannot defer. Excluded from historical context and training.
3. The remaining older ledger revisions are still owed.

### commit-000155-001.md

Source: `reviews/verdicts/commit-000155-001.md` (sha256 `3d440a9ef19dff55e1ee9cff9fe7d4b53e8a0ebd274f81083ec0860e0a76b02c`).

**Follow-ups**

1. Ledger, `exllamav3-model-diff-unconditional-deferral`: file r002 replacing "no registered model at this
   revision is established to exceed it". Issue 38's body, which is inside the cutoff from 155 on, shows a
   registered architecture (`DeciLMForCausalLM`) with an MLP sliced eight ways. State the limit as it now stands:
   such a model exists, and at this revision its unquantized load fails earlier on the padding mismatch.
2. Ledger, `exllamav3-sliced-fp16-padding-target`: file a revision adding issue 38's body as cutoff-bound
   corroboration (the traceback and the two sizes), available from 2025-05-14T06:52:25Z. Status stays suspected
   until a fix is reviewed; no execution was done here.
3. The remaining older ledger revisions are still owed.

### commit-000156-001.md

Source: `reviews/verdicts/commit-000156-001.md` (sha256 `fbb32aa94a04aa7c2953e02a9de9b29a22a8ce5f08b718e2da12b115f37c9a8e`).

**Follow-ups**

1. Ledger wording, at the next revision of `exllamav3-sliced-fp16-padding-target`: its limits field carries the
   sentence written for the other record ("unquantized loading fails earlier on the padding mismatch"). For this
   record that mismatch is the defect itself, not something that happens earlier. Also say there that the
   reporter's revision is not pinned. No new request is needed for this alone.
2. The remaining older ledger revisions are still owed.

### commit-000157-001.md

Source: `reviews/verdicts/commit-000157-001.md` (sha256 `9a11568d7622543ae9413b4926ece64ed952f70bd7b85b6d2a6b3ecec78f4a28`).

**Follow-ups**

1. The remaining older ledger revisions are still owed. Nothing new from this commit.

### commit-000158-001.md

Source: `reviews/verdicts/commit-000158-001.md` (sha256 `4f53256e13221d4d4be13dfd2006e334a7ba7a6ddd5e88966e4db002c3cc4b3d`).

**Follow-ups**

1. No ledger work from this commit.
2. The remaining older ledger revisions are still owed.

**Must fix before canonical use**

- The recurring note: the teacher read no tensor headers and says so. The header comparison above is mine and is
  not part of the entry.
- The entry would be more useful with the comparison to the Qwen3 MoE builder (first reviewer note).

### header-budget-implementation-001.md

Source: `reviews/verdicts/header-budget-implementation-001.md` (sha256 `2269b30b4de6583510f3b16e89235e5a9e3ad448c738431e193a32ba38d89148`).

**Conditions**

1. If a later architecture needs more than 16 MiB, stop and ask again; do not raise it in passing.
2. The ModelScope bound stays at 4 MiB until a case needs it and is reviewed.

## Journal dispositions at implementation

```json
{
  "replacement_reviews": [
    {
      "position": 17,
      "supersedes_run": ".teacher/runs/commit-000017-002",
      "candidate_run": ".teacher/runs/commit-000017-003",
      "packet": ".teacher/retrieval/000017-003",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/catalog-hints.decision.md",
        "sha256": "54b8a2a812b3d2bb32dae3921fa5838b568145e2fad473b683a28d8e8b9a5945"
      },
      "verdict": {
        "path": "reviews/verdicts/commit-000017-003.md",
        "sha256": "2b4f4297004a00fe66535fde0b3a50ea033e406ecf931b43145d066b3c39f6a7"
      }
    },
    {
      "position": 32,
      "supersedes_run": ".teacher/runs/commit-000032-001",
      "candidate_run": ".teacher/runs/commit-000032-002",
      "packet": ".teacher/retrieval/000032-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/catalog-hints.decision.md",
        "sha256": "54b8a2a812b3d2bb32dae3921fa5838b568145e2fad473b683a28d8e8b9a5945"
      },
      "request": "reviews/requests/commit-000032-002.md",
      "tier": "full_review",
      "reasons": [
        "nonmechanical_path",
        "findings_present_or_missing",
        "execution_claim"
      ],
      "policy": "exdev-mechanical-ancestor",
      "version": 1,
      "sampled": false,
      "changed_files": [
        "exllamav3/modules/linear.py"
      ],
      "verdict": {
        "path": "reviews/verdicts/commit-000032-002.md",
        "sha256": "4e92800ceea5ff4310c92a94bddae9237d2b1656a6aae495ebc76c3c72aebeef"
      }
    },
    {
      "position": 39,
      "supersedes_run": ".teacher/runs/commit-000039-001",
      "candidate_run": ".teacher/runs/commit-000039-002",
      "packet": ".teacher/retrieval/000039-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/reauthor-39-41.decision.md",
        "sha256": "66ceb6ad4c4c18ca0ba7c420a2421dbc4c70342a943a0b9c0f07e919ed296154"
      },
      "request": "reviews/requests/commit-000039-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000039-002.md",
        "sha256": "7853c45af864843e3ce639e0f5a3f7c71dc4dd9d581799219671e42bc996ce33"
      },
      "superseded_for_future_retrieval_by": ".teacher/runs/commit-000039-005"
    },
    {
      "position": 41,
      "supersedes_run": ".teacher/runs/commit-000041-001",
      "candidate_run": ".teacher/runs/commit-000041-002",
      "packet": ".teacher/retrieval/000041-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/reauthor-39-41.decision.md",
        "sha256": "66ceb6ad4c4c18ca0ba7c420a2421dbc4c70342a943a0b9c0f07e919ed296154"
      },
      "request": "reviews/requests/commit-000041-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000041-002.md",
        "sha256": "1d2397adea42322688ac99887c28612a5f1ba22f3ebe62fc40ddf10dfec818ba"
      }
    },
    {
      "position": 39,
      "supersedes_run": ".teacher/runs/commit-000039-002",
      "candidate_run": ".teacher/runs/commit-000039-003",
      "packet": ".teacher/retrieval/000039-003",
      "status": "rejected",
      "decision": {
        "path": "reviews/verdicts/thin-entries-and-retroactive.decision.md",
        "sha256": "805d83465f08e7e9d1ec59670962f934aadb768b41b264ece36c65cea15e09f9"
      },
      "request": "reviews/requests/commit-000039-003.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000039-003.md",
        "sha256": "9da6e1ce366493975c44882415a564f51cbf1112a09d612dea78b87da33555fd"
      }
    },
    {
      "position": 39,
      "supersedes_run": ".teacher/runs/commit-000039-002",
      "candidate_run": ".teacher/runs/commit-000039-004",
      "packet": ".teacher/retrieval/000039-004",
      "status": "rejected",
      "decision": {
        "path": "reviews/verdicts/config-reading-amendment.decision.md",
        "sha256": "a8ed9a5a101d2578d1ee1168d0528a7b72a52addf028094702a99b1a9d513a34"
      },
      "request": "reviews/requests/commit-000039-004.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000039-004.md",
        "sha256": "b41ba27c24e370b8f895a716c86f6af9e72a0ef16ae0c5d4fd36592a70f1b801"
      }
    },
    {
      "position": 39,
      "supersedes_run": ".teacher/runs/commit-000039-002",
      "candidate_run": ".teacher/runs/commit-000039-005",
      "packet": ".teacher/retrieval/000039-005",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/commit-000039-004.md",
        "sha256": "b41ba27c24e370b8f895a716c86f6af9e72a0ef16ae0c5d4fd36592a70f1b801"
      },
      "coverage_request": {
        "path": "reviews/verdicts/commit-000039-005.coverage.md",
        "sha256": "761034b3089351c4bc7eac1cb9c1b715c7f009cf0138147feb1781560c2b148a"
      },
      "final_attempt": true,
      "request": "reviews/requests/commit-000039-005.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000039-005.md",
        "sha256": "ead08fe973e3b31b1812a7e9607f4f925f60593b1f3d49e529f4d0a10c13935a"
      }
    },
    {
      "position": 44,
      "supersedes_run": ".teacher/runs/commit-000044-001",
      "candidate_run": ".teacher/runs/commit-000044-002",
      "packet": ".teacher/retrieval/000044-002",
      "status": "rejected",
      "decision": {
        "path": "reviews/verdicts/thin-entries-and-retroactive.decision.md",
        "sha256": "805d83465f08e7e9d1ec59670962f934aadb768b41b264ece36c65cea15e09f9"
      },
      "request": "reviews/requests/commit-000044-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000044-002.md",
        "sha256": "c326b8596b82541ebfe48f605715ea844d92e9779690d78601c05570f467e67e"
      }
    },
    {
      "position": 44,
      "supersedes_run": ".teacher/runs/commit-000044-001",
      "candidate_run": ".teacher/runs/commit-000044-003",
      "packet": ".teacher/retrieval/000044-003",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/commit-000044-002.md",
        "sha256": "c326b8596b82541ebfe48f605715ea844d92e9779690d78601c05570f467e67e"
      },
      "coverage_request": {
        "path": "reviews/verdicts/commit-000044-003.coverage.md",
        "sha256": "94cb9f66058550ed29e1535d1ea3832862e16c2618c9053cbefbeabcb8ba24bf"
      },
      "final_attempt": true,
      "request": "reviews/requests/commit-000044-003.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000044-003.md",
        "sha256": "dc8ee756455157d226e18bcf2bf1d2ce8d59574a923ca2fa5f6328208daf782f"
      }
    },
    {
      "position": 45,
      "supersedes_run": ".teacher/runs/commit-000045-001",
      "candidate_run": ".teacher/runs/commit-000045-002",
      "packet": ".teacher/retrieval/000045-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/thin-entries-and-retroactive.decision.md",
        "sha256": "805d83465f08e7e9d1ec59670962f934aadb768b41b264ece36c65cea15e09f9"
      },
      "coverage_request": {
        "path": "reviews/verdicts/commit-000045-002.coverage.md",
        "sha256": "f0187fdaafe109c5e9c7795ff8e974d0730385ef5ff5496e65286246e4c1df5a"
      },
      "coverage_semantic_audit": "Questions and pointers to parent construction, ancestor entries and eligible configs only; no conclusions, hindsight or length quota.",
      "request": "reviews/requests/commit-000045-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000045-002.md",
        "sha256": "b64db4aa76f32df33e7b13f1893628a3d41953b3b87aae3fc92c61a6ce3c6251"
      }
    },
    {
      "position": 55,
      "supersedes_run": ".teacher/runs/commit-000055-001",
      "candidate_run": ".teacher/runs/commit-000055-002",
      "packet": ".teacher/retrieval/000055-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/thin-entries-and-retroactive.decision.md",
        "sha256": "805d83465f08e7e9d1ec59670962f934aadb768b41b264ece36c65cea15e09f9"
      },
      "coverage_request": {
        "path": "reviews/verdicts/commit-000055-002.coverage.md",
        "sha256": "a8d0540538b5c8b794a8a70bd13898ddb2d249f6026a08ca58893f35c859652b"
      },
      "coverage_semantic_audit": "Pointers/questions to preceding strict ancestors, parent/task loading, slicing, conversion and eligible configurations only; no answers, hindsight or length quota.",
      "request": "reviews/requests/commit-000055-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000055-002.md",
        "sha256": "b25a2ab46c220f7c20e4d1ba1446e0e26e1e9c9b13185f031b255bc42da37f50"
      }
    },
    {
      "position": 69,
      "supersedes_run": ".teacher/runs/commit-000069-002",
      "candidate_run": ".teacher/runs/commit-000069-003",
      "packet": ".teacher/retrieval/000069-003",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/closed-discussion-salience.decision.md",
        "sha256": "e1fd1e90efd0153e2a2da00ae9ace8329a5adea54bea86df7db139a7bd65010f"
      },
      "selection": "Fuller approved attempt chosen by reviewer.",
      "request": "reviews/requests/commit-000069-003.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000069-003.md",
        "sha256": "1996e9dfaa8111f96e4d24112c1b07dc603cb9120566c8ba7012fd4e7315b5b7"
      }
    },
    {
      "position": 71,
      "supersedes_run": ".teacher/runs/commit-000071-001",
      "candidate_run": ".teacher/runs/commit-000071-002",
      "packet": ".teacher/retrieval/000071-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/commit-000071-001.md",
        "sha256": "b183c268c5b14d64b276b3b12486ebee84928dcca9b4f24455fe515cc72a19d8"
      },
      "coverage_request": {
        "path": "reviews/verdicts/commit-000071-002.coverage.md",
        "sha256": "6f3b7c8bb0afe8e45552d49efcd1dbef4028dae8fdf2fe864a7a460c88259217"
      },
      "dependent_runs": [],
      "request": "reviews/requests/commit-000071-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000071-002.md",
        "sha256": "5ad9bfdfaeec6003368657487476d692bba986e1ba59c96d820a68a447fe559b"
      }
    },
    {
      "position": 72,
      "supersedes_run": ".teacher/runs/commit-000072-001",
      "candidate_run": ".teacher/runs/commit-000072-002",
      "packet": ".teacher/retrieval/000072-002",
      "status": "approved_reviewed",
      "decision": {
        "path": "reviews/verdicts/commit-000072-001.md",
        "sha256": "1132dd92e88c238621c1791eac2b0551286bce395c2ec80c5759f4db7c5799a1"
      },
      "dependent_runs": [],
      "evidence_directory": "data/evidence/commit-000072-002",
      "request": "reviews/requests/commit-000072-002.md",
      "verdict": {
        "path": "reviews/verdicts/commit-000072-002.md",
        "sha256": "014fd6b931e3dec4c2ba4cfc9dd98048a70bb3eafd9ad34460a2ebd9eebb2ffa"
      }
    }
  ],
  "legacy_deci_ledger_review": {
    "status": "accepted_as_recorded",
    "record": "reports/defect-ledger/exllamav3-legacy-decilm-config--r001.json",
    "verdict": {
      "path": "reviews/verdicts/commit-000075-001.md",
      "sha256": "35ee61ae0bb2a87bc04a6f1bde1ff660a7ae582ac4a73e7e878e70a4a5c9ee1c"
    }
  },
  "review_followups": [
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000076-001.md",
        "sha256": "570c27fce971d8e48f6439fdbc65b4973ee2c01ec76ccbdd579bf6cca25c3248"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Reclassify single-device-progress as incomplete new interface rather than behavior change",
        "Account for the truncated load_gen docstring"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000077-001.md",
        "sha256": "f1f7748fd4963093dd51037917b465ac55ba98bfacb3a6ba6ee5ec7f2d700616"
      },
      "scope": "administrative only",
      "items": [
        "inherited-detach-diagnostic observes existing exllamav3-cache-detach-count-diagnostic; do not create a duplicate defect"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000079-001.md",
        "sha256": "eee4ec398cbbcd3970f16e19816db7854d1a89d133ed6081b3b58512096def68"
      },
      "scope": "before canonical use / future ledger; reviewer-only",
      "items": [
        "Extend unchecked-pack-bitrate to all four K-1 sites, including reconstruct and quantize_tiles; trace self.K on model-loading path",
        "Include zero and negative K triggers",
        "One ledger defect for four sites, introduced at 79; source run observes two, verdict points to other two"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000080-001.md",
        "sha256": "5c370be828374bdd27db8488aa730dfe0a32ccee508258aed75bf933e8bf514b"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Do not present binary64 threshold equality example as float32 repository boundary behavior"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000081-001.md",
        "sha256": "a6e3baf4b4b17cf87dbaa8647b009ed842c0e3a0ea556143ab4c7430db35ecd4"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "Classify top-p-description-mismatch as documentation mismatch; do not imply which competing description is intended"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000082-001.md",
        "sha256": "6afe0d531efa38f7c63c7dd98171a93ff599e1d01d8285871f6a5deea82448a3"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Mention multinomial sample shape (rows,1) versus other branches (rows,) and float expect_sample fixture construction"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000084-001.md",
        "sha256": "5f3252977a5b1cf712f532157ac0ef06bd5d95ddd7b465a070851cf1fc658644"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Search whether callers widen activations to padded width; capture_H uses padded width",
        "Describe padded load_exl3 width mismatch for previously converted unaligned layers"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000086-001.md",
        "sha256": "a58dc0a27ad59c8f43aeae8925286d6d6842b36a88a29806c67c9cc945142994"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "Keep both-axis padding observations at 84 and 86 as one identity; record accepted limitation from PR20",
        "Determine whether Reka unaligned input/output widths occur on same or different layers",
        "Activation-width gap from 84 remains"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000088-001.md",
        "sha256": "dfa23a8cb8e5b939709c911aaf8637e938cd2efb4b292a5bf6ef2ceb8ce83eb7"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "Retained two-axis and padding-before-slicing findings are observations on existing identities from 84/86, not new defects"
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000089-001.md",
        "sha256": "efac1756afa9e24ca05e80ef3c9ae81eb6bd0686a5e484c9f0b0d22789f4b7a3"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "State plainly that headless Linux Python without tkinter cannot import the library after commit 89; new_requirement understates the common-case failure."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000090-001.md",
        "sha256": "4e2ac572fa7e588f26e43947ffc2645bb8c9a864a115dc4496cfd6d58dafc27e"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Canonical entry needs presence/frequency zero-decay window-boundary NaN case; source-derived, not executed.",
        "Negative presence bonus violates unsigned atomic-max positivity assumption; reviewer observation, not teacher input.",
        "File missing-combo-sampler and separate reviewer-observed NaN boundary ledger records."
      ],
      "ledger_records": [
        "reports/defect-ledger/exllamav3-missing-combo-sampler--r001.json",
        "reports/defect-ledger/exllamav3-presfreq-zero-decay-boundary--r001.json"
      ],
      "ledger_status": "accepted as recorded",
      "ledger_verdict": {
        "path": "reviews/verdicts/commit-000091-001.md",
        "sha256": "a8b2907489e8769863440a5296ae372cf6025e61f3bb95239676c18009eb39cc"
      }
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000091-001.md",
        "sha256": "a8b2907489e8769863440a5296ae372cf6025e61f3bb95239676c18009eb39cc"
      },
      "scope": "administrative ledger only; reviewer-only",
      "items": [
        "Record commit 91 as source-verified fix for missing-combo-sampler.",
        "Add ComboSampler public route to zero-decay boundary as an observation on the existing identity."
      ],
      "ledger_records": [
        "reports/defect-ledger/exllamav3-missing-combo-sampler--r002.json",
        "reports/defect-ledger/exllamav3-presfreq-zero-decay-boundary--r002.json"
      ],
      "ledger_status": "accepted as recorded",
      "ledger_verdict": {
        "path": "reviews/verdicts/commit-000092-001.md",
        "sha256": "e3056f06f00498bbbdc9ad0aaea46c395a78ea584d5ad7fee8a7e39fff86e66a"
      }
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000092-001.md",
        "sha256": "e3056f06f00498bbbdc9ad0aaea46c395a78ea584d5ad7fee8a7e39fff86e66a"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "chat-min-p-disable and combo-default-min-p share one root defect; retain one ledger identity with two caller observations.",
        "Chat uses equal sustain and decay, avoiding zero-decay boundary; penalty_range zero disables both penalties."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000096-001.md",
        "sha256": "dae7969eadddc197612da50bb8a332340e31d932ffd98a2c20ecf2a5f502e9bc"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "plain-mlp-allocation is one defect with ParallelDecoderBlock and older TransformerBlock sites; establish the older introducing commit before ledger ingestion."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/modelscope-mirror-implementation-001.md",
        "sha256": "c6cf0153f302342ad95b88df448f18ef2aa658b2a6e167be45a6eda3b3dd3306"
      },
      "scope": "administrative provenance limits; reviewer-only",
      "items": [
        "Weight identity relies on matching service metadata, not local whole-weight hashing.",
        "Official current revision in mirror proofs is identity metadata, not historical availability pin.",
        "Second header URL adds header=metadata to avoid intermediary reuse of the first ranged response; report this transport detail."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000098-001.md",
        "sha256": "ceb937d61cb326dbbb323e476b66cd33355dc59f447ec229beca6060d240c1a3"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "Canonical entry needs its own header comparison: eight full-precision checkpoint shapes, ignored Plus q_norm/k_norm tensors, and incompatible packed 4bit storage.",
        "Clarify tied embeddings defaults for all other eight configurations as well.",
        "Record suspected cohere-qk-normalization external compatibility; reviewer tensor observation belongs to same identity."
      ],
      "ledger_records": [
        "reports/defect-ledger/exllamav3-cohere-qk-normalization--r001.json"
      ],
      "ledger_status": "accepted as recorded",
      "ledger_verdict": {
        "path": "reviews/verdicts/commit-000099-001.md",
        "sha256": "b42b6df0ce650090e06c0f80f3156eb7f2a7f301ebf9fa77eff8be133d0571c9"
      }
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000099-001.md",
        "sha256": "b42b6df0ce650090e06c0f80f3156eb7f2a7f301ebf9fa77eff8be133d0571c9"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Inherited single-device progress is same defect as commit 76; behavior_change classification needs correction before canonical use."
      ]
    }
  ],
  "canonical_followups": [
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000103-001.md",
        "sha256": "853564e10bd59136466ecf0fb2f6d64d9d380e53e3febc6692c915c6099a8810"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Canonical entry must establish tensor comparison from its own header reads; reviewer comparison does not become teacher input."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000104-001.md",
        "sha256": "ff5b0841fe7ee5935a83f6fdc5dac91fcf23b471f6454f62887fb420d52d8c35"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "documentation-dump-scope must be classified as documentation, not defect."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000105-001.md",
        "sha256": "9ecacb0ccb351c9ac4cee30ff76b4e860faea53d9a6f85ab00df4e1f9c143ea0"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "Record stream-argument-mismatch as new at 105, chat example only."
      ],
      "ledger_records": [
        "reports/defect-ledger/exllamav3-chat-stream-argument-mismatch--r001.json"
      ],
      "ledger_status": "pending review with commit 106"
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000106-001.md",
        "sha256": "eaa224b432c5908de49c98e4d081b9eb961b802fcfcc7471544ac32df925a655"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Carry surviving reasoning-boundary-answer-loss from 73/001 and 78/001: closing tag plus answer in one chunk loses answer from all_text."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000108-001.md",
        "sha256": "236f36b791507b86a80075a14e252388e2cf67a46cc5356e1f2494d580c92d61"
      },
      "scope": "ledger restriction; reviewer-only",
      "items": [
        "Do not record commit 108 as a fix for exllamav3-cohere-qk-normalization; model builders do not wire the hooks and per-head weight compatibility is unestablished."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000110-001.md",
        "sha256": "49388233a3ec882aff469ddc45175ec7a08d0e96bb17b3cdac4d4e95b0ddd090"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Canonical Qwen3 entry must establish tensor comparison, tied-embedding storage patterns and FP8 storage format from its own header reads."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000111-001.md",
        "sha256": "c06488d9cef4293421349f69ceb4c016e8534f5f58f76408ba68a74dd230c857"
      },
      "scope": "before canonical use / ledger; reviewer-only",
      "items": [
        "111 nonzero-default-min-p is a fourth observation of the existing SS_MinP zero defect, not a new record. At zero temperature the defect is now unreachable through ComboSampler."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000112-001.md",
        "sha256": "3bf123024513936c7cd1c8a5016b65175207edcda73751d5a28972e8f79f0805"
      },
      "scope": "before canonical use; reviewer-only",
      "items": [
        "Canonical entry should state that Qwen3 residual stream is float32 from the embedding default output dtype, so the widened MLP result is retained. Prior reviewer half-residual guess is withdrawn."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000113-002.md",
        "sha256": "6ce2b9e1984e8d88c94f6cdf56f12c727397dc8a7f36e1ab6c5a44bc9bd01c9f"
      },
      "scope": "canonical / ledger; reviewer-only",
      "items": [
        "Canonical entry should state zero top_p still asserts after 113.",
        "SS_MinP zero observations at 91,92,111 share one identity, fixed at 113; merge and close on next ledger revision.",
        "File SS_TopP zero assertion as reviewer-origin record, introduction unknown.",
        "Record min_p=1 endpoint exclusion at 113 as behavior change on ledger revision."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000114-001.md",
        "sha256": "f3a3844cda0923adf3f661608a52dcd707e6e6b0254e80d02306ef3a9b0a55ca"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "On next revision add 114 to top-p verified affected revisions.",
        "Min-p zero identity at 91,92,111 fixed at 113; endpoint 1.0 exclusion is a one-commit regression at 113 restored by 114, superseding 113 follow-up 3.",
        "Reviewer-observation validator support needs separate implementation request; not urgent. Do not relabel reviewer findings."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000115-001.md",
        "sha256": "a3bd6b9f8f3e0b6eddef295164756d39f1a4780e92b2768238156744fb3a37c5"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "On next top-p revision record fix at a7a6681e11d9bb99f5d1b9e8d223cb402ff80969, fix origin fix_derived from 115 entry; zero becomes active maximum truncation, not neutral. Affected at least 113 and 114; introduction unknown."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000117-001.md",
        "sha256": "6a63a2e6dbe02c93eff1d4289581c0e2742df3ffa1947ba84a779041499d2fb8"
      },
      "scope": "canonical / ledger; reviewer-only",
      "items": [
        "Canonical entry should link introducing commit 151edc00 (102), architecture-mismatch-diagnostic, fixed at 04dc55717c499539504b9a3d8454d631de84f7c2 (117). Record fix on next ledger revision.",
        "Stale expect_arch docstring remains; documentation only."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000118-001.md",
        "sha256": "75db19ffa161a6489e13ec120ef87ba4f1ff5b922ee66b9fcc04b39c012a3d3d"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "On next revision record unconditional-tk-import (89) fixed at 8d07bfb892c1a9347a962e2e439656528dc56d15 (118)."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000119-001.md",
        "sha256": "c4815cd7a5d1d8f9ca89ed8188b3b51907761616b6927a75c22a9ebd56a9fdf8"
      },
      "scope": "canonical / ledger; reviewer-only",
      "items": [
        "Before canonical use cover variant collection API incompatibility, sliced FP16 padding, and fused FP32 conversion regression introduced at 119; file three suspected reviewer-origin candidates with 120.",
        "deferred-bf16-odd-tail approved as drafted.",
        "Smaller reviewer notes: fused padding orientation for nonmultiples of 128 and latent deferred FP32 EXL3 bias consumption; no execution."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000120-001.md",
        "sha256": "f6d5b6ee4edb430f0cb260c9559b93ef61399ac7e4dd4f6fd1bf02e84b9c31bc"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "On next revision add 120 to affected revisions for variant collection, sliced FP16, fused FP32 and odd-tail.",
        "Link metrics-wrapper-compatibility to variant API record and include missing metrics attribute for -lm.",
        "119 deferred-bf16-odd-tail and 120 inherited-bf16-odd-tail are one identity, no second record."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000121-001.md",
        "sha256": "cdce80827a6f116e47c6e37d06783b15fb2f85cff0228c0d8f62a373ef434845"
      },
      "scope": "canonical / ledger; reviewer-only",
      "items": [
        "Canonical 121 should link 647bb7d5 (119) as introducing the same-directory same-stem object conflict; add this to 119 canonical-use list.",
        "On next ledger revision one suspected fix-derived record: introduced 647bb7d549b8485ad052ac0650148bd35fcee6d4, fixed 3c801c61b01407d13e609524941333c9a9198f80; affected 119 and 120. No build executed or exact build failure established."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000122-001.md",
        "sha256": "27c70aaf49a52f60bd0fc73fc9b2da5af7d93852474f3a91a5bbaa89e334497e"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "One identity: repetition penalty turns masked logits into NaN, introduced at 40863d06 (90). Factor-zero case fixed at a65386545773f0e1dc66146e7050f6c0f5a9e3e4 (122), fix-derived; factor-one remains open. Record partial fix, not two defects."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000123-001.md",
        "sha256": "d2c0355fb7bd13790849dff3bb279a5e9c09866ae1e634feab2bfc28ade3e78a"
      },
      "scope": "canonical / ledger; reviewer-only",
      "items": [
        "Cover unguarded shape-3 selector returns and removed launch-time divisibility checks before canonical use; file suspected reviewer-origin candidate with 124.",
        "DevCtx already existed; describe move to its own file.",
        "boolean-dimension-threshold approved as drafted; 12/30 section coverage accepted after reviewer inspected remainder."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000124-001.md",
        "sha256": "7bf2d1f2a7cccb91e14931c62e2f53416baf1ce9cf68c088d67d71b0fe79afb5"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "On next revision record humaneval-top-k-float as second site of chat-top-k-float identity from 92; not a new defect."
      ]
    },
    {
      "verdict": {
        "path": "reviews/verdicts/commit-000125-001.md",
        "sha256": "05abb6b7e86cb1d1e9e0a544b5706b179192327376865cfb0e47be826ff229b9"
      },
      "scope": "ledger; reviewer-only",
      "items": [
        "No new top-k record/site for merge 125. On next revision list 57a37f2658fa2b3deac5e3404d2df7120223a69a as affected under the 92 identity and 124 HumanEval site."
      ]
    }
  ],
  "chat_stream_ledger_review": {
    "r001": "accepted",
    "verdict": {
      "path": "reviews/verdicts/commit-000106-001.md",
      "sha256": "eaa224b432c5908de49c98e4d081b9eb961b802fcfcc7471544ac32df925a655"
    },
    "r002": "reports/defect-ledger/exllamav3-chat-stream-argument-mismatch--r002.json",
    "r002_status": "accepted",
    "r002_verdict": {
      "path": "reviews/verdicts/commit-000107-001.md",
      "sha256": "84fa2bdc3517a9428e0dcab274221944cfadb41af534239e6d5c144001cfa320"
    }
  },
  "top_p_ledger_review": {
    "record": "reports/defect-ledger/exllamav3-top-p-zero-assertion--r001.json",
    "status": "accepted_as_filed",
    "verdict": {
      "path": "reviews/verdicts/commit-000114-001.md",
      "sha256": "f3a3844cda0923adf3f661608a52dcd707e6e6b0254e80d02306ef3a9b0a55ca"
    },
    "historical_context_eligible": false,
    "training_eligible": false
  },
  "commit119_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-variant-collection-loader-api--r001.json",
      "reports/defect-ledger/exllamav3-sliced-fp16-padding-target--r001.json",
      "reports/defect-ledger/exllamav3-fused-fp32-weight-conversion--r001.json"
    ],
    "status": "accepted_as_filed",
    "origin_validator_limit": "reviewer_observation unsupported; evidence hashes verified; no implementation changed",
    "verdict": {
      "path": "reviews/verdicts/commit-000119-001.md",
      "sha256": "c4815cd7a5d1d8f9ca89ed8188b3b51907761616b6927a75c22a9ebd56a9fdf8"
    },
    "acceptance_verdict": {
      "path": "reviews/verdicts/commit-000120-001.md",
      "sha256": "f6d5b6ee4edb430f0cb260c9559b93ef61399ac7e4dd4f6fd1bf02e84b9c31bc"
    }
  },
  "commit123_ledger_candidate": {
    "record": "reports/defect-ledger/exllamav3-gemm-selector-divisibility--r001.json",
    "status": "accepted_as_filed",
    "origin_validator_limit": "reviewer_observation unsupported; evidence hashes verified; no implementation changed",
    "verdict": {
      "path": "reviews/verdicts/commit-000123-001.md",
      "sha256": "d2c0355fb7bd13790849dff3bb279a5e9c09866ae1e634feab2bfc28ade3e78a"
    },
    "acceptance_verdict": {
      "path": "reviews/verdicts/commit-000124-001.md",
      "sha256": "7bf2d1f2a7cccb91e14931c62e2f53416baf1ce9cf68c088d67d71b0fe79afb5"
    }
  },
  "commit126_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000126-001.md",
      "sha256": "298459c39ccd7a9d76b96cf5d7294bc39b0b4ce0e128ffeee15b7cc9d4794b00"
    },
    "ledger": "deferred-cuda-error-number approved as drafted; deferred CPU captured-but-unreported errno belongs to the same record.",
    "reviewer_only": "Post-cutoff issue 33 diagnosis and handle-caching/119 introduction leads stay out of teacher input; track for later ledger investigation. Worker errno may be stale for CUDA-copy failure or short read; no execution verified."
  },
  "commit127_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000127-001.md",
      "sha256": "41e9cbc032b12f73476081b2c8674f0497d4d0d0d48d7428c8992430faeb1cc7"
    },
    "canonical_required": "Name directions: printed KL divergence (A, B) computes KL(B || A), and printed (B, A) computes KL(A || B). Reviewer-only; never teacher input.",
    "ledger": "ppl-vocabulary-bound approved as drafted; no effect on reported numbers for vocabularies >= 2047 at this commit; larger vocabularies produce trailing empty slices. No model execution verified.",
    "reviewer_only": "Head padding columns participate in metrics without sampler-style masking; values and effect not established. Keep outside teacher input."
  },
  "commit128_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000128-001.md",
      "sha256": "1a456adfc82783706ac740a5f6ebd24b55ee3d13d63d5cdce581553fe17c83a0"
    },
    "ledger_when_next_revised": "Fix-derived suspected handle-accumulation record: per-file caching introduced at root, worsened at 119 (647bb7d5, five to eight handles); fixed by 128 (4710c012). No execution or handle-count measurement. Reviewer-only, excluded from teacher input.",
    "storage_followups": "Skip explanation and hard-link transfer documentation accepted; no further action required."
  },
  "commit129_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000129-001.md",
      "sha256": "d63398c35666f232531115d28d547f0e8b2370e68112ee949ef21e5c1a574f3b"
    },
    "ledger": "Scalar-codebook-double-transform and missing-gemv-header approved as drafted, introduced129 c4867edd. Header identity distinct from root quant/exl3_gemv.cuh/bindings.cpp. Boolean threshold retains123 identity;129 affected. Add129 to selector-divisibility record.",
    "reviewer_only": "Future-fix expectations and latent int product overflow excluded from teacher input.",
    "selector_divisibility_revision": {
      "path": "reports/defect-ledger/exllamav3-gemm-selector-divisibility--r002.json",
      "status": "accepted_as_filed",
      "evidence_hashes_verified": true,
      "origin_limitation": "Preserves accepted reviewer_observation origin; excluded from historical context and training; validator origin vocabulary unchanged.",
      "verdict": {
        "path": "reviews/verdicts/commit-000130-001.md",
        "sha256": "44bba3cca2dbf5ef9bded2c4de5a20ad946c0473d61fd7b4dbf59a1f7d925a40"
      },
      "next_revision_note": "Correct at129 typo only when next revised."
    }
  },
  "commit130_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000130-001.md",
      "sha256": "44bba3cca2dbf5ef9bded2c4de5a20ad946c0473d61fd7b4dbf59a1f7d925a40"
    },
    "ledger": "Unicode flush bypass introduced130; checkpoint-token attribute and terminal bypass each root543c4b27 identity,130 affected. Earlier129 records still owed.",
    "reviewer_only": "Checkpoint token counting/restore interaction remains untraced; no record requested. Future fix hint excluded from teacher input."
  },
  "commit131_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-scalar-codebook-double-transform--r001.json",
      "reports/defect-ledger/exllamav3-missing-gemv-kernel-header--r001.json",
      "reports/defect-ledger/exllamav3-boolean-dimension-threshold--r001.json",
      "reports/defect-ledger/exllamav3-unicode-flush-string-bypass--r001.json",
      "reports/defect-ledger/exllamav3-checkpoint-token-attribute--r001.json",
      "reports/defect-ledger/exllamav3-terminal-string-bypass--r001.json",
      "reports/defect-ledger/exllamav3-scalar-codebook-double-transform--r002.json"
    ],
    "status": "accepted_as_filed",
    "schema_and_evidence_validation": "passed",
    "historical_context_eligible": false,
    "verdict": {
      "path": "reviews/verdicts/commit-000131-001.md",
      "sha256": "8fb043f749520d23b11690c118d5b62d96375a9823df3f228c5dd91f1cf08d34"
    },
    "next_revision_notes": [
      "Drop pending review on scalar fix status and correct for65,502 typo.",
      "Use neutral descriptions for root checkpoint-token and terminal-string defects."
    ]
  },
  "commit131_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000131-001.md",
      "sha256": "8fb043f749520d23b11690c118d5b62d96375a9823df3f228c5dd91f1cf08d34"
    },
    "outstanding_ledger": [
      "min-p",
      "top-p",
      "mismatch diagnostic",
      "tk import",
      "object-name conflict",
      "repetition-penalty NaN",
      "handle accumulation",
      "119 affected revisions",
      "humaneval top-k",
      "126 errno pair"
    ],
    "reviewer_only": "Future-header-fix prediction excluded from teacher input."
  },
  "commit132_ledger_candidate": {
    "path": "reports/defect-ledger/exllamav3-missing-gemv-kernel-header--r002.json",
    "status": "accepted_as_filed",
    "schema_and_evidence_validation": "passed",
    "verdict": {
      "path": "reviews/verdicts/commit-000132-001.md",
      "sha256": "12f6d2bf0a3350eecb388433973f7513174b44423f84d5c7647db0eb4ac3fbba"
    },
    "next_revision_note": "Fix confirmed by source; drop pending review status on next revision."
  },
  "commit132_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000132-001.md",
      "sha256": "12f6d2bf0a3350eecb388433973f7513174b44423f84d5c7647db0eb4ac3fbba"
    },
    "root_header_fix_check": {
      "path": "reports/defect-ledger/exllamav3-missing-exl3-gemv-header--r001.json",
      "sha256": "0a225c09b591ddc40b87acf14069ad3037c86a85753339ab61a9381b0a75cf16",
      "fix_already_recorded": "7163258443e84ddfee2517adb6d8d46794c507d1",
      "position": 6,
      "evidence_hashes_verified": true,
      "revision_needed": false
    },
    "earlier_ledger_followups": "Remain tracked; no teacher input."
  },
  "commit133_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000133-001.md",
      "sha256": "1151b69aa52459792255048dc48b581e5bcc736c3f3d11ecbff4e3525c31884f"
    },
    "root_header_fix_check": "Accepted; fix already recorded at6.",
    "ledger": "Create multi-gemm-leading-dimension-validation introduced133; add133 affected to Boolean-threshold and selector-divisibility identities.",
    "reviewer_only": "Additional unchecked wrapper inputs, aliasing scratch and zero-grid notes remain source-only, never teacher input."
  },
  "commit134_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-multi-gemm-leading-dimension-validation--r001.json",
      "reports/defect-ledger/exllamav3-boolean-dimension-threshold--r002.json",
      "reports/defect-ledger/exllamav3-gemm-selector-divisibility--r003.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "Two authoring-observation records pass; selector-divisibility preserves accepted reviewer_observation origin outside current validator vocabulary.",
    "historical_context_eligible": false,
    "verdict": {
      "path": "reviews/verdicts/commit-000134-001.md",
      "sha256": "de98cbc650b536e2f46d833b7c059f4e93969f1a7a6c3ea4e2ad9a972ff8d43d"
    },
    "next_revision_note": "Correct limits spacing at123,129 and133 when the two selector records are next revised."
  },
  "commit134_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000134-001.md",
      "sha256": "de98cbc650b536e2f46d833b7c059f4e93969f1a7a6c3ea4e2ad9a972ff8d43d"
    },
    "earlier_ledger_followups": "Still owed; tracked in journal.",
    "reviewer_only": "Non-half error behavior and CPU branch side effect stay outside teacher input."
  },
  "commit135_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-deferred-read-errno-reporting--r001.json",
      "reports/defect-ledger/exllamav3-conversion-handle-accumulation--r001.json"
    ],
    "status": "accepted_as_filed",
    "schema_and_evidence_validation": "passed",
    "historical_context_eligible": false,
    "verdict": {
      "path": "reviews/verdicts/commit-000135-001.md",
      "sha256": "a6314835ff4e73ab581d715e6b7c205ca1f89d694612819750de32ea4e267557"
    }
  },
  "commit135_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000135-001.md",
      "sha256": "a6314835ff4e73ab581d715e6b7c205ca1f89d694612819750de32ea4e267557"
    },
    "ledger": "One zero-cap identity introduced123, copied133, division135; scratch new requirement introduced135; add135 affected to133 dimension-validation with output-write consequence.",
    "reviewer_only": "Scratch/input alias race stays out of teacher input.",
    "older_followups": "Remaining earlier ledger revisions still owed."
  },
  "commit136_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-gemm-zero-grid-cap--r001.json",
      "reports/defect-ledger/exllamav3-mgemm-broadcast-scratch-capacity--r001.json",
      "reports/defect-ledger/exllamav3-multi-gemm-leading-dimension-validation--r002.json"
    ],
    "status": "accepted_as_filed",
    "schema_and_evidence_validation": "passed",
    "historical_context_eligible": false,
    "verdict": {
      "path": "reviews/verdicts/commit-000136-001.md",
      "sha256": "6eeba01d95f73fa417401f4362e63d7b52407e14fdb4f6df14e00171ff6215e3"
    }
  },
  "commit136_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000136-001.md",
      "sha256": "6eeba01d95f73fa417401f4362e63d7b52407e14fdb4f6df14e00171ff6215e3"
    },
    "canonical_required": "Add Python3.12 int.is_integer finding or later attempt stating it;136 remains ancestor-only.",
    "ledger": "Reviewer-observation integer-check compatibility record introduced136; no fix yet; never historical context/training.",
    "reviewer_only": "Future-fix hint and optimized-Python note excluded from teacher input."
  },
  "commit137_ledger_candidate": {
    "path": "reports/defect-ledger/exllamav3-top-k-int-is-integer-compatibility--r001.json",
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "origin_limitation": "Requested reviewer_observation origin is outside current validator vocabulary; administrative only.",
    "verdict": {
      "path": "reviews/verdicts/commit-000137-001.md",
      "sha256": "abee5ae42288ff1c2e26be6c14ccccb8053e2623da9a51c235b8d0f4c23fc668"
    }
  },
  "commit137_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000137-001.md",
      "sha256": "abee5ae42288ff1c2e26be6c14ccccb8053e2623da9a51c235b8d0f4c23fc668"
    },
    "ledger": "Empty-codeblock-feedback introduced137 approved as drafted.",
    "reviewer_only": "Slash soft-switch/path consequences and color-comment note stay outside teacher input.",
    "older_followups": "Remaining earlier ledger revisions still owed."
  },
  "commit138_ledger_candidate": {
    "path": "reports/defect-ledger/exllamav3-empty-codeblock-feedback--r001.json",
    "status": "accepted_as_filed",
    "schema_and_evidence_validation": "passed",
    "verdict": {
      "path": "reviews/verdicts/commit-000138-001.md",
      "sha256": "63eadf95a7ba1db1a57fc3ef7ef55cdf12a4fe67195ff17948959f754c301cf0"
    }
  },
  "commit138_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000138-001.md",
      "sha256": "63eadf95a7ba1db1a57fc3ef7ef55cdf12a4fe67195ff17948959f754c301cf0"
    },
    "ledger": "Fix-derived ignored in-memory transpose: introduced119 647bb7d5, fixed138 538dcae3; rectangular shape error, square wrong calibration source-only.",
    "reviewer_only": "General lesson and module reach uncertainty stay outside teacher input.",
    "older_followups": "Remaining earlier ledger revisions still owed."
  },
  "commit139_ledger_candidate": {
    "path": "reports/defect-ledger/exllamav3-in-memory-weight-transpose--r001.json",
    "status": "accepted_as_filed",
    "schema_and_evidence_validation": "passed",
    "verdict": {
      "path": "reviews/verdicts/commit-000139-001.md",
      "sha256": "5c7282f76a8ea8dc1cb28495334368787efe253a65190f567e06f7d84636febb"
    }
  },
  "commit139_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000139-001.md",
      "sha256": "5c7282f76a8ea8dc1cb28495334368787efe253a65190f567e06f7d84636febb"
    },
    "ledger": "All-expert-fused-shape introduced139; reviewer-observation fused intermediate dtype introduced139 with unset/non-half caller condition.",
    "reviewer_only": "Calibration_all_experts requirement to check at architecture registration; padding and earlier MGEMM compatibility notes excluded from teacher input.",
    "older_followups": "Remaining earlier ledger revisions still owed."
  },
  "commit140_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-all-expert-fused-shape--r001.json",
      "reports/defect-ledger/exllamav3-block-sparse-fused-intermediate-dtype--r001.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "Authoring-observation record passes; requested reviewer_observation origin remains outside current validator vocabulary.",
    "historical_context_eligible": false,
    "verdict": {
      "path": "reviews/verdicts/commit-000140-001.md",
      "sha256": "8d2148d666b0bbb2786668cd9f416fc3a9f7b8c257643d172b671922d2de27e7"
    }
  },
  "commit140_followups": {
    "verdict": {
      "path": "reviews/verdicts/commit-000140-001.md",
      "sha256": "8d2148d666b0bbb2786668cd9f416fc3a9f7b8c257643d172b671922d2de27e7"
    },
    "ledger": "BF16 odd tail introduced119 with140 affected; reviewer-only missing abort introduced140; variant collection140 affected.",
    "reviewer_only": "Failure-state and variant collection notes excluded from teacher input;119 flush description discrepancy untraced."
  },
  "commit141_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-deferred-bf16-odd-tail--r001.json",
      "reports/defect-ledger/exllamav3-single-load-missing-deferred-abort--r001.json",
      "reports/defect-ledger/exllamav3-variant-collection-loader-api--r002.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "Authoring record passes; two reviewer_observation records preserve requested origin outside current vocabulary.",
    "historical_context_eligible": false,
    "acceptance": {
      "verdict": "reviews/verdicts/header-budget-implementation-001.md",
      "sha256": "2269b30b4de6583510f3b16e89235e5a9e3ad448c738431e193a32ba38d89148",
      "status": "accepted"
    }
  },
  "commit141_followups": {
    "ledger": "Add 141 affected to all-expert-fused-shape, 128 versus 8",
    "canonical": "Header findings and published variant compatibility required before canonical use; reviewer-only, never teacher input",
    "verdict_sha256": "ac8212ce237944cd159421451f42d3b586d7d7e7cc522c302a47d804c4690f2e"
  },
  "commit142_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-all-expert-fused-shape--r002.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "passed",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000142-001.md",
    "verdict_sha256": "6620739a76739b9bfa58e309cb85773bf159c47e6773a61bcf50097960145b62"
  },
  "commit142_followups": {
    "ledger": "Single repetition-penalty NaN identity introduced 90, partially fixed 122, fixed 142",
    "reviewer_only": true,
    "verdict_sha256": "6620739a76739b9bfa58e309cb85773bf159c47e6773a61bcf50097960145b62"
  },
  "commit143_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-repetition-penalty-masked-nan--r001.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "passed",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000143-001.md",
    "verdict_sha256": "f4aeb9c4ebcd10a85a02f6df61f81730d4fd41944185a55cca51b40ce191dc2f"
  },
  "commit143_followups": {
    "at_merge": "10222646",
    "ledger": "Add wheel matrix Python 3.10/3.11 build targets as evidence to exllamav3-top-k-int-is-integer-compatibility when merge reached",
    "reviewer_only": true,
    "verdict_sha256": "f4aeb9c4ebcd10a85a02f6df61f81730d4fd41944185a55cca51b40ce191dc2f",
    "request_clerical_correction": "143 request said 141 approval; actual prior approval and listed verdict hash were 142"
  },
  "commit144_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-top-k-int-is-integer-compatibility--r002.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "Preserves requested reviewer_observation origin outside unchanged validator vocabulary.",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000144-001.md",
    "verdict_sha256": "3bb1950975ca0185c35f550b0607420ea84a0452fb0400bcc3ade23e5320fbb5"
  },
  "commit144_followups": {
    "older_ledger_revisions": "remain tracked",
    "reviewer_only": true,
    "verdict_sha256": "3bb1950975ca0185c35f550b0607420ea84a0452fb0400bcc3ade23e5320fbb5"
  },
  "commit145_followups": {
    "ledger": [
      "Fix-derived unset max_total_tokens introduced root fixed 145",
      "Annotation mismatch introduced 145, no runtime effect"
    ],
    "reviewer_only": true,
    "verdict_sha256": "c4e752aed10e1a65511550113a9cd095fb933b7799b2a8680f0ff0922a6b09c6"
  },
  "commit146_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-empty-utf32-return-annotation--r001.json",
      "reports/defect-ledger/exllamav3-unset-max-total-tokens--r001.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "passed",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000146-001.md",
    "verdict_sha256": "f6399bef02d6695c90fd6c9ac1dd7a892d9b35b8d4bd5f67d674a760cca3df24"
  },
  "commit146_followups": {
    "ledger": "Next unset-max-total-tokens revision: add 146 as development-line fix merge and PR36 traceback as external observation",
    "reviewer_only": true,
    "verdict_sha256": "f6399bef02d6695c90fd6c9ac1dd7a892d9b35b8d4bd5f67d674a760cca3df24"
  },
  "commit147_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-unset-max-total-tokens--r002.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "passed",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000147-001.md",
    "verdict_sha256": "150a43b07c1b62c73606ee297a7f22b02969cf15aa2b22a8a152e8efc0dd5c5b"
  },
  "commit147_followups": {
    "ledger": [
      "Next repetition-penalty-masked-nan revision: maintainer PR35 explanation as external observation, eligible only from 144 on",
      "Next 92 top-k identity revision: HumanEval site fixed at beb7bcd9 (147), same identity as 92 and 124"
    ],
    "reviewer_only": true,
    "verdict_sha256": "150a43b07c1b62c73606ee297a7f22b02969cf15aa2b22a8a152e8efc0dd5c5b"
  },
  "commit148_followups": {
    "ledger": "Pending repetition-penalty NaN revision: cite 148 entry for maintainer explanation eligible on master; 144 on dev",
    "reviewer_only": true,
    "verdict_sha256": "1f936e5ef25407ec3ecc52258d1033a75e0460b8666f7aeeee1270fb76e47e36"
  },
  "commit149_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-repetition-penalty-masked-nan--r002.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "passed",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000149-001.md",
    "verdict_sha256": "815b7e557174b9d693294db1a4e97f9303fd0c5bc2cefff29a3de0808d08a666"
  },
  "commit149_followups": {
    "ledger": "Add 149 affected and HumanEval default reach to top-k compatibility, reviewer observation",
    "canonical": "149 must state older-Python integer-check finding with merge-specific reach before canonical use",
    "reviewer_only": true,
    "verdict_sha256": "815b7e557174b9d693294db1a4e97f9303fd0c5bc2cefff29a3de0808d08a666"
  },
  "commit150_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-top-k-int-is-integer-compatibility--r003.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "Preserves requested reviewer_observation origin outside unchanged validator vocabulary.",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000150-001.md",
    "verdict_sha256": "79368fab71da8d5724b9b1c7679c12e1c74632eb59e14290d34aacce6a9336c2"
  },
  "commit150_followups": {
    "catalog": "Investigate closed-catalog exact path overlap as independent qualifier; nonblocking implementation request",
    "canonical": "150 needs eligible PR35 comment available before canonical use",
    "ledger": "Fix-derived unconditional BOS: root introduction, fixed 150, no marker-recognition execution",
    "reviewer_only": true,
    "verdict_sha256": "79368fab71da8d5724b9b1c7679c12e1c74632eb59e14290d34aacce6a9336c2"
  },
  "commit151_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-humaneval-unconditional-bos--r001.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "passed",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000151-001.md",
    "verdict_sha256": "1ddafa816d7722e0837efadfd47a58a17d4b541673fcd0f3bb9418e59318763a"
  },
  "closed_path_overlap_implementation": {
    "status": "accepted",
    "request": "reviews/requests/closed-path-overlap-implementation-001.md",
    "request_sha256": "f05e3499441dd93faba80e0f48a90339b10c27b707af3e83c8c1420c776b17bc",
    "report": "reports/closed-path-overlap-implementation-001.json",
    "nonblocking": true,
    "default_rule": "salience-v2",
    "proposed_rule": "salience-v3-paths",
    "verdict": "reviews/verdicts/closed-path-overlap-implementation-001.md",
    "verdict_sha256": "3cb4af9b7b1800145b5c2138c7f5adae421ac6585168cdc4397d20010f35ff99",
    "conditions": [
      "Report path-only qualifying row count and cap truncation in each request",
      "Stop before authoring at first cut path-qualified row and propose ordering",
      "Do not regenerate bound packets/runs through 151; retain 150 canonical condition"
    ],
    "activation_note": "Acceptance first read after 152/001 completed under v2; preserve authored run, flag timing in 152 request, use v3 for next newly prepared packet.",
    "next_new_packet_rule": "salience-v3-paths"
  },
  "commit151_followups": {
    "ledger": "Top-k compatibility fixed 95cfa726, title upstream confirmation; retain 136 and 149 canonical conditions",
    "reviewer_only": true,
    "verdict_sha256": "1ddafa816d7722e0837efadfd47a58a17d4b541673fcd0f3bb9418e59318763a"
  },
  "commit152_ledger_candidates": {
    "records": [
      "reports/defect-ledger/exllamav3-top-k-int-is-integer-compatibility--r004.json"
    ],
    "status": "accepted_as_filed",
    "evidence_hashes_verified": true,
    "schema_validation": "Preserves requested reviewer_observation origin outside unchanged validator vocabulary.",
    "historical_context_eligible": false,
    "verdict": "reviews/verdicts/commit-000152-001.md",
    "verdict_sha256": "70e49d928e4abd9ffffeba23cd9a6de650c04266e0590cfd3bc81d687cafc311"
  },
  "commit152_followups": {
    "older_ledger_revisions": "remain tracked",
    "verdict_sha256": "70e49d928e4abd9ffffeba23cd9a6de650c04266e0590cfd3bc81d687cafc311"
  },
  "commit153_followups": {
    "verdict": "reviews/verdicts/commit-000153-002.md",
    "verdict_sha256": "1ed558b6edb6c31262812a5466b9162561d82f24cc183ea72278ffc055814815",
    "ledger_note": "reports/commit-000153-affected-identities-001.json",
    "canonical_conditions": [
      "Tensor headers and published variant loading remain unvalidated.",
      "Reviewer-assisted canonical use requires a selection decision."
    ],
    "older_ledger_revisions": "still owed",
    "revised_verdict_notes": "Decision unchanged; eight identities reach first-parent line at 153; identical-tree location fields require no change."
  },
  "commit154_followups": {
    "verdict": "reviews/verdicts/commit-000154-001.md",
    "verdict_sha256": "f390c6e559ce02c60cdd9a7d1c23dee0f1f0d103d72ba7f72b203b023adf6944",
    "accepted_note": "reports/commit-000153-affected-identities-001.json",
    "ledger_due": [],
    "older_ledger_revisions": "still owed"
  },
  "commit155_ledger_candidates": {
    "report": "reports/commit-000155-ledger-candidates-001.json",
    "status": "accepted_with_wording_followup"
  },
  "commit155_followups": {
    "verdict": "reviews/verdicts/commit-000155-001.md",
    "verdict_sha256": "3d440a9ef19dff55e1ee9cff9fe7d4b53e8a0ebd274f81083ec0860e0a76b02c",
    "ledger_due": [],
    "older_ledger_revisions": "still owed"
  },
  "commit156_ledger_candidates": {
    "report": "reports/commit-000156-ledger-candidates-001.json",
    "status": "accepted"
  },
  "commit156_followups": {
    "verdict": "reviews/verdicts/commit-000156-001.md",
    "verdict_sha256": "fbb32aa94a04aa7c2953e02a9de9b29a22a8ce5f08b718e2da12b115f37c9a8e",
    "next_sliced_fp16_revision": "Replace earlier-mismatch wording: mismatch is this defect itself; reporter revision is not pinned. No standalone revision required.",
    "older_ledger_revisions": "still owed"
  },
  "commit157_followups": {
    "verdict": "reviews/verdicts/commit-000157-001.md",
    "verdict_sha256": "9a11568d7622543ae9413b4926ece64ed952f70bd7b85b6d2a6b3ecec78f4a28",
    "new_ledger_work": false,
    "older_ledger_revisions": "still owed"
  },
  "token_cost_implementation": {
    "status": "implementing",
    "proposal": "reviews/fable/TOKEN-COST-PROPOSAL.md",
    "proposal_sha256": "28f60a2f8c92abba3247eca6992adfd933dadbbe30b88ab3d633b7e7267269aa",
    "parts": [
      "A: repository blocking cycle driver and approval command",
      "B: mechanically generated request skeleton",
      "C: durable follow-up and procedure tracking"
    ],
    "current_commit": 158,
    "current_blocker": null,
    "sequence": "Resolve 158 access, finish and file 158, then implement A/B/C and file token-cost-implementation-001 before any 159 teacher run.",
    "request": "reviews/requests/token-cost-implementation-001.md",
    "acceptance_required_before_next_commit": true,
    "teacher_visible_changes_allowed": false,
    "required_validation": [
      "Full host-enabled suite with stop-condition tests",
      "At least two approved-commit scratch rebuild comparisons: identical manifests and standing instructions",
      "Request counts and hashes preserved",
      "No verdict, ledger or tracking content in teacher input"
    ],
    "part_D": "Fable owns config change and restart after acceptance; do not change it here."
  }
}
```

## Recorded commit-000158-001

Approval: `reviews/verdicts/commit-000158-001.md`, sha256 `4f53256e13221d4d4be13dfd2006e334a7ba7a6ddd5e88966e4db002c3cc4b3d`. Discovery 004 accepted; no new ledger work.
Canonical: teacher did not read headers; reviewer header comparison is not entry evidence.
Comparison to Qwen3 MoE builder remains a canonical enhancement.
Older ledger revisions remain owed. Token-cost A/B/C request already filed; wait before 159.

## Token-cost implementation verdict

Accepted in substance, four fixes required before 159. Source: `reviews/verdicts/token-cost-implementation-001.md`, sha256 `4f96bd4c90ade55944e91fade0792b8eed44b70509f00b4991c215b75f916a31`.
Fix request: reviews/requests/token-cost-fixes-001.md. Fable applies part D after acceptance.

## Token-cost acceptances — 2026-11-15

A/B/C accepted in substance by `reviews/verdicts/token-cost-implementation-001.md` (sha256 4f96bd4c90ade55944e91fade0792b8eed44b70509f00b4991c215b75f916a31); all four fixes accepted by `reviews/verdicts/token-cost-fixes-001.md` (sha256 cefae5a7e94552db87083ce2c80594164bedccedcade13b02779094d04000ec8). Request hashes verified before administrative updates. Procedure now forbids printing the journal whole. Part D applied by Fable at 90000; user restarted window and authorized 159. Implementation advancement pause cleared; monitor 159–163. No teacher-visible changes.

## First live cycle — 159/160

159/001 mechanically approved (unsampled), 160/001 filed for full review in reviews/requests/commit-000160-001.md. Both fully read their sole task section; no findings. Cycle validation passed. No 161 started. Publishing unexpectedly emitted the full journal (tool output truncated); procedure step 11 now explicitly redirects publisher stdout to a temporary file and extracts only needed keys. No teacher input affected.

## Recorded commit-000160-001

Ancestor retrieval only. reviews/verdicts/commit-000160-001.md sha256 ced1fbcac12860ac9cd9a6a46a3b8fa3f3ac517fbf1cfd74247cafd2a3fc22e3

### Follow-ups

1. No ledger work from 159 or 160.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

None for this entry.

160 administrative correction: Fable, not the user, restarted the window after applying part D. No ledger work from 159/160; older revisions remain owed.

## Part E implementation pending — after 161 filing

Request reviews/requests/token-cost-detach-001.md; 277 host-enabled tests pass. setsid dummy-state smoke completed but queued notification could not resume thread: no local daemon/remote configured. Required failure report saved. Do not adopt detached live launch until review and verified wake-up route. 162 paused; no teacher started.

## Recorded commit-000161-001

Ancestor retrieval only. reviews/verdicts/commit-000161-001.md sha256 d3d32cc7497a4783600c93a15f1d416965998611ebae07521dda5ca8654e9b05

### Follow-ups

1. Ledger, `exllamav3-model-diff-unconditional-deferral`: file r003. From `48747ba0` the masking described in
   r002 is gone; add 161 as an affected revision with the mechanism in the first reviewer note, and state the
   reach: `eval/model_diff.py` with an unquantized model whose MLP is sliced. Still suspected, source inspection
   only, excluded from teacher input.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

None for this entry.

## 161 ledger acceptance and follow-up filing

Padding-target r003 accepted; fix at 161 is reviewer-confirmed by source inspection, no execution. Original candidate remains immutable. Unconditional-deferral r003 filed as an administrative addendum to token-cost-detach-001: 161 affected, model_diff sliced unquantized MLP reach now unmasked, still suspected and never teacher input. Part E review remains pending before 162.

## Detached smoke notification delivered

The queued smoke-test notification was subsequently delivered to this thread. Its saved result is advancement_paused and the live journal still has no 162 run. Eventual message delivery is observed; automatic resume remains unproven because the queue command reported a resume failure. This does not clear the part E pause.

## 2026-11-15 — detached cycle accepted for 162

reviews/verdicts/token-cost-detach-001.md SHA256 `638472000ff42b07e209939b44110bf50c8f0bf05cae4b492c34ff6e73d39c6c`: accepted. Queue-triggered smoke delivery confirmed by reviewer; exit 0 plus Queued message now succeeds despite resume warning. Full host suite: 278 tests passed. New hashes saved in reports/token-cost-detach-acceptance-001.json for 162 request. Unconditional-deferral r003 accepted, suspected/source only, excluded from teacher input. Prior smoke artifacts preserved. Part E pause cleared under explicit verdict; use setsid -f and end turn after confirming log.

## 162/001 filed

Unassisted request reviews/requests/commit-000162-001.md filed after detached cycle completion. Both task sections fully read; no findings, no new ledger candidate. Scalar-only execution and partial linear.py read disclosed. Salience-v3-paths: 0 closed/path-only rows, no truncation. Notification success change and new hashes included with 278-test result per accepted part E verdict. Await 162 verdict before 163.

## Recorded commit-000162-001

Ancestor retrieval only. reviews/verdicts/commit-000162-001.md sha256 f7e99ad345973aaf2677147582ad1be40a0619f39302fd1dc153f752d8a19dad

### Follow-ups

1. Ledger: a reviewer-observation record, classification `new_requirement`, introduced at `a19538cf`:
   `fwd_exllamav3` writes in place into an inference tensor and therefore requires its caller to be in inference
   mode; satisfied by `compare_q.main` at this commit. Source inspection only, not executed, excluded from
   teacher input.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

- The sentence in Reasoning that the three edits address their concerns "independently", and the missing
  dependency between the in-place mask and inference mode.

## 162 reviewer-observation candidate prepared

Created reports/defect-ledger/exllamav3-compare-q-inference-mask-context--r001.json for next request: new_requirement introduced a19538cf, already satisfied by main, suspected/source only, no PyTorch execution. Evidence is the preserved 162 verdict. Never teacher input; known reviewer_observation validator limitation retained. Canonical condition remains on the immutable entry’s independence sentence and omitted mask/context dependency. Notify change accepted.

## 163/001 filed

reviews/requests/commit-000163-001.md: fresh unassisted run; all 14 sections read; one conditional extra-tensor warning finding. Scalar shard-plan execution only, no model/serialization run. No ancestor prose read; caller-tail coverage disclosed. Two closed catalog rows selected, one path-only, no truncation. Reviewer-observation inference-mask-context r001 from 162 filed separately in this request, excluded from teacher input. Await verdict before 164.

2026-11-15: 163/001 rejected; reviews/verdicts/commit-000163-001.md sha256 e936787b342ab65e68a1afd92233dd4467582b705c5cd6f2dbbe37cfebcd98c7. All 14 request hashes verified. Fresh assisted 002 authorized with separate coverage only; no later runs/dependents. Inference-mask r001 accepted. Class/mapping ledger follow-up pending fresh attempt; reviewer details excluded from teacher.

2026-11-15: 163/002 reviewer-assisted request filed at reviews/requests/commit-000163-002.md, sha256 791b875e04e8a917ab5b8de1d67e759a015be8e214ae556cb88c486e491b8927. All 14 sections, 18/18 replay, one ancestor prose read. Qwen3 MoE class/mapping finding independently reported under the coverage request; r001 candidate uses authoring origin per 001 verdict. No carryover of 001 extra-tensor warning finding. Awaiting full review at 163; no 164 started.

## Recorded commit-000163-002

Ancestor retrieval only, reviewer-assisted. reviews/verdicts/commit-000163-002.md sha256 e0215c118ecb4a32fe72ee4b3b252b373c1f75fa76ab87baca659237adc36730. Supersedes rejected 163/001 for retrieval; canonical/training false.

Qwen3 MoE component-migration r001 accepted; no separate reviewer-origin duplicate. Warning-name observation from rejected 001 must be filed as reviewer-confirmed and excluded from teacher input. Assisted selection and missing warning finding remain canonical-use conditions. Older ledger revisions still owed.

Warning-name follow-up filed: reports/defect-ledger/exllamav3-extra-tensor-warning-name--r001.json, sha256 294d9a17916d166b93064e1babb7130d297f25b40500716bf6d2bd746fb10dda. Authoring origin preserves first observation in rejected 001; reviewer source confirmation explicit, suspected runtime status, administrative only. Include record and four evidence hashes with 164 request. Schema and evidence validation passed.

2026-11-15 — 164 architecture stop inspected before any teacher. Google full enumeration and recovery recorded in commit-000164-reference-discovery-003.json; all 152 gated root configs inspected through pre-cutoff hash-verified ModelScope copies (149 JSON, three non-JSON). Eleven matches. No policy or implementation change. Manual detached continuation must validate recovery before authoring and await review afterward.

2026-11-15 — Guidance-6 trial user decision read and recorded: 9ba58a40c5cbcd533171324a09a0010b729e1f9c9287ec83bd222a3f12011848. Implementation follows filing 164; trials follow implementation acceptance. Walk stays guidance 5; no trial teacher receives reviewer criteria.

## 2026-11-15 — 164 validation recovery and guidance-6 gate

164/001 finished before its supervisor replay failed on Invalid max_bytes. Original failure artifacts retained; manual exact FreshSession error conversion produced 35 identical results, with unchanged authored files and all recorded implementation/blob fingerprints verified before source edits. Filed commit-000164-001 for ancestor retrieval only with warning-name r001. No 165 started.

Guidance-6 trial gate filed in guidance-6-implementation-001 after the 164 request; v5 full opening byte-identical and 280 host-enabled tests pass. Trial sessions await acceptance, stay unpublished/outside journal and ancestor context. Permanent replay error handling separately filed in tool-replay-errors-implementation-001; await acceptance before next cycle. No new teacher session started during recovery/implementation.

## Recorded commit-000164-001

Ancestor retrieval only. reviews/verdicts/commit-000164-001.md sha256 778536404f0fc74518d9dd742cb2244cedd9fd03a606815e57703f1f9eaf8ede; manual architecture approval.


1. Ledger, `exllamav3-logits-padding-width-mismatch`: file a revision adding `966762a3` as an affected revision
   with the concrete case (vocabulary 262,208, head width 262,272, buffer width 262,208, eleven reference
   configurations). Reviewer observation, source only.
2. Implementation: the replay fix in `cycle.validate_run`, as its own request.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval by hand (architecture commits are manual).
2. Then, in either order between commits: the guidance-6 implementation request, and 165.

Canonical-use limitation: teacher read no tensor headers; reviewer comparison is not teacher evidence. Warning-name r001 and validation recovery accepted.

## 2026-11-15 — guidance trial gate and replay acceptance

- reviews/verdicts/guidance-6-implementation-001.md: ACCEPTED; SHA256 `2f8e32719257c11ebc231a21a8b42c9dd26cc44a77b09be913085a7170d4033b`; all 9 request hashes verified.
- reviews/verdicts/tool-replay-errors-implementation-001.md: ACCEPTED; SHA256 `0c5e20346ab827b1065eb650d24cff5422a9f515b325fd71d11675509b416367`; all 8 request hashes verified.
- Guidance 6 is trial-only. Four sessions between commits after 165, isolated under .teacher/trials; only manifest guidance_version changes, 163 uses 001 packet and compares approved 002 output metrics. Preserve first results, disclose any mechanical retry, prove walk files and journal entries unchanged, report all requested metrics. Walk remains guidance 5.
- Existing detached 165 supervisor PID 2637814 and cycle child 2637825 confirmed running; no duplicate launch. Trial baseline must follow 165 completion.

## 2026-11-16T03:11:35.448443+00:00 — 165 verdict verified

- Verdict reviews/verdicts/commit-000165-001.md SHA256 `fb1682601a0168d7496b8388b92815b8f55f9b7823e0587fe99a2444fd9ee290`; all 14 request hashes match. Approved ancestor-only; no canonical-use condition. Padding-width r002 accepted. --approve deferred until trial isolation snapshot ends; 166 authorized afterward.
- Two ledger candidates written: reports/defect-ledger/exllamav3-compare-q-no-reference-finalization--r001.json, reports/defect-ledger/exllamav3-compare-q-cache-clear-argument-mismatch--r001.json. Source and scalar checks only, suspected; ledger serialization pending review.

## Recorded commit-000165-001

Ancestor retrieval only. reviews/verdicts/commit-000165-001.md sha256 fb1682601a0168d7496b8388b92815b8f55f9b7823e0587fe99a2444fd9ee290

### Follow-ups

1. Ledger: file both findings, introduced at `3873d40a`. For the first, record that it turns a working path
   (perplexity without a reference, as of 162) into a failing one.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

None for this entry.

## 2026-11-15 — guidance-6 trials filed; 165 approval applied

- Four first-result sessions complete under .teacher/trials/guidance-6-001; no retries. 74 calls replay identical, all manifests differ only guidance_version, snapshot comparisons equal. Trial request reviews/requests/guidance-6-trial-001.md filed. Walk remains guidance 5.
- Applied verified 165 verdict with --approve after snapshots completed. 166 authorized and launching detached; both 165 findings ledger candidates due with its request.

## 2026-11-15 — guidance-6 trial assessed

- Trial verdict assessed: `reviews/verdicts/guidance-6-trial-001.md`, SHA256 `40416d0f227fc5c71e79b0bc2f1d3b721913e03cd1a467a6237ae71c1e044146`; all 55 request hashes verified. Conduct accepted; 163 and main 158 gap found, 154 missed, control clean, 74 vs 52 calls. No trial output approved, no guidance adoption. Proposed wording correction and fourth paragraph require user decisions; do not implement or pass reviewer criteria to teachers. Continue 166 guidance 5, existing detached cycle only.

## 2026-11-15 — 166 filed

- reviews/requests/commit-000166-001.md filed with both 165 ledger candidates. Full text coverage; 22 identical replays; guidance 5. No new finding. Await review before 167; Qwen3 MoE identity fix attribution follows independent review.

## Recorded commit-000166-001

Ancestor retrieval only. reviews/verdicts/commit-000166-001.md sha256 c6e9e4ee684d72d219a0b43986d0802a34dfd86267bae568758d00accfc1fac2

### Follow-ups

1. The ledger revision above.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

None for this entry.

## 166 approval and Qwen3 MoE fix revision

166/001 APPROVED for ancestor retrieval only; verdict SHA256 c6e9e4ee684d72d219a0b43986d0802a34dfd86267bae568758d00accfc1fac2; all 13 request hashes verified, approval applied via --approve. Both 165 ledger r001 records accepted. Qwen3 MoE component-migration r002 filed as pending candidate for the 167 request: fix 08858bc8, affected 163–165, reviewer-confirmed source inspection only. Guidance remains 5; 167 launching detached.

## 167 review request

167/001 request filed at reviews/requests/commit-000167-001.md; unassisted guidance 5, 14 exact replays, 3/3 sections, no ancestor prose reads. Nonpositive code-block index finding pending review. Qwen3 MoE r002 included with evidence hashes. Await verdict; do not start 168.

- 167 approved for ancestor retrieval only; all 18 request hashes verified; verdict SHA256 73b3a4577f3ff6b54090cf52e4d2e90e1c0fe78b5a82838adbb1c8488d7362ab. Qwen3 MoE r002 accepted. Canonical-use condition: inherited empty-block feedback from 137 omitted; do not alter authored run. New nonpositive-codeblock-index r001 and empty-codeblock-feedback r002 (167 affected, reviewer-only addition) pending review with 168. Continue guidance 5; reviewer material excluded from teacher input.

## Recorded commit-000167-001

Ancestor retrieval only. reviews/verdicts/commit-000167-001.md sha256 73b3a4577f3ff6b54090cf52e4d2e90e1c0fe78b5a82838adbb1c8488d7362ab

### Follow-ups

1. Ledger: file `nonpositive-codeblock-index`, introduced at `769ddb34`.
2. Ledger: add `769ddb34` as an affected revision of `exllamav3-empty-codeblock-feedback` (reviewer
   observation, source inspection).
3. The remaining older ledger revisions are still owed.

### Must fix before canonical use

- The entry does not say that the empty-block feedback condition recorded at 137 persists in the code it edits.

## 168 review request

168/001 request filed at reviews/requests/commit-000168-001.md; all 20 hashes verified, 14 exact replays, 1/1 task sections, one ancestor prose read. No findings; scalar accounting only. Nonpositive-codeblock-index r001 and empty-codeblock-feedback r002 included for review. Await verdict; do not start 169.

## Recorded commit-000168-001

Ancestor retrieval only. reviews/verdicts/commit-000168-001.md sha256 0af0691e0515a494150bd61588d07cf4a3e8134a23a5cabcd3d90db7b0ce1b9f

### Follow-ups

1. The remaining older ledger revisions are still owed. Nothing new from this commit.

### Must fix before canonical use

None for this entry.

## 168 approval

168/001 APPROVED for ancestor retrieval only; verdict SHA256 0af0691e0515a494150bd61588d07cf4a3e8134a23a5cabcd3d90db7b0ce1b9f, all 20 request hashes verified, approval applied via --approve. Nonpositive-codeblock-index r001 and empty-codeblock-feedback r002 accepted. No new findings or canonical-use conditions; older obligations remain. Continue 169 detached on guidance 5; reviewer-only notes excluded from teacher input.

## 169 review request

169/001 request filed at reviews/requests/commit-000169-001.md; 12 artifact hashes verified, eight exact replays, incomplete 4/9 text-section coverage explicitly disclosed (five story/passage fixtures unread), zero ancestor reads. Unsupported-cache-default-argument finding pending review; run executes extracted parent add_args AST, not full script or model. No new ledger candidates. Await verdict; do not start 170.

- 169/001 APPROVED for ancestor retrieval only; all 12 request hashes verified; verdict SHA256 64df74c9d14426c5cc8f411da8d6509f2df448a017c39b5675a5a4f35ed37ecd. Canonical-use conditions: describe altered-text tasks and name replacement; five unread story sections must be read or remain explicitly disclosed. Authored run immutable; reviewer notes never teacher input. Unsupported-cache-default-argument r001 prepared for next request, introduced 0488385e, verified by isolated execution of parent helper. Continue 170 detached guidance 5.

## Recorded commit-000169-001

Ancestor retrieval only. reviews/verdicts/commit-000169-001.md sha256 64df74c9d14426c5cc8f411da8d6509f2df448a017c39b5675a5a4f35ed37ecd

### Follow-ups

1. Ledger: file `unsupported-cache-default-argument`, introduced at `0488385e`, with verification by isolated
   execution of the parent helper.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

- Describe the nine tasks as they are, including the three altered-text tasks and the name replacement.
- Five text sections were not read; either read them or keep saying so.

## 170 review request

170/001 request filed at reviews/requests/commit-000170-001.md; all 16 hashes verified, ten identical replays, 1/1 task sections, approved 169 ancestor read. No findings; parent helper and reconstructed changed helper executed in isolation. Unsupported-cache-default-argument r001 included; fix attribution awaits review. Await verdict; do not start 171.

- 170/001 APPROVED for ancestor retrieval only; all 16 request hashes verified; verdict SHA256 fb6c3da34087620c4a4ccaaf39c0435d45208eb0629dcd4e4eb95af8f038cb6b. Unsupported-cache-default-argument r001 accepted; r002 prepared for the next request with fix 2432c64e, reviewer source-confirmed, affected 169 only. No new canonical-use conditions. Continue 171 detached guidance 5; reviewer-only notes excluded from teacher input.

## Recorded commit-000170-001

Ancestor retrieval only. reviews/verdicts/commit-000170-001.md sha256 fb6c3da34087620c4a4ccaaf39c0435d45208eb0629dcd4e4eb95af8f038cb6b

### Follow-ups

1. The ledger revision above.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

None for this entry.

- User adopted guidance via reviews/verdicts/guidance-6-adoption.decision.md, SHA256 fc6620e760801c060f85975a5fa73558a05dd4129e09119108c7392188454d7b. Finish and file the existing 171 cycle under guidance 5 first; do not launch 172. Then implement guidance_version 7 with adopted A and unchanged B/C; preserve v5/v6 byte identity, set prepare default to 7, run full host-enabled suite, file reviews/requests/guidance-7-adoption-001.md with patch and identity/text checks, await acceptance before another commit. No fourth paragraph authorized. Existing approved entries remain unchanged.

2026-11-15: Filed 171/001 on guidance 5 and guidance-7-adoption-001 implementation request under user adoption decision. 280 host-enabled tests pass; versions 5/6 reproduce unchanged. Await both verdicts before 172.

## Recorded commit-000171-001

Ancestor retrieval only. reviews/verdicts/commit-000171-001.md sha256 3c6b52f6c60cfed0eb3e48cbdcdbe008a1a64ad0a1954bc4cd925fe1f33444f0

### Follow-ups

1. Ledger: add `475dfcca` as an affected revision of both 165 records.
2. The remaining older ledger revisions are still owed.

### Must fix before canonical use

None for this entry.

2026-11-15: 171 APPROVED ancestor-only, verdict 3c6b52f6c60cfed0eb3e48cbdcdbe008a1a64ad0a1954bc4cd925fe1f33444f0 recorded. Cache-default r002 accepted. Both compare-q 165 records revised as r002 with 475dfcca affected, pending next-request review. Guidance-7 request already filed; 172 remains blocked.

2026-11-15: Guidance-7 adoption ACCEPTED, verdict SHA256 d86c96de3bb9eb9a4e3bfb1aa38315e4ed227038820deaa475e3536ed7ffd59b; all 10 request hashes verified. No journal advancement pause set; administrative stop cleared by acceptance. Continue 172 detached on guidance 7. Requests must name guidance 7, report ancestor reads/tool counts, and quote any teacher statement that instructions cannot be followed with available tools. Both 165 r002 candidates remain due with the next request.

2026-11-15: 172/001 request filed at reviews/requests/commit-000172-001.md; first live guidance-7 walk run, eight exact replays, 1/1 sections, one ancestor chapter (543c4b27), three full parent file reads. Synthetic scalar check only, no run file reads or real GGUF/cache execution. Two suspected findings await review. Both 165 r002 affected-revision candidates and evidence included. No teacher tool/instruction incompatibility reported. Await verdict; do not start 173.

## Recorded commit-000172-001

Ancestor retrieval only. reviews/verdicts/commit-000172-001.md sha256 dc27c9449ff1241042504a9a48e4db966112654f6f5ce769b18dc475d6b53de6

### Follow-ups

1. Ledger: add `07ffea7f` as an affected revision of both 165 records (file unchanged at this commit).
2. Ledger identities for this entry's two findings may be filed as suspected, source-only, with the limits the
   draft states.
3. The remaining older ledger revisions and the discussion-history cache are still owed; neither blocks.

### Must fix before canonical use

1. "The comparison CLI clears only test_ppl entries" overstates what `--clear_cache` does. At this commit it still
   calls `disk_lru_cache_clear("test_ppl", test_data_spec, spec)` while the cached call takes three arguments, so
   the key does not match and nothing is cleared (the recorded 165 finding, carried by 171). The point the
   sentence supports, that the storage cache is not cleared, stands.
2. The cached-accounting finding names only the `lcpp_get_storage_info` cache. A cached `test_ppl` result already
   holds `layer_bpw`, `head_bpw` and `vram_gb` and returns without calling the loader at all, so for a model that
   was measured before this commit that is the first cache that keeps the old numbers.
3. The entry does not carry the two 165 findings in `eval/compare_q.py`, which it read in full. Both are unchanged
   at this commit.

2026-11-15: 172 APPROVED ancestor-only; verdict SHA256 dc27c9449ff1241042504a9a48e4db966112654f6f5ce769b18dc475d6b53de6; request hash and all 23 artifact hashes verified, approval applied via --approve. Both 165 r002 records accepted; r003 candidates add 07ffea7f as affected, include with next request. Canonical-use conditions (reviewer-only): CLI clear uses the wrong two-argument key, cached test_ppl results bypass even the storage helper, and the entry omits the two unchanged 165 defects. Never teacher input. File suspected source-only ledger candidates for embedding-order and cached-accounting with their stated real-GGUF/execution limits; identities/origins to be checked before filing. Older ledger work and discussion-history cache remain owed/nonblocking. Continue 173 detached on guidance 7.

2026-11-15: 173/001 request filed: guidance 7, eight exact replays, 1/1 sections, two complete parent reads, one ancestor entry (165); scalar checks only/no run file reads. Both 165 r003 candidates and 172 embedding-order/cached-accounting r001 candidates filed with evidence hashes. Pending 173 findings and cache-key fix attribution await verdict. No teacher instruction/tool incompatibility reported. Do not start 174.

## Recorded commit-000173-001

Ancestor retrieval only. reviews/verdicts/commit-000173-001.md sha256 66f4d122bfb67b85920701692be8ff8d5c1274a03e06fa9580c0ba92e13e97f6

### Follow-ups

1. Ledger: record `e1d2fa11` as the fix of the cache-clear record, and add it as an affected revision of the
   no-reference record. A ledger identity for the filtered-reference finding may be filed as suspected.
2. The remaining older ledger revisions and the discussion-history cache are still owed; neither blocks.

### Must fix before canonical use

None for this entry.

2026-11-15: 173 APPROVED ancestor-only; verdict SHA256 66f4d122bfb67b85920701692be8ff8d5c1274a03e06fa9580c0ba92e13e97f6, request hash and all 25 artifacts verified. Four submitted ledger candidates accepted. Prepared r004 candidates: e1d2fa11 fixes cache-clear mismatch and is affected by no-reference finalization. Include both plus evidence with 174 request; also file suspected filtered-reference-dependency identity with stated missing-file/execution limits. No canonical-use conditions for 173. Continue 174 detached guidance 7; older ledger work and discussion-history cache remain owed/nonblocking.

## 174 request filed — 2026-11-16

174/001 request filed: guidance 7, 26 identical replays, 1/1 task sections, two ancestor prose reads; model.py and model_diff.py partial reads explicitly disclosed. Integer indexing/shape checks only, no tensor/loader/model execution; three suspected findings await review. All 25 artifact hashes verified. Three 173 ledger follow-ups filed (both 165 r004 revisions and filtered-reference-dependency r001). No teacher instruction/tool incompatibility reported. Await verdict; do not start 175.

## Recorded commit-000174-001

Ancestor retrieval only. reviews/verdicts/commit-000174-001.md sha256 d96de6287381d094d3a22417e9c2099d569e1e158b11046bbfcbeb6e16bec623

### Follow-ups

1. Ledger identities for the three findings may be filed as suspected, source-only, with the limits the draft
   states. Keep the orientation record conditional.
2. The remaining older ledger revisions and the discussion-history cache are still owed; neither blocks.

### Must fix before canonical use

1. The deferred-read finding should say that this is the default path, not a special configuration:
   `SafetensorsCollection` falls back to `mt_fread` when no load method is given, and an unsliced `Linear` permits
   deferral. On default settings the scaling is lost for every file-backed, unsliced ordinary linear.
2. `exllamav3/models/model.py` and `eval/model_diff.py` were read in part only; the request says so. The parts
   the findings rely on were within the bytes read.

## 174 approved — 2026-11-16

174 APPROVED for ancestor retrieval only; verdict SHA256 d96de6287381d094d3a22417e9c2099d569e1e158b11046bbfcbeb6e16bec623; request and all 25 artifacts verified, approval applied via --approve. All three ledger candidates accepted. Canonical-use notes: deferred scaling loss occurs on the default unsliced file-backed path; model.py and model_diff.py partial reads remain disclosed (relevant code was read). Reviewer-only notes never teacher input; authored run immutable. Pending next request: suspected/source-only ledger candidates for FP8 dtype support, deferred scaling and conditional scale orientation; check identity/introduction and retain actual-checkpoint, half-product and execution limits. Older ledger work and discussion-history cache remain owed/nonblocking. Continue 175 detached guidance 7.

- Guidance-8 trial authorized by reviews/verdicts/guidance-8-trial.decision.md (SHA256 941c51728fcf206d1757fbb943fdeaf852919139f9d2718caeaac37e2bef97b5). Patch staged, NOT APPLIED, at reports/guidance-8-implementation-001.patch; version-7 pre-edit snapshot saved in reports/guidance-8-v7-before.json. Apply only after live 175 finishes its implementation-hash validation; do not invalidate the active run. Then verify exact decision paragraph and unchanged v7 opening/tools/effort, full host-enabled suite, file guidance-8-implementation-001 request. Walk default remains 7, no advancement pause. After acceptance run four fresh unassisted unpublished trials at 154,140,157,156 under .teacher/trials/ between commits; same cutoff evidence, no reviewer material or journal attempts/ancestor approval. File guidance-8-trial-001 with drafts/transcripts/coverage/tool and token counts. Adoption requires another user decision.

- Guidance-8 trial gate implemented after 175 completed; request reviews/requests/guidance-8-implementation-001.md filed. All 280 host-enabled tests pass (24.418s); v7 complete opening/tools/effort byte-identical to pre-edit snapshot, v5/v6 snapshots unchanged, v8 paragraph exact decision and bundle validates. Walk default stays 7, no advancement pause; no trials until implementation verdict. Four trials and reporting remain owed as specified; no adoption. 175 review pending; 176 requires its approval.

## Recorded commit-000175-001

Ancestor retrieval only. reviews/verdicts/commit-000175-001.md sha256 c31aaca9731fa38a69b26e620481d9f99291c33e4b691546a3b9e3f9eeabbd0a

### Follow-ups

1. Ledger: record `c0a2028f` as the fix of the no-reference record; add it as an affected revision of the
   filtered-reference record. The three 174 identities are still owed.
2. The guidance-8 implementation request is expected next or soon; the walk stays on 7.

### Must fix before canonical use

1. The entry says `--kld` only selects the plotted metric. It should add what that now means on the repaired
   path: with `--kld` and no reference spec, results have no `kld` key and `plot` reads `r["kld"]`.
2. `eval/spec/wiki2_llama3_large.json` keeps the old tokenizer directory; the entry does not say the edit is to
   one of two Llama 3 data specs.

## 175 approved — 2026-11-16

175 APPROVED ancestor-only; verdict SHA256 c31aaca9731fa38a69b26e620481d9f99291c33e4b691546a3b9e3f9eeabbd0a; request and all 12 artifacts verified, --approve applied. Two implementation-hash differences explicitly accepted as guidance-8 edits after run validation. Prepared no-reference-finalization r005 with fix c0a2028f and filtered-reference-dependency r002 adding it as affected; include both and commit175 evidence with next request. Three 174 identities remain owed. Canonical-use notes (reviewer-only, never teacher input): --kld with no reference now reaches a missing kld key in plot; only one of the two Llama3 data specs changes tokenizer path. Guidance-8 request already filed, trials await acceptance; walk remains 7. Continue 176 detached.

- Guidance-8 implementation ACCEPTED as a trial gate; verdict SHA256 f07371b2fbe5abd2c0d89cb69939394659731f102e4647e72a00adfbc9d952c3; request and all 10 artifact hashes verified. Walk stays guidance 7. Prepare four fresh unpublished unassisted trials at 154,140,157,156 with unchanged cutoff evidence; launch only after running 176 finishes and its request is filed. No reviewer material, journal attempts or ancestor approval. Record token events administratively without changing teacher input. No adoption.

- 176/001 request filed: guidance 7; 48 identical replays, 38/38 sections, one ancestor chapter. Parent convert_model.py partial read disclosed; separate run-based source scan and scalar enumeration, no GPU/model execution. Both 175 ledger follow-ups included; 174 identities still owed. Await verdict, no 177. Guidance-8 trials launch between commits; defer journal/run approval writes until trial isolation snapshots complete.

- 176 APPROVED ancestor-only; verdict SHA256 1dcb904e968250bc53754fc7a2e42769c2caeaaea3d4030f6b3605b4b0c07ca9; request and all 27 artifact hashes verified. Both 175 ledger candidates accepted. Approval application via --approve and 177 launch await completion of the active guidance-8 trial isolation snapshot (currently first trial); do not modify walk runs/journal during it. Reviewer-only two-multiplier-resume-inconsistency r001 prepared for next request, source-only/suspected; inherited cost-buffer record still needs 176 affected revision. Three 174 identities remain owed. Canonical notes: divergent resume dispatch and MUL1 test scale 1.0 versus library 1.24371088; never teacher input. After trials, file trial request, apply 176 approval, continue 177 detached guidance 7.

## Recorded commit-000176-001

Ancestor retrieval only. reviews/verdicts/commit-000176-001.md sha256 1dcb904e968250bc53754fc7a2e42769c2caeaaea3d4030f6b3605b4b0c07ca9

### Follow-ups

1. Ledger: a new identity for the reviewer finding above (suspected, source-only, reviewer-originated). The
   inherited cost-buffer record gains `d359bcc0` as an affected revision. The three 174 identities are still owed.
2. The guidance-8 trial request is expected; the walk stays on 7.

### Must fix before canonical use

1. Add the two-multiplier inconsistency above, or at least stop short of implying the rejection in `prepare`
   covers every route to the quantizer.
2. Say that MUL1's tests use scale 1.0 while the library constant stays 1.24371088 for all modes; the entry
   reports the constant but not the contrast with the tests it describes.


## 2026-11-15 — guidance-8 trial filed; 176 approved

Filed reviews/requests/guidance-8-trial-001.md (SHA256 dacce61139830920100b67023c0e7715107eaddb9c2e6ec656496f4a332fcbdc). All four sessions completed once; 74/74 tool calls replay identically; walk snapshots unchanged. Trial assessment pending; no adoption or ancestor approval. Applied commit-000176-001 approval, verdict SHA256 1dcb904e968250bc53754fc7a2e42769c2caeaaea3d4030f6b3605b4b0c07ca9; ancestor retrieval only. Launching 177 detached on guidance 7. Include prepared two-multiplier-resume-inconsistency r001 and evidence with 177 request. Cost-buffer affected revision and three 174 identities remain owed. Reviewer material stays out of teacher inputs.


## 2026-11-15 — guidance-8 assessment recorded

reviews/verdicts/guidance-8-trial-001.md SHA256 `76f239ad8ce2b9b24ff66e2e8848d65a26b14692ba48d7abadad091ed298473f`: trial passes, assessment only, NOT adoption; no trial output approved for ancestor retrieval, canonical use or training. Request and all 59 listed artifact hashes verified. Walk remains guidance 7 pending a user decision file. Existing detached 177 continues; do not duplicate it. Reviewer trial observations remain administrative and excluded from teacher input.


## 2026-11-15 — guidance-8 adoption authorized, pending implementation

User decision `reviews/verdicts/guidance-8-adoption.decision.md` SHA256 `4c86a92b200686f892eb3b840e460520e3f82085c51417b4034a7f141bc6e494` adopts the trialled version-8 text unchanged. Existing detached 177 must finish and be filed under guidance 7. Then change prepare default to 8, run the full host-enabled suite, verify fresh packet instructions equal guidance 7 plus exact paragraph D and historical 5/6/7 reproduction, and file reviews/requests/guidance-8-adoption-001.md with patch and evidence. Do not start 178 or any further walk commit until adoption implementation is accepted, even if 177 is approved. Existing packets/runs remain untouched. After a few guidance-8 commits, report cost and effect against 172–176.


## 2026-11-15 — 177 and guidance-8 adoption filed

177/001 finished unassisted under guidance 7; request filed, 19/19 replays identical and 2710 read-only blobs verified. Includes reviewer-originated two-multiplier-resume-inconsistency r001. Awaiting verdict. Guidance-8 adoption request filed at reviews/requests/guidance-8-adoption-001.md: prepare default 8, unchanged trial text and historical inputs, 280 host-enabled tests pass. Explicit advancement_pause set; no 178 until adoption acceptance and 177 approval. Cost-buffer affected revision and three 174 identities remain owed. Cost/effect comparison with 172–176 owed after a few version-8 commits.

## Recorded commit-000177-001

Ancestor retrieval only. reviews/verdicts/commit-000177-001.md sha256 b470443ac1d1c0ed4ee58ce17b68f1f2ac978df3c0ebb5c8e64cc7ad1bf239c8

### Follow-ups

1. Ledger: the sorted-argmax record gains `8b0df691` as an affected revision; the cost-buffer affected revision and
   the three 174 identities are still owed.
2. `guidance-8-adoption-001` is expected next. No 178 before it is accepted.

### Must fix before canonical use

None for this entry.


## 2026-11-15 — 177 approved; adoption pending

Recorded reviews/verdicts/commit-000177-001.md, SHA256 `b470443ac1d1c0ed4ee58ce17b68f1f2ac978df3c0ebb5c8e64cc7ad1bf239c8`, after verifying request and all 12 artifact hashes. Ancestor retrieval only; canonical/training false. Two-multiplier-resume-inconsistency r001 accepted, source-only suspected reviewer observation. Sorted-argmax identity gains 8b0df691 as affected (owed); cost-buffer affected revision and three 174 identities remain owed. guidance-8-adoption-001 is already filed. Next position 178, explicit adoption advancement pause retained; no teacher launch before acceptance.


## 2026-11-15 — guidance-8 adoption accepted

Recorded reviews/verdicts/guidance-8-adoption-001.md, SHA256 `24fee78ffec696fec253ca06f6aff2a2e59ebd1b7e1a585f3f893d7377fbc183`; request and all 10 artifact hashes verified. Cleared adoption pause; launching 178 detached on guidance 8. Requests must name guidance 8, report tool counts and ancestor reads. Cost/effect comparison against 172–177 owed after a few commits. Trial outputs remain unapproved and excluded from ancestor context. Existing ledger obligations remain open.


## 2026-11-15 — 178 filed, guidance 8

Filed reviews/requests/commit-000178-001.md, awaiting verdict; no 179. Nine calls replay identically, 2720 read-only blobs verified, task 1/1 fully read. Two ancestor reads are chunks of one root generation chapter. Both repo_read windows truncated; scalar run reads no files. Inherited optional-output finding, no new ledger candidate. Sorted-argmax/cost-buffer identity records were not located by filename/content search; reconcile register history before creating revisions. Their affected follow-ups and three 174 identities remain open. Cost/effect comparison against 172–177 remains owed after a few guidance-8 commits.

## Recorded commit-000178-001

Ancestor retrieval only. reviews/verdicts/commit-000178-001.md sha256 bd6e8432eb1bce48ff6f0f0f4c570b51b6af2ba15c62717366ad60d3ff529b1b

### Must fix before canonical use

None for this entry.


## 2026-11-15 — 178 approved; root ledger identities prepared

178 approved for ancestor retrieval only, verdict SHA256 `bd6e8432eb1bce48ff6f0f0f4c570b51b6af2ba15c62717366ad60d3ff529b1b`; request and all artifacts verified. Reviewer correction resolves identity search: no prior sorted-argmax or cost-buffer records. Created exllamav3-first-pass-cost-buffer--r001 and exllamav3-sorted-argmax--r001, suspected/source-only authoring observations introduced at root 543c4b27, affected root plus 176/177 respectively. Include both and their four evidence copies with 179 request for ledger review. Optional-output root identity remains older-batch work; three 174 identities remain owed. Launching 179 detached on guidance 8. Canonical/training remain false; ledger never teacher input.


## 2026-11-15 — 179 filed

Filed reviews/requests/commit-000179-001.md on guidance 8, awaiting verdict; no 180. All 17 calls replay identically, 2725 read-only blobs verified, task 1/1 read; one ancestor prose read. Disclosed partial conversion/native reads and scalar-only numerical comparison. New root first-pass-cost-buffer r001 and sorted-argmax r001 filed with evidence for ledger acceptance. Optional-output and three 174 identities remain owed. Cost/effect comparison against 172–177 pending after a few guidance-8 commits.

## Recorded commit-000179-001

Ancestor retrieval only. reviews/verdicts/commit-000179-001.md sha256 db468d8a43e8bdf64d0bd8e5e556c67ab79634d210a5045a5e831653f541b466

### Follow-ups

1. Ledger: the optional-output identity and the three 174 identities are still owed.

### Must fix before canonical use

None for this entry.

- 179/001 APPROVED for ancestor retrieval only; verdict SHA256 db468d8a43e8bdf64d0bd8e5e556c67ab79634d210a5045a5e831653f541b466, request hash and all 16 artifact hashes verified; approval applied via --approve. First-pass-cost-buffer r001 and sorted-argmax r001 accepted (root-introduced, suspected/source-only). No canonical-use conditions for this entry. Optional-output identity and three 174 identities remain owed; reviewer material excluded from teacher input. Continue 180 detached on guidance 8.

- 180/001 request filed at reviews/requests/commit-000180-001.md: unassisted guidance 8, all ten artifact and 44 implementation hashes verified, 15 identical replays, 7/7 task sections, one complete parent file and one approved ancestor entry read. Standard-library helper transcription only, no run file reads or profiler/package/GPU execution. Two path-only closed rows selected/read, no truncation. No new findings or ledger candidates; optional-output and three 174 identities still owed. Await verdict; do not start 181.

## Recorded commit-000180-001

Ancestor retrieval only. reviews/verdicts/commit-000180-001.md sha256 7c1c198cf99154f5b58fd84740606a6492ec384bc3325a367ba475b30d599e58

### Follow-ups

1. Ledger: the optional-output identity and the three 174 identities are still owed.

### Must fix before canonical use

None for this entry.

- 180/001 APPROVED for ancestor retrieval only; verdict SHA256 7c1c198cf99154f5b58fd84740606a6492ec384bc3325a367ba475b30d599e58, request hash and all ten artifact hashes verified, approval applied via --approve. Clean, no canonical-use conditions or new ledger work. Optional-output identity and three 174 identities remain owed. Continue 181 detached on guidance 8; reviewer material excluded from teacher input.

- 181/001 request filed at reviews/requests/commit-000181-001.md: unassisted guidance 8, ten artifact and 44 implementation hashes verified; nine identical replays; 1/1 task sections, two full parent files and one root conversion chapter read. Three run calls read/extract the parent allocator and apply the two task substitutions with synthetic objects; no full conversion or GPU check. Remaining-unequal-KV and inherited exact-budget findings await review. No ledger candidates submitted; older optional-output and three 174 identities remain owed. Await verdict; no 182.

## Recorded commit-000181-001

Ancestor retrieval only. reviews/verdicts/commit-000181-001.md sha256 98c480bffa9f7e836504642c4ed733d4dc9f5099d137db3eeb3c0852351c7560

### Follow-ups

1. Ledger: an identity for the remaining-unequal finding (suspected; executed on the extracted function with
   synthetic sizes). For the inherited boundary, file it with the qualification above or hold it; do not file it
   as "exact match excluded" without the plus-one.
2. The optional-output identity and the three 174 identities are still owed.

### Must fix before canonical use

1. The inherited finding's "expected" side should say that `budget` is `int(bpw * numel) + surplus_bits + 1`:
   it is already one bit more than the target plus the bits carried in. In the entry's example the bits actually
   available are 1,791, and the "exact" candidate costs 1,792, so excluding it keeps the allocation within the
   real total. What the extra bit does do is come back out in the returned surplus: called five times in a row
   with nothing spent beyond the base, the function returns surplus 1, 2, 3, 4, 5 (my run). The defect, if it is
   one, is that drift, not a missed exact fit. The root entry's wording has the same gap.

- 181/001 APPROVED for ancestor retrieval only; verdict SHA256 98c480bffa9f7e836504642c4ed733d4dc9f5099d137db3eeb3c0852351c7560, request hash and all ten artifact hashes verified, approval applied via --approve. Canonical-use condition (reviewer-only): allocator budget already equals target plus carried bits plus one; the 1792-cost candidate exceeds the actual 1791 available bits, so its exclusion is not a missed exact fit. Potential defect is returned-surplus drift (reviewer observed 1,2,3,4,5 across repeated base-only calls), not the claimed exact-match exclusion; root wording has the same gap. Hold inherited-boundary ledger filing pending qualified treatment; never feed this correction to a teacher or edit the immutable draft. File a suspected remaining-unequal-KV identity with extracted-function/synthetic-size execution limits and establish its introduction. Older optional-output and three 174 identities remain owed. Continue 182 detached on guidance 8.

- 182/001 request filed at reviews/requests/commit-000182-001.md: guidance 8, ten artifact and 44 implementation hashes verified; 16 identical replays, 5/5 task sections. Four complete parent files plus partial kernel map (4900–7267), one complete approved ancestor entry. Scalar arithmetic only/no run file reads, CUDA, equivalence or speed check. One path-only closed row selected/read, no truncation. No new findings/candidates; inherited fused-buffer condition retained. Older ledger work remains owed, inherited budget-boundary filing held for plus-one qualification. Await verdict; no 183.

## Recorded commit-000182-001

Ancestor retrieval only. reviews/verdicts/commit-000182-001.md sha256 4e1f01e7f50c0ea0469358357fa68c5fd091295f753eb67b5eb8131f6513b0d1

### Follow-ups

1. Ledger: still owed are the optional-output identity, the three 174 identities and 181's remaining-unequal
   identity; the budget-boundary record stays held.

### Must fix before canonical use

1. Say that the fused path skips `Linear.forward`'s capture hook for K and V. The entry leaves "instrumentation
   paths" unestablished in general; the specific one is visible in the source. (Q still runs it, and the three
   share one capture key.)
2. Say that without indices nothing in the wrapper ties the number of output slots to the length of the pointer
   lists; the removed check was the only thing that implied it. Attention passes two and two.
3. The 32-token cutoff equals the row count at which `LinearEXL3.forward` already switches to reconstruction; the
   entry calls the number unexplained.

- 182/001 APPROVED for ancestor retrieval only; verdict SHA256 4e1f01e7f50c0ea0469358357fa68c5fd091295f753eb67b5eb8131f6513b0d1, request hash and all ten artifact hashes verified, approval applied via --approve. Three reviewer-only canonical-use conditions: fused K/V skips Linear.forward capture hooks (Q still runs its hook; all three share one key); without indices the wrapper does not tie output-slot count to pointer-list length (attention supplies two and two); the 32-token cutoff matches LinearEXL3.forward's existing reconstruction crossover. Preserve immutable draft; none of this enters teacher input. No ledger change. Optional-output, three 174 identities and 181 remaining-unequal identity remain owed; budget-boundary record stays held. Continue 183 detached guidance 8.

- 183/001 request filed at reviews/requests/commit-000183-001.md: guidance 8, ten artifact and 44 implementation hashes verified, 16 identical replays, 1/1 sections, two complete parent files and two ancestor prose reads. Scalar pairing algebra only/no run file reads or Torch/CUDA/test execution. Three source-only suspected findings await review (optional K, discarded test outputs, inherited partial width). One closed path-only row selected/read, no truncation. No ledger candidates submitted; older obligations remain open and budget-boundary held. Await verdict; no 184.

## Recorded commit-000183-001

Ancestor retrieval only. reviews/verdicts/commit-000183-001.md sha256 d44c8f640346a4b7cf21f324c122d7898ea8d477ddefc9e851ca777dc988cf95

### Follow-ups

1. Ledger: identities for the three findings may be filed as suspected, source-only (optional-K introduced at
   `6693b501`; the other two with their recorded introductions). Still owed: optional-output, the three 174
   identities, 181's remaining-unequal identity.

### Must fix before canonical use

None for this entry.

- 183/001 APPROVED for ancestor retrieval only; verdict SHA256 d44c8f640346a4b7cf21f324c122d7898ea8d477ddefc9e851ca777dc988cf95, request hash and all ten artifact hashes verified, approval applied via --approve. All three findings confirmed; no canonical-use conditions. Ledger follow-up: optional-K introduced at 6693b501, discarded reference-test results and partial-reference-width inherited with their introductions to be established/reconciled against existing identities; all suspected/source-only, no Torch/CUDA execution. Older optional-output, three 174 identities and 181 remaining-unequal identity remain owed; budget-boundary record still held. Continue 184 detached guidance 8; reviewer material excluded from teacher input.

## 2026-11-15 — 184 request filed

- 184/001 request filed: reviews/requests/commit-000184-001.md; guidance 8, 23 identical replays, 5/5 task sections, one ancestor prose read. Four partial parent reads and scalar-only execution disclosed; no run file reads or GPU execution. Three suspected findings await review (all-expert cardinality, dtype override, persistent output alias). All 10 artifact hashes and 44 unchanged implementation hashes verified; no new ledger candidates, older obligations retained. Await verdict; do not start 185.

## Recorded commit-000184-001

Ancestor retrieval only. reviews/verdicts/commit-000184-001.md sha256 fd986397334c8880263bb04d601c980ebebf69292816c5cf9101fac3039d9501

### Follow-ups

1. Ledger: identities for the output-dtype and aliasing findings may be filed as suspected behaviour changes,
   source-only; the all-experts record gains `8357593c` as affected. Earlier owed items stand.

### Must fix before canonical use

1. The entry leaves "optional bias" as unestablished in general. The source is specific: the previous route went
   through `LinearFP16.forward`, which adds the bias when there is one and uses `hgemm` when the input dtype
   differs from the output dtype; the native route does neither. The routing gate is built with `qmap = None`,
   `out_dtype = torch.half` and `pad_to = 1`, so it is never quantised and is always a `LinearFP16`.
2. `gate_tensor` is captured once in `load`; a later replacement of the gate's weight would not be seen. Nothing
   in the tree replaces it (the conversion swaps touch only linears that are being quantised).

## 2026-11-15 — 184 approval

- 184 APPROVED for ancestor retrieval only; verdict SHA256 fd986397334c8880263bb04d601c980ebebf69292816c5cf9101fac3039d9501, request and all 10 artifact hashes verified; approval applied via --approve. All three findings confirmed. Canonical-use conditions (reviewer-only): routing gate is always LinearFP16 (qmap=None, half output, pad_to=1); prior forward adds bias and uses hgemm on input/output dtype mismatch, while native routing does neither. gate_tensor captures the weight at load and would miss later replacement, but no such replacement exists in this tree. Never teacher input; authored run immutable. Ledger follow-ups: file output-dtype and persistent-output-alias identities as suspected source-only behaviour changes, add 8357593c as affected to the all-experts identity; earlier owed work stands. Continue 185 detached on guidance 8.

## 2026-11-15 — 185 request filed

- 185/001 request filed: reviews/requests/commit-000185-001.md; guidance 8, 45 identical replays, 7/7 task sections, four ancestor prose reads. Eight full parent reads, five partial reads and one missing-file error disclosed; scalar-only execution, no run file reads or GPU execution. Six finding groups await review. Two closed path-only rows both selected/read, no truncation. All 10 artifact hashes and 44 unchanged implementation hashes verified. No new ledger candidates; 184 and earlier obligations retained. Await verdict; do not start 186.

## Recorded commit-000185-001

Ancestor retrieval only. reviews/verdicts/commit-000185-001.md sha256 a99fd7a9943efe06d9210668c3423ebc549892f3b9c6c569fa1301be7c517450

### Follow-ups

1. Ledger: identities for the three new findings (suspected, source-only; the warp-sum record must keep "store
   order not established"). Affected-revision additions for the inherited ones. Earlier owed items stand.

### Must fix before canonical use

1. The native wrapper checks only `q_norm` (dimension and length). The kernel normalises K heads with `k_norm`
   whenever `q_norm` is given, so `q_norm` without `k_norm` dereferences a null pointer, and `k_norm`'s length and
   dtype-by-presence are not tied to the head width. The comment says they must be supplied together; nothing
   enforces it. Attention always passes both.
2. `Attention.__init__` asserts equal epsilon for the two norms but not equal bias; with the overwrite finding
   this is moot today, and should be said once that is fixed.

## 2026-11-15 — 185 approval

- 185 APPROVED for ancestor retrieval only; verdict SHA256 a99fd7a9943efe06d9210668c3423ebc549892f3b9c6c569fa1301be7c517450; request and all 10 artifact hashes verified, approval applied via --approve. All six finding groups confirmed. Canonical-use conditions (reviewer-only, never teacher input): native wrapper checks only q_norm dimensions/length, does not enforce paired k_norm; q_norm alone reaches null K norm, and K norm length/dtype-by-presence is not tied to head width (Attention always passes both). Constructor asserts equal norm epsilon but not bias; currently moot under overwritten settings, revisit after that fix. Ledger owed: three new suspected source-only identities for overwritten settings, warp-sum store race (store order not established), and padded reads; reconcile inherited frequency identity and add affected revisions for inherited reference/MLP findings. All earlier owed items stand. Continue 186 detached on guidance 8.

## 2026-11-15 — 186 request filed

- 186/001 request filed: reviews/requests/commit-000186-001.md; guidance 8, 19 identical replays, 4/4 task sections, one ancestor prose read. Six full and two partial parent reads disclosed; scalar-only execution, no run file reads or CUDA execution. Three suspected findings await review; existing zero-cap/Boolean identities to reconcile. All 10 artifact hashes and 44 unchanged implementation hashes verified. Assessment sampled=true but no sampled mechanical handover. No new ledger candidates; earlier obligations retained. Await verdict; do not start 187.

## Recorded commit-000186-001

Ancestor retrieval only. reviews/verdicts/commit-000186-001.md sha256 b6a263268247b3f8708ebacfea2f474ec656d1f4ef9e688327f669ed238bbf49

### Follow-ups

1. Ledger: `exllamav3-gemm-zero-grid-cap` gains `1284d43c` as affected for the multi path, with the wider range
   (fewer than 24 tiles), and a note that the single path is clamped from this commit; whether to record that as
   a partial fix is Astra's call, provided the multi path stays open. `exllamav3-boolean-dimension-threshold`
   gains `1284d43c` as affected. The stale declaration may be filed as a new suspected compatibility identity.
2. Earlier owed items stand.

### Must fix before canonical use

1. Say that the single-GEMM clamp removes the zero-block case on that path, which earlier entries recorded for
   both; the entry reports the clamp but not that it is a repair.
2. The comment "Shape 1 not currently used anywhere" above the kernel tables is now false; the entry does not
   mention it.

## 2026-11-15 — 186 approval

- 186 APPROVED for ancestor retrieval only; verdict SHA256 b6a263268247b3f8708ebacfea2f474ec656d1f4ef9e688327f669ed238bbf49; request and all 10 artifact hashes verified, approval applied via --approve. All three findings confirmed. Canonical-use conditions (reviewer-only, never teacher input): explicitly describe single-GEMM lower clamp as repairing its zero-block case; kernel-table comment that shape 1 is unused is now stale. Ledger guidance retained: exllamav3-gemm-zero-grid-cap gains 1284d43c as affected for multi path with expanded range below 24 tiles; record single-path clamp as partial repair while multi remains open. exllamav3-boolean-dimension-threshold gains 1284d43c as affected. Stale five-argument selector declaration may be filed as a new suspected source-only compatibility identity. Revisions not yet filed; all earlier obligations remain owed. Continue 187 detached on guidance 8.

## 2026-11-15 — 187 request filed

- 187/001 request filed: reviews/requests/commit-000187-001.md; guidance 8, 45 identical replays, 2/2 task sections, three ancestor entries. Eleven full and three partial repo reads disclosed; eleven complete config reads, no headers; scalar-only execution, no run file reads. One inherited conditional finding awaits review. Ten skeleton hashes, eleven config blob hashes and 44 unchanged implementation hashes verified. No new ledger candidates; earlier obligations retained. Await verdict; do not start 188.

## Recorded commit-000187-001

Ancestor retrieval only. reviews/verdicts/commit-000187-001.md sha256 26a888ee649098f68af4e0815a206eaa4d6732df86fda08d3528082f58c3e2fc

### Follow-ups

1. Ledger: the all-experts record gains `ec839e16` as affected only if Astra tracks every revision; otherwise no
   change. Earlier owed items stand.

### Must fix before canonical use

None for this entry.

## 2026-11-15 — 187 approval

- 187 APPROVED for ancestor retrieval only (clean); verdict SHA256 26a888ee649098f68af4e0815a206eaa4d6732df86fda08d3528082f58c3e2fc; request and all 21 artifact hashes verified, approval applied via --approve. Inherited all-experts finding confirmed; no canonical-use conditions. Optional ec839e16 affected-revision addition belongs to the existing all-experts identity if tracking every revision, not a new defect. Earlier owed ledger and administrative work remains open. Reviewer-only comparison with other models stays out of teacher input. Continue 188 detached on guidance 8.

- 2026-11-15: 188/001 filed for ancestor retrieval only: reviews/requests/commit-000188-001.md (SHA256 8e61f0118a5ce2b7efbb702727a511163d6a9b73e732eef6db99acca03cace66). Unassisted guidance 8; both sections, six complete parent-file reads, two ancestor prose reads; 16 identical replays and 2814 read-only blobs verified. Ten artifact and 44 unchanged implementation hashes checked. Scalar element-count check only, no tensor/CUDA/performance execution. No new ledger candidates; earlier obligations remain open. Journal awaiting_full_review at 188; do not start 189 before verdict.

## Recorded commit-000188-001

Ancestor retrieval only. reviews/verdicts/commit-000188-001.md sha256 88033355d6be3994e833259fadf4858e7c77ba9d3252ce8333a03ef57fb56ed5

### Follow-ups

1. Ledger: a new reviewer-originated identity for the attribute cache, suspected, source-only, introduced at
   `c2ec220c`. Do not record the fix until the walk reaches `dc69b167` and its entry is approved.
2. Earlier owed items stand.

### Must fix before canonical use

1. State the attribute-cache observation as a suspected finding for multi-device use, with the limit that the
   per-device nature of the attribute was not established from documentation.
2. With "must supply A_had" commented out, a call that passes `suh` without `A_had` now reaches the kernel with a
   null scratch pointer; the entry lists the removed check but not that consequence.

- 2026-11-15: 188 APPROVED for ancestor retrieval only; verdict SHA256 88033355d6be3994e833259fadf4858e7c77ba9d3252ce8333a03ef57fb56ed5; request and ten artifact hashes verified, approval applied via --approve. Reviewer-only kernel-attribute cache identity filed as pending reports/defect-ledger/exllamav3-kernel-attribute-cache-device--r001.json (suspected, source only; reviewer_observation preserved despite validator limitation). Include with 189 request; never teacher input. No fix recorded: wait until dc69b167 is reached and approved. Canonical-use conditions: state suspected multi-device finding with undocumented per-device semantics limit; explain null scratch pointer when suh is passed without A_had after guard removal. Authored run unchanged. Earlier owed work remains open. Continue 189 detached on guidance 8.

- 2026-11-15: 189/001 request filed for ancestor retrieval only (SHA256 ea5e5eafd3448dd5a9dc854e00b91d5208b08d62b7a4eca58dd774191eb6f189). Unassisted guidance 8; one complete section, three complete parent files plus one beyond-EOF read, two ancestor prose reads. Ten identical replays, 2821 read-only blobs, ten artifact hashes and 44 unchanged implementation hashes verified. No execution. Includes reviewer-only kernel-attribute-cache-device r001 and verdict evidence for review; no later fix recorded. Earlier obligations remain open. Await verdict before 190.

## Recorded commit-000189-001

Ancestor retrieval only. reviews/verdicts/commit-000189-001.md sha256 3322de37ed23fe9ca5f543419fc0ecf50a0da7be2039dcb4ac99a78e30a2fd94

### Follow-ups

1. Earlier owed ledger items stand.

### Must fix before canonical use

None for this entry.

- 2026-11-15: 189 APPROVED for ancestor retrieval only (clean); verdict SHA256 3322de37ed23fe9ca5f543419fc0ecf50a0da7be2039dcb4ac99a78e30a2fd94; request and all twelve artifact hashes verified, approval applied via --approve. No findings or canonical-use conditions. Kernel-attribute-cache-device r001 accepted as filed: reviewer_observation, suspected, source only, fixes empty; never teacher input. Earlier owed ledger and administrative items remain open. Continue 190 detached on guidance 8.

- 2026-11-15: 190/001 filed for ancestor retrieval only: reviews/requests/commit-000190-001.md (SHA256 c24ccc7f46dce723f22a7220537c23230162db56bbf7c9ce7547a58a1dc79408). Unassisted guidance 8; two complete sections, five complete parent files, one ancestor chapter. Eleven identical replays, 2828 read-only blobs, ten artifact and 44 unchanged implementation hashes verified. Scalar offsets over 255 shapes only; no tensor/CUDA execution. Two inherited suspected findings pending review (dtype dispatch and test argument mismatch); no new ledger candidates. Earlier obligations remain open. Await verdict before 191.

## Recorded commit-000190-001

Ancestor retrieval only. reviews/verdicts/commit-000190-001.md sha256 c6cba5f99c5d4c7b76446388bd1237b91a1ce0492f75bae1727fb773c03972d4

### Follow-ups

1. Ledger: both inherited findings gain `c94905bf` as affected if identities exist; otherwise file them as new
   identities at their recorded introductions. Earlier owed items stand.

### Must fix before canonical use

1. The removed `x.view(-1, x.size(-1))` did one more thing than bookkeeping: `view` raises when the tensor's
   strides do not allow flattening, so a non-contiguous input was refused. The native code reads `x.data_ptr()`
   as dense rows and has no contiguity check, so such an input is now read wrongly without an error. The entry
   lists strided layouts only as "not established". Every call site in the tree passes a freshly produced or
   viewed contiguous tensor.

- 2026-11-15: 190 APPROVED for ancestor retrieval only; verdict SHA256 c6cba5f99c5d4c7b76446388bd1237b91a1ce0492f75bae1727fb773c03972d4; request and ten artifact hashes verified, approval applied via --approve. Both inherited findings confirmed. Ledger follow-up remains due: reconcile dtype-dispatch and test-argument identities, add c94905bf as affected where identities exist, otherwise file at established introductions. Canonical-use condition (reviewer-only): removing the Python flattening view removes its rejection of strides incompatible with flattening; native dense-pointer reads have no contiguity guard. Reviewer reports tree callers supply freshly produced or viewed contiguous tensors. Preserve the distinction between incompatible strides and all non-contiguous tensors; no execution demonstrated. Authored run unchanged; this observation never teacher input. Earlier owed ledger and administrative work remains open. Continue 191 detached on guidance 8.

- 2026-11-16 UTC: 191/001 request filed at reviews/requests/commit-000191-001.md (SHA256 26ea77bab0b75cdb3f4834acfb30d748fdd38c06d33715f735513146fd9bc013); unassisted guidance 8, ten artifact hashes and 44 unchanged implementation hashes verified, 19 identical replays, 2,835 shared blobs, 1/1 task sections and two ancestor prose reads. Partial generator reads, three separate run file-read scopes and truncated discussion openings disclosed. Two suspected findings (prefill-counted-as-output and empty-filtered-dataset), scalar checks only; no inference/dataset execution. No new ledger candidates; prior obligations remain open. Journal awaiting_full_review; no 192 before verdict.

## Recorded commit-000191-001

Ancestor retrieval only. reviews/verdicts/commit-000191-001.md sha256 55cffd892d2f613aa54db5f43816d04724633cb31f7690584707fd60c502ed49

### Follow-ups

1. Ledger: identities for the two findings may be filed as suspected, introduced at `460e201c`. Earlier owed
   items stand.

### Must fix before canonical use

None for this entry.

- 2026-11-16 UTC: 191/001 APPROVED for ancestor retrieval only (clean); verdict SHA256 55cffd892d2f613aa54db5f43816d04724633cb31f7690584707fd60c502ed49. Request and all ten artifact hashes verified; approval recorded via --approve. Both findings confirmed, no canonical-use conditions. Ledger follow-up: prefill-counted-as-output and empty-filtered-dataset may be filed as suspected identities introduced at 460e201cc332ff93a4d65d7b1ca1f897ad372685; source/scalar evidence only, no dataset or generation execution. Earlier owed items remain open. Reviewer material stays out of teacher input; canonical/training false. Continue 192 detached on guidance 8.

- Guidance-9 trial decision read: reviews/verdicts/guidance-9-trial.decision.md. Trial only; walk default remains 8. Active 192 must finish validation and have its request filed before applying staged reports/guidance-9-implementation-001.patch (implementation files unchanged). Baseline captured in reports/guidance-9-v8-before.json; base hashes in reports/guidance-9-staging-001.json; verification script prepared at reports/guidance-9-verify-001.py. Next: verify base hashes, apply patch, verify exact paragraph and unchanged v8 inputs, run full host-enabled suite, file reviews/requests/guidance-9-implementation-001.md. No advancement pause. After acceptance run five fresh unassisted scratch trials at 184,188,190,189,178 under .teacher/trials/ with same cutoff evidence, no reviewer inputs, no journal attempts, publication or ancestor approval; file guidance-9-trial-001 with drafts/transcripts/coverage/tool and token counts. Reviewer success criteria remain administrative only. Adoption requires a later user decision.

- 192/001 request filed at reviews/requests/commit-000192-001.md; ten artifact and 44 implementation hashes verified before guidance-9 edits, 18 identical replays, 2,843 shared blobs. One task section, one complete ancestor chapter in two reads; partial generator.py read and recovered missing-path lookup disclosed. Two suspected findings, scalar-only checks; no run file reads. No new ledger candidates; older obligations remain open. Await verdict; no 193.

- Guidance-9 trial gate applied only after 192 validation and request filing; reviews/requests/guidance-9-implementation-001.md filed. Exact decision paragraph verified; v8 full opening/tools/effort byte-identical, legacy v5/v6 unchanged, 280 host-enabled tests pass (27.945s). Version 8 remains walk default, no advancement pause. All 191/192 request artifacts remain unchanged. Five trials await implementation acceptance, then run between walk commits under .teacher/trials/ with the recorded isolation requirements. No adoption.

## Recorded commit-000192-001

Ancestor retrieval only. reviews/verdicts/commit-000192-001.md sha256 3a0becbfd09ac70458d04fe843348fcfd3225d5a3343c54bc9b515bfa0c56d47

### Follow-ups

1. Ledger: a new identity for the unbound-return finding (suspected; branch transcription; introduced at
   `33466d78`); a new identity for the reported-probability finding (suspected, source-only). The root
   optional-output identity, when filed, should say its enabled-branch failure ends at this commit. Do not record
   a fix for the unbound return before the walk reaches it.
2. Earlier owed items stand; `guidance-9-implementation-001` is expected.

### Must fix before canonical use

None for this entry.

- 192/001 APPROVED for ancestor retrieval only (clean); verdict SHA256 3a0becbfd09ac70458d04fe843348fcfd3225d5a3343c54bc9b515bfa0c56d47; request and all ten artifact hashes verified, --approve recorded. Both findings confirmed; no canonical-use conditions. Ledger follow-ups owed: new disabled-options-unbound identity introduced 33466d785591bdd69dd43821e22730a55f0067f9 (suspected, branch transcription); new reported-probabilities-not-final identity (suspected, source-only); root optional-output enabled-branch failure ends here when that identity is filed. Do not record any unbound-return fix before the walk reaches it. Reviewer hindsight excluded from teacher input. Older obligations stand. Guidance-9 implementation request is already filed, trials await its acceptance; walk remains guidance 8, continue 193 detached.

- Guidance-9 trial gate ACCEPTED; verdict SHA256 7c57c8c7bd79414079cd371945b13f8d43e632c728b07fa9aa6269f421c81a0c; request hash and all ten artifact hashes verified. Prepared reports/guidance-9-trial-supervisor-001.py (syntax checked; five source manifests are version 8 and unassisted). Do not launch while 193 runs: after it completes, inspect and file 193, then launch trials detached between commits. Supervisor snapshots walk artifacts and journal runs/approved_entries, creates fresh packets differing only in guidance_version=9, records tool/token metrics, stops on failure without retry, and queues completion. Targets 184,188,190 and controls 189,178; unpublished/unapproved, never ancestor context or journal attempts. No reviewer inputs. File guidance-9-trial-001 after completion. Walk stays on 8; no adoption or advancement pause.

- 193/001 filed at reviews/requests/commit-000193-001.md: 13 identical replays, 2,850 shared blobs, ten run/evidence hashes and 44 implementation hashes verified; two implementation changes are accepted guidance-9 gate. Guidance 8 unchanged. Partial job.py/generator.py coverage and scalar branch checks disclosed. Fix attribution and inherited probability finding await verdict; no new ledger candidates, older work remains. Launching accepted guidance-9 trials at 184,188,190,189,178 via reports/guidance-9-trial-supervisor-001.py between commits. Preserve journal runs/approved_entries and all walk packets/runs until its isolation snapshot completes; if 193 verdict arrives meanwhile, verify and track it but defer approval application/194 launch until trial completion. No adoption.

- 193/001 verdict verified: APPROVED for ancestor retrieval only (clean), SHA256 e9ea38e8ed61c813c381c119efd02e28759eb5db71261fbe78395b2974a4dbc3; request hash and all 14 listed artifacts match. No canonical-use conditions. Reviewer confirms cf220845799b12c9475232e2cb309db360f083d3 fixes the 192 disabled-options-unbound identity; record that fix and add 193 as affected to reported-probabilities-not-final when filing those owed records. Earlier ledger obligations stand. Guidance-9 trial supervisor remains running (184 in progress at check). Defer --approve and 194 launch only until its after-snapshot completes, preserving the required walk runs/approved_entries comparison. On queued trial completion: inspect/report trials, apply this verified approval with --approve, then continue 194 detached on guidance 8. No adoption, no advancement pause, no reviewer input to teachers.

## Recorded commit-000193-001

Ancestor retrieval only. reviews/verdicts/commit-000193-001.md sha256 e9ea38e8ed61c813c381c119efd02e28759eb5db71261fbe78395b2974a4dbc3

### Follow-ups

1. Ledger: record `cf220845` as the fix of the 192 unbound-return identity; add it as an affected revision of
   the reported-probability identity. Earlier owed items stand.
2. `guidance-9-trial-001` is expected.

### Must fix before canonical use

None for this entry.

2026-11-16: 193/001 approved ancestor retrieval only, verdict SHA256 e9ea38e8ed61c813c381c119efd02e28759eb5db71261fbe78395b2974a4dbc3; all 14 request hashes verified. Approval applied after guidance-9 snapshots. Trials filed, assessment pending; guidance 8 remains default. cf220845 fix/affected ledger follow-ups retained in tracking.

2026-11-16: Guidance-9 trial assessment recorded: mixed/partial pass, not adoption or approval of trial outputs. Verdict reviews/verdicts/guidance-9-trial-001.md SHA256 c5e27b57c37bc03c23f4f80e33549a57cde55985bf670e1cee0e9632dfa4f0f5; request and all 72 artifact hashes verified. Walk stays guidance 8 pending user decision. Reviewer observations remain administrative only; 194 detached cycle already launched, no duplicate.

## Recorded commit-000194-001

Ancestor retrieval only. reviews/verdicts/commit-000194-001.md sha256 e0becf32ee24bb922d7ed4c8bb4f5f4b3b036e0025ccd429cd4539a2430c0d14

### Follow-ups

1. Ledger: the two 185 identities gain `8b1fccf7` as affected once they are filed. Earlier owed items stand.

### Must fix before canonical use

None for this entry.

2026-11-16: 194/001 approved for ancestor retrieval only, clean; verdict SHA256 e0becf32ee24bb922d7ed4c8bb4f5f4b3b036e0025ccd429cd4539a2430c0d14, request and ten artifact hashes verified. Canonical/training remain false. Ledger follow-up: add 8b1fccf7 as affected to both 185 RoPE identities once filed; earlier owed work remains. 195 authorized detached on guidance 8.

## Recorded commit-000195-001

Ancestor retrieval only. reviews/verdicts/commit-000195-001.md sha256 07c8cef9695b27a37bbc1c01309118df9728b12c35ab404ff0308a1905002545

### Follow-ups

1. Ledger: identities for the two findings may be filed as suspected, introduced at `965f5b2f`; the empty-order
   case may be added to the partition record as a second trigger. Earlier owed items stand.

### Must fix before canonical use

1. An empty `order` is accepted by the wrapper. In the kernel `rotate_len - 1` is then an unsigned wrap, the loop
   bound is enormous, and `order[0]` is read from an empty tensor before that. The entry lists "nonempty order"
   among unverified caller preconditions; it is the same kind of unsigned underflow as its first finding and
   should be stated as one.

2026-11-16: 195/001 approved ancestor retrieval only; verdict SHA256 07c8cef9695b27a37bbc1c01309118df9728b12c35ab404ff0308a1905002545; request and ten artifact hashes verified. Both findings confirmed at source level, remain suspected without GPU execution. Canonical-use condition: empty order is accepted, order[0] reads empty storage and unsigned rotate_len-1 wraps; must be stated as a finding before canonical use, not merely a precondition. Reviewer-only observation, never teacher input; authored run unchanged. Ledger identities owed for vector partition and unused test dtype, introduced 965f5b2f; empty-order may be a second partition trigger with reviewer provenance. Earlier owed items remain open. 196 authorized detached on guidance 8; canonical/training false.

- Guidance-10 trial decision read (SHA256 `9d1dcc4ec73d6465424184fe490b32f8f830ff3ca6a785ed6757f3fd7741c5fb`). Trial only, walk stays 8; version 9 must reproduce unchanged. Patch staged, NOT applied while 196 runs: reports/guidance-10-implementation-001.patch, base hashes in reports/guidance-10-staging-001.json. Pre-edit actual v8/v9 openings captured in reports/guidance-10-v8-before.json and guidance-10-v9-before.json; verifier reports/guidance-10-verify-001.py prepared. After 196 completes validation and its request is filed: verify base hashes, apply staged patch, run verifier with PYTHONPATH=., run full host-enabled suite, file reviews/requests/guidance-10-implementation-001.md. Only after acceptance run three fresh unassisted unpublished trials 188,189,178 under .teacher/trials/, never journal/ancestor context, then file guidance-10-trial-001 with artifacts, coverage, tool/token counts. Reviewer criteria excluded from teachers. No walk pause set.

- 196/001 failed final annotation validation: source_inspection verification cited repo_grep and run only; no draft/coverage/review produced. Original run untouched and packet/provenance implementation hashes verified before guidance-10 patch. Recovery request reviews/requests/commit-000196-001.md filed; asking for fresh unassisted same-packet 002, no output repair, no retry launched, no advance to 197. Standing 113 exception specifically concerns corrupted call IDs, so not silently extended to evidence-type errors.
- Guidance-10 gate applied after 196 exited and recovery request filed. reviews/requests/guidance-10-implementation-001.md filed; 280 host-enabled tests pass (31.537s), exact decision text, v8/v9 full openings byte-identical, v5/v6 legacy unchanged, failed196 opening and all 7 request artifact hashes unchanged. Walk default stays 8, v9 unchanged. Wait for implementation acceptance before the three scratch trials (188,189,178); recovery of196 separately awaits verdict.

- 196 recovery CONFIRMED: reviews/verdicts/commit-000196-001.md SHA256 `e5956cc81c489c53a39fd8aaab091115caefed2800e9040a991070482198f253`; request and all 7 artifact hashes verified. Fresh unassisted 196/002 authorized on original immutable packet/opening; failed001 remains excluded. No failed annotation or reviewer material supplied. If002 fails, stop/request; no third attempt. Standing rule now permits ONE fresh same-packet unassisted retry after final citation validation failure (missing ID or wrong evidence kind); disclose next request, preserve failure. A second consecutive failure requires review. If a third occurrence of this same rule arises, propose an implementation change; no validator/instruction change now.

- Guidance-10 implementation ACCEPTED as trial gate: reviews/verdicts/guidance-10-implementation-001.md SHA256 `b4cb18c07c361c7c4eb04d5af2117b0585903da1c78f0dd6cc60ea21a70e1ff0`; request hash and all 11 artifact hashes verified. Walk stays 8, not adoption. Three fresh unassisted trials188,189,178 authorized under .teacher/trials/, no journal attempts/approval/ancestor context/reviewer input. 196/002 already running; no duplicate. Launch trials after196/002 request is filed, before another walk commit, to preserve snapshot isolation.

- 196/002 request filed: reviews/requests/commit-000196-002.md. Fresh unassisted same-packet retry, exact opening, failed001 preserved;19 identical replays,2877 shared blobs,1/1 task sections. Two inherited suspected native findings; partial model/science/RoPE reads disclosed, one AST file-read/scalar run separate from9 repo_reads. Await verdict; no197. Guidance-10 three-session supervisor launching between commits: hold walk journal/run mutations during its before/after snapshot, then file trial request and apply any queued196 verdict.

- 196/002 APPROVED for ancestor retrieval only (clean): reviews/verdicts/commit-000196-002.md SHA256 `f8bc955321da43b631f55beca23f468c861891989bd23463819a8666c85c61d4`; request and all14 artifact hashes verified. Failed001 remains failed/excluded. a39fdfc4 confirmed fix of185 normalization-settings identity; add196 affected to the two native185 identities. No canonical conditions. Reviewer note about a finding present only in failed001 is not a ledger candidate or teacher input. Approval application and197 launch deferred only until active guidance-10 trial snapshot completes (188 currently running); preserve journal/runs for isolation. On trial completion, inspect/file trial request, then apply this verdict as instructed and launch197 detached on8. Do not lose this authorization.
