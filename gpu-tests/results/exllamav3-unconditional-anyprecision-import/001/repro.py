# Trigger: the AnyPrecision import fails (here: any_precision is not installed, so the first import raises
# ModuleNotFoundError) and a comparison selects load_fn "anyprecision".
# The worktree's eval/compare_q_anyprecision.py is imported unmodified, then load_anyprecision(<Qwen dir>) is
# called, which is what compare_q.py dispatches to for load_fn "anyprecision". Environment py312-compareq
# (real compare_q dependencies, any_precision absent). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : importing the module succeeds (the import failure is swallowed) and load_anyprecision
#                        raises NameError for AnyPrecisionForCausalLM, without reporting the import problem.
#   expected_behaviour : the import problem is reported before model construction: either importing the module
#                        raises the ImportError/ModuleNotFoundError for any_precision, or load_anyprecision
#                        raises an error naming the missing backend.
#   other              : anything else.
import os, sys
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; sys.path.insert(0, os.path.join(WT, "eval"))
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
try:
    import compare_q_anyprecision as cqa
except ImportError as e:
    hit = "any_precision" in str(e)
    rt.report("expected_behaviour" if hit else "other", e, stage="module_import", message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, stage="module_import", message=str(e)); raise SystemExit
print("module imported; AnyPrecisionForCausalLM defined:", hasattr(cqa, "AnyPrecisionForCausalLM"), flush=True)
try:
    cqa.load_anyprecision(M)
except NameError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "AnyPrecision" in str(e) else "other", e, stage="load_anyprecision", message=str(e)); raise SystemExit
except Exception as e:
    hit = "any_precision" in str(e).lower() or "anyprecision" in str(e).lower()
    rt.report("expected_behaviour" if hit else "other", e, stage="load_anyprecision", message=str(e)); raise SystemExit
rt.report("other", stage="load_anyprecision", message="returned without error")
