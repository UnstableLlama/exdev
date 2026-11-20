# Trigger: construct ComboSampler() (min_p omitted, default 0.0) with Python assertions enabled.
# Classification, fixed before running:
#   stated_behaviour   : AssertionError from exllamav3/generator/sampler/custom.py (SS_MinP) during construction.
#   expected_behaviour : ComboSampler() constructs.
#   other              : anything else.
import sys
import rt
rt.check_import()
assert sys.flags.optimize == 0
try:
    from exllamav3.generator.sampler import ComboSampler
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    s = ComboSampler()
except AssertionError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/generator/sampler/custom.py") else "other", e); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour", sampler_type=type(s).__name__)
