# Trigger: load an fkey/frange Linear for which a tensor exists at key + '.bias'.
# Fixture: a tiny random 1-layer Phi3ForCausalLM with fused self_attn.qkv_proj.weight and per-projection biases
# at self_attn.{q,k,v}_proj.bias (H elements each), fused mlp.gate_up_proj; loaded unquantized through
# Config.from_directory / Model.from_config / model.load, then one forward pass. Each of q/k/v's loaded bias is
# compared with the bias stored at its own key. Upstream is not modified.
# Attempt 002: biases now sit at key + '.bias' (attempt 001 stored them under the fused key).
# Classification, fixed before running:
#   stated_behaviour   : loading or forward raises from the bias handling, or some loaded q/k/v bias is not
#                        equal to the bias stored at its own key (e.g. empty after slicing with fused bounds).
#   expected_behaviour : every loaded q/k/v bias equals its own key's bias and forward is finite.
#   other              : anything else.
import json, tempfile, traceback
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
from exllamav3.modules import Linear
H, HEADS, IM, V = 256, 4, 512, 128
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0"
b = {k: torch.randn(H).half() for k in "qkv"}
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.self_attn.qkv_proj.weight": n(3 * H, H), f"{p}.self_attn.o_proj.weight": n(H, H),
     f"{p}.mlp.gate_up_proj.weight": n(2 * IM, H), f"{p}.mlp.down_proj.weight": n(H, IM)}
for k in "qkv": t[f"{p}.self_attn.{k}_proj.bias"] = b[k]
d = tempfile.mkdtemp()
json.dump(dict(architectures=["Phi3ForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               original_max_position_embeddings=512, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
cfg = Config.from_directory(d); model = Model.from_config(cfg)
try:
    model.load("cuda:0", progressbar=False)
except Exception as e:
    tb = "".join(traceback.format_exception(e))
    rt.report("stated_behaviour" if "bias" in tb else "other", e, stage="load", message=str(e).splitlines()[0]); raise SystemExit
res = {}
for k in "qkv":
    lin = [m for m in model if isinstance(m, Linear) and m.key.endswith(f"self_attn.{k}_proj")][0]
    bias = lin.inner.bias
    if bias is None: res[k] = {"bias": None}; continue
    bb = bias.flatten().cpu()
    res[k] = {"loaded_shape": list(bb.shape), "equals_own_bias": bool(bb.shape == b[k].shape and torch.equal(bb, b[k])),
              "frange": list(lin.frange) if getattr(lin, "frange", None) else None}
fwd = None
try:
    with torch.inference_mode(): y = model.forward(torch.randint(3, V, (1, 8)))
    fwd = {"ok": True, "finite": bool(y.float().isfinite().all())}
except Exception as e:
    fwd = {"ok": False, "exception_type": type(e).__name__, "site": rt._site(e.__traceback__), "message": str(e).splitlines()[0]}
print(res, fwd, flush=True)
if all(r.get("equals_own_bias") for r in res.values()) and fwd["ok"] and fwd["finite"]: rt.report("expected_behaviour", biases=res, forward=fwd)
elif any(not r.get("equals_own_bias") for r in res.values()) or not fwd["ok"]: rt.report("stated_behaviour", biases=res, forward=fwd)
else: rt.report("other", biases=res, forward=fwd)
