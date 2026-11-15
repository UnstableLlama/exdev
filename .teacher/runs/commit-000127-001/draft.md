# 9575f7d8b2afce94122bcf6141a63bfc01f207f2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9575f7d8b2afce94122bcf6141a63bfc01f207f2) · [Evidence ledger](draft.json)

Adds final-logit perplexity, top-K label accuracy, ordered agreement and bidirectional KL diagnostics to model_diff.py, with a suspected vocabulary-versus-sequence bound error in perplexity accumulation.

- [Final-logit quality and agreement diagnostics](#usage-evaluation)

## Problem

The model comparison script reported intermediate activation differences but lacked final-output perplexity, top-K accuracy/agreement and distribution-divergence metrics. [source; call_720aa966d66b46c09d89e9b19fb93456, call_1f069327b60e4cc0aad5426bfaba02a0]

## Reasoning

Reusing the final states adds complementary diagnostics: next-token likelihood, label ranking, exact ranked-list agreement and bidirectional KL calculations, without another model forward pass. [source; call_1f069327b60e4cc0aad5426bfaba02a0]

## Impact

The script now prints both models’ perplexities, label inclusion and agreement for K=1 through --topk_max (default 5), and two KL values. It also releases the last per-module comparison temporaries with del sa, sb. [source; call_1f069327b60e4cc0aad5426bfaba02a0]

## Source Notes

PR #26, “Superior 3INST parameters,” proposes decoder-parameter changes and discusses additional quality evaluation. louiehelm asks for KLD evaluation; turboderp identifies eval/model_diff.py as a suitable starting point and subsequently promises a quick KLD test. [source; call_1167c78e85574681abeb2f48222b9a4e, call_3b6f7a7849f44a59bb2259cd06b12b3b]

That discussion is plausibly related to this change because it explicitly names the changed script and requests the added metric; it does not establish an upstream commit-to-PR link or validate the proposed decoder improvements. [inference; call_1167c78e85574681abeb2f48222b9a4e, call_1f069327b60e4cc0aad5426bfaba02a0]

<a id="usage-evaluation"></a>

## Final-logit quality and agreement diagnostics

The existing pipeline tokenizes WikiText-2 test text using model A’s tokenizer into 2048-token windows with stride 512, then propagates paired states through zipped module lists. The new metrics consume those final states rather than independently generating text. [source; call_720aa966d66b46c09d89e9b19fb93456, call_1f069327b60e4cc0aad5426bfaba02a0]

Perplexity and label inclusion omit the final logit position and compare each preceding position with the following input token. The helper gathers target log-softmax values, accumulates their sum and count, and reports exp(-sum/count). Its chunk-size expression simplifies to 10240 for a positive vocabulary dimension. [source; call_1f069327b60e4cc0aad5426bfaba02a0]

Top-K label inclusion checks whether any of the first K predicted IDs equals the target. Agreement instead requires every corresponding rank to match: it is ordered-list equality, not set overlap. A scalar example with [2,1] versus [1,2] confirmed that identical top-two sets fail this ordered test. [execution; call_1f069327b60e4cc0aad5426bfaba02a0, call_77d5a97c5d9e4724825f5dd54e82f577]

The KL branch converts complete row logits to float, softmaxes both models, and calls F.kl_div(log(probs_a + 1e-10), probs_b), then swaps the operands. It sums over vocabulary, averages over positions and finally averages rows. Unlike the label metrics, this includes the final position. The epsilon offsets probabilities before logarithms; the separate addition of 1e-10 to all logits in the perplexity helper is mathematically a common shift, not probability smoothing. [source; call_1f069327b60e4cc0aad5426bfaba02a0]

The earlier keep_b entry explains that a configurable prefix replaces A’s activations with B’s after both branches have computed their outputs. [ancestor; call_c04d786f8c2e49dba6bb6bc69e602e67]

That replacement remains upstream of the new metrics. Consequently, with positive keep_b, the reported A metrics describe the modified activation path, not necessarily an independent full-model-A evaluation. The default zero leaves both paths independent. [source; call_720aa966d66b46c09d89e9b19fb93456, call_1f069327b60e4cc0aad5426bfaba02a0]

## Authoring-time findings — pending review

### ppl-vocabulary-bound (suspected; defect)

The new perplexity helper uses vocabulary size as the bound while slicing the sequence axis.

Trigger: The number of prediction positions exceeds vocabulary size; larger vocabularies instead produce unnecessary trailing empty slices.

Expected: Accumulate every next-token prediction exactly once by iterating over logits_.shape[0].

Actual: The loop stops at logits_.shape[1]. For 2047 prediction positions and vocabulary size 1024, its bounds cover only 1024 targets.

Locations: 9575f7d8b2afce94122bcf6141a63bfc01f207f2:eval/model_diff.py — main.ppl

Source evidence: call_1f069327b60e4cc0aad5426bfaba02a0

source_inspection: The diff shows logits shaped by selecting one row and removing the final sequence position, then ppl slicing axis zero while bounding on axis one. Its only direct call in the diff is main’s per-model loop. Whole-parent-tree searches found no model_diff references and no pre-existing caller of this new nested helper; the inspected script directly invokes main from its CLI guard. [call_1f069327b60e4cc0aad5426bfaba02a0, call_720aa966d66b46c09d89e9b19fb93456, call_3c44f91fc66d4090a5c92b3ecd31e431, call_cfc9d1fa954e4b45afa2a962c1daa5fa]. Limits: Text searches do not establish external or dynamic callers.

scalar_transcription: A standard-library bounds model counted 1024 of 2047 positions for vocabulary 1024; vocabulary 32000 covered all 2047 positions but required four iterations. [call_77d5a97c5d9e4724825f5dd54e82f577]. Limits: This models slicing bounds only; it does not execute the repository helper or establish Torch behavior on empty tensors.

## Uncertainty and limits

No Torch, model inference or GPU execution was performed. The bounded Python check models indexing and ranking only, not tensor-library handling of empty slices or floating-point behavior.

The script assumes corresponding model modules and compatible token vocabularies; the inspected code does not validate those assumptions.

Runtime memory cost, numerical stability and metric values on actual models remain unmeasured.
