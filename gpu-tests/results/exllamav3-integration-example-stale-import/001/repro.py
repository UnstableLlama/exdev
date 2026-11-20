# Trigger: run examples/transformers_integration.py in an environment where its preceding imports succeed.
# Environment: py312-compareq (real transformers 4.52.4, so `from transformers import ... Gemma3ForConditionalGeneration`
# succeeds). The example is executed unmodified with runpy from the worktree. Past its registration call the
# example loads a model from a hard-coded local directory that does not exist here; that later failure is
# beyond the trigger and is only recorded.
#
# Classification, fixed before running:
#   stated_behaviour   : ImportError naming patch_transformers, raised at the example's exllamav3.integration import.
#   expected_behaviour : the import succeeds and EXL3 is registered in transformers' quantizer mapping
#                        (whatever the example does afterwards).
#   other              : anything else.
import os, runpy, sys, traceback
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; ex = os.path.join(WT, "examples", "transformers_integration.py")
err = None
try:
    sys.argv = [ex]
    runpy.run_path(ex, run_name="__main__")
except BaseException as e:
    err = e
    traceback.print_exception(e, file=sys.stderr)
ex_frames = [fr for fr in traceback.extract_tb(err.__traceback__) if os.path.realpath(fr.filename) == os.path.realpath(ex)] if err else []
ex_line = ex_frames[-1].lineno if ex_frames else None
ex_src = (ex_frames[-1].line or "") if ex_frames else ""
try:
    from transformers.quantizers import auto as qa
    registered = sorted(k for k in qa.AUTO_QUANTIZER_MAPPING if "exl3" in k.lower())
except Exception as e:
    registered = f"could not inspect: {e!r}"
notes = dict(example_exception=(type(err).__name__ if err else None), example_line=ex_line, example_source=ex_src,
             message=(str(err).splitlines()[0] if err and str(err) else ""), exl3_quantizers_registered=registered)
if isinstance(err, ImportError) and "patch_transformers" in str(err) and "exllamav3.integration" in ex_src:
    rt.report("stated_behaviour", etype="ImportError", esite=f"examples/transformers_integration.py:{ex_line}", **notes)
elif not (isinstance(err, ImportError) and "patch_transformers" in str(err)) and isinstance(registered, list) and registered:
    rt.report("expected_behaviour", **notes)
else:
    rt.report("other", **notes)
