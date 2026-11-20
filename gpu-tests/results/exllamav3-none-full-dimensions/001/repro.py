# Trigger: Linear.load_fp16 takes its fused-tensor (fkey/frange) fallback and constructs LinearFP16 without
# full dimensions. Fixture: a tiny random Phi3ForCausalLM checkpoint storing fused self_attn.qkv_proj and
# mlp.gate_up_proj (as real Phi-3 checkpoints do), loaded unquantized through Config.from_directory,
# Model.from_config and model.load, then one forward pass. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : TypeError comparing int with None, raised from exllamav3/modules/quant/fp16.py
#                        (LinearFP16 construction) during model.load.
#   expected_behaviour : the model loads and a forward pass returns finite logits.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
H, HEADS, IM, V, L = 256, 4, 512, 128, 1
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
for i in range(L):
    p = f"model.layers.{i}"
    t[f"{p}.input_layernorm.weight"] = torch.ones(H).half(); t[f"{p}.post_attention_layernorm.weight"] = torch.ones(H).half()
    t[f"{p}.self_attn.qkv_proj.weight"] = n(3 * H, H); t[f"{p}.self_attn.o_proj.weight"] = n(H, H)
    t[f"{p}.mlp.gate_up_proj.weight"] = n(2 * IM, H); t[f"{p}.mlp.down_proj.weight"] = n(H, IM)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["Phi3ForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               num_hidden_layers=L, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               original_max_position_embeddings=512, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    cfg = Config.from_directory(d); model = Model.from_config(cfg)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    model.load("cuda:0", progressbar=False)
except TypeError as e:
    site = rt._site(e.__traceback__) or ""
    hit = "NoneType" in str(e) and site.startswith("exllamav3/modules/quant/fp16.py")
    rt.report("stated_behaviour" if hit else "other", e, stage="load", message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, stage="load", message=str(e)); raise SystemExit
try:
    with torch.inference_mode(): y = model.forward(torch.randint(3, V, (1, 8)))
except Exception as e:
    rt.report("other", e, stage="forward", message=str(e)); raise SystemExit
rt.report("expected_behaviour" if bool(y.float().isfinite().all()) else "other", logits_shape=list(y.shape))
