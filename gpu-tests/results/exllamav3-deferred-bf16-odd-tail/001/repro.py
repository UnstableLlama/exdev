# Trigger: a file-backed BF16 tensor with an odd element count is loaded to CUDA through the deferred path with
# allow_bf16 false. A safetensors file holds a BF16 tensor of 1001 elements (and, for contrast, one of 1000);
# exllamav3.loader.safetensors.SafetensorsCollection loads both to cuda:0 between begin_deferred_load() and
# end_deferred_load() (the deferred path). Results are compared with tensor.to(float16) computed by torch.
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the odd tensor's last element differs from the FP16 reference (its other elements
#                        and the even tensor match).
#   expected_behaviour : both tensors match the FP16 reference exactly.
#   other              : anything else.
import os, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.loader.safetensors import SafetensorsCollection
torch.manual_seed(0)
odd = (torch.randn(1001) * 3).bfloat16(); even = (torch.randn(1000) * 3).bfloat16()
d = tempfile.mkdtemp(); save_file({"odd": odd, "even": even}, os.path.join(d, "t.safetensors"))
stc = SafetensorsCollection(d)
stc.begin_deferred_load()
to = stc.get_tensor("odd", torch.device("cuda:0")); te = stc.get_tensor("even", torch.device("cuda:0"))
stc.end_deferred_load(); torch.cuda.synchronize()
ro, re_ = odd.to(torch.float16), even.to(torch.float16)
go, ge = to.cpu(), te.cpu()
mism = (go.view(torch.int16) != ro.view(torch.int16)).nonzero().flatten().tolist()
notes = dict(dtype=str(to.dtype), odd_mismatch_indices=mism[:10], odd_last_loaded=float(go[-1].float()), odd_last_expected=float(ro[-1].float()),
             even_matches=bool(torch.equal(ge, re_)), deferred_tensors=getattr(stc.metrics, "deferred_tensors", None) if hasattr(stc, "metrics") else None)
print(notes, flush=True)
if mism == [1000] and notes["even_matches"]: rt.report("stated_behaviour", **notes)
elif not mism and notes["even_matches"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
