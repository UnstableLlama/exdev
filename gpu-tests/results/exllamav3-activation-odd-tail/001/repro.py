# Trigger: a direct GatedMLP caller selects pad_to=1 and runs FP16 projections with an odd total intermediate
# element count: one token, hidden_size=128, intermediate_size=129.
# Fixture: a tiny random checkpoint holding one gate/up/down triple, loaded unquantized; GatedMLP constructed
# directly with pad_to=1. Output compared with down(silu(gate(x)) * up(x)) computed in torch, and with the
# variant where the last intermediate element is left ungated (up only), which is what the ledger predicts.
# Classification, fixed before running:
#   stated_behaviour   : output matches the "last element ungated" variant and not the correct reference.
#   expected_behaviour : output matches the correct reference.
#   other              : anything else.
import json, tempfile
import torch, torch.nn.functional as F
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import GatedMLP
H, IM, V = 128, 129, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.1).half()
p = "model.layers.0.mlp"
t = {f"{p}.gate_proj.weight": n(IM, H), f"{p}.up_proj.weight": n(IM, H), f"{p}.down_proj.weight": n(H, IM),
     "model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=2, num_key_value_heads=2,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    cfg = Config.from_directory(d)
    m = GatedMLP(config=cfg, key=p, hidden_size=H, intermediate_size=IM, key_up="up_proj", key_gate="gate_proj", key_down="down_proj",
                 qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.half, pad_to=1)
    m.load(torch.device("cuda:0"))
    x = (torch.randn(1, 1, H) * 2).half().cuda()
    with torch.inference_mode(): y = m.forward(x.clone(), {}).float()
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
xf = x.float().view(1, H); G, U, D = (t[f"{p}.{k}_proj.weight"].float().cuda() for k in ("gate", "up", "down"))
g, u = xf @ G.T, xf @ U.T
a = F.silu(g) * u
ref = (a @ D.T).view(1, 1, H)
a_bad = a.clone(); a_bad[:, -1] = u[:, -1]
ref_bad = (a_bad @ D.T).view(1, 1, H)
dr, db = (y - ref).abs().max().item(), (y - ref_bad).abs().max().item()
sep = (ref - ref_bad).abs().max().item()
notes = dict(diff_vs_correct=dr, diff_vs_last_ungated=db, reference_separation=sep, last_gate=float(g[0, -1]), last_up=float(u[0, -1]))
print(notes, flush=True)
tol = 0.1 * sep
if sep > 1e-3 and db <= tol < dr: rt.report("stated_behaviour", **notes)
elif dr <= tol: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
