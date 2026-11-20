# Trigger: a custom chain reaches SS_Argmax with sorted logits. CustomSampler([SS_Sort(), SS_Argmax()]) on
# logits [[1, 5, 2, 4]] (argmax token 1). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : forward fails (sample left None / not mapped) or returns a token other than 1.
#   expected_behaviour : forward returns token 1.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.generator.sampler.custom import CustomSampler, SS_Sort, SS_Argmax
x = torch.tensor([[1., 5., 2., 4.]], device="cuda:0")
try:
    st = CustomSampler([SS_Sort(), SS_Argmax()]).forward(x, rand_u32=0, return_state=True)
except Exception as e:
    rt.report("stated_behaviour", e, message=str(e)); raise SystemExit
smp = st.sample
notes = dict(sample=None if smp is None else smp.flatten().tolist(), state=str(st.state))
print(notes, flush=True)
if smp is None or smp.flatten().tolist() != [1]: rt.report("stated_behaviour", **notes)
else: rt.report("expected_behaviour", **notes)
