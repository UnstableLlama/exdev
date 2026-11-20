# Trigger: pass -tp to a CLI that uses the shared helpers (examples/chat.py) with otherwise valid arguments and no
# explicit device. Runs the unmodified examples/chat.py as a child process with -m Qwen2.5-0.5B-Instruct -mode chatml
# -tp (stdin closed); the process is expected to fail during loading if the stub is selected. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the run ends with NotImplementedError raised from Model.load_gen (exllamav3/models/model.py).
#   expected_behaviour : the model loads (the chat reaches its User prompt) in tensor-parallel mode.
#   other              : anything else.
import os, subprocess, sys
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
r = subprocess.run([sys.executable, os.path.join(WT, "examples", "chat.py"), "-m", M, "-mode", "chatml", "-basic", "-tp"],
                   stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
sys.stdout.write(r.stdout[-2000:]); sys.stderr.write(r.stderr[-3000:])
last = (r.stderr.strip().splitlines() or [""])[-1]
notes = dict(returncode=r.returncode, last_stderr_line=last, load_gen_in_traceback="load_gen" in r.stderr, reached_prompt="User:" in r.stdout)
if "NotImplementedError" in last and notes["load_gen_in_traceback"]: rt.report("stated_behaviour", etype="NotImplementedError", esite="exllamav3/models/model.py load_gen", **notes)
elif notes["reached_prompt"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
