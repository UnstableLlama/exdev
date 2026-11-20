# Trigger: call RoPE.apply_torch(q, None).
# RoPE built from RopeSettings(head_dim=64) on cuda:0; q of shape (1, 8, 4, 64) FP16. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : AttributeError ('NoneType' object has no attribute 'float') from exllamav3/util/rope.py.
#   expected_behaviour : returns a rotated q and None for k.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.util.rope import RoPE, RopeSettings
rope = RoPE("cuda:0", RopeSettings(head_dim=64))
q = torch.randn(1, 8, 4, 64, dtype=torch.half, device="cuda:0")
try:
    out = rope.apply_torch(q, None)
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "NoneType" in str(e) and site.startswith("exllamav3/util/rope.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
qo, ko = out
rt.report("expected_behaviour" if ko is None and qo.shape == q.shape else "other", k_is_none=ko is None)
