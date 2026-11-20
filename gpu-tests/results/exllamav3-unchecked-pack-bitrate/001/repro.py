# Trigger: call a native pack wrapper with K=9 and tensors satisfying its shape checks: unpacked final dim 256,
# packed final dim 256*9/16 = 144. ext.pack_trellis and ext.unpack_trellis are each called in a child process
# (indexing an 8-entry kernel table at [8] may crash). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : neither call is rejected with an ordinary exception naming the bitrate before launch:
#                        the child crashes, gets a CUDA launch error, or returns.
#   expected_behaviour : both calls raise an ordinary exception rejecting K=9.
#   other              : anything else.
import subprocess, sys
import rt
rt.check_import()
def child(fn):
    code = f'''
import torch, sys
from exllamav3.ext import exllamav3_ext as ext
u = torch.randint(0, 511, (2, 2, 256), dtype=torch.int16, device="cuda:0"); p = torch.zeros(2, 2, 144, dtype=torch.int16, device="cuda:0")
try:
    ext.{fn}(p, u, 9) if "{fn}" == "pack_trellis" else ext.{fn}(u, p, 9)
    torch.cuda.synchronize(); print("CHILD returned", flush=True)
except Exception as e:
    print("CHILD exception", type(e).__name__, str(e).splitlines()[0] if str(e) else "", flush=True); sys.exit(3)
'''
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr[-1500:])
    return dict(returncode=r.returncode, lines=[l for l in r.stdout.splitlines() if l.startswith("CHILD")], stderr_tail=r.stderr.strip().splitlines()[-1:])
res = {fn: child(fn) for fn in ("pack_trellis", "unpack_trellis")}
print(res, flush=True)
def rejected(x): return x["returncode"] == 3 and any(("K" in l or "bit" in l.lower()) and "CUDA" not in l and "incompatible" not in l for l in x["lines"])
if all(rejected(x) for x in res.values()): rt.report("expected_behaviour", **res)
elif any("incompatible function arguments" in " ".join(x["lines"]) for x in res.values()): rt.report("did_not_run", **res)
elif not any(rejected(x) for x in res.values()): rt.report("stated_behaviour", **res)
else: rt.report("other", **res)
