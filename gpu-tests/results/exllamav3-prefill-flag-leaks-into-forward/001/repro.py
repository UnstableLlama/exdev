# Trigger: reuse the same params dictionary for an ordinary forward after Model.prefill, without clearing prefill.
# Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 unquantized. params = {};
# model.prefill(ids, params); y_reused = model.forward(ids, params); y_fresh = model.forward(ids, {}).
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : params["prefill"] is still True after prefill and y_reused differs from y_fresh
#                        (blocks returned after attention).
#   expected_behaviour : y_reused equals y_fresh.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3 import Model, Config, Tokenizer
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
config = Config.from_directory(M); model = Model.from_config(config); model.load(progressbar=False)
tok = Tokenizer.from_config(config); ids = tok.encode("The capital of France is")
params = {}
model.prefill(ids, params); flag = params.get("prefill")
y_reused = model.forward(ids, params).float(); y_fresh = model.forward(ids, {}).float()
diff = (y_reused - y_fresh).abs().max().item()
notes = dict(prefill_flag_after_prefill=flag, max_abs_logit_diff=diff,
             argmax_reused=int(y_reused[0, -1].argmax()), argmax_fresh=int(y_fresh[0, -1].argmax()))
print(notes, flush=True)
if flag and diff > 1e-2: rt.report("stated_behaviour", **notes)
elif diff <= 1e-2: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
