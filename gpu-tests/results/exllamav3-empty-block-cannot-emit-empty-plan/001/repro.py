# Trigger: call make_tp_allocation (assertions enabled) on a DeciLM block whose attention and FFN are both no_op.
# Fixture: the tiny 3-layer DeciLMForCausalLM from empty-block-conversion (layer 1 fully disabled), built with
# Config.from_directory / Model.from_config (no load needed). make_tp_allocation is called on each transformer
# block. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the disabled block raises AssertionError "Tried to get TPAllocators from empty module
#                        list" (exllamav3/modules/module.py), while enabled blocks return allocations.
#   expected_behaviour : the disabled block returns an empty list.
#   other              : anything else.
import json, tempfile, sys
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
assert sys.flags.optimize == 0
from exllamav3 import Config, Model
H, HEADS, V, L, DISABLED, IM = 256, 4, 128, 3, 1, 512
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
blocks = []
for i in range(L):
    p = f"model.layers.{i}"
    if i == DISABLED:
        blocks.append({"attention": {"no_op": True, "n_heads_in_group": None}, "ffn": {"no_op": True, "ffn_mult": None}}); continue
    blocks.append({"attention": {"no_op": False, "n_heads_in_group": 1}, "ffn": {"no_op": False, "ffn_mult": 3.0}})
    t[f"{p}.input_layernorm.weight"] = torch.ones(H).half(); t[f"{p}.post_attention_layernorm.weight"] = torch.ones(H).half()
    for k in "qkvo": t[f"{p}.self_attn.{k}_proj.weight"] = n(H, H)
    t[f"{p}.mlp.up_proj.weight"] = n(IM, H); t[f"{p}.mlp.gate_proj.weight"] = n(IM, H); t[f"{p}.mlp.down_proj.weight"] = n(H, IM)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["DeciLMForCausalLM"], model_type="nemotron-nas", hidden_size=H, num_attention_heads=HEADS, num_hidden_layers=L,
               vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=2048, bos_token_id=1, eos_token_id=2,
               tie_word_embeddings=False, block_configs=blocks), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
model = Model.from_config(Config.from_directory(d))
res = {}; exc = None
for m in model.modules:
    if not m.key.startswith("model.layers."): continue
    try:
        res[m.key] = {"ok": True, "n_allocations": len(m.make_tp_allocation())}
    except Exception as e:
        res[m.key] = {"ok": False, "exception_type": type(e).__name__, "message": str(e), "site": rt._site(e.__traceback__)}
        if m.key.endswith(f".{DISABLED}"): exc = e
print(res, flush=True)
dis = res.get(f"model.layers.{DISABLED}", {}); others = [v for k, v in res.items() if not k.endswith(f".{DISABLED}")]
if (not dis.get("ok")) and dis.get("exception_type") == "AssertionError" and all(o["ok"] for o in others): rt.report("stated_behaviour", exc, blocks=res)
elif dis.get("ok") and dis.get("n_allocations") == 0: rt.report("expected_behaviour", blocks=res)
else: rt.report("other", exc, blocks=res)
