# Trigger: eval/compare_q_logits.py reaches save_tensor after successful forwarding.
# Third-party imports are stubbed; the wikitext data source is replaced by random token ids. The model is real.
import argparse, json, os, sys
import torch
from safetensors import safe_open
import rt, cq
rt.check_import()
import compare_q_logits as L
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
torch.manual_seed(0)
L.get_test_data = lambda spec: torch.randint(100, 5000, (2, 32))
out = os.path.join(cq.TMP, "logits.safetensors"); d = os.path.join(cq.TMP, "d.json"); json.dump(cq.DATA, open(d, "w"))
try:
    L.main(argparse.Namespace(model_dir=M, dataspec=d, device=0, rows=2, rows_per_batch=1, out_logits=out))
except Exception as e:
    import traceback
    frames = [f.name for f in traceback.extract_tb(e.__traceback__)]
    rt.report("stated_behaviour" if "save_tensor" in frames else "other", e, message=str(e)[:300], frames=frames[-4:], file_written=os.path.exists(out))
else:
    with safe_open(out, framework="pt") as f: k = sorted(f.keys())
    rt.report("expected_behaviour" if k == ["tensor.0", "tensor.1"] else "other", keys=k)
