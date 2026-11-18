# Trigger: load a CohereForCausalLM checkpoint with use_qk_norm=true and run attention.
# No small public checkpoint uses this option, so a tiny random checkpoint is generated here.
# The same weights (including q_norm/k_norm tensors) are loaded with the option off and on.
import json, os, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
H, HEADS, HD, IM, V, L = 256, 4, 64, 512, 128, 2
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": (1 + torch.randn(H) * .1).half()}
for i in range(L):
    p = f"model.layers.{i}"
    t[f"{p}.input_layernorm.weight"] = (1 + torch.randn(H) * .1).half()
    for k in "qkv": t[f"{p}.self_attn.{k}_proj.weight"] = n(HEADS * HD, H)
    t[f"{p}.self_attn.o_proj.weight"] = n(H, HEADS * HD)
    for k in "qk": t[f"{p}.self_attn.{k}_norm.weight"] = (1 + torch.randn(HD) * .5).half()
    t[f"{p}.mlp.up_proj.weight"] = n(IM, H); t[f"{p}.mlp.gate_proj.weight"] = n(IM, H); t[f"{p}.mlp.down_proj.weight"] = n(H, IM)
root = tempfile.mkdtemp()
base = dict(architectures=["CohereForCausalLM"], hidden_size=H, num_attention_heads=HEADS, num_key_value_heads=HEADS, intermediate_size=IM,
            num_hidden_layers=L, vocab_size=V, hidden_act="silu", bos_token_id=1, eos_token_id=2, pad_token_id=0, max_position_embeddings=512,
            rotary_scale=1.0, logit_scale=0.0625, layer_norm_eps=1e-5, tie_word_embeddings=True)
ids = torch.randint(3, V, (1, 24)); out = {}
try:
    for name, extra in (("off", {"use_qk_norm": False}), ("on", {"use_qk_norm": True})):
        d = os.path.join(root, name); os.makedirs(d)
        json.dump(dict(base, **extra), open(d + "/config.json", "w")); save_file(t, d + "/model.safetensors")
        c = Config.from_directory(d); m = Model.from_config(c); m.load("cuda:0", progressbar=False)
        with torch.inference_mode(): out[name] = m.forward(ids.clone()).float().cpu()
        print(name, "has_q_norm", any("q_norm" in k for mod in m.modules for k in mod.get_tensors()), "logits", out[name].shape, flush=True)
        m.unload()
except Exception as e:
    rt.report("did_not_run" if not out else "other", e, message=str(e)); raise SystemExit
assert out["off"].isfinite().all() and out["on"].isfinite().all()
diff = (out["off"] - out["on"]).abs().max().item()
rt.report("stated_behaviour" if diff == 0 else "expected_behaviour", max_abs_logit_difference=diff)
