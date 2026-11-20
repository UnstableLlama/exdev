# Trigger: supply shared_experts and forward exactly one flattened token with all routed expert projections
# stored as EXL3.
# Fixture: a tiny random 1-layer MixtralForCausalLM checkpoint (4 experts, top 2), quantized to EXL3 with the
# repository's own converter at the commit under test (convert_model parser/prepare/main, in-process).
# No built-in constructor supplies shared_experts at these commits, so BlockSparseMLP is constructed directly
# with the same arguments MixtralModel uses, plus shared_experts = a GatedMLP over expert 0's EXL3 tensors
# (any EXL3 gated MLP will do as the shared branch). Upstream is not modified.
#
# Classification, fixed before running (one token, shape (1, 1, H)):
#   stated_behaviour   : output with shared_experts equals the routed-only output (shared branch skipped).
#   expected_behaviour : output equals routed-only output + shared GatedMLP output.
#   other              : neither, or the fused branch was not taken (layer not fully EXL3).
import json, os, shutil, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import BlockSparseMLP, GatedMLP
from exllamav3.conversion.convert_model import parser, prepare, main

QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, IM, E, K, V = 256, 512, 4, 2, 151936
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
P = "model.layers.0"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{P}.input_layernorm.weight": torch.ones(H).half(), f"{P}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{P}.block_sparse_moe.gate.weight": n(E, H)}
for k in "qkvo": t[f"{P}.self_attn.{k}_proj.weight"] = n(H, H)
for e in range(E):
    t[f"{P}.block_sparse_moe.experts.{e}.w1.weight"] = n(IM, H)
    t[f"{P}.block_sparse_moe.experts.{e}.w3.weight"] = n(IM, H)
    t[f"{P}.block_sparse_moe.experts.{e}.w2.weight"] = n(H, IM)
root = tempfile.mkdtemp(); src, work, out = (os.path.join(root, x) for x in ("src", "work", "out")); os.makedirs(src)
for f in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"): shutil.copy(os.path.join(QWEN, f), src)
json.dump(dict(architectures=["MixtralForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, num_local_experts=E, num_experts_per_tok=K, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5,
               rope_theta=10000.0, max_position_embeddings=2048, bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False,
               torch_dtype="float16"), open(os.path.join(src, "config.json"), "w"))
save_file(t, os.path.join(src, "model.safetensors"))

try:
    a = parser.parse_args(["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "-d", "0"])
    in_args, job_state, ok, err = prepare(a)
    assert ok, f"prepare failed: {err}"
    main(in_args, job_state)
    print("converted:", sorted(os.listdir(out)), flush=True)
except Exception as e:
    rt.report("did_not_run", e, stage="conversion", message=str(e)); raise SystemExit

KEY = f"{P}.block_sparse_moe"
def moe(cfg, shared):
    return BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                          key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                          key_routing_gate="gate", qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.half, shared_experts=shared)
def gmlp(cfg):
    return GatedMLP(config=cfg, key=f"{KEY}.experts.0", hidden_size=H, intermediate_size=IM, key_up="w3", key_gate="w1",
                    key_down="w2", qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.half)
try:
    cfg = Config.from_directory(out)
    dev = torch.device("cuda:0")
    m_shared = moe(cfg, gmlp(cfg)); m_shared.load(dev)
    m_plain = moe(cfg, None); m_plain.load(dev)
    shared = gmlp(cfg); shared.load(dev)
    print("is_quantized:", m_shared.is_quantized, m_plain.is_quantized,
          "shared inner:", type(shared.gates[0].inner).__name__, flush=True)
    x = (torch.randn(1, 1, H) * 0.5).half().cuda()
    with torch.inference_mode():
        y_shared = m_shared.forward(x.clone(), {}).float()
        y_plain = m_plain.forward(x.clone(), {}).float()
        s = shared.forward(x.clone(), {}).float()
    torch.cuda.synchronize()
except Exception as e:
    rt.report("did_not_run", e, stage="forward", message=str(e)); raise SystemExit

d_plain = (y_shared - y_plain).abs().max().item()
d_sum = (y_shared - (y_plain + s)).abs().max().item()
notes = dict(fused_branch_eligible=bool(m_shared.is_quantized), shared_out_max_abs=s.abs().max().item(),
             max_abs_diff_vs_routed_only=d_plain, max_abs_diff_vs_routed_plus_shared=d_sum, out_shape=list(y_shared.shape))
tol = 1e-2 * max(1.0, s.abs().max().item())
if not m_shared.is_quantized: rt.report("other", **notes)
elif d_plain <= 1e-3 and d_sum > tol: rt.report("stated_behaviour", **notes)
elif d_sum <= tol and d_plain > tol: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
