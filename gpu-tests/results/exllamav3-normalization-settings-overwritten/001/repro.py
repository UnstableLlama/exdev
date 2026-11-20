# Trigger: RoPE with paired Q/K head norms whose epsilon differs from 1e-6 (or with nonzero constant bias).
# Fixture: a tiny random 1-layer Qwen3ForCausalLM with rms_norm_eps = 1e-3 (Qwen3 passes this epsilon to
# q_norm/k_norm), constructed with Config.from_directory / Model.from_config. The Attention module's
# norm_eps / norm_constant_bias, the values its fused decode routes pass to the native RMSNorm+RoPE call,
# are compared with its q_norm's configured rms_norm_eps / constant_bias. The model is also loaded and run
# once to show the fused path executes. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : Attention.norm_eps is 1e-6 while q_norm.rms_norm_eps is 1e-3 (setting overwritten).
#   expected_behaviour : Attention.norm_eps equals q_norm.rms_norm_eps and norm_constant_bias equals
#                        q_norm.constant_bias.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
from exllamav3.modules import Attention
H, HEADS, HD, IM, V, EPS = 256, 4, 64, 512, 128, 1e-3
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.self_attn.q_norm.weight": torch.ones(HD).half(), f"{p}.self_attn.k_norm.weight": torch.ones(HD).half(),
     f"{p}.mlp.gate_proj.weight": n(IM, H), f"{p}.mlp.up_proj.weight": n(IM, H), f"{p}.mlp.down_proj.weight": n(H, IM)}
for k in "qkv": t[f"{p}.self_attn.{k}_proj.weight"] = n(HEADS * HD, H)
t[f"{p}.self_attn.o_proj.weight"] = n(H, HEADS * HD)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["Qwen3ForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               head_dim=HD, num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=EPS, rope_theta=10000.0,
               max_position_embeddings=512, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    model = Model.from_config(Config.from_directory(d))
    attn = [m for m in model if isinstance(m, Attention)][0]
    s = dict(attn_norm_eps=attn.norm_eps, attn_norm_constant_bias=attn.norm_constant_bias,
             q_norm_eps=attn.q_norm.rms_norm_eps, q_norm_constant_bias=attn.q_norm.constant_bias, has_rope=attn.rope is not None or hasattr(attn, "rope_settings"))
    print(s, flush=True)
    model.load("cuda:0", progressbar=False)
    with torch.inference_mode(): y = model.forward(torch.randint(3, V, (1, 8)))
    s["forward_ok"] = bool(y.float().isfinite().all())
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
if abs(s["attn_norm_eps"] - 1e-6) < 1e-12 and abs(s["q_norm_eps"] - EPS) < 1e-12: rt.report("stated_behaviour", **s)
elif s["attn_norm_eps"] == s["q_norm_eps"] and s["attn_norm_constant_bias"] == s["q_norm_constant_bias"]: rt.report("expected_behaviour", **s)
else: rt.report("other", **s)
