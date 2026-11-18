# 415a55cc2d7f5ff01b7029f1ee6ed2ec53f47cb2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/415a55cc2d7f5ff01b7029f1ee6ed2ec53f47cb2) · [Evidence ledger](draft.json)

MMLU now reports accuracy and four-choice confidence as each subject finishes, with flags to skip subjects and cap test questions. The cap is not reflected in progress totals, empty selections can divide by zero, and the inherited few-shot count defect remains.

- [Report MMLU results as subjects finish](#usage-evaluation)

## Problem

The MMLU evaluator showed progress bars but reported accuracy and confidence only after the entire run. Subject selection was available, but there was no way to skip the first N selected subjects or cap the number of questions per subject. [source; call_bb51b69855654726afae566258979650, call_50169d8729ee4d789221b18a02321e30]

## Reasoning

Per-subject counters serve two purposes in separate phases. During enqueueing, each counter records how many questions have been admitted and gates the cap. Once enqueueing is complete, the same counter records how many admitted questions still need to be scored. Reaching zero after scoring triggers the subject report. [source; call_50169d8729ee4d789221b18a02321e30]

Reusing one reporting helper for subject and aggregate results keeps the metric definitions consistent. It rescans the test rows on each report rather than maintaining separate running totals, trading extra row scans for simpler bookkeeping. [source; call_50169d8729ee4d789221b18a02321e30]

## Impact

The CLI now prints a result as each evaluated subject finishes, then prints a final `all` row. The default flags preserve question selection. A positive cap changes the evaluated sample, so the resulting aggregate describes the scored subset rather than the full selected test set. [source; call_50169d8729ee4d789221b18a02321e30, call_bb51b69855654726afae566258979650]

## Source Notes

The introducing entry, “Add MMLU eval,” describes the inherited one-token logit scoring and records the missing few-shot counter increment. [ancestor; call_c9dcb080caed4f3fafe52e90dc6303ff]

The missing increment carries over: the parent loop starts `fewshots` at zero and never updates it, and this patch does not change that loop. The new question cap is applied later, to test jobs rather than development demonstrations. [source; call_bb51b69855654726afae566258979650, call_50169d8729ee4d789221b18a02321e30]

The whole-parent searches for `mmlu` and `main(` found the evaluator's own `__main__` block as its only identifiable in-tree direct caller. That block parses both new attributes before invoking `main`. An external caller that supplies an old-style argument object without `skip_subjects` would fail at the new slice; one lacking `max_q_per_subject` would fail when a selected test row is encountered. [source; call_f72de34b2a17456d92d686d901b26ae9, call_92592cdc51864363ae3148becef75370, call_bb51b69855654726afae566258979650, call_50169d8729ee4d789221b18a02321e30]

Closed issue #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” reports NaNs during quantization and a Cholesky failure; the reporter later said a retry succeeded without warnings. [source; call_e48ed23bd9ae4d0ea725aaf7e19373f4]

The discussion's evaluation references are to prequant evaluation and the separate `eval/model_diff.py` and `eval/compare_q.py` scripts. That explains the shared evaluation terminology, but the traceback is in conversion and the patch changes only `eval/mmlu.py`; the discussion does not establish a link to the new MMLU output. [inference; call_e48ed23bd9ae4d0ea725aaf7e19373f4, call_50169d8729ee4d789221b18a02321e30]

<a id="usage-evaluation"></a>

## Report MMLU results as subjects finish

`-skip` / `--skip_subjects` defaults to zero. It slices the lexicographically sorted set of valid, selected subject names before choice shuffling and preprompt construction. The slice determines membership, not reporting order: it is converted back to a set, and reports follow completion events. Negative values use ordinary slice semantics, so `-1` retains only the last selected subject. [source; call_50169d8729ee4d789221b18a02321e30, call_bb51b69855654726afae566258979650]

`-mqps` / `--max_q_per_subject` defaults to `None`; zero also disables it because the check uses truthiness. A positive cap admits the first N rows for each retained subject in test traversal order. The test list is sorted by subject, preserving order within a subject; `--shuffle` permutes choices within rows, not question order. The cap is therefore a prefix selection, not a random sample. [source; call_50169d8729ee4d789221b18a02321e30, call_bb51b69855654726afae566258979650]

A job carries its test row as the identifier and asks for one token's logits. On an EOS result, the evaluator compares the logits for the four space-prefixed A–D tokens, stores argmax correctness and the correct choice's probability under a four-way softmax, and then decrements the subject counter. Only already-scored rows enter the report. The final `all` line is question-weighted, not a mean of subject percentages, and confidence is conditional on the four answer choices. [source; call_bb51b69855654726afae566258979650, call_50169d8729ee4d789221b18a02321e30]

In a bounded scalar transcription with three `a` rows and two `b` rows, cap 1 admitted one job per subject but left the progress total at five. Feeding synthetic completions in reverse order produced `b` then `a` reports. Skipping both subjects or setting cap −1 admitted no jobs and reproduced the aggregate's zero-denominator error. [execution; call_f677525db49f4037acad961283590e0d]

## Authoring-time findings — pending review

### progress-count-ignores-question-cap (suspected; defect)

The progress bars use the count before capping instead of the number of jobs actually admitted.

Trigger: Run the MMLU CLI with a positive `--max_q_per_subject` below the available question count for any retained subject.

Expected: The Questions and Testing bars count only admitted jobs, with Testing completed work equal to admitted jobs minus outstanding jobs.

Actual: Questions updates stop short of the declared total before context exit forces completion. Testing reports `uncapped_total - outstanding_jobs`, overstating completed work by the number of omitted questions. The final score uses scored rows instead and does not use this inflated total.

Locations: 415a55cc2d7f5ff01b7029f1ee6ed2ec53f47cb2:eval/mmlu.py — main

Source evidence: call_50169d8729ee4d789221b18a02321e30, call_bb51b69855654726afae566258979650, call_43c22bdf2a384b5dab7c765dc254bfbd, call_891b9dbeb13d4209ae913ab929468b7e, call_f72de34b2a17456d92d686d901b26ae9, call_92592cdc51864363ae3148becef75370

source_inspection: Compared the pre-cap count, queue admission, pending-plus-active count, and progress wrapper. The in-tree MMLU CLI calls this function directly. [call_50169d8729ee4d789221b18a02321e30, call_43c22bdf2a384b5dab7c765dc254bfbd, call_891b9dbeb13d4209ae913ab929468b7e]. Limits: The Rich terminal display was not exercised.

scalar_transcription: Cap 1 admitted two synthetic jobs against a progress total of five, confirming a three-job offset. [call_f677525db49f4037acad961283590e0d]. Limits: Models counts only; does not run the generator or progress wrapper.

### empty-evaluation-divides-by-zero (suspected; defect)

The inherited unguarded aggregate denominator is reachable through the new selection flags.

Trigger: After successful model and dataset initialization, pass `--skip_subjects` at least as large as the number of selected subjects, or pass `--max_q_per_subject -1` with a nonempty selection.

Expected: Reject an invalid limit or report that no questions were evaluated without computing percentages.

Actual: Skipping all subjects removes every eligible row. A negative cap is truthy and rejects each row because its subject counter starts at zero. With no jobs scored, the unconditional `print_results(None)` divides by zero and emits no aggregate row. The CLI directly invokes `main`; no other in-tree direct caller was identified.

Locations: 415a55cc2d7f5ff01b7029f1ee6ed2ec53f47cb2:eval/mmlu.py — main.print_results

Source evidence: call_50169d8729ee4d789221b18a02321e30, call_bb51b69855654726afae566258979650, call_f72de34b2a17456d92d686d901b26ae9, call_92592cdc51864363ae3148becef75370

source_inspection: Traced integer parsing, empty admission, the skipped scoring loop, and the unconditional aggregate report. [call_50169d8729ee4d789221b18a02321e30]. Limits: Assumes initialization and dataset loading succeed.

scalar_transcription: Both an exhausted subject slice and a negative cap produced zero jobs and a `ZeroDivisionError` in the modeled percentage calculation. [call_f677525db49f4037acad961283590e0d]. Limits: Does not run the CLI or model initialization.

### fewshot-counter-still-not-advanced (suspected; defect)

The previously recorded few-shot count defect remains in the preprompt builder.

Trigger: Use the MMLU CLI with `--fewshot_examples 1` and retain a subject with more than one development example.

Expected: Include one development demonstration in that subject's preprompt.

Actual: The counter stays at zero, so every matching development row is included for any positive requested count. Zero still stops before any demonstration is appended. The CLI reaches this loop before applying the new test-question cap.

Locations: 415a55cc2d7f5ff01b7029f1ee6ed2ec53f47cb2:eval/mmlu.py — main

Source evidence: call_bb51b69855654726afae566258979650, call_50169d8729ee4d789221b18a02321e30, call_f72de34b2a17456d92d686d901b26ae9, call_92592cdc51864363ae3148becef75370

source_inspection: Checked the parent's break condition and prompt append against the patch; neither the counter nor the loop is changed. The only identifiable direct caller is the script entry point. [call_bb51b69855654726afae566258979650, call_50169d8729ee4d789221b18a02321e30, call_f72de34b2a17456d92d686d901b26ae9, call_92592cdc51864363ae3148becef75370]. Limits: Does not establish actual demonstration counts for a particular dataset revision.

scalar_transcription: A request for one demonstration admitted all five synthetic same-subject rows. [call_f677525db49f4037acad961283590e0d]. Limits: No prompt tokenization or scoring was performed.

## Uncertainty and limits

No MMLU dataset download, tokenizer check, model inference, GPU execution, terminal rendering, or benchmark-score measurement was performed. The bounded Python checks used synthetic rows and completion events, not repository execution.

Literal caller searches cannot rule out dynamic imports or external callers.
