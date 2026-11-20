# Trigger: import the package on Python 3.11 or older; architectures imports MiMo, Mistral and Qwen2.
# Runs on Python 3.11 (py311 environment). Imports the registry, which imports every model module.
# Classification, fixed before running:
#   stated_behaviour   : ImportError "cannot import name 'override' from 'typing'" from one of
#                        exllamav3/models/{mimo,mistral,qwen2}.py.
#   expected_behaviour : exllamav3.models.architectures imports on Python 3.11.
#   other              : anything else.
import sys
import rt
assert sys.version_info[:2] == (3, 11), sys.version
try:
    import exllamav3
    rt.check_import()
    import exllamav3.models.architectures as A
except ImportError as e:
    site = rt._site(e.__traceback__) or ""
    hit = "override" in str(e) and "typing" in str(e) and any(f"exllamav3/models/{m}.py" in site for m in ("mimo", "mistral", "qwen2"))
    rt.report("stated_behaviour" if hit else "other", e, python=sys.version.split()[0], message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour", python=sys.version.split()[0], n_architectures=len(getattr(A, "ARCHITECTURES", {})))
