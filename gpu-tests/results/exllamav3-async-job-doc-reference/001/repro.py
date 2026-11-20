# Trigger: a reader follows AsyncJob's docstring instruction to consult DynamicJob.
# Reads exllamav3.AsyncJob.__doc__ and checks whether the named class exists anywhere in the package
# (exllamav3 and exllamav3.generator namespaces) and what AsyncJob actually instantiates.
# Classification, fixed before running:
#   stated_behaviour   : the docstring names DynamicJob and no DynamicJob is defined in the package.
#   expected_behaviour : the docstring names a class that exists (e.g. Job).
#   other              : anything else.
import inspect, pkgutil, importlib
import rt
rt.check_import()
import exllamav3, exllamav3.generator as gen
from exllamav3 import AsyncJob
doc = AsyncJob.__doc__ or ""
names = set()
for m in pkgutil.walk_packages(exllamav3.__path__, "exllamav3."):
    if ".exllamav3_ext" in m.name: continue
    try: mod = importlib.import_module(m.name)
    except Exception: continue
    names |= {n for n, o in vars(mod).items() if inspect.isclass(o)}
src = inspect.getsource(AsyncJob.__init__)
notes = dict(docstring=doc.strip(), mentions_DynamicJob="DynamicJob" in doc, DynamicJob_defined="DynamicJob" in names, init_instantiates_Job="Job(" in src)
print(notes, flush=True)
if notes["mentions_DynamicJob"] and not notes["DynamicJob_defined"]: rt.report("stated_behaviour", **notes)
elif not notes["mentions_DynamicJob"] or notes["DynamicJob_defined"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
