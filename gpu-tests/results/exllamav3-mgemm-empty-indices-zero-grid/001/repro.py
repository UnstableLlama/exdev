# Trigger: exl3_mgemm with rank-two indices of shape (1, 0), positive allocated input and output batch sizes
# and otherwise compatible dimensions (k = n = 1024, K = 4, automatic shape: positive SM count).
# Runs in a child process (the extension's gpu_assert exits the process on a CUDA error); the parent records how
# the call ended. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the wrapper attempts the launch: the child dies with a CUDA launch error (gpu_assert)
#                        or the call returns without rejecting the empty active set.
#   expected_behaviour : the call raises an ordinary exception before launch, or returns having launched nothing
#                        (output untouched) by explicit design.
#   other              : anything else.
import subprocess, sys
import rt
rt.check_import()
CHILD = r'''
import torch, sys
from exllamav3.ext import exllamav3_ext as ext
k = n = 1024; K = 4; dev = torch.device("cuda:0")
g = torch.Generator().manual_seed(0)
tr = torch.randint(-32768, 32767, (k // 16, n // 16, 16 * K), dtype=torch.int16, generator=g).to(dev)
suh = torch.ones(k, dtype=torch.half, device=dev); svh = torch.ones(n, dtype=torch.half, device=dev)
P = lambda t: torch.tensor([t.data_ptr()], dtype=torch.long, device=dev)
A = torch.randn(1, 1, k, dtype=torch.half, device=dev); Ah = torch.empty_like(A); C = torch.full((1, 1, n), -7.0, dtype=torch.half, device=dev)
idx = torch.empty(1, 0, dtype=torch.long, device=dev)
nargs = ext.exl3_mgemm.__doc__.split("\n")[0].count("arg")
print("CHILD calling", flush=True)
try:
    ext.exl3_mgemm(*([A, P(tr), C, P(suh), Ah, P(svh), idx, None, K, -1] + ([0, 0] if nargs >= 12 else []))); torch.cuda.synchronize()
except Exception as e:
    print("CHILD exception", type(e).__name__, str(e).splitlines()[0] if str(e) else "", flush=True); sys.exit(3)
print("CHILD returned untouched=%s" % bool((C == -7.0).all()), flush=True)
'''
r = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, timeout=120)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
notes = dict(child_lines=[l for l in r.stdout.splitlines() if l.startswith("CHILD")], child_returncode=r.returncode, child_stderr_tail=r.stderr.strip().splitlines()[-1:] )
if "GPU assert" in r.stderr or (r.returncode not in (0, 3) and "CHILD calling" in r.stdout): rt.report("stated_behaviour", etype="CUDA launch error (gpu_assert)", **notes)
elif r.returncode == 3 and "CUDA" not in r.stdout and "incompatible function" not in r.stdout: rt.report("expected_behaviour", **notes)
elif r.returncode == 0: rt.report("stated_behaviour", **notes)
else: rt.report("other", **notes)
