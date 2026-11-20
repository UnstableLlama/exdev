# Trigger: BlockSparseMLP.forward with one flattened token, fully EXL3 experts, activate_all_experts=True and
# num_experts (4) different from num_experts_per_tok (2).
# Fixture: a tiny random 1-layer MixtralForCausalLM (4 experts, top 2) quantized to 4 bpw EXL3 with the
# repository's own converter at the commit under test, Qwen2.5-0.5B-Instruct tokenizer files. BlockSparseMLP is
# constructed with MixtralModel's arguments. Reference: the same layer on a 2-token batch of the same token
# (ordinary path, which supports all-expert evaluation), first row. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the one-token fused call raises RuntimeError from the multi-GEMM index-count check,
#                        reached from exllamav3/modules/block_sparse_mlp.py.
#   expected_behaviour : the one-token call returns output matching the all-expert ordinary-path reference.
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
m = moe(cfg, interm_dtype=torch.half); m.load(dev)
print("is_quantized:", m.is_quantized, flush=True)
x = (torch.randn(1, 1, H) * 0.5).half().cuda()
with torch.inference_mode():
    ref = m.forward(torch.cat([x, x], dim=1), {"activate_all_experts": True})[:, :1].float()   # ordinary path, 2 tokens
try:
    with torch.inference_mode(): y = m.forward(x.clone(), {"activate_all_experts": True}).float()
    torch.cuda.synchronize()
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/modules/block_sparse_mlp.py") and m.is_quantized else "other", e,
              fused_branch_eligible=bool(m.is_quantized), message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e).splitlines()[0] if str(e) else ""); raise SystemExit
diff = (y - ref).abs().max().item()
rt.report("expected_behaviour" if m.is_quantized and diff <= 1e-2 * max(1.0, ref.abs().max().item()) else "other",
          fused_branch_eligible=bool(m.is_quantized), max_abs_diff_vs_all_expert_ordinary_path=diff, ref_max_abs=ref.abs().max().item())
