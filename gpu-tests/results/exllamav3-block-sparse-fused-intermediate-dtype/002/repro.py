# Trigger: one flattened token and fully EXL3 experts select the fused path, with interm_dtype unset.
# At 6fc153d7a062 BlockSparseMLP has just been added and no architecture uses it, so the converter cannot produce
# an MoE checkpoint. Fixture (disclosed): a tiny random 4-layer LlamaForCausalLM (hidden 256, intermediate 512)
# is quantized to 4 bpw EXL3 with the repository's own converter at this commit; the script then copies, without
# changing any tensor, layer e's quantized mlp.{gate,up,down}_proj tensors to
# model.layers.0.block_sparse_moe.experts.{e}.{w1,w3,w2} and adds an FP16 router gate (4 x 256), giving 4 EXL3
# experts. BlockSparseMLP (top 2) is constructed twice on that checkpoint, with interm_dtype=torch.half and
# with interm_dtype unset, and both are run on the same single token. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the unset-dtype output is non-finite or differs from the half-dtype output by more
#                        than 10x the tolerance (activation read float32 bytes as half).
#   expected_behaviour : outputs agree within tolerance, or the unset dtype is rejected with a dtype error.
#   other              : anything else.
import json, os, shutil, tempfile
import torch
from safetensors.torch import save_file, load_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import BlockSparseMLP
from exllamav3.conversion.convert_model import parser, prepare, main
QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, IM, E, K, V, L = 256, 512, 4, 2, 151936, 4
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
for i in range(L):
    p = f"model.layers.{i}"
    t[f"{p}.input_layernorm.weight"] = torch.ones(H).half(); t[f"{p}.post_attention_layernorm.weight"] = torch.ones(H).half()
    for k in "qkvo": t[f"{p}.self_attn.{k}_proj.weight"] = n(H, H)
    t[f"{p}.mlp.gate_proj.weight"] = n(IM, H); t[f"{p}.mlp.up_proj.weight"] = n(IM, H); t[f"{p}.mlp.down_proj.weight"] = n(H, IM)
root = tempfile.mkdtemp(); src, work, out, moe_dir = (os.path.join(root, x) for x in ("src", "work", "out", "moe")); os.makedirs(src)
for f in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"): shutil.copy(os.path.join(QWEN, f), src)
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=L, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=2048,
               bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False, torch_dtype="float16"), open(os.path.join(src, "config.json"), "w"))
save_file(t, os.path.join(src, "model.safetensors"))
try:
    a = parser.parse_args(["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "-d", "0"])
    in_args, job_state, ok, err = prepare(a); assert ok, err
    main(in_args, job_state)
except Exception as e:
    rt.report("did_not_run", e, stage="conversion", message=str(e)); raise SystemExit
shutil.copytree(out, moe_dir, ignore=shutil.ignore_patterns("*.safetensors"))
q = {}
for f in os.listdir(out):
    if f.endswith(".safetensors"): q.update(load_file(os.path.join(out, f)))
KEY = "model.layers.0.block_sparse_moe"
moe_t = {k: v for k, v in q.items() if not k.startswith("model.layers.")}
for e in range(E):
    for s, d in (("gate_proj", "w1"), ("up_proj", "w3"), ("down_proj", "w2")):
        pre = f"model.layers.{e}.mlp.{s}."
        for k, v in q.items():
            if k.startswith(pre): moe_t[f"{KEY}.experts.{e}.{d}." + k[len(pre):]] = v
moe_t[f"{KEY}.gate.weight"] = n(E, H)
save_file(moe_t, os.path.join(moe_dir, "model.safetensors"))
print("expert tensor suffixes:", sorted({k.split(".")[-1] for k in moe_t if ".experts.0.w1." in k}), flush=True)
cfg = Config.from_directory(moe_dir); dev = torch.device("cuda:0")
def moe(**kw):
    return BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                          key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                          key_routing_gate="gate", qmap="block.mlp", out_dtype=torch.half, **kw)
torch.manual_seed(1); x = (torch.randn(1, 1, H) * 0.5).half().cuda()
outs, quant = {}, {}
for name, kw in (("half", {"interm_dtype": torch.half}), ("unset", {})):
    m = moe(**kw); m.load(dev); quant[name] = bool(getattr(m, "is_quantized", False))
    try:
        with torch.inference_mode(): outs[name] = m.forward(x.clone(), {}).float()
        torch.cuda.synchronize()
    except Exception as e:
        outs[name] = e
    m.unload()
print("is_quantized:", quant, flush=True)
h, u = outs["half"], outs["unset"]
if not all(quant.values()): rt.report("other", note="fused path not eligible", is_quantized=quant); raise SystemExit
if isinstance(h, Exception): rt.report("did_not_run", h, message=str(h)); raise SystemExit
if isinstance(u, Exception):
    rt.report("expected_behaviour" if "dtype" in str(u).lower() else "other", u, message=str(u).splitlines()[0]); raise SystemExit
diff = (u - h).abs().max().item(); fin = bool(u.isfinite().all())
notes = dict(max_abs_diff_unset_vs_half=diff, unset_finite=fin, half_max_abs=h.abs().max().item(), is_quantized=quant)
tol = 1e-2 * max(1.0, h.abs().max().item())
if (not fin) or diff > 10 * tol: rt.report("stated_behaviour", **notes)
elif diff <= tol: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
