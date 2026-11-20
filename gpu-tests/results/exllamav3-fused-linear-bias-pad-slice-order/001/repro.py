# Trigger: load an fkey/frange Linear for which a tensor exists at key + '.bias'.
# Fixture: a tiny random 1-layer Phi3ForCausalLM with fused self_attn.qkv_proj (weight and bias) and fused
# mlp.gate_up_proj, loaded unquantized through Config.from_directory / Model.from_config / model.load. The q, k
# and v Linear modules are then inspected: each one's loaded bias should equal its slice of the fused bias
# (q: [0, H), k: [H, 2H), v: [2H, 3H)). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : loading raises from the bias pad/slice, or a loaded q/k/v bias differs from its slice.
#   expected_behaviour : each loaded bias equals its slice of the fused bias.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
from exllamav3.modules import Linear
H, HEADS, IM, V = 256, 4, 512, 128
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0"
qkv_b = torch.randn(3 * H).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.self_attn.qkv_proj.weight": n(3 * H, H), f"{p}.self_attn.qkv_proj.bias": qkv_b, f"{p}.self_attn.o_proj.weight": n(H, H),
     f"{p}.mlp.gate_up_proj.weight": n(2 * IM, H), f"{p}.mlp.down_proj.weight": n(H, IM)}
d = tempfile.mkdtemp()
json.dump(dict(architectures=["Phi3ForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               original_max_position_embeddings=512, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
cfg = Config.from_directory(d); model = Model.from_config(cfg)
try:
    model.load("cuda:0", progressbar=False)
except Exception as e:
    rt.report("stated_behaviour" if "bias" in "".join(__import__("traceback").format_exception(e)) else "other", e, stage="load", message=str(e).splitlines()[0]); raise SystemExit
res = {}
for name, (a, b) in (("q_proj", (0, H)), ("k_proj", (H, 2 * H)), ("v_proj", (2 * H, 3 * H))):
    lin = [m for m in model if isinstance(m, Linear) and m.key.endswith("self_attn." + name)][0]
    bias = lin.inner.bias
    want = qkv_b[a:b]
    if bias is None: res[name] = {"bias": None}; continue
    bb = bias.flatten().cpu()
    res[name] = {"shape": list(bb.shape), "equals_slice": bool(bb.shape == want.shape and torch.equal(bb, want)),
                 "equals_slice_prefix": bool(bb.numel() >= want.numel() and torch.equal(bb[:want.numel()], want))}
print(res, flush=True)
if all(r.get("equals_slice_prefix") for r in res.values()): rt.report("expected_behaviour", **res)
elif any(r.get("bias", 1) is None or not r.get("equals_slice_prefix") for r in res.values()): rt.report("stated_behaviour", **res)
else: rt.report("other", **res)
