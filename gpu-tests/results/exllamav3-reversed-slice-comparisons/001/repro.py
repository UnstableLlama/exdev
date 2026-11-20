# Trigger: ordinary FP16 loading receives a full weight with an axis larger than its requested local axis: split
# GatedMLP projections loaded through alternate full-weight keys (intermediate_size > MAX_MLP_INTERMEDIATE, 55296),
# so each slice loads from the full gate/up/down tensors. Same script as sliced-fp16-padding-target 001.
# Fixture: a tiny random 1-layer LlamaForCausalLM with hidden 128 and intermediate_size 55424 (> 55296, a
# multiple of 128), loaded unquantized through Config.from_directory / Model.from_config / model.load, then one
# forward pass (logits checked for finiteness).
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : a shape-mismatch RuntimeError during model.load or forward (full matrix kept instead of
#                        the local slice), raised in exllamav3/loader/ or exllamav3/modules/.
#   expected_behaviour : the model loads and a forward pass returns finite logits.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
H, HEADS, IM, V = 128, 2, 55424, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.02).half()
p = "model.layers.0"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.mlp.gate_proj.weight": n(IM, H), f"{p}.mlp.up_proj.weight": n(IM, H), f"{p}.mlp.down_proj.weight": n(H, IM)}
for k in "qkvo": t[f"{p}.self_attn.{k}_proj.weight"] = n(H, H)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    cfg = Config.from_directory(d); model = Model.from_config(cfg)
    mlp = [m for m in model if type(m).__name__ == "GatedMLP"][0]
    print("GatedMLP num_slices:", mlp.num_slices, flush=True)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    model.load("cuda:0", progressbar=False)
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    hit = ("size" in str(e) or "shape" in str(e)) and (site.startswith("exllamav3/loader/") or site.startswith("exllamav3/modules/"))
    rt.report("stated_behaviour" if hit else "other", e, num_slices=mlp.num_slices, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, num_slices=mlp.num_slices, message=str(e).splitlines()[0] if str(e) else ""); raise SystemExit
try:
    with torch.inference_mode(): y = model.forward(torch.randint(3, V, (1, 8)))
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/") else "other", e, stage="forward", num_slices=mlp.num_slices, message=str(e).splitlines()[0]); raise SystemExit
rt.report("expected_behaviour" if bool(y.float().isfinite().all()) else "other", num_slices=mlp.num_slices, logits_shape=list(y.shape))
