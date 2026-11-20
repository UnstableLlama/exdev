# Trigger: SS_Sample_mn after a sorting step with a nonidentity indices mapping.
# CustomSampler([SS_Sort(), SS_MinP(0.5), SS_Sample_mn()]) on logits [[0, 0, 0, 0, 0, 10]]: after sorting, token 5
# is in column 0 and min-p removes everything else, so the only possible sample is token 5. Also run with SS_Sample
# in place of SS_Sample_mn as a control. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : SS_Sample_mn returns 0 (the sorted column) while the control returns 5.
#   expected_behaviour : SS_Sample_mn returns 5.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.generator.sampler.custom import CustomSampler, SS_Sort, SS_MinP, SS_Sample_mn, SS_Sample
x = torch.tensor([[0., 0., 0., 0., 0., 10.]], device="cuda:0")
mn = [int(CustomSampler([SS_Sort(), SS_MinP(0.5), SS_Sample_mn()]).forward(x.clone(), rand_u32=i).flatten()[0]) for i in range(8)]
ctl = [int(CustomSampler([SS_Sort(), SS_MinP(0.5), SS_Sample()]).forward(x.clone(), rand_u32=i).flatten()[0]) for i in range(8)]
notes = dict(ss_sample_mn=mn, ss_sample_control=ctl)
print(notes, flush=True)
if set(mn) == {0} and set(ctl) == {5}: rt.report("stated_behaviour", **notes)
elif set(mn) == {5}: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
