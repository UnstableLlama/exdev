# Trigger: call allocate_q on a block containing a plain (ungated) MLP with a valid quantization budget.
# A TransformerBlock (mlp_norm + plain MLP, no attention) and a ParallelDecoderBlock (input_norm + plain MLP) are
# built over a tiny checkpoint and loaded unquantized; allocate_q({"bits": 4.0}, 0) is called on each.
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : both raise AttributeError for .ups/.downs (plain MLP exposes .up/.down) from
#                        exllamav3/modules/transformer.py.
#   expected_behaviour : both return a strategy covering the MLP's up and down projections.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import TransformerBlock, ParallelDecoderBlock, MLP, RMSNorm
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4, num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
p = "model.layers.0"
save_file({"model.norm.weight": torch.ones(256).half(), f"{p}.post_attention_layernorm.weight": torch.ones(256).half(),
           f"{p}.input_layernorm.weight": torch.ones(256).half(),
           f"{p}.mlp.up_proj.weight": (torch.randn(512, 256) * .05).half(), f"{p}.mlp.down_proj.weight": (torch.randn(256, 512) * .05).half()}, d + "/model.safetensors")
cfg = Config.from_directory(d)
mk = lambda: MLP(config=cfg, key=f"{p}.mlp", hidden_size=256, intermediate_size=512, key_up="up_proj", key_down="down_proj", qmap="block.mlp")
blocks = {"TransformerBlock": TransformerBlock(config=cfg, key=p, mlp_norm=RMSNorm(config=cfg, key=f"{p}.post_attention_layernorm", rms_norm_eps=1e-5), mlp=mk()),
          "ParallelDecoderBlock": ParallelDecoderBlock(config=cfg, key=p, input_norm=RMSNorm(config=cfg, key=f"{p}.input_layernorm", rms_norm_eps=1e-5), mlp=mk())}
res = {}; exc = None
for name, b in blocks.items():
    b.load(torch.device("cuda:0"))
    try:
        s, _ = b.allocate_q({"bits": 4.0}, 0); res[name] = {"ok": True, "keys": sorted(s)}
    except AttributeError as e:
        res[name] = {"ok": False, "exception_type": "AttributeError", "message": str(e), "site": rt._site(e.__traceback__)}; exc = e
    except Exception as e:
        res[name] = {"ok": False, "exception_type": type(e).__name__, "message": str(e), "site": rt._site(e.__traceback__)}; exc = e
print(res, flush=True)
if all((not r["ok"]) and r["exception_type"] == "AttributeError" and ("ups" in r["message"] or "downs" in r["message"]) for r in res.values()): rt.report("stated_behaviour", exc, **res)
elif all(r["ok"] for r in res.values()): rt.report("expected_behaviour", **res)
else: rt.report("other", exc, **res)
