# Trigger: select the same GEMM kernel on another CUDA device after it has been cached on the first device.
# Runs with physical GPUs 0 and 1 visible (user approval 2026-11-19 for this test). The extension's own
# exl3_gemm binding is called directly with well-formed K=4 EXL3 buffers (random contents, generated on CPU
# from a fixed seed so both devices get identical inputs). Shape 1x2048x2048, automatic kernel selection;
# these kernels launch with SMEM_MAX = 90 KB dynamic shared memory, above the 48 KB default, so a device
# without cudaFuncSetAttribute should refuse the launch. Each scenario runs in a fresh child process because
# the cached set is process-global and a CUDA error is sticky. Upstream is not modified.
#   test    : exl3_gemm on cuda:0, then the same call on cuda:1, in one process.
#   control : exl3_gemm on cuda:1 only.
# Classification, fixed before running:
#   stated_behaviour   : the control succeeds, and in the test the cuda:1 call fails with a CUDA error or its
#                        output differs from the control's.
#   expected_behaviour : the control succeeds and the test's cuda:1 output equals the control's exactly.
#   other              : anything else (including the control failing).
import json, subprocess, sys
import rt
rt.check_import()
CHILD = r'''
import json, sys, torch
from exllamav3.ext import exllamav3_ext as ext
order = sys.argv[1].split(",")
m, k, n, K = 1, 2048, 2048, 4
g = torch.Generator().manual_seed(0)
trellis = torch.randint(-32768, 32767, (k // 16, n // 16, 16 * K), dtype=torch.int16, generator=g)
suh = (torch.randn(k, generator=g) * 0.1).half(); svh = (torch.randn(n, generator=g) * 0.1).half()
A = torch.randn(m, k, generator=g).half()
res = {"devices": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]}
for dname in order:
    dev = torch.device(dname)
    try:
        C = torch.zeros(m, n, dtype=torch.half, device=dev)
        Ad = A.to(dev); Ah = torch.empty_like(Ad)
        shape = ext.exl3_gemm(Ad, trellis.to(dev), C, suh.to(dev), Ah, svh.to(dev), -1, 0, 0)
        torch.cuda.synchronize(dev)
        res[dname] = {"ok": True, "shape_idx": shape, "out": C.float().cpu().tolist()[0][:64], "sum": float(C.float().sum().cpu()), "finite": bool(C.isfinite().all())}
    except Exception as e:
        res[dname] = {"ok": False, "exception_type": type(e).__name__, "message": str(e).splitlines()[0] if str(e) else ""}
        break
print("CHILDRESULT " + json.dumps(res), flush=True)
'''
def run(order):
    r = subprocess.run([sys.executable, "-c", CHILD, order], capture_output=True, text=True, timeout=300)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
    line = [l for l in r.stdout.splitlines() if l.startswith("CHILDRESULT ")]
    return (json.loads(line[-1][12:]) if line else None), r.returncode
test, rc_t = run("cuda:0,cuda:1")
ctl, rc_c = run("cuda:1")
if test is None or ctl is None:
    rt.report("did_not_run", test_returncode=rc_t, control_returncode=rc_c); raise SystemExit
t1, c1 = test.get("cuda:1"), ctl.get("cuda:1")
brief = lambda r: None if r is None else {k: v for k, v in r.items() if k != "out"}
notes = dict(devices=test["devices"], test_cuda0=brief(test.get("cuda:0")), test_cuda1=brief(t1), control_cuda1=brief(c1))
if not (c1 and c1["ok"]) or not test.get("cuda:0", {}).get("ok"): rt.report("other", **notes)
elif not (t1 and t1["ok"]): rt.report("stated_behaviour", etype=t1["exception_type"] if t1 else None, esite="exllamav3_ext exl3_gemm (second device)", **notes)
elif t1["out"] != c1["out"] or t1["sum"] != c1["sum"]: rt.report("stated_behaviour", **notes)
else: rt.report("expected_behaviour", identical_to_control=True, **notes)
