# Trigger: create a Cleanupper inside a main function, register a callback, return without keeping a reference.
# A fresh child interpreter runs: main() creates Cleanupper and registers a callback printing CB; main returns;
# gc.collect(); prints AFTER_MAIN_GC; then the interpreter exits. The order of CB and AFTER_MAIN_GC in its
# output shows when the callback ran. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : CB is printed after AFTER_MAIN_GC (callback deferred to interpreter exit).
#   expected_behaviour : CB is printed before AFTER_MAIN_GC (callback ran when main's scope ended).
#   other              : anything else (e.g. CB never printed).
import subprocess, sys
import rt
rt.check_import()
CHILD = r'''
import gc
from exllamav3.util.misc import Cleanupper
def main():
    c = Cleanupper()
    c.register_atexit(lambda: print("CB", flush=True))
main()
gc.collect()
print("AFTER_MAIN_GC", flush=True)
'''
r = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, timeout=120)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
lines = [l for l in r.stdout.splitlines() if l in ("CB", "AFTER_MAIN_GC")]
notes = dict(order=lines, child_returncode=r.returncode)
if lines == ["AFTER_MAIN_GC", "CB"]: rt.report("stated_behaviour", **notes)
elif lines == ["CB", "AFTER_MAIN_GC"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
