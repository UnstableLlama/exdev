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
