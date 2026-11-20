# Trigger: call allocate_transformer with g=None and list-valued u and d.
# Real Linear modules (sliced up/down projections, 2 slices each) are built over a tiny checkpoint, loaded
# unquantized, and passed as u=[up0, up1], d=[down0, down1], g=None, with q/k/v/o None. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : TypeError "unhashable type: 'list'" from exllamav3/conversion/allocation.py.
#   expected_behaviour : returns a strategy dict keyed by concrete module keys.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import Linear
from exllamav3.conversion.allocation import allocate_transformer
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
t = {"model.norm.weight": torch.ones(256).half()}
for i in range(2):
    t[f"m.up.slice.{i}.weight"] = (torch.randn(256, 256) * .05).half(); t[f"m.down.slice.{i}.weight"] = (torch.randn(256, 256) * .05).half()
save_file(t, d + "/model.safetensors")
cfg = Config.from_directory(d)
ups = [Linear(config=cfg, key=f"m.up.slice.{i}", in_features=256, out_features=256, qmap="block.mlp") for i in range(2)]
downs = [Linear(config=cfg, key=f"m.down.slice.{i}", in_features=256, out_features=256, qmap="block.mlp") for i in range(2)]
for m in ups + downs: m.load(torch.device("cuda:0"))
try:
    strat, surplus = allocate_transformer(4.0, 0, None, None, None, None, None, ups, downs)
except TypeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "unhashable" in str(e) and site.startswith("exllamav3/conversion/allocation.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour", strategy_keys=sorted(strat.keys()))
