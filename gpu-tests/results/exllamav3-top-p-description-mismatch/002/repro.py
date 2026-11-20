# Trigger: a normalized sorted distribution crossing P after its first token: [0.5, 0.25, 0.125, 0.125], P=0.625.
# Attempt 002: CustomSampler.forward at this commit has no return_state, so retention is observed through sampling:
# CustomSampler([SS_TopP(0.625), SS_Sample()]) on logits log([0.5, 0.25, 0.125, 0.125]) is sampled 300 times
# (rand_u32 0..299). If only the first token is retained every sample is 0; if two are retained, token 1 appears
# about one third of the time. SS_TopP's docstring is recorded. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : all 300 samples are token 0 (one token retained).
#   expected_behaviour : samples are tokens 0 and 1 only, with token 1 present (two retained).
#   other              : anything else.
import math, torch, collections
import rt
rt.check_import()
from exllamav3.generator.sampler.custom import CustomSampler, SS_TopP, SS_Sample
x = torch.tensor([[math.log(.5), math.log(.25), math.log(.125), math.log(.125)]], device="cuda:0")
s = CustomSampler([SS_TopP(0.625), SS_Sample()])
c = collections.Counter(int(s.forward(x.clone(), rand_u32=i).flatten()[0]) for i in range(300))
notes = dict(sample_counts=dict(c), docstring=(SS_TopP.__doc__ or "").strip())
print(notes, flush=True)
if set(c) == {0}: rt.report("stated_behaviour", **notes)
elif set(c) == {0, 1}: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
