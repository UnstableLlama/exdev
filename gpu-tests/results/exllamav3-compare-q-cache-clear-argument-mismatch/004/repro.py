# Trigger: a cached result exists for the three-argument test_ppl call and the user passes --clear_cache.
# First run populates the script's own disk cache; second run adds --clear_cache.
import rt, cqcli as c
rt.check_import()
import json, os
# out_logits makes the run collect reference logits, so evaluation can finish and be cached at these commits.
json.dump([{"load_fn": "exllamav3", "fwd_fn": "exllamav3", "model_dir": c.M, "label": "qwen2.5-0.5b", "out_logits": os.path.join(c.TMP, "ref")}], open(c.SPEC, "w"))
A = ["-d", c.DATA, "-m", c.SPEC]
rc, t = c.run("compare_q.py", *A)
if rc or "Testing:" not in t:
    et, s = c.tb(t); rt.report("did_not_run", etype=et, esite=s, stage="populate", returncode=rc, tail=t[-400:]); raise SystemExit
rc, t2 = c.run("compare_q.py", *A, "--clear_cache")
et, s = c.tb(t2)
if rc: rt.report("other", etype=et, esite=s, stage="clear", returncode=rc, tail=t2[-400:])
elif "Testing:" in t2: rt.report("expected_behaviour", note="second run re-evaluated the model")
else: rt.report("stated_behaviour", note="second run returned the cached result without evaluating")
