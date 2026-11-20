# Trigger: a caller consults load_gen's reserve_per_device documentation.
# Attempt 002: reads Model.load_gen's docstring and source; the documented default is taken from the docstring line
# "The default reserve per device is ... GB", the implemented default from the literals in
# `reserve_per_device = [X] * num_devices` and `reserve_per_device.append(X)` (GB, converted by * 1024**3 later).
# Classification, fixed before running:
#   stated_behaviour   : documented default 0.25 GB, implemented default 0.5 (GB).
#   expected_behaviour : documented and implemented defaults agree.
#   other              : anything else.
import inspect, re
import rt
rt.check_import()
from exllamav3 import Model
doc = inspect.getdoc(Model.load_gen) or ""; src = inspect.getsource(Model.load_gen)
documented = re.findall(r"default reserve per device is ([0-9.]+)\s*GB", doc)
implemented = sorted(set(re.findall(r"reserve_per_device = \[([0-9.]+)\] \* num_devices", src) + re.findall(r"reserve_per_device\.append\(([0-9.]+)\)", src)))
notes = dict(documented=documented, implemented=implemented)
print(notes, flush=True)
if documented == ["0.25"] and implemented == ["0.5"]: rt.report("stated_behaviour", **notes)
elif documented and implemented and set(documented) == set(implemented): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
