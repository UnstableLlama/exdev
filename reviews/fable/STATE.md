# STATE: exdev (teacher walk review)

Current picture, refreshed 2026-11-14 late evening, at the save the user asked for after commit 129. The previous version is kept beside this file as
`STATE-2026-11-13.md` (older open threads, the NUC's paths). The repo's README, `docs/`, `reports/` and
`reviews/verdicts/` are the detailed record; this is the map.

## What it is

Builds a historical Encyclopedia and code graph of exllamav3 (2,264 commits, pinned tip `bd1f519`), commit by commit with
no hindsight, to generate training data later. Source mirror in `.sources/exllamav3.git` (ignored).

## Who does what

- **Astra** (OpenAI `gpt-6-astra`, medium, Codex CLI **0.167.0 pinned**) writes all code, runs the teacher sessions, keeps
  the ledger and journal. Rules: `reviews/AUTHOR-INSTRUCTIONS.md` via root `AGENTS.md`.
- **I am Fable, the reviewer.** I write only under `reviews/verdicts/` (verdicts, `<topic>.decision.md` quoting the user's
  words, pointer-only `commit-N-A.coverage.md`) and my notes under `reviews/fable/`.
- Approvals are for **ancestor retrieval only**. Canonical and training stay false; never approve those.
- Do not commit or push unless the user asks. The user asked once, on 2026-11-14 after commit 129: everything up to
  that point is committed on `main` and pushed (`3cbf0b9` "Walk through commit 129 ...", then merge `57d0291`). Work
  after it is uncommitted again.
- **How to commit and push from this machine.** It has no Git identity and no credential helper. Commit with the
  identity of the existing history (`git -c user.name="$(git log -1 --format=%an d0a2d08)" -c user.email=... commit`)
  and push with `git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin main`.
  `git merge` does not take `-F -`; write the message to a file. The user also pushes to `main` from other checkouts
  (the graph atlas under `docs/graph-atlas/` arrived that way), so fetch first and merge, never force. Merge rather
  than rebase: Astra has live files in the tree.

## Where it runs now (the laptop)

The user's NUC (Linux, user `unstable`) stays at their workplace. The walk runs on their Apple Silicon MacBook inside an
OrbStack Linux machine. Do not suggest moving back to the NUC.

- Machine: **`exdev-314`**: Ubuntu 26.04 arm64, Python 3.14.4 (matches the recorded runs), bubblewrap 0.11.1. Another
  OrbStack machine `ubuntu` exists and is not ours.
- Live checkout: `/home/brandonrabe/git/exdev` inside the machine. `/Users/brandonrabe/Downloads/exdev` on the Mac is a
  stale clean copy at `d0a2d08`; ignore it.
- From the Mac, run things in the machine with
  `/Applications/OrbStack.app/Contents/MacOS/bin/orbctl run -m exdev-314 bash -ls <<'EOF' … EOF` (a heredoc on stdin avoids
  quoting trouble). The user's own shell has `orb`.
- Pinned Codex: `~/.codex/packages/standalone/releases/0.167.0-aarch64-unknown-linux-musl/bin/codex` (on PATH only in
  interactive shells; use the full path in scripts).
- Astra's thread id on this machine: **`01a1da07-7653-7b81-8507-f69683828acb`**. Astra's window is a terminal tab started
  with `orb -m exdev-314 bash -ic "cd ~/git/exdev && codex resume --last --approve-for-me"`. `--approve-for-me` is Codex's
  automatic approval review (not the dangerous bypass); without it Astra stops for a prompt on every command. I can open
  such a tab with the terminal tool but cannot type into it.
- If a new Astra window says "This conversation is open in another app", a leftover Codex app-server process holds the
  thread lock. Find it (`ps`, and `/proc/<pid>/fd` for `thread-writer-locks/<thread>.lock`), kill it, reopen.
- GitHub CLI in the machine is logged in (account UnstableLlama). No Hugging Face token, by the user's choice.

## The loop

Watch (run in the background; it exits when a request has no same-named verdict):

`orbctl run -m exdev-314 bash -lc 'cd ~/git/exdev && while true; do for f in reviews/requests/*.md; do b=$(basename $f); [ -e reviews/verdicts/$b ] || { echo "PENDING $b"; exit 0; }; done; sleep 5; done'`

Review, write `reviews/verdicts/<same name>.md`, then notify:

`codex queue --thread 01a1da07-7653-7b81-8507-f69683828acb --resume -C $HOME/git/exdev --message "Verdict ready: reviews/verdicts/<name>.md — <one line>"`

It prints "could not resume thread … start a local daemon" as a warning; the open Astra window still picks the message up.
Restart the watch after every verdict. Tell the user one line at the start and end of each review, in plain words:
what the commit does, whether it is approved, and anything that needs them. They found the dense versions confusing.

## How I review a run

`reviews/fable/review.sh` (inside the machine) does the routine pass on whatever is pending: request text, `check.py`,
request hashes, the draft, the diff stat, a replay of every recorded tool call through `teacher.runner.Runner`, a
comparison of the standing instructions with the previous position's run, a hindsight grep, and the open issues at the
cutoff from GitHub. It assumes a `commit-NNNNNN-AAA` request; for anything else read the request by hand. Known quirks:
a recorded tool *error* shows as one replay mismatch (the tool raises where the transcript stored an error object);
merge commits legitimately add two `merge_facts` sentences to the instructions; the open-at-cutoff query
uses each issue's current `closed_at`, so an issue closed then reopened later is miscounted (33 at 129: check the
timeline when the count disagrees with the catalog); when the packet is shared with another
attempt, point `check.py` at it by hand.

