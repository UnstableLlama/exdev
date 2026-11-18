# Trigger: a cached result exists for the three-argument test_ppl call and --clear_cache is requested.
# Third-party imports are stubbed; get_test_data is replaced by a probe that records a recomputation.
import rt, cq
rt.check_import()
from exllamav3.util.file import disk_lru_cache
SENTINEL = {"label": "probe", "ppl": "CACHED-SENTINEL"}
@disk_lru_cache("test_ppl")
def seed(*a): return SENTINEL
seed(cq.DATA, cq.SPEC, None)                            # same key the three-argument call uses
class Recomputed(Exception): pass
def probe(spec): raise Recomputed()
cq.compare_q.get_test_data = probe
cq.compare_q.load_fns["probe"] = cq.compare_q.fwd_fns["probe"] = probe
a = cq.args(); a.clear_cache = True
try:
    cq.compare_q.main(a)
except Recomputed:
    rt.report("expected_behaviour", note="cached entry was invalidated and test_ppl recomputed")
except Exception as e:
    rt.report("other", e, message=str(e))
else:
    rt.report("stated_behaviour", note="main returned the stale cached result after --clear_cache")
