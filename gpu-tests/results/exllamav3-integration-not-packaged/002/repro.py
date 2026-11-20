# Trigger: build a distribution using setup.py's explicit package list, then import exllamav3 outside the source
# checkout. Runs `setup.py build_py --build-lib <tmp>` (the pure-Python part of building a distribution, using
# setup.py's own packages=[...] list) in the worktree, checks whether exllamav3/integration was included, then
# imports exllamav3 from <tmp> (with the separately built native extension on the path and the worktree NOT on the
# path). Environment py312-compareq (has transformers, which the integration imports). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the built tree lacks exllamav3/integration and importing exllamav3 from it raises
#                        ModuleNotFoundError for exllamav3.integration.
#   expected_behaviour : the built tree contains exllamav3/integration and exllamav3 imports from it.
#   other              : anything else.
import os, subprocess, sys, tempfile
import rt
WT = os.environ["EXL3_WT"]; lib = tempfile.mkdtemp()
b = subprocess.run([sys.executable, "setup.py", "build_py", "--build-lib", lib], cwd=WT, capture_output=True, text=True,
                   env=dict(os.environ, EXLLAMA_NOCOMPILE="1"), timeout=600)
sys.stdout.write(b.stdout[-1500:]); sys.stderr.write(b.stderr[-1500:])
has = os.path.isdir(os.path.join(lib, "exllamav3", "integration"))
extdirs = [p for p in os.environ.get("PYTHONPATH", "").split(":") if p and os.path.realpath(p) != os.path.realpath(WT) and "results" not in p]
env = dict(os.environ, PYTHONPATH=":".join([lib] + extdirs)); env.pop("EXL3_WT", None)
code = "import exllamav3, os; print('IMPORTED_FROM', os.path.dirname(exllamav3.__file__))"
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=tempfile.mkdtemp(), env=env, timeout=300)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr[-1500:])
last = (r.stderr.strip().splitlines() or [""])[-1]
notes = dict(build_returncode=b.returncode, built_has_integration=has, import_returncode=r.returncode, import_error=last, imported_from=[l for l in r.stdout.splitlines() if l.startswith("IMPORTED_FROM")])
if not has and r.returncode != 0 and "exllamav3.integration" in last: rt.report("stated_behaviour", etype="ModuleNotFoundError", **notes)
elif has and r.returncode == 0: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
