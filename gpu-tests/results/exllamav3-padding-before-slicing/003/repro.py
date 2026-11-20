# Trigger: load a full 512x64 weight into a Linear requesting 130 outputs and 64 inputs, with
# full_out_features=512, first_out_feature=0 and the default pad_to=128.
# Fixture: a tiny checkpoint holding the 512x64 weight under one key; Linear is constructed directly and loaded
# unquantized on cuda:0. Attempt 003: 128 inputs and a 512x128 weight, so no input padding is involved and only the
# output side (130 outputs padded to 256, full 512) differs from the ledger trigger (64 inputs, which the constructor
# rejects at this pad_to; attempt 001). The expected local weight is rows 0..129 of the full weight (as input x output after
# the loader's transpose), padded to 256 outputs. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : load raises a shape-mismatch RuntimeError from the padding step (exllamav3/modules/linear.py).
#   expected_behaviour : load succeeds and the first 130 output columns equal the full weight's rows 0..129.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import Linear
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4, num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
W = (torch.randn(512, 128) * .05).half()
save_file({"model.norm.weight": torch.ones(256).half(), "x.proj.weight": W}, d + "/model.safetensors")
cfg = Config.from_directory(d)
lin = Linear(config=cfg, key="x.proj", in_features=128, out_features=130, full_in_features=128, full_out_features=512, first_in_feature=0, first_out_feature=0)
print("padded out_features:", lin.out_features, flush=True)
try:
    lin.load(torch.device("cuda:0"))
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/modules/linear.py") else "other", e, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
w = lin.inner.get_weight_tensor().cpu()
ok = w.shape[1] >= 130 and torch.equal(w[:, :130], W[:130].T)
rt.report("expected_behaviour" if ok else "other", loaded_shape=list(w.shape))
