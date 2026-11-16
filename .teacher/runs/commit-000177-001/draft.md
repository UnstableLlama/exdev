# 8b0df6910382b84fd9225353c2eb4cd2708482fb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8b0df6910382b84fd9225353c2eb4cd2708482fb) · [Evidence ledger](draft.json)

Adds per-step RNG requirements so ordinary sampling avoids global reseeding, while explicitly seeded multinomial validation retains it. Performance and GPU equivalence were not measured.

- [Initialize global RNGs only for requesting sampling steps](#sampling)

## Problem

CustomSampler previously reset both Torch and Python RNGs whenever rand_u32 was supplied, even though ordinary Gumbel sampling passes that value directly to native noise kernels. [source; call_f1748c862a114512bfc56912ba3f267d, call_89926da9606046c4a7c181905664aaee, call_6d3137a78b184765807be9c78c959c38]

## Reasoning

The change distinguishes steps needing global RNG initialization from steps consuming an explicit seed. Avoiding unnecessary initialization is consistent with the commit message; a speed improvement has not been measured. [inference; call_f1748c862a114512bfc56912ba3f267d, call_6d3137a78b184765807be9c78c959c38]

## Impact

Job.receive_logits supplies a per-job random integer positionally on each sampling call. Built-in presets therefore stop resetting global RNGs through this path, while custom chains containing SS_Sample_mn retain explicit-seed initialization. [source; call_8ac566e194ce47ef9efb58af1e766389, call_dd14e171b770416992cfca2424dbe68f, call_f1748c862a114512bfc56912ba3f267d]

## Source Notes

The root sampling entry was read. It establishes the composable-step design and explicit-seed native Gumbel path, and records a sorted-argmax defect. [ancestor; call_09a9b4edb8c4454986d68cd2fe6a8263]

<a id="sampling"></a>

## Initialize global RNGs only for requesting sampling steps

Sampler.__init__ now initializes reqs_torch_seed to False. SS_Base supplies a same-named capability method returning False, and SS_Sample_mn overrides it to True. CustomSampler calls the base constructor before OR-aggregating step requirements, so the base-class edit supplies the accumulator required by the constructor edit. [source; call_dc679b65d5f44b5eb311d284ab680b61, call_f1748c862a114512bfc56912ba3f267d, call_89926da9606046c4a7c181905664aaee]

Requirements are collected from the original supplied steps, before alternative substitution and prerequisite insertion. Existing alternatives are no-ops and existing prerequisites are normalization or sorting, so none introduces an unreported RNG requirement. External steps using global randomness must override the new capability method. [source; call_f1748c862a114512bfc56912ba3f267d, call_89926da9606046c4a7c181905664aaee, call_bbd541d89c6740dc955624fa8a9dd068]

SS_Sample uses the supplied integer in all three native Gumbel-noise variants; their kernels initialize Philox from that integer and the element index. SS_Sample_mn instead calls torch.multinomial without an explicit generator and accepts only normalized probability states, requesting normalization during preparation. This explains why the latter opts into global initialization while the former does not. [source; call_89926da9606046c4a7c181905664aaee, call_6d3137a78b184765807be9c78c959c38, call_f1748c862a114512bfc56912ba3f267d]

An explicit rand_u32, including zero, now resets Torch and Python only when the aggregate flag is true. An omitted value still draws from Python's RNG over the inclusive unsigned-32-bit range 0 through 2^32−1 and does not enter the reseeding branch, even for multinomial sampling. The flag gates both seed calls despite its Torch-specific name. [source; call_f1748c862a114512bfc56912ba3f267d, call_89926da9606046c4a7c181905664aaee]

All six preset classes build chains from existing steps and inherit CustomSampler initialization; none uses SS_Sample_mn. The custom test chains using SS_Sample_mn inherit its new opt-in and pass rand_u32=0. The top-k-only custom test inherits False. No pre-existing reqs_torch_seed definition or consumer was found. [source; call_a6645ee16cab4c8f8d2318cc323c360c, call_dd14e171b770416992cfca2424dbe68f, call_3c78c8431155489c926c160049cd6d33, call_06d57a734166406b84043fe5ea91932b]

A four-case standard-library transcription verified the branch distinction: explicit zero with the flag false left Python RNG state unchanged; with the flag true it reset that state and recorded one Torch-seed call. Omitted seeds advanced Python state and recorded no Torch-seed call for either flag value. [execution; call_9d8c2604e81a402285ad40ee2cea106a]

The change reduces global RNG side effects rather than replacing the sampling algorithm. Consequently, code interleaving explicitly seeded ordinary sampling with other Python-random operations can observe a different subsequent random sequence. [inference; call_f1748c862a114512bfc56912ba3f267d, call_9d8c2604e81a402285ad40ee2cea106a]

## Authoring-time findings — pending review

### inherited-sorted-argmax (suspected; defect)

The sorted-argmax defect recorded by the ancestor remains unchanged; conditional reseeding does not repair it.

Trigger: A custom chain reaches SS_Argmax.run with sorted logits or probabilities, for example SS_Sort followed by SS_Argmax.

Expected: Map the selected sorted position back to a token ID and store it in state.sample.

Actual: The sorted branches assign to state.state rather than state.sample and then overwrite state.state with DONE. If indexing succeeds, ordinary forward subsequently attempts state.sample.view while sample remains None; indexing also lacks the row-wise mapping used by SS_Sample.

Locations: 8b0df6910382b84fd9225353c2eb4cd2708482fb:exllamav3/generator/sampler/custom.py — SS_Argmax.run

Source evidence: call_89926da9606046c4a7c181905664aaee, call_f1748c862a114512bfc56912ba3f267d, call_124711739a354705800c8a3250a90319, call_dd14e171b770416992cfca2424dbe68f

source_inspection: Compared the parent implementation with the complete task diff and searched the whole parent tree for SS_Argmax uses. Its direct invocation is through CustomSampler's step loop. Inspected preset constructions do not place sorting before argmax, so this observation concerns custom sorted-argmax composition, not every greedy workflow. [call_89926da9606046c4a7c181905664aaee, call_f1748c862a114512bfc56912ba3f267d, call_124711739a354705800c8a3250a90319, call_dd14e171b770416992cfca2424dbe68f]. Limits: No tensor execution was performed; the precise first failure depends on the indices and tensor dimensions.

## Uncertainty and limits

No PyTorch, CUDA, repository test suite or end-to-end generation was executed; timing and token-level equivalence remain unmeasured.

The scalar check executes a transcription of the seed branch with a Torch-call recorder, not CustomSampler or torch.manual_seed.

Whole-tree literal searches cover repository definitions and uses, not external subclasses or dynamically constructed sampling steps.
