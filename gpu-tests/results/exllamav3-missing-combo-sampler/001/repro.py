# Trigger: import exllamav3 once preceding imports succeed (torch, the native extension and the package's
# other dependencies are installed in this environment).
# Classification, fixed before running:
#   stated_behaviour   : ImportError naming ComboSampler, raised from the exllamav3 package import.
#   expected_behaviour : the package imports and exposes ComboSampler from exllamav3.generator.sampler.
#   other              : anything else.
import os, sys, traceback
WT = os.path.realpath(os.environ["EXL3_WT"])
import rt  # rt.check_import() would import exllamav3 itself; the import below is the trigger
try:
    import exllamav3
    from exllamav3.generator.sampler import ComboSampler
except ImportError as e:
    site = rt._site(e.__traceback__)
    ok = "ComboSampler" in str(e) and os.path.realpath(sys.modules.get("exllamav3").__file__ if "exllamav3" in sys.modules else "").startswith(WT + os.sep)
    rt.report("stated_behaviour" if "ComboSampler" in str(e) else "other", e, imported_from_worktree=ok, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.check_import()
rt.report("expected_behaviour", combo=ComboSampler.__module__)
