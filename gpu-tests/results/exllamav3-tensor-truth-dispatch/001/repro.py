# Trigger: loaded Attention with RoPE, Q/K RMSNorm and a multi-element norm weight, then forward.
# Fixture: a tiny random 1-layer Qwen3ForCausalLM checkpoint (head_dim 64, q_norm/k_norm weights of 64
# elements, as real Qwen3 checkpoints have), loaded unquantized through Config.from_directory,
# Model.from_config and model.load; one forward pass over 8 tokens. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : RuntimeError "Boolean value of Tensor with more than one value is ambiguous" from
#                        exllamav3/modules/attn.py during forward.
#   expected_behaviour : forward returns finite logits.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
H, HEADS, HD, IM, V = 256, 4, 64, 512, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.self_attn.q_norm.weight": (1 + torch.randn(HD) * 0.1).half(), f"{p}.self_attn.k_norm.weight": (1 + torch.randn(HD) * 0.1).half(),
     f"{p}.mlp.gate_proj.weight": n(IM, H), f"{p}.mlp.up_proj.weight": n(IM, H), f"{p}.mlp.down_proj.weight": n(H, IM)}
for k in "qkv": t[f"{p}.self_attn.{k}_proj.weight"] = n(HEADS * HD, H)
t[f"{p}.self_attn.o_proj.weight"] = n(H, HEADS * HD)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["Qwen3ForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               head_dim=HD, num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-6, rope_theta=10000.0,
               max_position_embeddings=512, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    cfg = Config.from_directory(d); model = Model.from_config(cfg); model.load("cuda:0", progressbar=False)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    with torch.inference_mode(): y = model.forward(torch.randint(3, V, (1, 8)))
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    hit = "ambiguous" in str(e) and site.startswith("exllamav3/modules/attn.py")
    rt.report("stated_behaviour" if hit else "other", e, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e).splitlines()[0] if str(e) else ""); raise SystemExit
rt.report("expected_behaviour" if bool(y.float().isfinite().all()) else "other", logits_shape=list(y.shape))
