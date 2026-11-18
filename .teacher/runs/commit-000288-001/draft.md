# a7e667c3ea3ea3350474fc975ab31be6eec75a49


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a7e667c3ea3ea3350474fc975ab31be6eec75a49) · [Evidence ledger](draft.json)

Broadens Mistral3's accepted Pixtral processor identifiers and normalizes square patch-size dictionaries to the scalar form required by its existing vision pipeline.

- [Normalize Pixtral processor configuration](#models)

## Problem

Mistral3 configuration accepted only the PixtralImageProcessorFast identifier and scalar patch sizes, rejecting the alternate processor identifier and square height/width dictionaries. [source; call_62c4708a9902463a84112a1e2d233dbc, call_366a2311ee6a4c46ab303f347c4f2817]

## Reasoning

Accepting the alternate identifier alone is insufficient: normalizing both patch-size sources preserves the scalar representation required by convolution construction, preprocessing and feature-grid arithmetic. [source; call_62c4708a9902463a84112a1e2d233dbc, call_366a2311ee6a4c46ab303f347c4f2817]

## Impact

Both processor identifiers now enter the same existing image pipeline; the change does not instantiate or dispatch to either Transformers processor implementation. [source; call_62c4708a9902463a84112a1e2d233dbc, call_366a2311ee6a4c46ab303f347c4f2817]

## Source Notes

Read the Mistral3 introduction, subsequent list-ingestion entry and chat-formatting entry. The introduction establishes the original strict processor check and spatial-merger requirements; list ingestion records sequential singleton-image processing. [ancestor; call_cb046d1a638541a5b58a349af95dd11f, call_1581bf4f830c4886b31373cc12d313aa, call_47298ca8a7be47b78f56a1d6e8819c06]

The introduction's recorded resize-overflow mechanism has changed in the inspected parent: the helper floors scaled dimensions before patch alignment. This task leaves that helper unchanged. [source; call_acea61288fca4f0e97f0e2301abc14f9, call_62c4708a9902463a84112a1e2d233dbc]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure; PR #4, “chore: update config.py,” corrects a spelling. Their connections here are inferred solely from config.py appearing in the traceback or title and being inspected for this change, not evidence that either motivated the Pixtral fix. [inference; call_9c840945dbdd4f058677339b62b1220a, call_ae604f9d14ba44df8fea8c7f184099c4, call_4976b36d4c134f7abe81442dba5cb46e]

<a id="models"></a>

## Normalize Pixtral processor configuration

Mistral3Config.__init__ admits exactly PixtralImageProcessor and PixtralImageProcessorFast. Its local unpack_patch_size helper accepts an integer or a dictionary whose height and width agree, then requires the resulting side length to be an integer. Rectangular dictionaries are rejected rather than propagated as rectangular convolution dimensions. [source; call_62c4708a9902463a84112a1e2d233dbc]

Both vision_config->patch_size and preprocessor_config.json's patch_size are read as object and normalized separately. The model-side default remains 14, a patch side length, while the preprocessor value remains required. The existing equality assertion compares normalized sides, permitting an integer in one file and an equivalent square dictionary in the other. [source; call_62c4708a9902463a84112a1e2d233dbc, call_0067a97e8a604ba399bef719c665fb3b, call_4976b36d4c134f7abe81442dba5cb46e]

Whole-parent-tree searches found Mistral3 patch-size consumers in its vision constructor, preprocess, default_load_params and get_image_embeddings. They continue to receive scalar integers: convolution duplicates the side into a square kernel, preprocessing multiplies it by spatial_merge_size, and feature-grid calculations divide image dimensions by it. Gemma3's separate patch-size reader and consumers remain unchanged. The Mistral3 class search found no additional subclass or alternate configuration builder beyond its architecture registration and local component classes. [source; call_0e19801caa2b43589d7d383434426ffc, call_2c4a3fbbf35f431abff17f7df150b3cc, call_366a2311ee6a4c46ab303f347c4f2817]

The configuration compatibility broadening has one narrower edge: read_dict previously converted integral floats such as 14.0 to int when asked for int. Reading as object bypasses that conversion, so unpack_patch_size now rejects 14.0. Integer-valued JSON numbers remain accepted. [source; call_0067a97e8a604ba399bef719c665fb3b, call_62c4708a9902463a84112a1e2d233dbc]

A standard-library transcription returned 14 for both 14 and {height:14,width:14}, and raised AssertionError for unequal sides, a missing width, an empty dictionary and 14.0. This checks normalization branches, not execution of Mistral3Config. [execution; call_ef9aa327162e427698f90ee1b213e2bf]

For mistralai/Mistral-Small-3.1-24B-Base-2503, the inspected config declares Mistral3ForConditionalGeneration, scalar patch_size=14 and spatial_merge_size=2; normalization preserves 14 without using the default. Independently, the Instruct-2503 config declares the same architecture and values and likewise remains on the scalar path. Neither config demonstrates the newly accepted dictionary representation. [source; call_41d246d2732741b88043694b44de85b7, call_a3acc9cdf8a74150b8dabaf917c9abed, call_62c4708a9902463a84112a1e2d233dbc]

The design keeps format variability at the configuration boundary instead of teaching every downstream consumer about dictionaries. Its benefit is broader input compatibility with unchanged image computation; numerical equivalence to either named Transformers processor is not established by accepting its identifier. [inference; call_62c4708a9902463a84112a1e2d233dbc, call_366a2311ee6a4c46ab303f347c4f2817]

## Uncertainty and limits

No repository configuration constructor, image-library operation, checkpoint loading or GPU inference was executed; the Python check transcribed only the new normalization logic.

The reference config.json files establish model-side patch sizes, not the processor identifiers or patch-size representations in their preprocessor_config.json files.

Whole-tree literal searches do not establish external or dynamically constructed consumers.