Then by hand: read the upstream diff and check every claim at parent and task; trace findings independently; check
that nothing after the cutoff is in the packet. Verdict sections: Decision, Artifacts, Run checks, Not verified, Must
fix before canonical use, Follow-ups, Next. Reviewer-only knowledge goes under a heading that says so and never to a
teacher.

**When a commit adds an architecture:** check the reference list against the publisher's organisation myself, and
compare the constructor's declared tensors with the bundle's safetensors headers myself (names, shapes, leftovers).
The teacher rarely reads headers. At 39 that hid the central defect; at 98, 103 and 110 it hid nothing, but I only know
because I looked.

**Do not write a verdict sentence about something I am checking in the same command.** At 112 I guessed a dtype in the
verdict and the check printed the opposite; I had to revise the file and send Astra the new hash.

## Where the walk is

- Approved for ancestor retrieval: **commits 2 to 129** (93 was approved mechanically under the standing policy; I
  looked and agree). 113 is attempt **002**; 113/001 failed validation on a garbled evidence call id and stays as a
  failed, unpublished run (recovery verdict `commit-000113-001.md`). A fresh unassisted attempt on the same packet is
  the standing recovery for that kind of failure.
- **Pending at the save: commit 130.** `reviews/requests/commit-000130-001.md` was filed just after the commit and
  has no verdict; it and two modified reports are the only uncommitted paths. Review it first. Its task is `2e7b00d3`
  "Generator: Prevent particular failure mode in generator from holding output indefinitely".
- Still owed by Astra, not blocking: the discussion-history cache (request 2 in `DISK-AND-CACHE-PROPOSAL.md`). Today
  every commit refetches every discussion (about 2 of each 6 minutes; 576 discussions by the tip). When the request
  comes, check regenerated catalogs for 113 to 129 against the recorded ones and the cutoff cases at 126, 128, 129.
- Pace measured this session: about 6 minutes per small commit (Astra's preparation 3, teacher 1, request 1, my
  review 1 to 1.5); large commits (119, 123, 129) take two to three times that.
- **Packet storage (accepted 2026-11-14, `blob-store-implementation-001`):** packets under `.teacher/` hold read-only hard
  links into `.teacher/blob-store/` (2,171 objects, about 0.6 GB; all of `.teacher` about 1 GB, was 38 GB). Copying
  `.teacher` without preserving hard links expands it again. `review.sh` and `check.py` work unchanged.
- Commit 39: attempts 006 and 007 (unassisted, with Deci evidence) were rejected; **39/005 stays in force**, no further
  attempt. The older-Deci incompatibility is preserved in the ledger instead.
- Reviewer-assisted entries in force: 39/005, 44/003, 45/002, 55/002, 71/002.

## Rules decided this session (files in `reviews/verdicts/`)

