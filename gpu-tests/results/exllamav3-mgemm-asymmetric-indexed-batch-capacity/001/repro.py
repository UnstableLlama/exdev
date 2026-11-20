# Trigger: exl3_mgemm with valid weight IDs and (input slots, output slots, index count) of (4, 2, 4) or (2, 4, 3).
# Observation inside the script's own allocations (as in multi-gemm-leading-dimension-validation 001):
#   (4, 2, 4): C is a view of the first 2 slots of a 4-slot sentinel buffer; writes to slots 2-3 change sentinels.
#   (2, 4, 3): A is a view of the first 2 slots of a 3-slot buffer whose third slot is poison (1e3); a read of
#              input slot 2 shows up as C[2] dominated by the poison.
# Two random well-formed K=4 EXL3 matrices (k = n = 1024); the extension's exl3_mgemm binding is called directly.
# Classification, fixed before running:
#   stated_behaviour   : either case writes beyond C or reads the poisoned input slot, with no exception.
#   expected_behaviour : both cases are rejected before launch or touch only valid slots.
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
# case A: (input slots, output slots, index count) = (4, 2, 4); C is a view of the first 2 slots of a 4-slot sentinel buffer
bufC = torch.full((4, 1, n), SENT, dtype=torch.half, device=dev); C = bufC[:2]
A = (torch.randn(4, 1, k, generator=g) * 0.5).half().to(dev)
try:
    call(A, C, torch.tensor([[0, 1, 0, 1]], dtype=torch.long, device=dev))
    res["case_4_2_4"] = {"ok": True, "beyond_C_changed": int((bufC[2:].float() != SENT).sum())}
except Exception as e:
    res["case_4_2_4"] = {"ok": False, "exception_type": type(e).__name__, "message": str(e).splitlines()[0] if str(e) else ""}
# case B: (2, 4, 3); A is a view of the first 2 slots of a 3-slot buffer whose third slot is poison (1e3)
bufA = torch.empty(3, 1, k, dtype=torch.half, device=dev); bufA[:2] = (torch.randn(2, 1, k, generator=g) * 0.5).half().to(dev); bufA[2] = 1e3
C2 = torch.zeros(4, 1, n, dtype=torch.half, device=dev)
try:
    call(bufA[:2], C2, torch.tensor([[0, 1, 0]], dtype=torch.long, device=dev))
    mags = [float(C2[i].float().abs().max()) for i in range(4)]
    res["case_2_4_3"] = {"ok": True, "max_abs_per_slot": mags, "poison_read": bool(mags[2] > 20 * max(mags[0], mags[1], 1e-3))}
except Exception as e:
    res["case_2_4_3"] = {"ok": False, "exception_type": type(e).__name__, "message": str(e).splitlines()[0] if str(e) else ""}
print(res, flush=True)
a, b = res["case_4_2_4"], res["case_2_4_3"]
bad = (a["ok"] and a["beyond_C_changed"] > 0) or (b["ok"] and b["poison_read"])
good = ((not a["ok"]) or a["beyond_C_changed"] == 0) and ((not b["ok"]) or not b["poison_read"])
if bad: rt.report("stated_behaviour", **res)
elif good and not any((not c["ok"]) and c["exception_type"] == "TypeError" for c in (a, b)): rt.report("expected_behaviour", **res)
else: rt.report("other", **res)
