# Trigger: pass --rows 0 to eval/ppl_transformers.py with at least one available window.
# Runs the unmodified script as a child process: -m Qwen2.5-0.5B-Instruct -r 0 -l 256 (offline wikitext cache).
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the script scores a row anyway (prints "Evaluated: 1 rows").
#   expected_behaviour : it rejects 0, or evaluates zero rows without scoring.
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
rc, out, err = run("-r", "0", "-l", "256")
m = re.search(r"Evaluated: (\d+) rows of (\d+) tokens", out); ppl = re.search(r"Perplexity: ([\d.]+)", out)
notes = dict(returncode=rc, evaluated_rows=int(m.group(1)) if m else None, perplexity=float(ppl.group(1)) if ppl else None, last_stderr_line=err)
if m and int(m.group(1)) >= 1: rt.report("stated_behaviour", **notes)
elif rc != 0 and "rows" in err.lower(): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
