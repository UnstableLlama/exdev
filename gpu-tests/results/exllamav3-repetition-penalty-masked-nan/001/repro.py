# Trigger: an enabled repetition penalty receives an infinite (masked, -inf) logit with positive finite rep_p,
# with interpolation factor 0 (token not in the penalty window) and factor 1 (token inside the sustain range).
# The extension's apply_rep_pens (the kernel SS_RepP.run calls) is called directly with float32 logits of
# vocab 1024: token 10 = -inf and in past_ids (factor 1); token 20 = -inf and not in past_ids (factor 0);
# token 30 finite and in past_ids (control: must be penalized). rep_p = 1.5, sustain_range = 64, decay 0.
# Upstream is not modified.
# Behaviour label, fixed before running:
#   stated_behaviour   : at least one -inf input becomes NaN.
#   expected_behaviour : both -inf inputs stay -inf and the finite control is penalized.
#   other              : anything else.
# Per-case results (factor0_nan, factor1_nan) are recorded so a partial fix can be judged on the case it claims.
import torch
import rt
rt.check_import()
from exllamav3.ext import exllamav3_ext as ext
V = 1024
logits = torch.randn(1, 1, V, dtype=torch.float, device="cuda:0")
logits[..., 10] = float("-inf"); logits[..., 20] = float("-inf"); logits[..., 30] = 2.0
past = torch.tensor([[5, 10, 30, 7]], dtype=torch.long, device="cuda:0")
out = torch.empty_like(logits)
try:
    ext.apply_rep_pens(logits, out, past, 1.5, 64, 0); torch.cuda.synchronize()
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
o = out[0, 0].cpu()
r = dict(factor1_value=str(o[10].item()), factor0_value=str(o[20].item()), control_value=o[30].item(),
         factor1_nan=bool(o[10].isnan()), factor0_nan=bool(o[20].isnan()))
print(r, flush=True)
ok_inf = (o[10].item() == float("-inf")) and (o[20].item() == float("-inf"))
if r["factor1_nan"] or r["factor0_nan"]: rt.report("stated_behaviour", **r)
elif ok_inf and abs(r["control_value"] - 2.0 / 1.5) < 1e-4: rt.report("expected_behaviour", **r)
else: rt.report("other", **r)
