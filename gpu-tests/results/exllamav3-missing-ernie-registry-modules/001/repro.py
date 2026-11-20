# Trigger: import exllamav3.models.architectures, including through Config.from_directory.
# Two steps, each recorded: (1) import exllamav3.models.architectures directly; (2) Config.from_directory on a
# minimal LlamaForCausalLM config.json (one tensor; no real weights are needed to resolve the architecture).
# Classification, fixed before running:
#   stated_behaviour   : both steps raise ModuleNotFoundError for exllamav3.models.ernie4_5 (or ernie4_5_moe).
#   expected_behaviour : both steps succeed and the config resolves to the Llama architecture.
#   other              : anything else.
import json, os, tempfile
import rt
rt.check_import()
steps = {}
try:
    import exllamav3.models.architectures as A
    steps["registry_import"] = {"ok": True, "n_architectures": len(A.ARCHITECTURES) if hasattr(A, "ARCHITECTURES") else None}
except Exception as e:
    steps["registry_import"] = {"ok": False, "exception_type": type(e).__name__, "message": str(e), "site": rt._site(e.__traceback__)}
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0,
               max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
from safetensors.torch import save_file
import torch
save_file({"model.norm.weight": torch.ones(256).half()}, d + "/model.safetensors")
try:
    from exllamav3 import Config
    c = Config.from_directory(d)
    steps["config_from_directory"] = {"ok": True, "config_class": type(c).__name__}
except Exception as e:
    steps["config_from_directory"] = {"ok": False, "exception_type": type(e).__name__, "message": str(e), "site": rt._site(e.__traceback__)}
print(steps, flush=True)
ern = lambda s: (not s["ok"]) and s["exception_type"] == "ModuleNotFoundError" and "ernie4_5" in s["message"]
r, c = steps["registry_import"], steps["config_from_directory"]
if ern(r) and ern(c): rt.report("stated_behaviour", etype="ModuleNotFoundError", esite=r["site"], **steps)
elif r["ok"] and c["ok"] and "Llama" in c["config_class"]: rt.report("expected_behaviour", **steps)
else: rt.report("other", **steps)
