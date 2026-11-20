# Trigger: construct a valid Qwen3MoeConfig and pass it to Model.from_config.
# Fixture: a tiny random 1-layer Qwen3MoeForCausalLM checkpoint (4 experts, top 2, q_norm/k_norm), read with
# Config.from_directory. Model.from_config(config) is the factory every in-tree caller uses. Upstream is not
# modified.
# Classification, fixed before running:
#   stated_behaviour   : TypeError from the factory's component lookup (exllamav3/models/), before any model
#                        is constructed.
#   expected_behaviour : Model.from_config returns a Qwen3MoeModel.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
H, HEADS, HD, IM, E, V = 256, 4, 64, 256, 4, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.self_attn.q_norm.weight": torch.ones(HD).half(), f"{p}.self_attn.k_norm.weight": torch.ones(HD).half(),
     f"{p}.mlp.gate.weight": n(E, H)}
for k in "qkv": t[f"{p}.self_attn.{k}_proj.weight"] = n(HEADS * HD, H)
t[f"{p}.self_attn.o_proj.weight"] = n(H, HEADS * HD)
for e in range(E):
    for k, s in (("gate_proj", (IM, H)), ("up_proj", (IM, H)), ("down_proj", (H, IM))): t[f"{p}.mlp.experts.{e}.{k}.weight"] = n(*s)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["Qwen3MoeForCausalLM"], hidden_size=H, num_attention_heads=HEADS, num_key_value_heads=HEADS, head_dim=HD,
               moe_intermediate_size=IM, intermediate_size=IM, num_experts=E, num_experts_per_tok=2, norm_topk_prob=True,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-6, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    cfg = Config.from_directory(d)
    print("config:", type(cfg).__name__, "model_classes:", getattr(cfg, "model_classes", None), flush=True)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    m = Model.from_config(cfg)
except TypeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/models/") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour" if type(m).__name__ == "Qwen3MoeModel" else "other", model=type(m).__name__)
