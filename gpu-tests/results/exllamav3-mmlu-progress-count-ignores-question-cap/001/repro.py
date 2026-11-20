# Trigger: a cap that discards eligible rows, with sampling enabled, so the omitted count exceeds requested // 10
# before any job produces a result: -r 100 -mqps 1 (100 random questions, at most one per subject; with 57 subjects
# at least 43 are omitted, more than 100 // 10 = 10).
# Runs the unmodified eval/mmlu.py as a child process with Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775
# and cais/mmlu "all" @ c30699e8356da336a370243923dbaf21066bb9fe from the local HF cache (offline). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the run ends with ZeroDivisionError from an interim print_results(None) before any result
#                        line was printed.
#   expected_behaviour : the run completes and reports results.
#   other              : anything else.
import os, re, subprocess, sys, math
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
SCRIPT = os.path.join(WT, "eval", "mmlu.py")
def run(*args):
    env = dict(os.environ, HF_DATASETS_OFFLINE="1", HF_HUB_OFFLINE="1")
    r = subprocess.run([sys.executable, SCRIPT, "-m", M, "-cs", "16384", *args], capture_output=True, text=True, timeout=1500, env=env)
    sys.stdout.write(r.stdout[-4000:]); sys.stderr.write(r.stderr[-3000:])
    return r.returncode, r.stdout, (r.stderr.strip().splitlines() or [""])[-1], r.stderr
rc, out, err, full = run("-r", "100", "-mqps", "1")
result_lines = [l for l in out.splitlines() if "random samples" in l]
notes = dict(returncode=rc, last_stderr_line=err, result_lines_before_failure=result_lines[:3])
if rc != 0 and "ZeroDivisionError" in err and not result_lines: rt.report("stated_behaviour", etype="ZeroDivisionError", esite="eval/mmlu.py print_results", **notes)
elif rc == 0 and result_lines: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
