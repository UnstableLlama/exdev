# Trigger: construct SS_TopP(0.0) (and ComboSampler(top_p=0.0) at nonzero temperature) with assertions enabled.
# Classification, fixed before running (on SS_TopP(0.0); ComboSampler recorded in notes):
#   stated_behaviour   : AssertionError from exllamav3/generator/sampler/custom.py.
#   expected_behaviour : SS_TopP(0.0) constructs (its alt() may then return a no-op step).
#   other              : anything else.
import sys
import rt
rt.check_import()
assert sys.flags.optimize == 0
from exllamav3.generator.sampler.custom import SS_TopP
from exllamav3.generator.sampler import ComboSampler
combo = {}
try:
    ComboSampler(top_p=0.0, temperature=0.8); combo = {"ok": True}
except Exception as e:
    combo = {"ok": False, "exception_type": type(e).__name__, "site": rt._site(e.__traceback__)}
try:
    s = SS_TopP(0.0)
except AssertionError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/generator/sampler/custom.py") else "other", e, combo_sampler=combo); raise SystemExit
except Exception as e:
    rt.report("other", e, combo_sampler=combo); raise SystemExit
alt = type(s.alt()).__name__ if hasattr(s, "alt") and s.alt() is not None else None
rt.report("expected_behaviour", alt=alt, combo_sampler=combo)
