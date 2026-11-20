# Trigger: compile the extension, including exl3_comp_unit_1.cu .. exl3_comp_unit_8.cu, from the repository contents.
# Runs `python setup.py build_ext --build-lib <tmp> --build-temp <tmp>` in the worktree (torch cpp_extension
# with ninja, as installed in the environment). The harness's extension cache is not used (--no-ext).
# The full build log is saved beside this file as build-<sha12>.log.
# Classification, fixed before running:
#   stated_behaviour   : the build fails and the log reports that exl3_gemv_kernel.cuh cannot be found
#                        from a comp_unit source.
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
dup = re.findall(r"(\S*exl3_comp_unit_\d\.cu\S*).*?exl3_gemv_kernel\.cuh: No such file", text)
missing = "exl3_gemv_kernel.cuh: No such file" in text
so = glob.glob(os.path.join(lib, "**", "*.so"), recursive=True)
notes = dict(returncode=r.returncode, missing_header_reported=missing, units_reporting=sorted(set(os.path.basename(d.split(':')[0]) for d in dup)), shared_objects=[os.path.basename(s) for s in so], log=os.path.basename(log))
if r.returncode != 0 and missing: rt.report("stated_behaviour", etype="compile error (missing header)", esite="exl3_comp_unit_*.cu include ../exl3_gemv_kernel.cuh", **notes)
elif r.returncode == 0 and so: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
