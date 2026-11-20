# Trigger: half input, out_dtype=torch.float and ordinary (non-fused) execution in BlockSparseMLP.
# Qwen3MoeModel passes interm_dtype=torch.half, out_dtype=torch.float; 4 flattened half tokens select the
# ordinary path (bsz > 1; the experts are also unquantized). Fixture: a tiny random unquantized MoE layer
# (8 experts, top 2) in a MixtralForCausalLM-shaped checkpoint, BlockSparseMLP constructed directly with
# Qwen3Moe's dtype settings, default routing. Config built with MixtralConfig(dir). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : RuntimeError from index_add_ about mismatched dtypes, raised in
#                        exllamav3/modules/block_sparse_mlp.py.
#   expected_behaviour : forward returns a finite (1, 4, H) torch.float result.
#   other              : anything else (including failing earlier, before the accumulation).
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
P = "model.layers.0"; KEY = f"{P}.block_sparse_moe"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H), f"{KEY}.gate.weight": n(E, H)}
for e in range(E):
    t[f"{KEY}.experts.{e}.w1.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w3.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w2.weight"] = n(H, IM)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["MixtralForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, num_local_experts=E, num_experts_per_tok=K, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5,
               rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
try:
    cfg = MixtralConfig(d)
    m = BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                       key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                       key_routing_gate="gate", qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.float)
    m.load(torch.device("cuda:0"))
    print("deepseekv3_routing:", getattr(m, "deepseekv3_routing", "n/a"), flush=True)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
x = (torch.randn(1, 4, H) * 0.5).half().cuda()
try:
    with torch.inference_mode(): y = m.forward(x, {})
    torch.cuda.synchronize()
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    hit = "index_add_" in str(e) and ("dtype" in str(e) or "scalar type" in str(e)) and site.startswith("exllamav3/modules/block_sparse_mlp.py")
    rt.report("stated_behaviour" if hit else "other", e, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e).splitlines()[0] if str(e) else ""); raise SystemExit
rt.report("expected_behaviour" if y.shape[-1] == H and y.dtype == torch.float and bool(y.isfinite().all()) else "other", shape=list(y.shape), dtype=str(y.dtype))