- `arm64-graph-backend.decision.md`, `arm64-python-version.decision.md`: native arm64 backend; Python 3.14.
- `commit-000098-reference-mirrors.decision.md` (user: "look for unsloth mirrors and if they dont have them modelscope.cn
  will"): when official Hugging Face repositories are gated and no token is configured, a **hash-verified ModelScope
  mirror** may stand in. Identity is shown against the hashes Hugging Face publishes for gated files without a login
  (`/api/models/<repo>?blobs=true`). unsloth's copies were re-saved and do not match, so they are not used.
- Addendum plus `commit-000103-reference-access-001.md` (my ruling, user informed): a non-weight file whose official copy
  was edited after the cutoff may come from a pre-cutoff mirror revision under status
  `mirror_historical_unverified_identity`, if two distinct mirrors agree and every other file verifies. First case:
  `c4ai-command-r7b-12-2024/config.json`. **Reviewer-only: the edited field is `max_position_embeddings`; its later value
  must never reach a teacher.**
- `architecture-trigger-fixes-implementation-001.md`: renames are recognised by Git; identities are read from the config
  class. Condition: any `curator_attestation` outcome or unresolved bundle must be named in that commit's request and
  gets a full review. After commit 102 the registry-key detector no longer fires; derived identity is the guard.
- Accepted implementations: `blob-store-implementation-001`, `arm64-runtime-implementation-002`, `reference-absence-implementation-001`,
  `modelscope-mirror-implementation-001`, `historical-mirror-implementation-001` (240 tests at last count).

## Ledger and carried reviewer knowledge

Records filed or revised this session: `exllamav3-legacy-decilm-config`, `exllamav3-missing-combo-sampler` (fixed at 91),
`exllamav3-presfreq-zero-decay-boundary` (mine: NaN at the window edge when decay is 0; reachable through
`ComboSampler`), `exllamav3-cohere-qk-normalization` (**not** fixed by 108; Plus models store per-head `q_norm`/`k_norm`
weights `[96,128]`/`[8,128]`), `exllamav3-chat-stream-argument-mismatch` (105, fixed at 106).

Findings approved in drafts and not yet in the ledger, or needing merged identities:
- `SS_MinP` rejects 0 and has no no-op: one defect seen at 91, 92 and 111 under three names. **Fixed at 113.**
- `SS_TopP(0.0)` asserts although its `alt()` names 0.0 as a no-op (mine, 113/002 verdict; other half of PR 30;
  reachable through `ComboSampler` and the chat example). Filed as `exllamav3-top-p-zero-assertion--r001` (accepted at 114; still present at 114; **fixed at 115**: zero accepted as
  maximum truncation, not a no-op; ledger revision pending). `min_p = 1.0` is
  rejected at 113 only; 114 accepts it again. The ledger validator rejects `reviewer_observation` origins (open).
- Both-axes linear padding: one identity across 84, 86 and 88 (accepted as a restriction in PR 20).
- Unchecked `K - 1` table index (79): four sites, the entry names two; `reconstruct` is on the load path.
- `unconditional-tk-import` (89): the package needs `tkinter` to import. **Fixed at 118.**
- `plain-mlp-allocation` (96) also exists in `TransformerBlock`; introducing commit not established.
- `architecture-mismatch-diagnostic` (102; **fixed at 117**, entry does not link back), `chat-top-k-float` (92), `single-device-progress` (76, class it as an
  incomplete feature), `multinomial-sorted-token-mapping` (82), `top-p-description-mismatch` (81, documentation).
- `reasoning-boundary-answer-loss` (73) still holds after 106, which edits that branch and does not say so.
- Reviewer-only from headers: the two Cohere `-4bit` repositories are bitsandbytes-packed and the six Qwen3 FP8
  repositories use `F8_E4M3` with `weight_scale_inv`; neither can load. Qwen3's residual stream is float32 (embedding
  default), which is why 112 matters.

- Reviewer-only from 116: `count_inf_nan` launches CUDA unconditionally (a captured `Linear` on the CPU would break; only
  `Embedding` prefers the CPU and it has no qmap), and its block index wraps at 2^32 elements. Neither reachable yet.

- Reviewer-only from 119 (deferred loader; mine, source inspection, asked Astra to file three candidates): the variant
  collection lacks the new `get_tensor` keywords and the deferred-load methods; truly sliced FP16 linears get a
  `pad_to` smaller than the full tensor; fused FP32 weights are no longer halved. Watch for the fixes. The entry's own
  finding `deferred-bf16-odd-tail` (CUDA only) is approved. The three are filed and accepted (120 verdict); none
  is fixed at 120, which adds `metrics-wrapper-compatibility` (removed `get_metrics` still called twice).

- 119 also created a same-stem source pair (`stloader.cpp` / `stloader.cu`) that 121 renames away ("Fix object filename
  conflict"). I missed it at 119. Lesson: when a commit adds a source file, check for a same-directory same-stem
  sibling.

- Repetition penalty and masked logits (from 90): `-inf` through `v*(1-f) + w*f` gave NaN at f = 0 (fixed at 122 with a
  1e-30 offset) and still gives NaN at f = 1, which is every history token under the default sustain range. Watch for
  the second fix.

- Reviewer-only from 123 (cooperative GEMM; mine, source inspection, asked Astra to file): `select_gemm_shape` returns the
  256-wide shape without a divisibility test in four branches and the launch-time check is gone, so a padded width that
  is an odd multiple of 128 loses its last 128 columns silently. The entry's own finding (Boolean compared with 8192 on
  Hopper) is approved. 123 was approved with 12 of 30 sections read; I read the rest (uniform compile units). Filed and accepted as
  `exllamav3-gemm-selector-divisibility--r001`.

