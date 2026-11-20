# Trigger: construct an otherwise valid (ungated) MLP with activation_fn="gelu" and call forward.
# Fixture: a tiny random checkpoint holding one up/down pair, loaded unquantized; MLP is constructed directly
# (no in-tree caller builds an ordinary MLP). The output is compared with torch references computed from the
# same weights: down(gelu_tanh(up(x))) and down(silu(up(x))). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : output matches the silu reference and not the gelu reference.
#   expected_behaviour : output matches the gelu reference (tanh or exact form), or construction rejects gelu.
#   other              : anything else.
import json, tempfile
import torch, torch.nn.functional as F
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import MLP
H, IM, V = 256, 512, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0.mlp"
t = {f"{p}.up_proj.weight": n(IM, H), f"{p}.down_proj.weight": n(H, IM), "model.embed_tokens.weight": n(V, H),
     "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
x = (torch.randn(1, 8, H) * 2.0).half().cuda()
up, down = t[f"{p}.up_proj.weight"].float().cuda(), t[f"{p}.down_proj.weight"].float().cuda()
h = x.float() @ up.T
ref = {"gelu_tanh": F.gelu(h, approximate="tanh") @ down.T, "gelu_exact": F.gelu(h) @ down.T, "silu": F.silu(h) @ down.T}
try:
    cfg = Config.from_directory(d)
    m = MLP(config=cfg, key=p, hidden_size=H, intermediate_size=IM, key_up="up_proj", key_down="down_proj", qmap="block.mlp", activation_fn="gelu")
except (ValueError, AssertionError, NotImplementedError) as e:
    rt.report("expected_behaviour", e, rejected_at_construction=True); raise SystemExit
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    m.load(torch.device("cuda:0"))
    with torch.inference_mode(): y = m.forward(x.clone(), {}).float()
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
diff = {k: (y - v).abs().max().item() for k, v in ref.items()}
sep = (ref["gelu_tanh"] - ref["silu"]).abs().max().item()
tol = 0.05 * sep
notes = dict(max_abs_diff=diff, silu_vs_gelu_reference_gap=sep, tol=tol)
print(notes, flush=True)
if diff["silu"] <= tol and min(diff["gelu_tanh"], diff["gelu_exact"]) > tol: rt.report("stated_behaviour", **notes)
elif min(diff["gelu_tanh"], diff["gelu_exact"]) <= tol and diff["silu"] > tol: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
