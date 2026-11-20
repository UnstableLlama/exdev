# Trigger: ext.rms_norm with input/output dtype other than float32/float16 (here bfloat16) while satisfying its
# shape and weight checks (weight FP16, last dim divisible by 4, x and y same shape). Runs in a child process.
# The output is compared with an RMSNorm computed in float32 by torch. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the call is accepted (no exception) and the bfloat16 output does not match the reference.
#   expected_behaviour : the call raises an exception rejecting the dtype.
#   other              : anything else.
import subprocess, sys
import rt
rt.check_import()
CHILD = r'''
import torch, sys
from exllamav3.ext import exllamav3_ext as ext
torch.manual_seed(0)
x = torch.randn(4, 256, device="cuda:0").bfloat16(); w = torch.ones(256, dtype=torch.half, device="cuda:0"); y = torch.empty_like(x)
try:
    ext.rms_norm(x, w, y, 1e-6, 0.0); torch.cuda.synchronize()
except Exception as e:
    print("CHILD exception", type(e).__name__, str(e).splitlines()[0] if str(e) else "", flush=True); sys.exit(3)
xf = x.float(); ref = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + 1e-6)
print("CHILD returned maxdiff=%r finite=%s" % ((y.float() - ref).abs().max().item(), bool(y.float().isfinite().all())), flush=True)
'''
r = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, timeout=120)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
line = [l for l in r.stdout.splitlines() if l.startswith("CHILD")]
notes = dict(child_lines=line, child_returncode=r.returncode)
import re
m = re.search(r"maxdiff=([^ ]+)", r.stdout)
if r.returncode == 3: rt.report("expected_behaviour", **notes)
elif m and (m.group(1) == "nan" or float(m.group(1)) > 0.05): rt.report("stated_behaviour", **notes)
else: rt.report("other", **notes)
