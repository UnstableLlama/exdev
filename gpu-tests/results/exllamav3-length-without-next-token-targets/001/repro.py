# Trigger: invoke eval/ppl_transformers.py (the standalone script added at this commit) with --length 1.
# Runs the unmodified script as a child process: -m Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775
# -l 1 -r 2, wikitext-2-raw-v1 test from the local HF cache (offline). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the script is not rejected at argument time and fails in scoring with ZeroDivisionError
#                        (zero targets) or a tensor error on the empty slices.
#   expected_behaviour : the script rejects --length 1 before model work.
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
rc, out, err = run("-l", "1", "-r", "2")
notes = dict(returncode=rc, last_stderr_line=err, loaded="Loading" in out or "Tokenizing" in out)
if rc != 0 and ("ZeroDivisionError" in err or "RuntimeError" in err or "IndexError" in err): rt.report("stated_behaviour", etype=err.split(":")[0], **notes)
elif rc != 0 and ("error: argument" in err or "length" in err.lower()): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
