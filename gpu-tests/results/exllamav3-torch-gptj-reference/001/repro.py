# Trigger: RoPE.apply_torch with GPTJ style on a >= 4-channel head at a nontrivial angle.
# RoPE is built from RopeSettings(head_dim=64, rope_theta=10000, rope_style=GPTJ). q and k of shape
# (1, 8 tokens, 4 heads, 64) at positions 5..12 go through apply_torch (the torch reference path) and through
# apply (the native kernel). Both are compared with an independent GPTJ reference computed here:
# adjacent pairs (2i, 2i+1) rotated by pos * theta^(-2i/d). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : apply_torch differs from the GPTJ reference (max abs diff > 1e-2) while native apply
#                        matches it (<= 1e-2).
#   expected_behaviour : apply_torch matches the GPTJ reference (<= 1e-2).
#   other              : anything else (including native apply not matching the reference).
import torch
import rt
rt.check_import()
from exllamav3.util.rope import RoPE, RopeSettings, RopeStyle
D, HEADS, T, POS = 64, 4, 8, 5
torch.manual_seed(0)
q = torch.randn(1, T, HEADS, D, dtype=torch.half, device="cuda:0"); k = torch.randn(1, T, HEADS, D, dtype=torch.half, device="cuda:0")
def ref(x):
    x = x.float(); i = torch.arange(D // 2, device=x.device, dtype=torch.float)
    inv = 1.0 / (10000.0 ** (2 * i / D)); pos = torch.arange(POS, POS + T, device=x.device, dtype=torch.float)
    ang = pos[:, None] * inv[None, :]; c, s = ang.cos()[None, :, None, :], ang.sin()[None, :, None, :]
    a, b = x[..., 0::2], x[..., 1::2]
    return torch.stack((a * c - b * s, a * s + b * c), dim=-1).flatten(-2)
try:
    rope = RoPE("cuda:0", RopeSettings(head_dim=D, rope_theta=10000.0, rope_style=RopeStyle.GPTJ))
    qt, kt = rope.apply_torch(q.clone(), k.clone(), pos=POS)
    qn, kn = rope.apply(q.clone(), k.clone(), position=POS)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
rq, rk = ref(q), ref(k)
d_torch = max((qt.float() - rq).abs().max().item(), (kt.float() - rk).abs().max().item())
d_native = max((qn.float() - rq).abs().max().item(), (kn.float() - rk).abs().max().item())
notes = dict(apply_torch_vs_gptj_reference=d_torch, native_apply_vs_gptj_reference=d_native)
print(notes, flush=True)
if d_torch > 1e-2 and d_native <= 1e-2: rt.report("stated_behaviour", **notes)
elif d_torch <= 1e-2: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
