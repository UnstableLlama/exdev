# Trigger: an uncached evaluation with nonempty valid data and no model spec containing out_logits.
# Third-party imports are stubbed; the data source, model loader and forward function are small probes.
import torch
import rt, cq
rt.check_import()
V = 32; torch.manual_seed(0)
cq.compare_q.get_test_data = lambda spec: torch.randint(0, V, (2, 16))
cq.compare_q.load_fns["probe"] = lambda d: (object(), 1.0, 1.0, 8)
cq.compare_q.fwd_fns["probe"] = lambda m, ids: torch.randn(ids.shape[0], ids.shape[1], V)
try:
    cq.compare_q.main(cq.args())
except ZeroDivisionError as e:
    rt.report("stated_behaviour", e, message=str(e))
except Exception as e:
    rt.report("other", e, message=str(e))
else:
    rt.report("expected_behaviour", note="main completed and returned perplexity without a reference")
