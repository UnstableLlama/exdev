# Trigger: construct an ordinary MLP with activation_fn="relu", then call forward.
# Fixture: a tiny checkpoint with one up/down pair (256 -> 512 -> 256), loaded unquantized. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : construction succeeds and forward raises AttributeError for activation_fn_call
#                        (exllamav3/modules/mlp.py).
#   expected_behaviour : construction rejects "relu", or forward applies a defined activation.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import MLP
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4, num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
p = "model.layers.0.mlp"
save_file({"model.norm.weight": torch.ones(256).half(), f"{p}.up_proj.weight": (torch.randn(512, 256) * .05).half(), f"{p}.down_proj.weight": (torch.randn(256, 512) * .05).half()}, d + "/model.safetensors")
cfg = Config.from_directory(d)
try:
    m = MLP(config=cfg, key=p, hidden_size=256, intermediate_size=512, key_up="up_proj", key_down="down_proj", qmap="block.mlp", activation_fn="relu")
except Exception as e:
    rt.report("expected_behaviour", e, stage="construction", message=str(e)); raise SystemExit
m.load(torch.device("cuda:0"))
try:
    with torch.inference_mode(): y = m.forward(torch.randn(1, 4, 256, dtype=torch.half, device="cuda:0"), {})
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "activation_fn_call" in str(e) and site.startswith("exllamav3/modules/mlp.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour", note="forward ran", shape=list(y.shape))
