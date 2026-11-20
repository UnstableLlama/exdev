# Trigger: on Python 3.10/3.11 with assertions enabled, construct SS_TopK with an integer top_k through a
# non-greedy sampler route (ComboSampler(top_k=40, temperature=0.8)); SS_TopK(40) directly is also recorded.
# Runs on Python 3.11 (py311 environment).
# Classification, fixed before running (on the ComboSampler route):
#   stated_behaviour   : AttributeError "'int' object has no attribute 'is_integer'" from
#                        exllamav3/generator/sampler/custom.py.
#   expected_behaviour : construction succeeds.
#   other              : anything else.
import sys
import rt
rt.check_import()
assert sys.flags.optimize == 0 and sys.version_info[:2] == (3, 11), sys.version
from exllamav3.generator.sampler.custom import SS_TopK
from exllamav3.generator.sampler import ComboSampler
direct = {}
try:
    SS_TopK(40); direct = {"ok": True}
except Exception as e:
    direct = {"ok": False, "exception_type": type(e).__name__, "message": str(e), "site": rt._site(e.__traceback__)}
try:
    ComboSampler(top_k=40, temperature=0.8)
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    hit = "is_integer" in str(e) and site.startswith("exllamav3/generator/sampler/custom.py")
    rt.report("stated_behaviour" if hit else "other", e, python=sys.version.split()[0], direct_ss_topk=direct); raise SystemExit
except Exception as e:
    rt.report("other", e, python=sys.version.split()[0], direct_ss_topk=direct); raise SystemExit
rt.report("expected_behaviour", python=sys.version.split()[0], direct_ss_topk=direct)
