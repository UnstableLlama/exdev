# Trigger: call regularize with skip_g_scale=True and verbose=True after successful preprocessing.
# exllamav3.modules.quant.exl3_lib.quantize.regularize is called on a random float32 (256, 256) CUDA weight with
# su = sv = ones, quant_args {"apply_out_scales": None}, H_diag None, pb None. A control call with verbose=False
# shows the function otherwise completes. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the verbose call raises UnboundLocalError/NameError for mse_scale while the quiet call
#                        returns.
#   expected_behaviour : the verbose call returns.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.modules.quant.exl3_lib.quantize import regularize
def call(verbose):
    torch.manual_seed(0)
    w = torch.randn(256, 256, device="cuda:0"); su = torch.ones(256, device="cuda:0"); sv = torch.ones(256, device="cuda:0")
    return regularize(w, su, sv, {"apply_out_scales": None}, verbose, None, None, skip_g_scale=True)
try:
    call(False); ctl = "ok"
except Exception as e:
    ctl = f"{type(e).__name__}: {e}"
try:
    call(True)
except (UnboundLocalError, NameError) as e:
    rt.report("stated_behaviour" if "mse_scale" in str(e) and ctl == "ok" else "other", e, control_quiet=ctl, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, control_quiet=ctl, message=str(e)); raise SystemExit
rt.report("expected_behaviour", control_quiet=ctl)
