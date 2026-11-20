# Trigger: exl3_mgemm with otherwise suitable contiguous tensors where
#   case 1: A leading (batch) dimension 2, C leading dimension 1, indices shape (1, 1);
#   case 2: A leading dimension 2, C leading dimension 3, indices shape (1, 3).
# Observation without touching memory outside the script's own allocations:
#   case 1: C is a view of the first slot of a 3-slot buffer filled with a sentinel; a write to C slot 1 (beyond
#           C) shows up as changed sentinels.
#   case 2: A is a view of the first 2 slots of a 3-slot buffer whose third slot holds a large poison value
#           (1e3); if the kernel reads a third input matrix, C[2] is dominated by the poison (|C[2]| much larger
#           than |C[0]|, |C[1]|).
# Buffers: two random but well-formed K=4 EXL3 matrices (k = n = 1024) passed by pointer; the extension's own
# exl3_mgemm binding is called directly (arity chosen from its signature). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : case 1 writes beyond C, or case 2 reads the poisoned third input, with no exception.
#   expected_behaviour : both cases either raise an ordinary exception before launch, or complete with no
#                        write beyond C and no poisoned read.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.ext import exllamav3_ext as ext
k = n = 1024; K = 4; dev = torch.device("cuda:0"); SENT = -7.0
g = torch.Generator().manual_seed(0)
mats = []
for _ in range(2):
    tr = torch.randint(-32768, 32767, (k // 16, n // 16, 16 * K), dtype=torch.int16, generator=g).to(dev)
    suh = (torch.randn(k, generator=g) * 0.05).half().to(dev); svh = (torch.randn(n, generator=g) * 0.05).half().to(dev)
    mats.append((tr, suh, svh))
ptrs = lambda i: torch.tensor([m[i].data_ptr() for m in mats], dtype=torch.long, device=dev)
B, SUH, SVH = ptrs(0), ptrs(1), ptrs(2)
nargs = ext.exl3_mgemm.__doc__.split("\n")[0].count("arg")
def call(A, C, idx):
    Ah = torch.empty((A.shape[0], A.shape[1], k), dtype=torch.half, device=dev)
    args = [A, B, C, SUH, Ah, SVH, idx, None, K, -1] + ([0, 0] if nargs >= 12 else [])
    ext.exl3_mgemm(*args); torch.cuda.synchronize()
res = {"binding_arity": nargs}
# case 1
bufC = torch.full((3, 1, n), SENT, dtype=torch.half, device=dev); C1 = bufC[:1]
A1 = (torch.randn(2, 1, k, generator=g) * 0.5).half().to(dev)
try:
    call(A1, C1, torch.zeros(1, 1, dtype=torch.long, device=dev))
    res["case1"] = {"ok": True, "beyond_C_changed": int((bufC[1:].float() != SENT).sum())}
except Exception as e:
    res["case1"] = {"ok": False, "exception_type": type(e).__name__, "message": str(e).splitlines()[0] if str(e) else ""}
# case 2
bufA = torch.empty(3, 1, k, dtype=torch.half, device=dev); bufA[:2] = (torch.randn(2, 1, k, generator=g) * 0.5).half().to(dev); bufA[2] = 1e3
A2 = bufA[:2]; C2 = torch.zeros(3, 1, n, dtype=torch.half, device=dev)
try:
    call(A2, C2, torch.tensor([[0, 1, 0]], dtype=torch.long, device=dev))
    mags = [float(C2[i].float().abs().max()) for i in range(3)]
    res["case2"] = {"ok": True, "max_abs_per_slot": mags, "poison_read": bool(mags[2] > 20 * max(mags[0], mags[1], 1e-3))}
except Exception as e:
    res["case2"] = {"ok": False, "exception_type": type(e).__name__, "message": str(e).splitlines()[0] if str(e) else ""}
print(res, flush=True)
c1, c2 = res["case1"], res["case2"]
bad = (c1["ok"] and c1["beyond_C_changed"] > 0) or (c2["ok"] and c2["poison_read"])
if any((not c["ok"]) and c["exception_type"] == "TypeError" for c in (c1, c2)): rt.report("did_not_run", **res)
elif bad: rt.report("stated_behaviour", **res)
elif all((not c["ok"]) or (c is c1 and c["beyond_C_changed"] == 0) or (c is c2 and not c["poison_read"]) for c in (c1, c2)): rt.report("expected_behaviour", **res)
else: rt.report("other", **res)
