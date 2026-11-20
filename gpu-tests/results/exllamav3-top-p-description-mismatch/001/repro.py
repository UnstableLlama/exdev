# Trigger: a normalized sorted distribution crossing P after its first token: [0.5, 0.25, 0.125, 0.125], P=0.625.
# CustomSampler([SS_TopP(0.625)]) is run on logits log([0.5, 0.25, 0.125, 0.125]) with return_state; the number
# of tokens with nonzero probability after the step is counted, and SS_TopP's docstring is recorded.
# Classification, fixed before running:
#   stated_behaviour   : one token is retained (the description promises the smallest set exceeding P: two).
#   expected_behaviour : two tokens are retained.
#   other              : anything else.
import math, torch
import rt
rt.check_import()
from exllamav3.generator.sampler.custom import CustomSampler, SS_TopP
x = torch.tensor([[math.log(.5), math.log(.25), math.log(.125), math.log(.125)]], device="cuda:0")
st = CustomSampler([SS_TopP(0.625)]).forward(x, rand_u32=0, return_state=True)
p = st.probs.float().cpu().flatten().tolist()
kept = sum(1 for v in p if v > 0)
notes = dict(probs_after=p, kept=kept, docstring=(SS_TopP.__doc__ or "").strip())
print(notes, flush=True)
rt.report("stated_behaviour" if kept == 1 else "expected_behaviour" if kept == 2 else "other", **notes)