- Commits by outside authors (five up to 124): check the pull request's opening time against the cutoff and that the
  packet has no trace of it when it is later (PR 32 opened five minutes after 124's date). I wrote "first outside author"
  in the 124 verdict without checking and had to revise it; same lesson as 112.

- **Reviewer-only hindsight (issue 33, comments after 126's cutoff; never to a teacher):** the conversion failure was a
  limit on open files. `stloader_open_file` keeps `STLOADER_THREADS` handles per file (5, raised to 8 at 119). Expect a
  fix; check then which commit introduced per-file handle caching. **Fixed at 128** (handles closed per module);
  caching dates from the first commit, 5 to 8 handles per file at 119.

- **Reviewer-only hindsight after 129:** "Fix regression" (`456f14f9`) and "Fix bad include" (`c2b8516f`) follow within a
  day (not necessarily the very next positions; 130 is a generator change); expect them to fix 129's double mask/XOR in
  `decode_3inst` and the include of a header that does not exist.

- **Ledger revision owed** (all recorded in the verdicts' Follow-ups and Astra's journal; nothing filed yet): min-p
  identity fixed at 113 with the one-commit 1.0 regression; top-p record fixed at 115; mismatch diagnostic (102) fixed
  at 117; tk import (89) fixed at 118; object-name conflict introduced 119, fixed 121; repetition-penalty NaN (90)
  half fixed at 122; handle accumulation fixed at 128; affected-revision additions for the 119 and 123 records;
  `humaneval-top-k-float` as a second site of 92's; 126's errno pair; 129's two new findings.

## Open threads

- Canonical-use notes recur: entries for architecture commits read no headers (98, 103, 110).
- How to count `run` calls that read or execute repository files (101 executed a helper; 108 scanned the tree).
- The NUC's exact Python and bubblewrap versions were never confirmed against this machine.
- `reports/teacher-boundary.json` reference should be regenerated on amd64 some day.
- Older threads are in `STATE-2026-11-13.md`: assisted-entry policy for canonical use, the unreadable image at 74,
  expectations for issues 99 and 233 at positions 560 and 1100.

## Update after commit 141 (2026-11-14, late night; nothing committed since `d980d21`)

- Approved for ancestor retrieval: **130 to 141** as well (all attempt 001). Next is **142**. Everything from 130 on
  is uncommitted; the user was told and has not asked for a commit.
- Accepted implementation: `header-budget-implementation-001` (official Hugging Face header bound 16 MiB in recovery
  and runtime; ModelScope stays 4 MiB; a further increase needs a new review). 247 tests. To run the suite from a
  non-interactive shell, put the pinned Codex directory on `PATH` first, otherwise two wire tests error at spawn.
- 141 registered Qwen3 MoE. Headers checked by me: the three unquantized repositories match the builder exactly;
  FP8 (F8_E4M3 plus `weight_scale_inv`) and GPTQ (packed) cannot load. Canonical-use note recurs.
- Both predicted fixes from 129 arrived (131 scalar decoder, 132 include).
- **Canonical-use condition on 136:** the entry lacks the finding that `int.is_integer()` needs Python 3.12 (ledger
  `exllamav3-top-k-int-is-integer-compatibility`). **Reviewer-only hindsight:** upstream `95cfa726` (2025-05-12)
  "top_k sampler: Fix int check for older Pythons"; expect it soon. Also `8cfa711a` (2026-05-02) fixes the
  `held_token` typo, far ahead.
- My missed-at-the-time items found this session: 119 left the in-memory loader branch ignoring `transpose` (fixed
  138; ledger filed); 140 `_load_single` has no abort on failure (ledger filed); 139 fused path wrong unless
  `interm_dtype` is half (ledger filed; 141 passes half).
- Multi-GEMM records (133, 135): leading-dimension validation, zero grid cap (rooted at 123), broadcast scratch
  capacity. The 139 fused path is the first caller and satisfies them at Qwen3 MoE sizes.
- Still open, mine, not filed: checkpoint offset undercount when a replacement character interrupts a banned-string
  hold (noted in the 130 verdict; needs a proper trace).
- Lessons added: when a commit moves a transformation into a loader keyword, check every loader branch for it (138);
  when new code copies a bracket from another path, compare the error handling too (140); this machine has only
  Python 3.14, so version-dependent behaviour cannot be shown by a teacher run (136).
- The user asked about an external drive (one attached, 2 TB NTFS "Expansion") and Google Drive; they then said
  nothing is needed. No upload was made.

## Update after commit 153 (2026-11-15 afternoon; nothing committed since `d980d21`)

- Approved for ancestor retrieval: **142 to 152** as well (all attempt 001). The details are in each verdict; this
  section was written at a session restart from the verdict files, not from memory of the reviews.
- **153 (merge of pull request 37, dev into master) attempt 001 is REJECTED as thin** (3 of 44 sections read). The
  coverage request for a reviewer-assisted attempt 002 is `reviews/verdicts/commit-000153-002.coverage.md`. The walk
  does not move to 154 until 153 has an approved entry.
- Accepted implementation: `closed-path-overlap-implementation-001` (`salience-v3-paths`, for packets from 152 on,
  under the three conditions in that verdict).
- **Astra is stopped.** The notification for the 153 verdict reached Astra's thread at 00:41 PST on 2026-11-15 and
  the turn ended at once with `usage_limit_exceeded` (no credits; "try again at Nov 18th, 2026 4:25 AM"). Nothing in
  the tree has changed since. The window is still open (`codex resume`, pts/1). When the limit lifts or the user
  adds credits, re-send the notification with `codex queue`; the first one was consumed by the failed turn.
- No request is pending. Everything from 130 on is still uncommitted.

## Update 2026-11-15 afternoon (PST): walk blocked on Astra's usage limit

- Approved for ancestor retrieval: through **152** (130 to 152 all attempt 001). **153/001 is REJECTED: thin**; the
  coverage request for attempt 002 is `reviews/verdicts/commit-000153-002.coverage.md`. 153 is the merge of pull
  request 37 (dev into master, tree identical to dev). Do not let 154 start before 153 has an approved entry.
- **Astra stopped at 2026-11-15T08:39Z with "You've hit your usage limit ... try again at Nov 18th, 2026 4:25 AM".**
  My rejection notice was delivered into the thread at 08:41Z and the turn failed with the same error, so Astra has
  not acted on it. When the limit clears (or the user buys credits), re-send the notice with `codex queue`.
  How to tell: when Astra is silent, read the last line of
  `~/.codex/sessions/2026/11/14/rollout-...-01a1da07-...jsonl`; the `task_complete` event carries the error.
- Accepted implementations since the last update: `closed-path-overlap-implementation-001` (`salience-v3-paths`,
  in use from 153; conditions: per-request report of path-only rows and truncation, stop at the first truncation
  and propose an ordering, no rewriting of earlier packets). 253 tests.
- Ledger: all follow-ups from 130 to 152 were filed and accepted except those listed as "older ledger revisions
  owed" before 130. The Python 3.12 record is closed (introduced 136, widened at 144 and 149, fixed 151).
- Canonical-use conditions outstanding: 136 and 149 (integer check finding), 141 (headers), 150 (pull request 35
  comment was not in the packet).
- The machine's clock is PST; `date -u` gives UTC. The background watch dies with exit 255 when the Mac sleeps;
  just restart it.
- Nothing committed since `d980d21`. The user has not asked for a commit.
- **Later the same day:** the user restored credits; I re-sent the notice; Astra authored 153/002 and I **approved it
  (reviewer-assisted)**. It is the sixth assisted entry in force. Next is **154**.

## HANDOFF 2026-11-15 evening (PST): read this section first; it supersedes the "pending" lines above

**Where the walk is.** Approved for ancestor retrieval only: commits **2 to 154**. 153 is attempt **002**
(reviewer-assisted, coverage request `reviews/verdicts/commit-000153-002.coverage.md`); 153/001 was rejected as
thin and stays unpublished. Next request to expect: **commit-000155-001**. Astra's usage limit cleared on the
afternoon of the 15th and it is working. Nothing is committed since `d980d21`; the user has not asked for a
commit, and everything from 130 on lives only in this machine.

**Accepted this session (verdict files of the same name):** `header-budget-implementation-001` (official Hugging
Face header bound 16 MiB; ModelScope stays 4 MiB) and `closed-path-overlap-implementation-001`
(`salience-v3-paths`, in use from 153). Conditions on the second: each request reports path-only rows and
truncation; at the first truncated position Astra stops and proposes an ordering; no earlier packet is rebuilt.
I accepted it on the merits; Astra's request said the user asked for it and the user never confirmed or objected.

**Canonical-use conditions outstanding** (entries approved for retrieval but incomplete): 136 and 149 (the
`int.is_integer` Python 3.12 finding), 141 and 153 (tensor headers, which variants load), 150 (pull request 35's
comment was not in the packet), 153 (reviewer-assisted).

**History shape.** Master and dev split after 132 and rejoined at 149 (master into dev) and 153 (pull request 37,
dev into master, tree identical to dev). For a commit on a side line the packet holds only strict ancestors, so
the entry count is not position minus one; check it against `git rev-list`.

**Ledger.** Every follow-up from 130 to 153 is filed and accepted. Asked for in the 154 verdict and not yet
filed: `ppl-axis-bound` (introduced `9575f7d8`), and a reviewer-observation record for unconditional deferral
in `eval/model_diff.py` (introduced `5c3ff204`). The "older ledger revisions owed" list from before 130 is
partly done (errno pair, handle accumulation, rep-pen NaN, top-p/min-p not yet); check each when it comes.
Reviewer-origin records fail the unchanged validator on the origin word; that is known and accepted.

**Open, mine, not filed:** checkpoint offset undercount when a replacement character interrupts a banned-string
hold (130 verdict); the default-path BOS loss in HumanEval (150 verdict, intent unclear, watch only).

**Hindsight I hold (never to a teacher):** `8cfa711a` (2026-05-02) fixes the `held_token` typo;
"Fix off-by-one error for penalty ranges" and "Respect negative presence penalty" (2026) touch `rep_pen.cu`;
"Generator: Fix max_new_tokens off-by-one error" (2026). I saw the last three by accident from whole-history
`git log -S`; **limit such searches to the task's ancestry** (give the task sha as the revision).

**Habits that paid off this session.**
- For a merge: check `git merge-tree --write-tree P1 P2` equals the commit's tree, and compare the instructions
  with the previous *merge* run, not the previous run (merges carry one extra paragraph).
- For an outside author or a pull-request commit: get the pull request's open time and title history from the
  GitHub timeline and compare with the cutoff; several were opened minutes after their commit.
- When new code copies a bracket from another path (deferred load), compare the guard before it and the error
  handling after it. Both 140 and 154 dropped something.
- When a commit moves a transformation into a loader keyword, check every loader branch (119/138).
- This machine has only Python 3.14; version-dependent behaviour cannot be shown by a teacher run.
- Thin entries may be rejected with a pointers-and-questions coverage request (user decision of 11-13); I used
  it once, at 153, for a 44-file merge of which 3 files were described.
- Run the test suite with the pinned Codex directory on `PATH`. The watch dies with exit 255 when the Mac
  sleeps; restart it. When Astra is silent, read the last line of its session log for a usage-limit error.

## After 155 (2026-11-15 evening, written by the session that took over from the handoff above)

- **155 and 156 approved** (155: router `pad_to = 1`, no-op for the 128-expert reference models; 156: plot colours by bracket). Both issue-38 ledger revisions accepted. 157 approved (extra close in conversion; a no-op on the normal path). 158 approved (Mixtral; headers match exactly; the gated Mistral-Large repo resolved by mirror in `commit-000158-reference-access-001.md`; Mixtral does not set `calibration_all_experts`). 159 mechanical and 160 approved through the driver. 161 approved (the issue-38 fix; padding-target fixed; it makes the 154 model_diff deferral observation reachable, r003 asked). Part E accepted (`token-cost-detach-001`): from 162 Astra launches `teacher.cycle_notify` detached and is woken by a queued message. Watch with `reviews/fable/watch.sh` (also catches a stalled cycle). 162 approved with a canonical-use condition (the entry missed that the in-place logit mask needs inference mode). 163/001 REJECTED (says every config passes a mapping; `Qwen3MoeConfig` still passes a bare class, so Qwen3 MoE cannot load at 163; reviewer-only). Coverage request `commit-000163-002.coverage.md`. 163/002 approved (assisted; found the Qwen3 MoE break itself; ledger `exllamav3-qwen3-moe-component-migration`). **Hindsight to watch: expect a one-line upstream fix for `qwen3_moe.py`.** Guidance 6 draft awaits the user (`GUIDANCE-6-DRAFT.md`). 164 approved (Gemma3 text; 11 mirror bundles verified; vocabulary 262,208 makes the logits-padding record concrete; `Gemma3ForCausalLM` not registered yet; architecture commits stay manual and cost Astra 4.9M tokens here). Guidance-6 gate and the replay fix accepted. 165 approved (KLD test; two correct regressions found unassisted under guidance 5; 0.65M tokens, 13 calls). 166 approved (the Qwen3 MoE fix; 0.49M tokens, 6 calls). 167 approved with a canonical-use note (did not read 137, whose finding persists in the edited function; another case for guidance B; 0.47M, 12 calls). 168 approved (head BPW suffix match for Gemma3; 0.55M, 10 calls). 169 approved with canonical-use notes (long-context script cannot start: `add_args` lacks `default_cache_size`; expect the missing `model_init.py` change soon; 0.46M, 7 calls). 170 approved (the missing `model_init` half of 169; 0.52M, 7 calls). 171 approved (GPTQ layer accounting; last commit under guidance 5; 0.84M, 10 calls). **Guidance 7 live from 172** (`guidance-7-adoption-001` accepted). Next: **172**, the first commit under it; compare tool calls and ancestor reads with 165-171 (four trial sessions under `.teacher/trials/`). Comparison for the user delivered after 163/001.
- Issue 38 (opened 2025-05-14T06:52Z, inside the cutoff from 155) is the field report of my 119 record
  `exllamav3-sliced-fp16-padding-target`: Nemotron-Ultra 253B (DeciLM), MLP sliced eight ways, loader copy
  mismatch 49,920 vs 399,360. Asked Astra for two ledger revisions (155 verdict follow-ups 1 and 2).
- **Hindsight (never to a teacher):** the maintainer's comment on 38, after the cutoff, blames the padding work;
  expect the fix in the next commit or two. When it comes, check it against the 119 record and whether
  `model_diff.py`'s unconditional deferral (154) becomes reachable once sliced loads work again.
- Two reviewer sessions ran at once for 153/002 on the 15th and both wrote that verdict (final hash
  `1ed558b6…`). Only one session should run the loop; check `list_sessions` if a verdict appears that you did
  not write.
- **Token cost work (user asked 2026-11-15 evening).** Proposal sent to Astra: `reviews/fable/TOKEN-COST-PROPOSAL.md`
  (one blocking driver, generated request skeleton, durable tracking file; then I lower Codex's
  `model_auto_compact_token_limit` to about 60k and restart Astra's window at a commit boundary). Expect
  `reviews/requests/token-cost-implementation-001.md`. Baseline for Astra's thread, commits 131 to 156: about 22
  calls and 3.4M input tokens per commit (156: 15 calls, 1.72M; 155: 24, 2.48M; 154: 29, 2.48M). After it lands,
  compare five commits before and after: calls, tokens, sections read, tool calls, ancestor reads, entry length,
  findings, review results. The measuring script is in the session transcript: per-commit deltas of
  `total_token_usage` in Astra's rollout between request file times. The user wants quality watched closely.
- **Token-cost change is live from 159** (`token-cost-implementation-001` accepted with four fixes,
  `token-cost-fixes-001` accepted). Astra now runs `python3 -m teacher.cycle` (one blocking command; request
  skeleton in `reports/`; `reviews/ASTRA-TRACKING.md` short, `ASTRA-REGISTER.md` history). I set
  `model_auto_compact_token_limit = 90000` in `~/.codex/config.toml` (backup `config.toml.before-token-cost`) and
  restarted Astra with `codex resume <thread id> --approve-for-me` in terminal tab "Astra (Codex)".
  **Owed to the user: a before/after comparison after 163** (159-163 against 152-157): Astra's calls and tokens
  per commit; per entry sections read, tool calls, ancestor reads, length, findings; my review results. Also
  count ancestor reads: the teacher read none at 157 and 158, and the user may want a guidance change later
  (deliberately not mixed with this change). `check.py` will now show 43 implementation hashes.
- Token profile script: `python3 reviews/fable/token_profile.py START_FILE END_FILE label` (window between two files' mtimes). First reading 159+160: 33 calls, 1.38M input, max context 51k (156: 14 calls, 1.72M; 157: 17 calls, 2.24M).
- **Guidance 6 trial approved by the user** (2026-11-15, `reviews/verdicts/guidance-6-trial.decision.md`): three
  added paragraphs (changed contracts; read the entry for code the task builds on; edits that depend on each
  other). Trial only: four unpublished sessions on 154, 158, 163 and control 156. Expect
  `guidance-6-implementation-001`, then `guidance-6-trial-001`. **Owed to the user: the trial result and a
  recommendation; adoption needs their yes.** Also measure how much longer the trial sessions are.
- Cost readings after the token change (Astra's thread, input tokens): 159+160 1.38M/33 calls; 161 0.99M/16;
  162 0.84M/20; 163 0.54M/8 (first clean detached cycle); 163/002 by hand 1.03M/19. Before: 155 2.48M, 156
  1.72M, 157 2.24M. Reported to the user as roughly a quarter per commit.
- **Guidance 6 trial assessed** (`reviews/verdicts/guidance-6-trial-001.md`): 163 found unassisted, 158's main
  difference found, 154 not found (different kind of gap: a mechanism reused from a new place), control 156
  clean, about 40% more tool calls. Reported to the user with a recommendation: adopt A, B, C with A reworded to
  "the whole parent tree, read together with the task diff"; trial a fourth paragraph D (existing callers'
  guards) on 154 and 140. **Awaiting the user's decision; the walk stays on guidance 5.**
- **Guidance adopted by the user** (2026-11-15, `reviews/verdicts/guidance-6-adoption.decision.md`, "Adopt it"):
  paragraphs A (reworded: "search the whole parent tree, read together with the task diff"), B and C become
  the walk's guidance as **version 7**; version 6 stays as trialled. Expect `guidance-7-adoption-001`; check
  versions 5 and 6 unchanged and the version-7 text against the decision file. **Still owed to the user:** a
  proposal and trial for a fourth paragraph (existing callers' guards; cases 154 and 140), wording to be approved
  first. Keep counting ancestor reads and tool calls per commit after adoption to report the real cost.

## HANDOFF 2026-11-15 night (PST): read this section first; it supersedes every "pending"/"Next" line above

**Where the walk is.** Approved for ancestor retrieval only: commits **2 to 171**. 153 and 163 are attempt 002
(reviewer-assisted; their 001s were rejected). 159 was approved mechanically. **172 is being authored now**, the
first commit under guidance 7; its request will be `reviews/requests/commit-000172-001.md`. No request was
pending when this was written. Nothing is committed since `d980d21`: everything from 130 on lives only in this
machine (about 600 uncommitted paths). The user has not asked for a commit; it would be reasonable to offer one.

**Only one reviewer session may run.** Two ran at once on the 15th and both wrote the 153/002 verdict. My watch
was stopped at this handoff. Before starting, check `list_sessions` for another running "Fable exdev" session.

**How the loop works now (changed today, at the user's request, to cut Astra's token use).**
- Astra runs one commit with `setsid -f python3 -m teacher.cycle_notify …` (detached); the driver
  (`teacher/cycle.py`) does recovery, the stop checks, the teacher, validation and replay, and queues a message
  to Astra's thread when it exits. Astra writes the request from a skeleton in `reports/`. Architecture commits,
  replacements and assisted attempts are still done by hand.
- Astra's Codex config has `model_auto_compact_token_limit = 90000` (backup beside it). Its short state is
  `reviews/ASTRA-TRACKING.md`; history in `reviews/ASTRA-REGISTER.md`.
- Astra's window: terminal tab "Astra (Codex)", started with
  `orb -m exdev-314 bash -ic "cd ~/git/exdev && codex resume 01a1da07-7653-7b81-8507-f69683828acb --approve-for-me"`.
  It must stay open or queued messages wait.
- My watch: `orbctl run -m exdev-314 bash -lc '~/git/exdev/reviews/fable/watch.sh'` in the background. It exits
  with `PENDING <request>`, `STALL …` (journal says running, no process for two minutes; check before worrying:
  a hand-run teacher once tripped it), or `NOTIFY-FAILED …`. Exit 255 means the Mac slept or the watch was killed.
- Routine pass: `reviews/fable/review.sh` (now reports 44 implementation hashes). Pipe its output to a file and
  read the file; cut long lines. A recorded tool error shows as one replay mismatch in my script (not in Astra's).
- Cost per commit: `python3 reviews/fable/token_profile.py START_FILE END_FILE label` (Astra's thread between
  two files' mtimes). Before: about 2M input tokens and 14 to 23 calls per commit. Now: 0.46M to 0.84M and 6 to
  13 calls (165 to 171). Architecture commits stay expensive (164: 4.9M). Reported to the user as about a quarter.

**Guidance.** The user approved a trial ("yes that sounds good", "ok approve") and then adoption ("Adopt it").
Decision files: `guidance-6-trial.decision.md`, `guidance-6-adoption.decision.md`; trial assessment
`guidance-6-trial-001.md`. Guidance **7** (three paragraphs: changed contracts searched in the parent tree;
read the entry for code the task builds on; edits that depend on each other) is the walk default from 172.
Version 6 is the trialled wording, kept so the four trial runs under `.teacher/trials/` reproduce; trial runs are
never ancestor context.

**Owed to the user.**
1. After a few commits under guidance 7: the real cost and effect (tool calls, ancestor reads, findings, review
   results) against 165 to 171. Figures for 165 to 171, tool calls / ancestor reads: 165 21/1, 166 22/1, 167
   14/0, 168 14/1, 169 8/0, 170 10/1, 171 11/1.
2. A proposed **fourth paragraph** for the gap the trial did not close (154: an existing mechanism reused from a
   new place without the guard its other callers apply; 140 is the other known case). Wording must be approved by
   the user before any teacher sees it, then a small trial. Draft idea: when the task starts calling an existing
   function or mechanism from a new place, find its existing callers in the parent tree and compare the
   conditions, guards and error handling around those calls with the new one.
3. Astra still owes the discussion-history cache and the older ledger revisions; neither blocks.

**Canonical-use conditions added today:** 158 (no comparison with the Qwen3 MoE builder), 162 (calls three edits
independent; the in-place logit mask needs inference mode), 163 (assisted; lost 001's warning-name finding), 164
(no headers read by the teacher), 167 (137's empty-block condition persists and is not mentioned), 169 (does not
describe the altered-text tasks; five story sections unread).

**Things I am watching for (hindsight, never to a teacher).**
- Fixes for 165's two regressions in `eval/compare_q.py` (zero-over-zero when no reference; `--clear_cache` key).
- `eval/model_diff.py` still defers every module without `can_defer_load()`; reachable since 161.
- `Gemma3ForCausalLM` (the 1b models) is not registered at 164.
- Gemma 3's vocabulary (262,208) makes the old logits-padding-width record concrete for `return_logits`.
- Older items in the sections above still stand (`held_token` typo fix far ahead; rep-pen range fixes in 2026).

**Lessons from today.**
- When a commit changes what a shared constructor or function takes, list every user in the tree, including
  files the diff does not touch (163). When a commit copies a mechanism, read how its other callers guard it (154).
- For large files on Hugging Face compare the SHA-256, not the Git blob id (164's tokenizers).
- Check Astra's session log before believing a notification failed or Astra is stuck: the queue warning about
  "could not resume thread" is normal and the message still arrives.
- Keep tool output short; this session ran long mostly on output I did not need.
