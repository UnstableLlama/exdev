# Trigger: SS_PresFreqP(p, f, N, 0) with history reaching distance N and nonneutral penalties.
# CustomSampler([SS_PresFreqP(0.5, 0.5, 4, 0)]) on 32 finite logits, with sequence_ids holding 8 distinct past
# tokens (10..17), so tokens lie at distances 1..8 from the end, including exactly 4. The penalized logits
# (return_state) are checked for NaN. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : some penalized logit is NaN.
#   expected_behaviour : all logits finite.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.generator.sampler.custom import CustomSampler, SS_PresFreqP
x = torch.zeros(1, 32, device="cuda:0") + 1.0
seq = torch.arange(10, 18, dtype=torch.long).unsqueeze(0)
st = CustomSampler([SS_PresFreqP(0.5, 0.5, 4, 0)]).forward(x.clone(), sequence_ids=seq, rand_u32=0, return_state=True)
lg = st.logits.float().cpu().flatten()
nan_idx = torch.nonzero(lg.isnan()).flatten().tolist()
notes = dict(nan_tokens=nan_idx, logits_10_17=[float(v) for v in lg[10:18]])
print(notes, flush=True)
rt.report("stated_behaviour" if nan_idx else "expected_behaviour", **notes)
