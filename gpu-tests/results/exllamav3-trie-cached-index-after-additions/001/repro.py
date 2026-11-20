# Trigger: build the trie, add files containing new descendant names, then repeat a trie-backed query.
# SafetensorsCollection over dir1 (tensor "x.a"); list_tensors("x") builds and caches the trie; add_tensor_files(dir2)
# adds "x.b"; list_tensors("x") is repeated and compared with has_tensor("x.b"). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the repeated query omits "x.b" while has_tensor("x.b") is True.
#   expected_behaviour : the repeated query includes "x.b".
#   other              : anything else.
import os, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.loader.safetensors import SafetensorsCollection
d1, d2 = tempfile.mkdtemp(), tempfile.mkdtemp()
save_file({"x.a": torch.ones(2)}, os.path.join(d1, "m1.safetensors")); save_file({"x.b": torch.ones(2)}, os.path.join(d2, "m2.safetensors"))
stc = SafetensorsCollection(d1)
first = sorted(stc.list_tensors("x"))
stc.add_tensor_files(d2)
second = sorted(stc.list_tensors("x")); visible = stc.has_tensor("x.b")
notes = dict(first=first, after_add=second, has_tensor_x_b=visible)
print(notes, flush=True)
if visible and "x.b" not in second: rt.report("stated_behaviour", **notes)
elif "x.b" in second: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
