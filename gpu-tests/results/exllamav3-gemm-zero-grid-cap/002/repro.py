# Trigger: call exl3_mgemm with shape 2 forced, size_k=128 and size_n=128. The selector computes
# max_slices = (128/32)*(128/128)/12 = 0 and caps num_sms at 0; the host then evaluates total_sms / num_sms.
# A host-side integer division by zero raises SIGFPE and kills the process, so the call runs in a child
# process and the parent records how the child ended. The call goes straight to the extension's own
# exl3_mgemm binding (the ledger notes no Python caller reaches these sizes). Inputs are well-formed EXL3
# buffers for K=4 bits (trellis int16 [k/16, n/16, 16*K], suh/svh half) with random contents: only kernel
# selection and launch are under test, not numerical output. Upstream is not modified.
# Attempt 002: the call matches each commit's binding (10 arguments before mcg_mult/mul1_mult existed, 12 after),
# chosen from the binding's own signature text; a TypeError argument mismatch is classified did_not_run.
#
# Classification, fixed before running:
#   stated_behaviour   : child killed by SIGFPE (signal 8) inside the exl3_mgemm call.
#   expected_behaviour : child finishes the call and synchronizes (positive launch width), or the call is
#                        rejected with an ordinary exception before launch.
#   other              : any other ending (e.g. a CUDA launch error after the call returned).
import os, signal, subprocess, sys
import rt
rt.check_import()

CHILD = r'''
import sys, torch
from exllamav3.ext import exllamav3_ext as ext
k = n = 128; K = 4
torch.manual_seed(0)
dev = torch.device("cuda:0")
trellis = torch.randint(-32768, 32767, (k // 16, n // 16, 16 * K), dtype=torch.int16, device=dev)
suh = torch.ones(k, dtype=torch.half, device=dev); svh = torch.ones(n, dtype=torch.half, device=dev)
ptr = lambda t: torch.tensor([t.data_ptr()], dtype=torch.long, device=dev)
A = torch.randn(1, 1, k, dtype=torch.half, device=dev); A_had = torch.empty_like(A)
C = torch.zeros(1, 1, n, dtype=torch.half, device=dev)
indices = torch.zeros(1, 1, dtype=torch.long, device=dev)
print("CHILD calling exl3_mgemm k=128 n=128 K=4 force_shape_idx=2", flush=True)
try:
    nargs = ext.exl3_mgemm.__doc__.split("\n")[0].count("arg")
    print("CHILD binding arity", nargs, flush=True)
    base = [A, ptr(trellis), C, ptr(suh), A_had, ptr(svh), indices, None, K, 2]
    ext.exl3_mgemm(*(base + [0, 0] if nargs >= 12 else base))
    torch.cuda.synchronize()
except Exception as e:
    print("CHILD exception", type(e).__name__, str(e).splitlines()[0] if str(e) else "", flush=True); sys.exit(3)
print("CHILD returned; C finite:", bool(C.isfinite().all()), flush=True)
sys.exit(0)
'''
r = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, timeout=300)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
rc = r.returncode
called = "CHILD calling" in r.stdout
notes = dict(child_returncode=rc, child_signal=(signal.Signals(-rc).name if rc < 0 else None), reached_call=called,
             child_stdout_tail=r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")
if called and rc == -signal.SIGFPE:
    rt.report("stated_behaviour", etype="SIGFPE", esite="exllamav3_ext exl3_mgemm (host, total_sms / num_sms)", **notes)
elif called and rc == 0:
    rt.report("expected_behaviour", **notes)
elif called and rc == 3 and "CHILD exception TypeError" in r.stdout and "incompatible function arguments" in r.stdout:
    rt.report("did_not_run", **notes)
elif called and rc == 3 and "CHILD exception RuntimeError" in r.stdout and "CUDA" not in r.stdout:
    rt.report("expected_behaviour", etype=r.stdout.split("CHILD exception ")[1].split()[0], **notes)
elif not called:
    rt.report("did_not_run", **notes)
else:
    rt.report("other", **notes)
