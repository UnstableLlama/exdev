# Trigger: call _strings_to_utf32([]) (also reached by Job construction with an empty stop-string collection).
# Calls exllamav3.generator.job._strings_to_utf32 with [] and compares the returned value with the function's
# declared return annotation (typing.get_type_hints). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the value returned for [] does not conform to the annotation (here: (bytearray(), None)
#                        against tuple[np.ndarray, np.ndarray] | None).
#   expected_behaviour : the returned value conforms to the annotation.
#   other              : anything else.
import typing
import numpy as np
import rt
rt.check_import()
from exllamav3.generator import job as J
r = J._strings_to_utf32([])
ann = typing.get_type_hints(J._strings_to_utf32).get("return")
conforms = r is None or (isinstance(r, tuple) and len(r) == 2 and all(isinstance(x, np.ndarray) for x in r))
notes = dict(returned=repr(r), returned_types=[type(x).__name__ for x in r] if isinstance(r, tuple) else type(r).__name__, annotation=str(ann))
print(notes, flush=True)
rt.report("expected_behaviour" if conforms else "stated_behaviour", **notes)
