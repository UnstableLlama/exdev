# Trigger: supply a prefix equal to a stored tensor key whose mapped filename is not itself a tensor key.
# A directory holds model.safetensors with tensors "a.b" and "a.b.c"; SafetensorsCollection(dir).list_tensors("a.b")
# and .get_tensors("a.b") are called. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : list_tensors raises KeyError (the filename used as a key) or get_tensors fails looking up
#                        the filename as a tensor.
#   expected_behaviour : both return {"a.b", "a.b.c"}.
#   other              : anything else.
import os, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.loader.safetensors import SafetensorsCollection
d = tempfile.mkdtemp(); save_file({"a.b": torch.ones(4), "a.b.c": torch.ones(2)}, os.path.join(d, "model.safetensors"))
stc = SafetensorsCollection(d)
res = {}
for fn in ("list_tensors", "get_tensors"):
    try:
        res[fn] = {"ok": True, "keys": sorted(getattr(stc, fn)("a.b"))}
    except Exception as e:
        res[fn] = {"ok": False, "exception_type": type(e).__name__, "message": str(e)[:200], "site": rt._site(e.__traceback__)}
print(res, flush=True)
if all(r["ok"] and r["keys"] == ["a.b", "a.b.c"] for r in res.values()): rt.report("expected_behaviour", **res)
elif any((not r["ok"]) and ("model.safetensors" in r["message"] or r["exception_type"] == "KeyError") for r in res.values()): rt.report("stated_behaviour", **res)
else: rt.report("other", **res)
