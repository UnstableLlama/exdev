# Trigger: a caller consults load_gen's reserve_per_device documentation.
# Reads Model.load_gen's docstring and source from the worktree and records the reserve amount each states.
# Classification, fixed before running:
#   stated_behaviour   : the docstring states 0.25 GB while the implementation uses 0.5 * 1024**3.
#   expected_behaviour : docstring and implementation agree.
#   other              : anything else.
import inspect, re
import rt
rt.check_import()
from exllamav3 import Model
doc = inspect.getdoc(Model.load_gen) or ""; src = inspect.getsource(Model.load_gen)
dl = [l.strip() for l in doc.splitlines() if "reserve" in l.lower() or "GB" in l]
impl = re.findall(r"[0-9.]+\s*\*\s*1024\s*\*\*\s*3", src)
notes = dict(doc_lines=dl, implementation_constants=impl)
print(notes, flush=True)
d25 = any("0.25" in l for l in dl); i5 = any(s.replace(" ", "").startswith("0.5*") for s in impl)
rt.report("stated_behaviour" if d25 and i5 else "expected_behaviour" if not d25 else "other", **notes)
