# Verdict: commit-000308-001 (teacher Sol, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (20:40 UTC). Upstream `e12a1a5d` "chat.py: Add some more commands".
Run: `.teacher/runs/commit-000308-001`. Packet: `.teacher/retrieval/000308-001`.

## Decision

**Approved for ancestor retrieval only. 308/001 is the entry in force for commit 308.** Canonical and
training stay false. Two new suspected findings accepted (explicit-filename `/load` falls through to
generation; `/r` and `/e` index an empty history), one carried (`/cc` nonpositive index).

Not a run-ahead; full packet (307 of 307 ancestors). The entry makes the checks that matter itself: the
`try`/`continue` of `/load` sits inside `if len(c) == 1`, so a named file is never read and the
command text becomes a user turn; `/r` and `/e` read `context[-1]` with no guard, reachable at startup,
after `/clear` and always under `--amnesia`; the edited reply is a prefix appended after the open
assistant turn, wins over the think tag, and is streamed first so it lands in `all_text`; the empty-list
ban default takes the same `Job` branch as the old `None`; JSON turns come back as lists.

## Artifacts

Request hashes match (0 not OK). `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal
to the accepted set, 28 evidence calls all cited, final equals annotation, 307 of 307 ancestors, 4408 blobs,
nothing after the cutoff. My plain replay matched 28 of 28.

## Run checks (mine, tree at `e12a1a5d`)

Diff read in full. `chat.py`: both console modes set `read_input_fn = read_input_ptk` (lines 33, 36), so
the fourth argument is always accepted; amnesia reset precedes input; `job.py` 211 to 220 treats `[]` and
`None` alike; `Streamer_basic.stream` appends to `all_text`; no other `.stream(` chat callers. As stated.

## Ledger

The four records submitted with this request are accepted as filed: odd-tail r005, checkpoint-token r003 and
terminal-string-bypass r003 each append exactly one observation and keep the earlier ones byte-equal;
generation-capacity r001 gives the root finding a persisted identity plus the 307 observation, no new defect.
All stay suspected, training false. File 308's two new findings and the carried one with the next request.

## Must fix before canonical use

Nothing blocking. Optional precision: `get_input_ids(_prefix)` tests its parameter but appends the
enclosing `prefix` (same value at both call sites, so no behaviour difference).
