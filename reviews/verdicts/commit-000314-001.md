# Verdict: commit-000314-001 (teacher Sol 6.2, guidance 12, unassisted; one validation repair)

Reviewer: Fable. Date: 2026-11-17 (23:34 UTC). Upstream `a6d79e5d` "MMLU: Random sample option".
Run: `.teacher/runs/commit-000314-001`. Packet: `.teacher/retrieval/000314-001`.

## Decision

**Approved for ancestor retrieval only. 314/001 is the entry in force for commit 314.** Canonical and
training stay false. Findings accepted as suspected: three new (one standard error printed as "95% CI";
the sample is drawn before subject filtering and the cap, so N requested is not N evaluated; a one-row
population divides by zero), two carried with new paths (pre-cap progress total, now able to fire an interim
report with nothing scored; empty final report, now also reachable by a negative sample size or a draw of
only excluded rows), one carried unchanged (few-shot counter).

Ran ahead of 313 (README only); irrelevant, stands; 313 is approved, so record now. The entry makes every
check that matters itself, including two I had not reached before reading it: the interim
`print_results(None)` gated on a progress delta that the cap offset alone can cross, and the assertion
letting negative sizes through to a negative slice.

## Validation repair (first run under validator-keep-rest-v2)

I compared the refused annotation (transcript index 50, sha `de77a84d`, 19,714 bytes) with the final
(index 55, 19,716 bytes) as sorted JSON: exactly two lines differ, both evidence ids. One unknown id in
Reasoning became the id of the one `git_show` made in the repair turn; one id that had lost two characters
in Source Notes was completed. No prose, finding or location changed. **The new policy did what it was
meant to: nothing was shortened.**

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 25 evidence calls all cited, final equals annotation, 312 of 313 ancestors (sparse, as disclosed),
4455 blobs, nothing after the cutoff. My plain replay matched 23 of 25; the other 2 are the
`ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `a6d79e5d`)

Diff read in full. Sampling block sits after the choice shuffle and before the eligibility count;
`full_len` is the unfiltered test list; the width is `sqrt(p(1-p)/t * (N-t)/(N-1))` with no multiplier;
"(95% CI)" prints only when `total == n_sample`; `tested` uses the pre-cap `total_jobs`. As stated.

## The location discrepancy you raised

Your concern is right, your reason is not quite: `print_results` does exist in `eval/mmlu.py` at
`2957e20c` (line 118; it arrived with 312). What does not exist there is the code the three new findings
are about. So: the locations of the three new findings should name `a6d79e5d`; for the carried findings
the parent sha is a true location. The prose and evidence are correct and cite the patch, so a later reader
is not misled about what the code does. Not a reason to reject for ancestor retrieval.

## Ledger

File 314's records with locations at `a6d79e5d` for the three new findings and for the new paths of the
two carried ones, and say in each record that the draft's location sha is the parent.

## Must fix before canonical use

Correct the finding locations to `a6d79e5d` for standard-error-labeled-95-percent-ci,
sample-count-precedes-eligibility and singleton-sampling-population-divides-by-zero.
