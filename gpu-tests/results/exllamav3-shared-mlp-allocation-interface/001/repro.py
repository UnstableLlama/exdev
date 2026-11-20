# Trigger: construct a TransformerBlock containing BlockSparseMLP(shared_experts=<MLP instance>) and call allocate_q.
# Fixture: a tiny random unquantized MoE layer (8 experts, top 2) plus a plain shared MLP (up/down), in a
# MixtralForCausalLM-shaped checkpoint (config built with MixtralConfig). The block is loaded on cuda:0 and
# allocate_q({"bits": 4.0}, 0) is called. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : AttributeError for .gates (or .ups/.downs) on the plain MLP, from exllamav3/modules/.
#   expected_behaviour : returns a strategy including the shared MLP's up and down projections.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.models.mixtral import MixtralConfig
from exllamav3.modules import BlockSparseMLP, MLP, TransformerBlock, RMSNorm
H, IM, E, K, V = 256, 256, 8, 2, 128
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
P = "model.layers.0"; KEY = f"{P}.block_sparse_moe"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H), f"{KEY}.gate.weight": n(E, H),
     f"{P}.post_attention_layernorm.weight": torch.ones(H).half(), f"{KEY}.shared.up_proj.weight": n(IM, H), f"{KEY}.shared.down_proj.weight": n(H, IM)}
for e in range(E):
    t[f"{KEY}.experts.{e}.w1.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w3.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w2.weight"] = n(H, IM)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["MixtralForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, num_local_experts=E, num_experts_per_tok=K, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5,
               rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
cfg = MixtralConfig(d)
shared = MLP(config=cfg, key=f"{KEY}.shared", hidden_size=H, intermediate_size=IM, key_up="up_proj", key_down="down_proj", qmap="block.mlp")
moe = BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                     key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                     key_routing_gate="gate", qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.half, shared_experts=shared)
blk = TransformerBlock(config=cfg, key=P, mlp_norm=RMSNorm(config=cfg, key=f"{P}.post_attention_layernorm", rms_norm_eps=1e-5), mlp=moe)
blk.load(torch.device("cuda:0"))
try:
    s, _ = blk.allocate_q({"bits": 4.0}, 0)
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/modules/") and any(w in str(e) for w in ("gates", "ups", "downs")) else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour" if any("shared" in k for k in s) else "other", strategy_keys=sorted(s))
