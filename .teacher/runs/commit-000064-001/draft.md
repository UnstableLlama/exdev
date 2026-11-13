# 25d9388bce25b89c48a4a078bc6fc8365c661692


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/25d9388bce25b89c48a4a078bc6fc8365c661692) · [Evidence ledger](draft.json)

Adds --keep_b to reset A's activations to B's over a module prefix, allowing suffix divergence comparison without skipping prefix execution.

- [Start divergence comparison after a B-state prefix](#usage-evaluation)

## Problem

The existing model-difference diagnostic propagates independent A and B states, so later differences include divergence accumulated through earlier modules. [source; call_78f8168671b1492690b19f4818e9a15d]

## Reasoning

Replacing A's state with B's output over a configurable prefix allows subsequent comparison to begin from B's activations rather than A's accumulated prefix error. [inference; call_e90e9e56cee24d0c8f00be2856e43095, call_78f8168671b1492690b19f4818e9a15d]

## Impact

The default preserves the previous comparison. A positive keep_b changes both the state propagated into later modules and the reported prefix errors; it does not skip prefix computation. [source; call_e90e9e56cee24d0c8f00be2856e43095, call_78f8168671b1492690b19f4818e9a15d]

## Source Notes

The earlier entry describes model_diff.py as an accumulated layerwise-divergence diagnostic rather than a language-quality score. [ancestor; call_756f77ffb2f5453bab619962783ef1e8]

<a id="usage-evaluation"></a>

## Start divergence comparison after a B-state prefix

The parser adds -kb/--keep_b as an integer with default 0 and help text 'Maintain B state for number of modules'. For each zero-based module index, main first runs and unloads both modules, then assigns state_a = state_b.clone() when idx < args.keep_b. [source; call_e90e9e56cee24d0c8f00be2856e43095, call_78f8168671b1492690b19f4818e9a15d]

For keep_b=k>0, the first k paired module outputs are replaced before error calculation. With finite values and nonzero B row norms, their reported errors therefore become zero. At index k, both branches start from B's preceding output; afterward they again evolve independently, accumulating suffix divergence rather than isolating every remaining module. [source; call_e90e9e56cee24d0c8f00be2856e43095, call_78f8168671b1492690b19f4818e9a15d]

The comparison still loads and forwards both prefix branches and prints every paired module. This offers an activation-reset boundary, not a runtime shortcut or checkpoint resume. Negative values perform no replacement; values covering the entire zipped list leave no unreset suffix to compare. [source; call_e90e9e56cee24d0c8f00be2856e43095, call_78f8168671b1492690b19f4818e9a15d]

A four-step scalar transcription using A(x)=2x+1 and B(x)=2x confirmed the boundary behavior: keep_b=2 produced relative differences [0, 0, 0.125, 0.1875]; keep_b=0 and -1 matched, while 4 and 5 reset every step. This executed a standard-library model of the branch, not repository inference code. [execution; call_294320aaf8de4900b61fbe760bb09fb0, call_e90e9e56cee24d0c8f00be2856e43095]

## Uncertainty and limits

No model, Torch operation, or CUDA kernel was executed. The scalar check models only replacement timing and subsequent divergence, not tensor devices, allocation, precision, or nonfinite values.

The option counts entries in zipped top-level module lists, not necessarily decoder-layer numbers. Model-list compatibility remains unchecked by this script.
