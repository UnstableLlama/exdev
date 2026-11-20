# Trigger: run test_rms_norm (and its benchmark) from tests/test_ext_norm.py against the native binding.
# Runs pytest (8.x, resolved as of 2025-05-25) on the worktree's tests/test_ext_norm.py, selecting one
# parametrization of test_rms_norm (-k "test_rms_norm and 1-8-in_dtype0-out_dtype0-1e-05" style keyword) to keep
# it short, and records the failure type. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the test fails with TypeError "incompatible function arguments" from ext.rms_norm.
#   expected_behaviour : the selected test passes.
#   other              : anything else.
import os, subprocess, sys
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]
r = subprocess.run([sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", os.path.join(WT, "tests", "test_ext_norm.py"),
                    "-k", "test_rms_norm and not benchmark", "--maxfail=1"], capture_output=True, text=True, timeout=600, cwd=WT)
sys.stdout.write(r.stdout[-4000:]); sys.stderr.write(r.stderr[-2000:])
out = r.stdout
notes = dict(pytest_returncode=r.returncode, incompatible_args="incompatible function arguments" in out, summary=[l for l in out.splitlines() if "passed" in l or "failed" in l][-1:])
if r.returncode != 0 and notes["incompatible_args"]: rt.report("stated_behaviour", etype="TypeError", esite="tests/test_ext_norm.py (ext.rms_norm call)", **notes)
elif r.returncode == 0: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
