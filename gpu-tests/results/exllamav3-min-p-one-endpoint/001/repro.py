# Trigger: SS_MinP(1.0) with assertions enabled.
# Constructs the repository's sampler step directly (python without -O, so asserts run). Also constructs
# SS_MinP(0.5) as a control that every tested commit should accept. Upstream is not modified.
#
# Classification, fixed before running:
#   stated_behaviour   : SS_MinP(1.0) raises AssertionError from exllamav3/generator/sampler/custom.py.
#   expected_behaviour : SS_MinP(1.0) constructs and keeps min_p == 1.0.
#   other              : anything else (including the control failing).
import sys
import rt
rt.check_import()
assert sys.flags.optimize == 0, "assertions disabled"
from exllamav3.generator.sampler.custom import SS_MinP
try:
    ctl = SS_MinP(0.5)
except Exception as e:
    rt.report("other", e, control="SS_MinP(0.5) failed"); raise SystemExit
try:
    s = SS_MinP(1.0)
except AssertionError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/generator/sampler/custom.py") else "other", e, control_ok=True); raise SystemExit
except Exception as e:
    rt.report("other", e, control_ok=True); raise SystemExit
rt.report("expected_behaviour" if s.min_p == 1.0 else "other", min_p=s.min_p, control_ok=True)
