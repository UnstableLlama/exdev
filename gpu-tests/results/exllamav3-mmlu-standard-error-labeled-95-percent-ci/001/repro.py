# Trigger: complete a positive requested sample with exactly that many rows scored and population > 1: -r 20.
# Runs the unmodified eval/mmlu.py as a child process with Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775
# and cais/mmlu "all" @ c30699e8356da336a370243923dbaf21066bb9fe from the local HF cache (offline). Upstream is not modified.
# The final "(95% CI)" line's printed half-width is compared with the plug-in standard error
# sqrt(p(1-p)/n * (N-n)/(N-1)) (N = 14042 test rows) and with 1.96 times it.
# Classification, fixed before running:
#   stated_behaviour   : the line is labelled "(95% CI)" and its half-width equals one plug-in standard error
#                        (within 0.01 percentage points), not 1.96 of them.
#   expected_behaviour : the label and the width agree (e.g. width about 1.96 SE, or labelled as a standard error).
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
rc, out, err, full = run("-r", "20")
m = re.findall(r"(\d+)/\s*(\d+) =\s*([\d.]+)% \+/-\s*([\d.]+)%( \(95% CI\))?", out)
if rc != 0 or not m: rt.report("did_not_run", returncode=rc, last_stderr_line=err); raise SystemExit
c, n, pct, width, lab = m[-1]; c, n = int(c), int(n); N = 14042; p = c / n
se = math.sqrt(p * (1 - p) / n * (N - n) / (N - 1)) * 100
notes = dict(final_line=f"{c}/{n} = {pct}% +/- {width}%{lab}", labelled_95=bool(lab), printed_halfwidth=float(width), plugin_se_pct=se, se_times_1_96=1.96 * se)
print(notes, flush=True)
if lab and abs(float(width) - se) <= 0.01: rt.report("stated_behaviour", **notes)
elif (lab and abs(float(width) - 1.96 * se) <= 0.05) or not lab: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
