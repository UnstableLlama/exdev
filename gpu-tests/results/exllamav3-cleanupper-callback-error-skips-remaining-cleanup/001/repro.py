# Trigger: register two callbacks on one Cleanupper and let the earlier one raise during _shutdown.
# A fresh child interpreter creates a module-level Cleanupper, registers fn1 (raises RuntimeError("fn1 fails"))
# then fn2 (prints CB2), and exits normally, so _shutdown runs from weakref's exit processing. Separately,
# _shutdown() is also called directly in a second child to observe the same loop without exit handling.
# Upstream is not modified.
# Classification, fixed before running (on the exit-time child):
#   stated_behaviour   : fn1's error is reported and CB2 is never printed.
#   expected_behaviour : CB2 is printed (later callbacks still get an attempt).
#   other              : anything else.
import subprocess, sys
import rt
rt.check_import()
SETUP = r'''
from exllamav3.util.misc import Cleanupper
def fn1(): raise RuntimeError("fn1 fails")
def fn2(): print("CB2", flush=True)
c = Cleanupper()
c.register_atexit(fn1); c.register_atexit(fn2)
'''
r1 = subprocess.run([sys.executable, "-c", SETUP + 'print("EXITING", flush=True)\n'], capture_output=True, text=True, timeout=120)
r2 = subprocess.run([sys.executable, "-c", SETUP + 'try:\n    c._shutdown()\nexcept Exception as e:\n    print("DIRECT_RAISED", type(e).__name__, flush=True)\nprint("AFTER_DIRECT", flush=True)\n'], capture_output=True, text=True, timeout=120)
for r in (r1, r2): sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
notes = dict(exit_cb2_printed="CB2" in r1.stdout, exit_error_reported="fn1 fails" in r1.stderr, exit_returncode=r1.returncode,
             direct_cb2_printed="CB2" in r2.stdout.split("AFTER_DIRECT")[0], direct_raised="DIRECT_RAISED RuntimeError" in r2.stdout)
if notes["exit_error_reported"] and not notes["exit_cb2_printed"]: rt.report("stated_behaviour", **notes)
elif notes["exit_cb2_printed"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
