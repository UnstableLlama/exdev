# a6d79e5d0dd016764b228f7a4d4d709dc15dd374


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a6d79e5d0dd016764b228f7a4d4d709dc15dd374) · [Evidence ledger](draft.json)

Adds a fixed-seed MMLU question sample and interim pooled accuracy reports. Sampling precedes subject filtering and caps, so fewer questions may run than requested. The reported “95% CI” is a standard-error width, and the inherited progress and empty-report problems remain.

- [Sample MMLU questions and report pooled accuracy during evaluation](#usage-evaluation)

## Problem

The MMLU evaluator could select or skip subjects and cap questions per subject, but that cap took questions in traversal order. The parent had no option to draw a fixed-size random sample across the test split. [source; call_156719dd75c042f894fef6710e878219]

## Reasoning

The patch implements the commit message’s “Random sample option” by shuffling the test rows and taking a prefix. The same sliced list then supplies both the generation jobs and the rows scanned for reports. Saving its original length before slicing supplies the population size for the new finite-population calculation. [source; call_8c38931993b54f7e837bec2a18e0f3c4, call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219]

This makes a smaller run possible without taking a fixed prefix from each subject. It samples questions, not subjects, so it does not give each subject equal representation. Filtering to the target population before drawing, and deriving progress from jobs actually enqueued, would make the requested count, report denominator and sampling frame agree. A balanced per-subject draw would instead be a different sampling design. [inference; call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219]

## Impact

Omitting `--random_sample` or passing zero leaves question selection and per-subject reporting in place. The final label becomes `all subjects`, and the existing mean four-choice correct-answer probability is labeled `prob.`. With sampling enabled, periodic pooled accuracy and a plus-or-minus width replace per-subject lines and displayed probabilities; a final pooled report is still unconditional. [source; call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219]

## Source Notes

Read “Add MMLU eval,” which documents the introducing one-token logit workflow and records the missing few-shot counter increment, and “MMLU eval: More feedback during eval,” which records the subject-completion reporting, the pre-cap progress total and the empty-evaluation failure. [ancestor; call_a3e17610eb33423da706bdc40acb51b5, call_4ed0c6688d4e4d18a5f7e6d7773c8695]

Comparing the parent with the patch shows that the missing few-shot increment and pre-cap counting both carry over. The empty-report failure also carries over: the patch moves division into `score` and `conf` assignments without guarding the denominator, and adds another call that can reach it before the end of evaluation. [source; call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24]

Whole-parent searches identified the script’s `__main__` block as the only identifiable direct caller of this `main`, and only local calls to its nested `print_results`. The updated parser always supplies `random_sample`; an older argument object passed directly to `main` without that attribute fails at the new read if initialization reaches it. The old reporting calls supplied a subject after its last job or `None` after the queue drained. The new call also supplies `None`, but its gate is a progress delta rather than a check that at least one result was scored. [source; call_2c2f7e0ab1354e028418fa298924da8e, call_479662c47fa641b689d9c864e531788a, call_0ff2e04b7acb47fc8e863264ae788c9b, call_293b902919e54985bdff70e50cfee061, call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24]

The parent’s calibration helper `shuffle_lines` already pairs `random.seed(0)` with an in-place shuffle, after removing whitespace-only lines and before token packing. The new MMLU path uses the same global Python RNG pattern but shuffles the full test list before excluding subjects. The other literal shuffle match is benchmark text stored as calibration data, not a second library caller. Other inspected seed sites initialize experiments or tests, or conditionally seed the custom sampler from its supplied random integer. [source; call_cc926a6cfd684bcaaf306a0a16bd7766, call_c4f2903fe5df4e3dbad2824ca1069ae0, call_1917368b00514c61a6b18535ce87ee52, call_ff5d0a910ef6437599a65dca50b2b7b6, call_3a364d7ebfa14bfba7d4464fb9020c24]

Issue #10, “Soooo Cool !!! Thanks a lot for the new version ! I loved the v2,” is a note of appreciation with an empty body and an emoji reply. [source; call_dd927b6355484f369ad688e7b6375746]

<a id="usage-evaluation"></a>

## Sample MMLU questions and report pooled accuracy during evaluation

`-r` / `--random_sample` is an integer defaulting to `None`. For a truthy value, `main` saves `N = len(dataset_all)`, asserts the request is at most `N`, resets Python’s global RNG to seed 0, shuffles the sorted test list in place and slices it. For positive requests this draws distinct row positions without replacement. Choice permutation, if enabled, happens earlier and is not controlled by this seed. Development rows still supply preprompts and are not sampled. [source; call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219]

Subject selection and skipping establish eligibility before the shuffle, but are applied to test rows only after the slice. The per-subject cap is applied later still, at enqueue time. Thus the number sampled, the number of eligible rows used as `total_jobs`, the number enqueued, and the number scored can all differ. With a cap, which rows survive within each subject follows the shuffled order. [source; call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219]

The unchanged one-token jobs carry their test row as an identifier. For each EOS result, the evaluator compares logits for the four space-prefixed answer tokens and records argmax correctness and the correct choice’s four-way softmax probability. `print_results` scans for scored rows, so pooled accuracy is question-weighted; sample mode still computes the probability mean but does not print it. [source; call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24]

After each `iterate`, `tested` is `total_jobs` minus pending and active jobs. The generator removes completed jobs before returning results, and MMLU processes the entire EOS batch before checking whether to print. The threshold is a strict increase of more than `requested // 10` since the last report: nominally about tenths, not ten guaranteed reports. A request below ten prints on any increase; a final iteration that crosses the threshold can print the same aggregate again when the unconditional final call runs. [source; call_3a364d7ebfa14bfba7d4464fb9020c24, call_aa62d9a86ace43fd86edf33666049650, call_1233cd80535240e3b3b1549ae366b8c2, call_ebb5857ed6064cfbafd6d51c5fae6b55]

The printed width is `sqrt(p*(1-p)/t * (N-t)/(N-1))`, where `p` is scored accuracy and `t` is the number scored. `p*(1-p)` estimates the variance of binary correctness; dividing by `t` scales it for a mean. The finite-population factor reduces the width as the scored count approaches `N` and gives zero at a full census when `N > 1`. Under simple random sampling without replacement this is a plug-in standard-error expression, not a 95% interval. A two-sided normal approximation would use roughly 1.96 standard errors under suitable conditions; interim completion order and post-draw exclusions should not be presumed to preserve simple random sampling. [inference; call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219, call_1233cd80535240e3b3b1549ae366b8c2, call_292a5c9c041b416c9370eb08a08fd2a3, call_0b29c4b0b89143a1a1ad06a3b856be90]

In the scalar checks, a draw of three from six rows left two after filtering to one subject, or two with both subjects and a cap of one. With a request of 20 and one completion per iteration, interim reports fell at 3, 6, 9, 12, 15 and 18. For 50 correct out of 100 from a population of 1,000, the patch’s width was 4.74579 percentage points, versus 9.301748 for 1.96 times that width. Enumerating the six equally likely two-row draws from a four-row population with two correct answers gave coverage of only four out of six for the printed interval. [execution; call_292a5c9c041b416c9370eb08a08fd2a3, call_0b29c4b0b89143a1a1ad06a3b856be90]

## Authoring-time findings — pending review

### standard-error-labeled-95-percent-ci (suspected; defect)

The final-width label claims a confidence level not supplied by the calculation.

Trigger: Complete a positive requested sample with exactly that many rows scored and a population larger than one.

Expected: Label the width as an estimated standard error, or compute an interval with a method appropriate to the claimed confidence level and sampling design.

Actual: `print_results` appends `(95% CI)` whenever the scored count equals the request, but prints one plug-in standard error on either side, with no confidence multiplier or exact interval construction. All-correct or all-incorrect samples give zero width even when the sample is smaller than the population.

Locations: 2957e20cad48ba6c8768f6dc82a49ff786e84e76:eval/mmlu.py — main.print_results

Source evidence: call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24

scalar_transcription: Calculated the literal width and enumerated a binary population where the printed interval covers the true mean in four of six draws. [call_292a5c9c041b416c9370eb08a08fd2a3, call_0b29c4b0b89143a1a1ad06a3b856be90]. Limits: The counterexample assumes equally likely draws; it does not measure coverage on MMLU.

### sample-count-precedes-eligibility (suspected; behavior_change)

A request for a random sample of N questions is a draw size before filtering, not a guarantee of N evaluated questions.

Trigger: Request a positive sample with subject selection, subject skipping or a per-subject cap that removes at least one drawn row.

Expected: If the request represents the number to evaluate, draw from the eligible pool or reject or explain a smaller result.

Actual: Rows are discarded without replacement draws. The final report labels the observed count `all subjects` even when only selected subjects contributed, and the width still uses the unfiltered test split size.

Locations: 2957e20cad48ba6c8768f6dc82a49ff786e84e76:eval/mmlu.py — main

Source evidence: call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219

scalar_transcription: Drew three from six rows, then demonstrated two enqueued jobs under either a subject restriction or a cap. [call_292a5c9c041b416c9370eb08a08fd2a3]. Limits: Synthetic rows demonstrate the ordering, not which rows a real MMLU run would select.

### question-cap-inflates-progress-and-can-trigger-empty-report (suspected; defect)

The uncapped progress total now drives interim sample reports as well as the Testing bar.

Trigger: Use a cap that discards eligible rows. For the new interim failure, also enable sampling and have the omitted count exceed `requested // 10` on an iteration before any job produces an EOS result.

Expected: Base progress on enqueued jobs and defer scoring reports until at least one result has been scored.

Actual: The Questions bar’s declared total includes omitted jobs; Testing starts with an offset equal to the omitted count. If that offset alone crosses the reporting threshold, `print_results(None)` is called with zero scored rows and raises `ZeroDivisionError` at `correct / total`.

Locations: 415a55cc2d7f5ff01b7029f1ee6ed2ec53f47cb2:eval/mmlu.py — main, 2957e20cad48ba6c8768f6dc82a49ff786e84e76:eval/mmlu.py — main.print_results

Source evidence: call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24, call_aa62d9a86ace43fd86edf33666049650, call_17401b738c3e4e039cb0e54399a609f9

scalar_transcription: With three eligible jobs, two admitted and both outstanding at the first check, the modeled progress was one and the scored count was zero. The threshold fired and the modeled report rejected the zero denominator. [call_292a5c9c041b416c9370eb08a08fd2a3]. Limits: The no-completion iteration was modeled; no production prefill schedule or Rich display was exercised.

### sample-selection-can-reach-empty-final-report (suspected; defect)

The inherited empty-evaluation division now has additional ways to reach it.

Trigger: After successful initialization, skip every subject, use a negative per-subject cap, draw only excluded rows, or pass a negative sample size whose magnitude is at least the full row count.

Expected: Reject unsupported negative counts and report an empty evaluation without computing percentages.

Actual: The upper-bound assertion accepts negative sample sizes; negative slicing drops rows from the end, so `-1` keeps all but one and a sufficiently negative value keeps none. For these empty-admission cases the evaluation loop is skipped and the unconditional final `print_results(None)` divides by zero.

Locations: 2957e20cad48ba6c8768f6dc82a49ff786e84e76:eval/mmlu.py — main.print_results

Source evidence: call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24

scalar_transcription: A one-row draw containing only an excluded subject and a size of minus six over six test rows both left no jobs; the zero-count report raised `ZeroDivisionError` in the arithmetic model. [call_292a5c9c041b416c9370eb08a08fd2a3]. Limits: Assumes successful CLI initialization and uses synthetic dataset contents.

### singleton-sampling-population-divides-by-zero (suspected; defect)

A one-row census makes the new finite-population denominator zero.

Trigger: If the loaded test split contains exactly one row, sample one question and successfully score it.

Expected: Report the observed census accuracy without dividing by `N - 1`.

Actual: The request passes the upper-bound check, but the sample-mode width divides by `full_len - 1` after the first score, yielding `ZeroDivisionError`.

Locations: 2957e20cad48ba6c8768f6dc82a49ff786e84e76:eval/mmlu.py — main.print_results

Source evidence: call_3a364d7ebfa14bfba7d4464fb9020c24, call_156719dd75c042f894fef6710e878219

scalar_transcription: Evaluated the sampled width with one scored row and population size one. [call_292a5c9c041b416c9370eb08a08fd2a3]. Limits: This is a conditional input case, not a claim that the published MMLU test split is a singleton.

### fewshot-count-still-not-advanced (suspected; defect)

Sampling does not repair the inherited development-example count.

Trigger: Request one few-shot example and retain a subject with multiple development rows, in either report mode.

Expected: Append one demonstration for that subject.

Actual: `fewshots` stays at zero, so the preprompt includes every matching development row. A zero request still stops before the first demonstration.

Locations: 2957e20cad48ba6c8768f6dc82a49ff786e84e76:eval/mmlu.py — main

Source evidence: call_156719dd75c042f894fef6710e878219, call_3a364d7ebfa14bfba7d4464fb9020c24

scalar_transcription: The unchanged loop kept all three synthetic matching rows when asked for one or two, and none when asked for zero. [call_0b29c4b0b89143a1a1ad06a3b856be90]. Limits: No real prompts were tokenized or scored.

## Uncertainty and limits

The bounded Python checks transcribed selection, reporting arithmetic and completion counts over synthetic inputs. They did not execute the repository evaluator or establish actual dataset size or composition, tokenizer compatibility, model scores, GPU scheduling, or terminal rendering.

The sample seed fixes the shuffle for the same ordered input and RNG implementation; it does not pin the dataset revision or seed the earlier answer-choice shuffle. Cross-environment reproducibility was not tested.

Literal parent-tree searches cannot rule out external callers or dynamically constructed references.
