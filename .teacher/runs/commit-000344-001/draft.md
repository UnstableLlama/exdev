# c8ed45c6152fd6050a2a3f2f9035120fac35cb94


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c8ed45c6152fd6050a2a3f2f9035120fac35cb94) · [Evidence ledger](draft.json)

Ernie 4.5 MoE now reads its optional correction tensor under the name ExLlamaV3 exports. The change leaves standard routing untouched, but stops preserving the tensor from sources that provide only Baidu's sampled `moe_statics` spelling.

- [Read the correction tensor under the name ExLlamaV3 exports](#ernie-moe-bias-key)

## Problem

Ernie 4.5 MoE looked up its optional expert-score correction tensor under `moe_statics.e_score_correction_bias`, but `BlockSparseMLP.get_tensors` exported it under `gate.e_score_correction_bias`. A standalone checkpoint containing only the exported spelling could not restore the tensor with the old lookup. [source; call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_23d632a4bcb54298b74670b7778768b6]

## Reasoning

The one-line change makes Ernie's lookup agree with the shared module's export name and constructor default. This supports interpreting the fix as alignment with ExLlamaV3's serialized format, not a correction to Baidu's checkpoint spelling: the sampled Baidu PT headers use the old name. [inference; call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_7414502a02884096ad6815da0e6e9262, call_ce92b4dab9c4416eace5c70920fac170]

Turboderp's commit message says the tensor is “not used.” That is true of Ernie's routing calculation, not of loading or export. Ernie leaves `router_type` at `std`: `routing_std` selects top-k gate logits and applies softmax to the selected logits without consulting the correction tensor. The unselected `routing_ds3` and `routing_dots` helpers do consume it. Neither the router selection nor the gate projection changes. [source; call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_b84935913eef479a9bfa613c521181ba, call_ef5f05a7f9ed45e0b73d72837a1e7fc9]

## Impact

A checkpoint that already contains the `gate` spelling can now restore the correction tensor. A source containing only the `moe_statics` spelling instead yields `None` and does not re-export that tensor. Supporting both formats would require a fallback or explicit remapping; this patch adds neither. The tensor's presence does not change expert selection or weights on the inspected standard routing path. [source; call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_23d632a4bcb54298b74670b7778768b6]

## Source Notes

The Ernie introduction entry records the original dense-prefix/routed-layer design, the custom-name export mismatch, and two inherited fused-routing observations. The single-turn prompt entry records the separate replacement of the original ChatML markers. [ancestor; call_e34df28f66c8488484db25c91605a22b, call_7dbc8c80d8f04e5c9ec9f809795f300a, call_556b29ea6fb54ad7943a68e430e1ad96]

The whole-parent search finds the old `moe_statics` override only in Ernie MoE, and the `gate` spelling in the shared loader default and exporter. The introduction entry's reload observation should be qualified: a standalone export lacks the old name, but conversion's in-memory overlay can still fall back to the original file map by exact key. [source; call_f655210cf03a4db4983e2dd392f63609, call_64fa6cd466804771902cedadb3c7e8e0, call_968a115aa8944d0eadbae8f11a1a6fc5, call_23d632a4bcb54298b74670b7778768b6]

The unreferenced discussions overlap only through shared code. PR #26, “Superior 3INST parameters,” proposes a decoder multiplier; the inspected converter passes multiplier settings to its quantizer. Issue #33, “Error converting model,” reports a Qwen conversion file-open error through `get_tensors`/`get_tensor`. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports a Cholesky failure; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports a bitrate-specific Midnight-Miqu failure; and #52, “Error converting moonshotai/Kimi-Dev-72B,” reports Cholesky failures at some bitrates. Their traces include the inspected converter's `linear.convert_exl3` call. Issue #53, “Command A support,” asks for Command A support and available EXL3 weights, not for an Ernie fix; its overlap is the shared conversion workflow. These are inferred associations, not reproductions or evidence of the author's motivation. [inference; call_7d5da40df1064287b3c7c0aa089df6d4, call_4d7c511ba31140e4b6bb4dfc3655773b, call_d4ec6067eef44a9b8ac611e99f336086, call_016f890818aa4f31b0b0497bb8126af2, call_2fdf4cf1d3a2439f90d57e0dcdbf5487, call_60ccfc6a1ddf43a89e4c4e1383717f95, call_968a115aa8944d0eadbae8f11a1a6fc5, call_ae89f24a3d7d408aaead880bdbc3187f, call_23d632a4bcb54298b74670b7778768b6]

<a id="ernie-moe-bias-key"></a>

## Read the correction tensor under the name ExLlamaV3 exports

`Ernie4_5MoEModel.__init__` supplies the suffix only to `BlockSparseMLP`, not to the dense-prefix `GatedMLP`. The shared loader appends the suffix to `model.layers.<idx>.mlp` and makes one optional exact-key lookup. A missing key returns `None`, not an exception or a lookup under the other spelling. The correction tensor is separate from the unchanged router matrix `gate.weight` and from Linear's optional `gate.bias`. [source; call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_b84935913eef479a9bfa613c521181ba, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_23d632a4bcb54298b74670b7778768b6, call_6437dcd491ac4de2a46ffd890f6391e3]

The four pinned baidu 21B configs—`ERNIE-4.5-21B-A3B-Base-PT`, `ERNIE-4.5-21B-A3B-Base-Paddle`, `ERNIE-4.5-21B-A3B-PT`, and `ERNIE-4.5-21B-A3B-Paddle`—each map to this architecture with hidden size 2560, 28 layers, one dense-prefix layer, 64 routed experts, six selected per token, expert width 1536 and two shared experts. All supply the one-layer interval and omit `head_dim` and `moe_gate_act`; the builder derives head width from the 20 query heads and the sparse module still defaults to `std`. None of these config values supplies the checkpoint key. [source; call_c2c3ca4b178d49cf94ac330f0c7098c6, call_886f29ad015a47958a0914f901298463, call_d7cda8687dd744acba655c9d491b62d0, call_31894b9e47464d6c803a803f67c0fa08, call_b84935913eef479a9bfa613c521181ba, call_ef5f05a7f9ed45e0b73d72837a1e7fc9]

The seven pinned baidu 300B configs—`ERNIE-4.5-300B-A47B-Base-PT`, `ERNIE-4.5-300B-A47B-Base-Paddle`, `ERNIE-4.5-300B-A47B-PT`, `ERNIE-4.5-300B-A47B-Paddle`, `ERNIE-4.5-300B-A47B-2Bits-Paddle`, `ERNIE-4.5-300B-A47B-FP8-Paddle`, and `ERNIE-4.5-300B-A47B-W4A8C8-TP4-Paddle`—each map to hidden size 8192, 54 layers, three dense-prefix layers, 64 routed experts, eight selected per token and expert width 3584. Each supplies interval one, omits `head_dim` and uses the derived width from 64 query heads, omits the shared-expert count and defaults it to zero, and omits `moe_gate_act`. The quantized variants' format declarations do not change the builder's correction-name lookup or router selection. [source; call_5e01d05e6cf845a8a93a1c3404e20630, call_41edf21710d8480b9320aec640022713, call_277827eb7c2c455686a805b25134c3f2, call_b9c11542aa8d45d7880286ec384c26de, call_ed776cb20d72432dbf43c8146081bad5, call_4f3f451b22c042de9b3a309839c0b2cf, call_7aa3fd8643c8434988dfde568f5a475b, call_b84935913eef479a9bfa613c521181ba, call_ef5f05a7f9ed45e0b73d72837a1e7fc9]

The 21B Base-PT and PT header samples list `model.layers.1.mlp.moe_statics.e_score_correction_bias` as BF16 `[1,64]`; the 300B Base-PT and PT samples list `model.layers.3.mlp.moe_statics.e_score_correction_bias` as F32 `[1,64]`. That is one stored value per routed expert, with no shape validation added by the patch. These samples list `gate.weight` at `[64,2560]` or `[64,8192]` but do not list the newly requested `gate.e_score_correction_bias` beside it. The new correction lookup never requests the stored `moe_statics` name and will take the optional-miss path if the new name is absent from the file map. [source; call_7414502a02884096ad6815da0e6e9262, call_61e17dada507487e84d583eb12ee65b9, call_ce92b4dab9c4416eace5c70920fac170, call_8ff351828b424827917113d5c3698571, call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_23d632a4bcb54298b74670b7778768b6]

Matching config dimensions does not imply Paddle weight compatibility. The 21B Base-Paddle sample stores `ernie.layers.15.mlp.moe_statics.e_score_correction_bias` at `[1,64]`, `gate.weight` and a `gate.weight_1` at `[2560,64]`, and fused `up_gate_proj.weight` at `[2560,3072]` for a routed expert. The builder requests none of those exact names. The 300B Base-Paddle sample likewise uses an `ernie` prefix and fused `up_gate_proj`; the 2Bits, FP8 and W4A8C8-TP4 samples contain `quant_weight` names rather than the requested separate projections. Changing the correction suffix adds no translation for those layouts. [source; call_9591d0d5aa6b4db3ab8dd6b72c7228a1, call_6c4e285dc11b4e38b37cb177013bb6c3, call_dc802b08ffe64da78d272bfa342e6858, call_037a98418e934602aebc0c09335b6eb3, call_ed45487ff78949baacef18a698097b3b, call_b84935913eef479a9bfa613c521181ba, call_b5c5dd9b7dee4fc6b7be8b59b36eaba2]

The direct sparse load is reached by recursive `Module.load` because `TransformerBlock` registers its MLP. Conversion also loads the block, iterates its registered modules for `get_tensors`, saves the result, and reloads with those tensors as an overlay. The compiler copies the resulting names by prefix into output shards. The new name therefore fixes agreement with an already-exported tensor, but changing the input name can also prevent that tensor from entering a fresh export in the first place. [source; call_f8d1694280154f8d99df0fbae9ac79e7, call_638680646e5547bc983af9c973385bfb, call_968a115aa8944d0eadbae8f11a1a6fc5, call_ae89f24a3d7d408aaead880bdbc3187f, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_b5c5dd9b7dee4fc6b7be8b59b36eaba2]

A standard-library transcription found that an old-name-only source returns the modeled bias before the change and `None` after it; a standalone gate-name-only export gives the opposite result. It also showed that the old-name lookup can still hit the original files beneath an export overlay. Integer arithmetic gave head width 128 for both families, 27 versus 51 sparse layers, and shared width 3072 versus no shared branch. No tensor operations ran. [execution; call_b3b2de9870ab4b03b7ef936be3640826]

The ancestor's fused-path observations are carried over: the diff changes only the bias suffix, leaving all-expert dispatch, selected-expert-sized buffers and the workspace-backed return unchanged. The original ChatML-formatting observation is separate and no longer describes the MoE parent: its formatter already emits the begin-of-sentence marker and `User:`/`Assistant:` labels. [source; call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_b84935913eef479a9bfa613c521181ba]

## Authoring-time findings — pending review

### old-name-correction-not-preserved (suspected; behavior_change)

Aligning the export reader drops correction-tensor preservation for old-name-only input.

Trigger: Load an Ernie sparse layer whose file map contains `<mlp>.moe_statics.e_score_correction_bias` but not `<mlp>.gate.e_score_correction_bias`, then collect the layer tensors for export.

Expected: If preserving optional source metadata across conversion, read the original tensor and emit it under the canonical `gate` name.

Actual: The exact optional lookup returns `None`, so the exporter omits the tensor. The path is reached through the block's recursive load and conversion's module iteration; the standard router ignores the field, so this does not demonstrate a generation regression.

Locations: c8ed45c6152fd6050a2a3f2f9035120fac35cb94:exllamav3/models/ernie4_5_moe.py — Ernie4_5MoEModel.__init__, 6565dee474d3f9b247673e24dbfe3b9a72ed278c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.load / get_tensors

Source evidence: call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_23d632a4bcb54298b74670b7778768b6, call_7414502a02884096ad6815da0e6e9262, call_ce92b4dab9c4416eace5c70920fac170, call_b1ef09e878bf49a989e2343763d496a3, call_968a115aa8944d0eadbae8f11a1a6fc5, call_638680646e5547bc983af9c973385bfb

scalar_transcription: Modeled exact-key resolution against old-only and exported-only dictionaries, including precedence of the in-memory overlay. [call_b3b2de9870ab4b03b7ef936be3640826]. Limits: No actual checkpoint load or conversion. The trigger requires absence of the new name from the complete source map, not merely one sampled shard.

### inherited-all-expert-fused-capacity (suspected; defect)

The unchanged fused branch can be selected with more expert indices than its buffers hold.

Trigger: Forward one flattened token through fully EXL3 Ernie experts with `activate_all_experts=True`.

Expected: Evaluate all requested experts with compatible buffers, or use the ordinary expert path.

Actual: `TransformerBlock.forward` passes the flag through. The router returns 64 indices, but the gate multi-GEMM has one input plane and six or eight output planes, so its index-count check rejects the call. Conversion sets the flag during unquantized calibration and omits it during the inspected post-conversion forward, so the ordinary conversion sequence does not establish this trigger.

Locations: 6565dee474d3f9b247673e24dbfe3b9a72ed278c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_1aac7f96686249e0891a44f060137db1, call_f8d1694280154f8d99df0fbae9ac79e7, call_252edbcd6de94cf891e40a5ba483fd55, call_ccfef028b1624bd19fb3f0b77e25a5e6, call_968a115aa8944d0eadbae8f11a1a6fc5

scalar_transcription: Compared the all-expert index count against the configured fused output capacity for the two families. [call_b3b2de9870ab4b03b7ef936be3640826]. Limits: Integer capacity check only; the extension was not invoked.

### inherited-fused-result-contract (suspected; behavior_change)

The unchanged fused result is workspace-backed and bypasses the per-call dtype conversion used by the ordinary path.

Trigger: Retain a fused sparse output across another fused call on the same module, or directly request an `out_dtype` different from the workspace dtype.

Expected: If relying on ordinary-path semantics, the result remains independent of subsequent calls and honors the requested dtype.

Actual: The fused branch returns a view of the reusable `cfg.out_d` buffer without calling `to2`. The inspected Ernie TransformerBlock caller passes no dtype override and immediately adds the result to its residual, so it does not demonstrate either incompatibility.

Locations: 6565dee474d3f9b247673e24dbfe3b9a72ed278c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_b5c5dd9b7dee4fc6b7be8b59b36eaba2, call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_1aac7f96686249e0891a44f060137db1, call_f8d1694280154f8d99df0fbae9ac79e7

source_inspection: Compared the return expressions in both branches and inspected how Ernie's TransformerBlock consumes the MLP result. [call_ef5f05a7f9ed45e0b73d72837a1e7fc9, call_f8d1694280154f8d99df0fbae9ac79e7]. Limits: No tensor-lifetime or dtype test; no claim that ordinary Ernie inference hits the incompatibility.

## Uncertainty and limits

No repository model load, conversion, serialization round trip, routing computation, or GPU kernel was executed. The Python run modeled exact-key lookup and integer dimensions only.

Header comparisons cover representative shards and tensor names, not every layer and shard or a converted EXL3 artifact. The `gate` spelling was not listed alongside the sampled PT correction tensors; absence across every shard was not independently established.

The pinned configs specify `moe_use_aux_free`, but the inspected builder does not use that field to choose a router. The reference implementation's intended inference use of the stored correction values was not established.

Caller reach is based on literal searches and inspection of the module and conversion dispatch paths; dynamic or external callers were not enumerated.
