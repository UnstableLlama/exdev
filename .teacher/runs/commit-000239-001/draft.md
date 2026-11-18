# db65151b07e7085ed47cafe890aa0dadb985eb5a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/db65151b07e7085ed47cafe890aa0dadb985eb5a) · [Evidence ledger](draft.json)

Makes comparison backend imports optional, but leaves Transformers storage accounting incompatible with missing-class None sentinels.

- [Optional comparison-backend imports](#usage-evaluation)

## Problem

compare_q imports its adapters before selecting a backend, so an unused backend's missing package could prevent startup, including through compare_q_logits. [source; call_55a0345483f7414d85f2ff4314871196, call_cc6c93ed71b14b9ab0a2fee0dccceb95, call_948dd4cae06a45ceaba146e7098c4d20]

## Reasoning

The change catches ModuleNotFoundError around backend-specific imports rather than changing dispatch. This defers dependency requirements, but the Transformers adapter's None fallbacks are incompatible with its unchanged isinstance checks. [source; call_948dd4cae06a45ceaba146e7098c4d20, call_642bfe834eb74211a7e30f8020e0cad2, call_4c2a3110385b43de95b4d0d9eb31a792, call_191f6bf70b5546be9364686f4a4c3efa, call_b88e36ad155041d5b1e0e5f2bb4d2681]

## Impact

Missing AnyPrecision and ExLlamaV2 packages no longer necessarily block unrelated adapter imports. This is not full dependency independence: Torch and Transformers remain unconditional imports, and compare_q itself still imports ExLlamaV3 utilities. [source; call_948dd4cae06a45ceaba146e7098c4d20, call_642bfe834eb74211a7e30f8020e0cad2, call_191f6bf70b5546be9364686f4a4c3efa, call_55a0345483f7414d85f2ff4314871196]

## Source Notes

The AnyPrecision introduction entry records its unconditional-import requirement; the root usage-evaluation chapter establishes the shared adapter and storage-accounting design. [ancestor; call_544d3ea2b3b845ac92938b9c7299cd9d, call_3ea84a6ef3864d9a9d2280a8ef81ed03]

The recorded AnyPrecision import-time issue is removed for ModuleNotFoundError by the new catch. Selecting that unavailable backend still reaches the unchanged loader, which references AnyPrecisionForCausalLM without an availability check. [source; call_948dd4cae06a45ceaba146e7098c4d20, call_9d1d094602fb4782884b68e7df075c63, call_55a0345483f7414d85f2ff4314871196]

PR #26, “Superior 3INST parameters,” proposes codebook parameter changes. Its relevance is only inferred from the catalog's shared compare_q.py path; the inspected opening does not establish motivation for this import change. [inference; call_c533d59b39b34b2b825bbee299d44613, call_55a0345483f7414d85f2ff4314871196]

<a id="usage-evaluation"></a>

## Optional comparison-backend imports

AnyPrecision, ExLlamaV2 and ExLlamaV3 imports become try/except blocks with pass on ModuleNotFoundError. Function definitions remain available to the runner's dispatch tables, but absent class bindings are not replaced by working implementations. Their loaders still directly reference the imported classes. [source; call_948dd4cae06a45ceaba146e7098c4d20, call_642bfe834eb74211a7e30f8020e0cad2, call_4c2a3110385b43de95b4d0d9eb31a792, call_9d1d094602fb4782884b68e7df075c63, call_f31aa6f13af2420d9661d3db85dd93ed, call_608c9ac14fe140f2b27bd1c3fd2534c9]

Transformers quantization integrations are isolated into separate guarded groups for GPTQModel, AQLM, AWQ, VPTQ and bitsandbytes. Any failed GPTQModel import resets all three GPTQ class names to None. Other groups each reset their own class name. The unused AutoModelForCausalLM import is removed from the AnyPrecision adapter, not from the Transformers adapter. [source; call_191f6bf70b5546be9364686f4a4c3efa, call_948dd4cae06a45ceaba146e7098c4d20, call_9d1d094602fb4782884b68e7df075c63]

Successful import is only the first boundary: test_ppl selects a loader, and load_transformers computes storage information immediately after loading. Its first module test uses Linear4bit as an isinstance type without filtering None. Later checks likewise consume the optional AQLM, VPTQ, AWQ and GPTQ class names unchanged. [source; call_55a0345483f7414d85f2ff4314871196, call_b88e36ad155041d5b1e0e5f2bb4d2681, call_191f6bf70b5546be9364686f4a4c3efa]

A bounded standard-library transcription of the isinstance generator expression raised TypeError for a None bitsandbytes class and for a None AQLM class. It did not load a model or execute the repository adapter. [execution; call_39fb30ef6f8b4136a76e462ab55bc842]

## Authoring-time findings — pending review

### optional-class-sentinels (suspected; defect)

Optional quantization-class imports become None, but storage accounting still passes those values to isinstance.

Trigger: Load a Transformers model successfully with bitsandbytes unavailable, then enumerate at least one module in get_storage_info. Other missing optional classes can fail when their later branches are reached.

Expected: An unused unavailable quantization backend should be skipped while accounting for the selected model.

Actual: The first check evaluates isinstance(module, None) when Linear4bit is None and raises TypeError before storage metadata is returned.

Locations: db65151b07e7085ed47cafe890aa0dadb985eb5a:eval/compare_q_transformers.py — get_storage_info

Source evidence: call_191f6bf70b5546be9364686f4a4c3efa, call_b88e36ad155041d5b1e0e5f2bb4d2681, call_43bd75127d534275af2217c9bc5983c3, call_55a0345483f7414d85f2ff4314871196

source_inspection: Whole-parent-tree caller search and source inspection identify load_transformers as the local direct caller. Both auto wrappers delegate to it; compare_q dispatches all three loaders from test_ppl. The diff adds no sentinel filtering. [call_43bd75127d534275af2217c9bc5983c3, call_b88e36ad155041d5b1e0e5f2bb4d2681, call_55a0345483f7414d85f2ff4314871196, call_191f6bf70b5546be9364686f4a4c3efa]. Limits: Reach requires model loading and storage accounting to occur; cached results or other earlier failures can avoid this path.

scalar_transcription: Executed the inspected isinstance/any expression with None class sentinels and observed TypeError. [call_39fb30ef6f8b4136a76e462ab55bc842]. Limits: Standard-library reproduction, not repository or GPU execution.

## Uncertainty and limits

No installed-backend import, model loading, GPU inference or end-to-end comparison was executed. The Python check models only the changed sentinel/type-check interaction.

Only the opening of PR #26 was inspected; no task-specific discussion provenance is established.

The catches handle ModuleNotFoundError, including missing transitive modules, but do not establish recovery from other import or native-library failures.
