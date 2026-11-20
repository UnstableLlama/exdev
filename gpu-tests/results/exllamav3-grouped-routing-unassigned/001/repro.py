# Trigger: enable DeepSeek-V3 routing on BlockSparseMLP with n_group or topk_group different from 1
# (including the default None values), then forward.
# Fixture: a tiny random unquantized MoE layer (8 experts, top 2, with gate.e_score_correction_bias) in a
# MixtralForCausalLM-shaped checkpoint; BlockSparseMLP is constructed directly (no built-in constructor
# enables DS3 routing at the affected commits).
# API adaptation, disclosed: the affected commits enable DS3 routing with deepseekv3_routing=True; the fix
# replaces that flag with router_type="ds3". The script passes whichever the commit's constructor accepts,
# with identical n_group / topk_group / routed_scaling_factor. Upstream is not modified.
#
# Classification, fixed before running, on the primary case (n_group=4, topk_group=2, 4 tokens):
#   stated_behaviour   : forward raises UnboundLocalError/NameError for selected_experts in block_sparse_mlp.py.
#   expected_behaviour : forward returns a finite (4, H) result, or raises an explicit configuration error
#                        before routing.
#   other              : anything else.
# The secondary case (n_group/topk_group left at None) is run and recorded in notes only.
import inspect, json, os, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import BlockSparseMLP

H, IM, E, K, V = 256, 256, 8, 2, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
P = "model.layers.0"; KEY = f"{P}.block_sparse_moe"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{P}.input_layernorm.weight": torch.ones(H).half(), f"{P}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{KEY}.gate.weight": n(E, H), f"{KEY}.gate.e_score_correction_bias": (torch.randn(E) * 0.1).float()}
for k in "qkvo": t[f"{P}.self_attn.{k}_proj.weight"] = n(H, H)
for e in range(E):
    t[f"{KEY}.experts.{e}.w1.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w3.weight"] = n(IM, H); t[f"{KEY}.experts.{e}.w2.weight"] = n(H, IM)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["MixtralForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, num_local_experts=E, num_experts_per_tok=K, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5,
               rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False),
          open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")

params = inspect.signature(BlockSparseMLP.__init__).parameters
api = "router_type" if "router_type" in params else "deepseekv3_routing" if "deepseekv3_routing" in params else None
print("DS3 API at this commit:", api, flush=True)
if api is None:
    rt.report("did_not_run", message="BlockSparseMLP has neither deepseekv3_routing nor router_type"); raise SystemExit
flag = {"router_type": "ds3"} if api == "router_type" else {"deepseekv3_routing": True}

cfg = Config.from_directory(d); dev = torch.device("cuda:0")
x = (torch.randn(1, 4, H) * 0.5).half().cuda()
def run(**grp):
    m = BlockSparseMLP(config=cfg, key=KEY, hidden_size=H, intermediate_size=IM, num_experts=E, num_experts_per_tok=K,
                       key_up="experts.{expert_idx}.w3", key_gate="experts.{expert_idx}.w1", key_down="experts.{expert_idx}.w2",
                       key_routing_gate="gate", qmap="block.mlp", interm_dtype=torch.half, out_dtype=torch.half,
                       routed_scaling_factor=1.0, **flag, **grp)
    m.load(dev)
    try:
        with torch.inference_mode(): y = m.forward(x.clone(), {})
        torch.cuda.synchronize()
        return dict(ok=True, shape=list(y.shape), finite=bool(y.float().isfinite().all())), None
    except Exception as e:
        return dict(ok=False, exception_type=type(e).__name__, site=rt._site(e.__traceback__), message=str(e).splitlines()[0] if str(e) else ""), e
    finally:
        m.unload()

try:
    sec, _ = run()  # defaults: n_group=None, topk_group=None
    print("secondary (None groups):", sec, flush=True)
    pri, exc = run(n_group=4, topk_group=2)
    print("primary (n_group=4, topk_group=2):", pri, flush=True)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit

notes = dict(api=api, primary=pri, secondary_none_groups=sec)
unbound = (not pri["ok"] and pri["exception_type"] in ("UnboundLocalError", "NameError") and "selected_experts" in pri["message"]
           and (pri["site"] or "").startswith("exllamav3/modules/block_sparse_mlp.py"))
if unbound: rt.report("stated_behaviour", exc, **notes)
elif pri["ok"] and pri["finite"] and pri["shape"][-1] == H: rt.report("expected_behaviour", **notes)
elif not pri["ok"] and pri["exception_type"] in ("ValueError", "AssertionError", "NotImplementedError"):
    rt.report("expected_behaviour", exc, **notes)
else: rt.report("other", exc, **notes)
