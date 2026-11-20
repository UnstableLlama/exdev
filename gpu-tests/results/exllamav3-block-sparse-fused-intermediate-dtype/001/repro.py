# Trigger: one flattened token and fully EXL3 experts select the fused path, with interm_dtype unset.
# Fixture as in all-expert-fused-shape: a tiny random 1-layer MixtralForCausalLM (4 experts, top 2) quantized to
# 4 bpw EXL3 at the commit under test. The same quantized layer is constructed twice with MixtralModel's arguments,
# once with interm_dtype=torch.half (as MixtralModel passes) and once with interm_dtype left unset, and both are
# run on the same token. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the unset-dtype output is non-finite or differs from the half-dtype output by more
#                        than 10x the tolerance (activation read float32 bytes as half).
#   expected_behaviour : outputs agree within tolerance, or the unset dtype is rejected with a dtype error.
#   other              : anything else.
import json, os, shutil, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import BlockSparseMLP
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
def moe(cfg, **kw):
    return BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                          key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                          key_routing_gate="gate", qmap="block.mlp", out_dtype=torch.half, **kw)
cfg = Config.from_directory(out); dev = torch.device("cuda:0")
torch.manual_seed(1)
x = (torch.randn(1, 1, H) * 0.5).half().cuda()
outs = {}
for name, kw in (("half", {"interm_dtype": torch.half}), ("unset", {})):
    m = moe(cfg, **kw); m.load(dev)
    try:
        with torch.inference_mode(): outs[name] = m.forward(x.clone(), {}).float()
        torch.cuda.synchronize()
    except Exception as e:
        outs[name] = e
    print(name, "is_quantized:", m.is_quantized, "interm_dtype:", m.interm_dtype, flush=True); m.unload()
h, u = outs["half"], outs["unset"]
if isinstance(h, Exception): rt.report("did_not_run", h, message=str(h)); raise SystemExit
if isinstance(u, Exception): rt.report("expected_behaviour" if isinstance(u, (TypeError, RuntimeError, AssertionError, ValueError)) and "dtype" in str(u).lower() else "other", u, message=str(u).splitlines()[0]); raise SystemExit
diff = (u - h).abs().max().item(); fin = bool(u.isfinite().all())
notes = dict(max_abs_diff_unset_vs_half=diff, unset_finite=fin, half_max_abs=h.abs().max().item())
tol = 1e-2 * max(1.0, h.abs().max().item())
if (not fin) or diff > 10 * tol: rt.report("stated_behaviour", **notes)
elif diff <= tol: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
