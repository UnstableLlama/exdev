# 151edc00b202b645fcfa2cc2c679d7ef381916fb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/151edc00b202b645fcfa2cc2c679d7ef381916fb) · [Evidence ledger](draft.json)

Moves architecture registration metadata onto config and model classes while preserving the eight registry mappings; the mismatch diagnostic retains an undefined variable.

- [Class-owned architecture metadata](#models)

## Problem

Architecture identifiers and config/model associations were duplicated between the central registry and individual configuration constructors. [source; call_3ba7866e756041489a361480d6fa41ed]

## Reasoning

The change makes each configuration class declare arch_string and each model class declare config_class. The registry derives its existing three-field records from those attributes, retaining an explicit list of supported models. [source; call_3ba7866e756041489a361480d6fa41ed]

This reduces repeated registration metadata without introducing automatic discovery. The tradeoff is that registration now depends on correct class attributes rather than independently written registry entries. [inference; call_3ba7866e756041489a361480d6fa41ed]

## Impact

A standard-library comparison of the parent registry with a symbolic transcription of the new definitions found the same eight architecture/config/model associations. [execution; call_32dbb877939a4f71ac7578d9c4b3c36a]

The normal Config.from_directory interface remains unchanged. Direct subclasses of Config must adapt to the removed expect_arch positional parameter; constructor arch_string keyword overrides no longer determine architecture validation. [source; call_ffd8f68f39794e96a22fbae7c6d4b0e8, call_3ba7866e756041489a361480d6fa41ed, call_f8d7863f37414d09b1b8b7589c31b4e6]

## Source Notes

PR #4, “chore: update config.py,” proposes only “containg -> containing.” Its relationship to this change is inferred solely from the shared filename; the task does not make that correction. [inference; call_c2666d88a56648eb851c0449f6c8bf8c, call_ffd8f68f39794e96a22fbae7c6d4b0e8, call_3ba7866e756041489a361480d6fa41ed]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” includes config.py's RopeSettings import in its traceback and reports a compiler/environment workaround. The inferred overlap is that unchanged import line, not the architecture-validation logic. [inference; call_db2a95295c4049d6af9131a5af11c78b, call_ffd8f68f39794e96a22fbae7c6d4b0e8, call_3ba7866e756041489a361480d6fa41ed]

Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns quantization regularization. Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” concerns native compilation. Neither discussion establishes a connection to this metadata refactor. [inference; call_229231c0877f4b7992ed38af8bb50b26, call_37baa277d73b4da08d0b3b17eafe1206, call_3ba7866e756041489a361480d6fa41ed]

<a id="models"></a>

## Class-owned architecture metadata

ARCHITECTURES keeps the keys LlamaForCausalLM, MistralForCausalLM, Qwen2ForCausalLM, Phi3ForCausalLM, Gemma2ForCausalLM, DeciLMForCausalLM, Glm4ForCausalLM and CohereForCausalLM. Each record still exposes architecture, config_class and model_class; the comprehension now obtains all three through the listed model class. [source; call_3ba7866e756041489a361480d6fa41ed]

Config.from_directory reads config.json, requires one supported architectures entry, looks up its config_class and invokes that class with directory and kwargs. Config.__init__ then reads the file again and compares its architecture with self.arch_string instead of a constructor argument. Registry selection and validation therefore share the configuration class's declaration. [source; call_ffd8f68f39794e96a22fbae7c6d4b0e8, call_3ba7866e756041489a361480d6fa41ed]

MistralConfig and Qwen2Config still inherit LlamaConfig. Their class-level arch_string overrides replace the explicit keyword forwarded through the Llama constructor. The inherited constructor continues passing LlamaModel as the instance's model_class; adding model-class config_class attributes does not change that existing data flow. [source; call_0262c21d7c7641399c7400951435af63, call_3ba7866e756041489a361480d6fa41ed]

gemma.py is renamed gemma2.py and the registry import follows the rename. The parent-tree literal search for .gemma found only that registry import. The diff provides no compatibility module at the old path. [source; call_5891990f531c4b4492cad94d7305ab83, call_3ba7866e756041489a361480d6fa41ed]

The inspected configs for TinyLlama/TinyLlama-1.1B-Chat-v1.0, mistralai/Mistral-7B-v0.1, Qwen/Qwen2.5-0.5B, microsoft/Phi-3-mini-4k-instruct and unsloth/gemma-2-2b respectively match the retained Llama, Mistral, Qwen2, Phi3 and Gemma2 architecture strings. This checks dispatch identifiers, not dimensions or defaults. [source; call_30192523db9b4551854d885949ba7aa5, call_743c4c9691844e50be87282d8685a031, call_a47d9b88cad64279bea6d0952b164e52, call_0f32cfeb0b554e1d89a2e80c0f9b71d1, call_60cc52624f5040e1a4ecabf0888fbd0a, call_3ba7866e756041489a361480d6fa41ed]

Each inspected CohereLabs config—aya-23-35B, aya-23-8B, aya-expanse-32b, aya-expanse-8b, c4ai-command-r-08-2024, c4ai-command-r-plus, c4ai-command-r-plus-08-2024, c4ai-command-r-plus-4bit, c4ai-command-r-v01 and c4ai-command-r-v01-4bit—declares CohereForCausalLM and therefore matches the retained dispatch identifier. No model-specific dimensional or default compatibility is asserted. [source; call_6753a722e5e344669ea5a22a82ce0626, call_81faae4311ae46fc97e24a4e22d65d4a, call_9b5b6b228bdf45eb8520d8d041987ab7, call_b07e06bad9804b8883403def93d2e7da, call_ff3fcf01e2d84fd89c1f2a91115707d4, call_f965e4113d354041b5b4607b91189da1, call_2f381c3acf164a3d8b0262185b2b38f1, call_953ea84ec9234c4c941fc8e7224f97f9, call_eeecad84e16b4bf38020ef3813959dc4, call_ec9cb9297ef0486baacd07282cda911d, call_3ba7866e756041489a361480d6fa41ed]

Each inspected Deci config—DeciCoder-6B, DeciLM-6b, DeciLM-6b-instruct, DeciLM-7B, DeciLM-7B-instruct and DeciLM-7B-instruct-GGUF—declares DeciLMForCausalLM. The same identifier appears in nvidia/Llama-3_1-Nemotron-51B-Instruct, nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1, nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 and nvidia/Llama-3_3-Nemotron-Super-49B-v1. All match the retained registry key; matching that key alone does not establish construction or loading compatibility. [source; call_2dc1795c673745b58ca27c065b6f8aea, call_c012c9df5ae548d8988b3027d8142ffa, call_cc25fb610de0444bbe7046022af3d678, call_bf3c2038f28246619daba6af10c9fa0b, call_9a591149fed84a73892ff8cff62596a3, call_0ca010f828d04e4fa04cd215f51d304a, call_d846214e3c6a476492493fa067453ad3, call_038fe05132c84b9881f87ea7a4b7222e, call_04b44aa7729f4b5fb9138c21ef45950a, call_352538d464e943f9845e651dd92fd2b2, call_3dafe600b7624095a56a6084beb158a7, call_14183a5b1a0547a29608648c54d345c1, call_3ba7866e756041489a361480d6fa41ed]

Each inspected zai-org config—GLM-4-32B-0414, GLM-4-32B-Base-0414, GLM-4-9B-0414, GLM-Z1-32B-0414, GLM-Z1-9B-0414 and GLM-Z1-Rumination-32B-0414—declares Glm4ForCausalLM and matches the retained dispatch identifier. Their differing dimensions are outside this metadata-equivalence check. [source; call_4a0554a2a7c244e4a9f79a9b52a83988, call_a0ba7c2528ed4ccfae4d25a8d3c33874, call_7691375911a64dd9908b5c5287bd1a5a, call_9239f5982ebc4bac818292894191df75, call_304d306ad1ee42349f3e348c0f5fab5d, call_7e2253352b2142d1a6a6460e35c76884, call_3ba7866e756041489a361480d6fa41ed]

## Authoring-time findings — pending review

### architecture-mismatch-diagnostic (suspected; defect)

Config.__init__ removes expect_arch from its parameters but retains its reference in the assertion message.

Trigger: With assertions enabled, instantiate a configuration class against a file whose single architecture differs from that class's arch_string.

Expected: Reject the mismatch with an AssertionError identifying the actual and expected architectures.

Actual: Evaluating the failure message references undefined expect_arch and raises NameError instead. Matching architectures do not evaluate this message. Ordinary Config.from_directory selects the matching configuration class first, so a stable supported config does not trigger this branch through that factory.

Locations: 151edc00b202b645fcfa2cc2c679d7ef381916fb:exllamav3/models/config.py — Config.__init__

Source evidence: call_3ba7866e756041489a361480d6fa41ed, call_ffd8f68f39794e96a22fbae7c6d4b0e8, call_e3f59ae697854ec69de6c53c606a7eaf, call_73b04629e3374721a11f6be54693fffb, call_0262c21d7c7641399c7400951435af63

source_inspection: Inspected the changed assertion, all eight configuration constructor chains and the factory's config_class invocation. Whole-parent literal searches located configuration definitions and factory callers across examples, conversion, evaluation and tests; these broader entry points are not evidence that every workflow triggers a mismatch. [call_3ba7866e756041489a361480d6fa41ed, call_ffd8f68f39794e96a22fbae7c6d4b0e8, call_0262c21d7c7641399c7400951435af63, call_e3f59ae697854ec69de6c53c606a7eaf, call_73b04629e3374721a11f6be54693fffb]. Limits: External and dynamically constructed callers were not established.

scalar_transcription: Executed the changed assertion with a minimal stand-in object: the matching Llama identifier passed, while a Qwen2 identifier raised NameError for expect_arch. [call_32dbb877939a4f71ac7578d9c4b3c36a]. Limits: This reproduces the assertion expression only; it does not import the package or execute the full Config constructor.

## Uncertainty and limits

No package import, model loading, inference or GPU test was executed. The registry comparison and assertion check are symbolic/scalar transcriptions, not execution of the changed repository.

Model configuration checks establish architecture-string matching only, not weight-format compatibility or successful model construction. Dimensions, numerical defaults and model-specific execution behavior were not validated.

Literal parent-tree searches do not establish compatibility for external subclasses, dynamic callers or imports of the former gemma module.
