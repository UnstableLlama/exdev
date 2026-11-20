# Trigger: ext.histogram with nonempty contiguous CUDA float input, an empty kLong output, min_value=0,
# max_value=1, exclusive=false. Runs in a child process (an out-of-range shared-memory write may corrupt the
# CUDA context); the parent records how the call ended. Input includes 0.0. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the call is not rejected before launch: it returns, or fails only with a CUDA
#                        error from the launched kernel (illegal address etc.).
#   expected_behaviour : the call raises an ordinary exception naming the bin count before launching.
#   other              : anything else.
import subprocess, sys
import rt
rt.check_import()
CHILD = r'''
import torch, sys
from exllamav3.ext import exllamav3_ext as ext
x = torch.tensor([0.0, 0.25, 0.5, 0.75], device="cuda:0"); out = torch.empty(0, dtype=torch.long, device="cuda:0")
try:
    ext.histogram(x, out, 0.0, 1.0, False)
    print("CHILD returned", flush=True)
except Exception as e:
    print("CHILD exception", type(e).__name__, str(e).splitlines()[0] if str(e) else "", flush=True); sys.exit(3)
try:
    torch.cuda.synchronize(); print("CHILD synchronized", flush=True)
except Exception as e:
    print("CHILD sync_error", type(e).__name__, str(e).splitlines()[0], flush=True); sys.exit(4)
'''
r = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, timeout=120)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
lines = [l for l in r.stdout.splitlines() if l.startswith("CHILD")]
notes = dict(child_lines=lines, child_returncode=r.returncode)
if r.returncode == 3 and "CUDA" not in r.stdout: rt.report("expected_behaviour", **notes)
elif "CHILD returned" in r.stdout: rt.report("stated_behaviour", **notes)
else: rt.report("other", **notes)
