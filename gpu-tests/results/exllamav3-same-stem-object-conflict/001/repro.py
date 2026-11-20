# Trigger: build the native extension with the repository's setup.py, which discovers sources automatically.
# Runs `python setup.py build_ext --build-lib <tmp> --build-temp <tmp>` in the worktree (torch cpp_extension
# with ninja, as installed in the environment). The harness's extension cache is not used (--no-ext).
# The full build log is saved beside this file as build-<sha12>.log.
# Classification, fixed before running:
#   stated_behaviour   : the build fails and the log reports two rules generating the same object file
#                        for a same-stem source pair (e.g. stloader.cpp / stloader.cu -> stloader.o).
#   expected_behaviour : the build succeeds and produces the extension shared object.
#   other              : anything else.
import glob, os, re, subprocess, sys, tempfile
import rt
WT = os.environ["EXL3_WT"]
here = os.path.dirname(os.path.abspath(__file__))
sha = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()[:12]
lib, tmp = tempfile.mkdtemp(), tempfile.mkdtemp()
log = os.path.join(here, f"build-{sha}.log")
with open(log, "w") as f:
    r = subprocess.run([sys.executable, "setup.py", "build_ext", "--build-lib", lib, "--build-temp", tmp], cwd=WT,
                       stdout=f, stderr=subprocess.STDOUT, env=dict(os.environ, EXLLAMA_VERBOSE=""), timeout=3600)
text = open(log, errors="replace").read()
dup = re.findall(r"multiple rules generate (\S+)", text)
so = glob.glob(os.path.join(lib, "**", "*.so"), recursive=True)
notes = dict(returncode=r.returncode, duplicate_outputs=[os.path.basename(d) for d in dup], shared_objects=[os.path.basename(s) for s in so], log=os.path.basename(log))
if r.returncode != 0 and dup: rt.report("stated_behaviour", etype="ninja build error", esite="setup.py build_ext (ninja: multiple rules generate)", **notes)
elif r.returncode == 0 and so: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
