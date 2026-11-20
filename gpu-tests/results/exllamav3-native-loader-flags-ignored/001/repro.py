# Trigger: invoke eval/ppl_transformers.py with --gpu_split, --load_metrics or --override.
# Runs the unmodified script as a child process with -r 1 -l 256 plus, in one run, --load_metrics and
# --gpu_split 0.5 (a cap far below the model size, which the native loader would enforce), and in another run
# --override /nonexistent/override.yaml (a native loader would fail to open it). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : both runs complete and print a perplexity, with no loader metrics output and no error
#                        about the override file: the options are accepted and ignored.
#   expected_behaviour : the options take effect (metrics printed, split enforced, override read) or are rejected.
#   other              : anything else.
import os, re, subprocess, sys
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
SCRIPT = os.path.join(WT, "eval", "ppl_transformers.py")
def run(*args):
    env = dict(os.environ, HF_DATASETS_OFFLINE="1", HF_HUB_OFFLINE="1")
    r = subprocess.run([sys.executable, SCRIPT, "-m", M, *args], capture_output=True, text=True, timeout=900, env=env)
    sys.stdout.write(r.stdout[-3000:]); sys.stderr.write(r.stderr[-3000:])
    err = (r.stderr.strip().splitlines() or [""])[-1]
    return r.returncode, r.stdout, err
rc1, out1, err1 = run("-r", "1", "-l", "256", "--load_metrics", "--gpu_split", "0.5")
rc2, out2, err2 = run("-r", "1", "-l", "256", "--override", "/nonexistent/override.yaml")
p1, p2 = re.search(r"Perplexity: ([\d.]+)", out1), re.search(r"Perplexity: ([\d.]+)", out2)
notes = dict(run_metrics_split=dict(returncode=rc1, perplexity=p1.group(1) if p1 else None, metrics_printed=bool(re.search(r"Deferred|chunks|tensors in", out1)), last_stderr_line=err1),
             run_override=dict(returncode=rc2, perplexity=p2.group(1) if p2 else None, last_stderr_line=err2))
print(notes, flush=True)
if rc1 == 0 and rc2 == 0 and p1 and p2 and not notes["run_metrics_split"]["metrics_printed"]: rt.report("stated_behaviour", **notes)
elif rc2 != 0 or notes["run_metrics_split"]["metrics_printed"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
