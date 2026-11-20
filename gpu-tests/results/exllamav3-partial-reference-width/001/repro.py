# Trigger: full-width Q/K with head_dim=128 and partial_rotary_factor=0.5 passed to RoPE.apply_torch.
# Classification, fixed before running:
#   stated_behaviour   : RuntimeError about incompatible tensor sizes from exllamav3/util/rope.py.
#   expected_behaviour : returns Q/K whose first 64 channels are rotated and the rest unchanged.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.util.rope import RoPE, RopeSettings
rope = RoPE("cuda:0", RopeSettings(head_dim=128, partial_rotary_factor=0.5))
q = torch.randn(1, 8, 4, 128, dtype=torch.half, device="cuda:0"); k = torch.randn_like(q)
try:
    qo, ko = rope.apply_torch(q.clone(), k.clone(), pos=3)
except RuntimeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/util/rope.py") else "other", e, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
tail_same = bool(torch.equal(qo[..., 64:], q[..., 64:]))
rt.report("expected_behaviour" if tail_same else "other", tail_unchanged=tail_same)
