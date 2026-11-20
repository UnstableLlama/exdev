# Trigger: load a present score-correction bias through a nondefault key_e_score_bias, then call
# BlockSparseMLP.get_tensors. Fixture: a tiny random unquantized MoE layer (8 experts, top 2) whose bias is stored
# as <key>.gate.custom_bias; BlockSparseMLP is constructed with key_e_score_bias="gate.custom_bias" and
# router_type="dots". Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the bias is loaded, and get_tensors exports it under gate.e_score_correction_bias,
#                        not gate.custom_bias.
#   expected_behaviour : get_tensors exports it under gate.custom_bias.
#   other              : anything else (including the bias not loading).
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.models.mixtral import MixtralConfig
from exllamav3.modules import BlockSparseMLP
H, IM, E, K, V = 256, 256, 8, 2, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
KEY = "model.layers.0.block_sparse_moe"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H), f"{KEY}.gate.weight": n(E, H),
     f"{KEY}.gate.custom_bias": (torch.randn(E) * 0.1).float()}
for e in range(E):
    t[f"{KEY}.experts.{e}.w1.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w3.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w2.weight"] = n(H, IM)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["MixtralForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, num_local_experts=E, num_experts_per_tok=K, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5,
               rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
cfg = MixtralConfig(d)
m = BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                   key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                   key_routing_gate="gate", key_e_score_bias="gate.custom_bias", router_type="dots", routed_scaling_factor=1.0,
                   qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.half)
m.load(torch.device("cuda:0"))
loaded = m.e_score_correction_bias is not None
keys = sorted(k for k in m.get_tensors() if "bias" in k)
notes = dict(bias_loaded=loaded, exported_bias_keys=keys)
print(notes, flush=True)
if loaded and f"{KEY}.gate.e_score_correction_bias" in keys and f"{KEY}.gate.custom_bias" not in keys: rt.report("stated_behaviour", **notes)
elif loaded and f"{KEY}.gate.custom_bias" in keys: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
