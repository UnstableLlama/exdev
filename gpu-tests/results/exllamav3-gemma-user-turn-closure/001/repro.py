# Trigger: format a request through Gemma2Model / Gemma3Model / Gemma3TextModel .default_chat_prompt.
# Called on the classes directly (the method does not use self) with prompt "Hello" and no system prompt; the
# result is checked for a closing <end_of_turn> after the user content, before <start_of_turn>model.
# Classification, fixed before running:
#   stated_behaviour   : no <end_of_turn> appears before the model turn starts (in all three).
#   expected_behaviour : the user turn is closed with <end_of_turn> before <start_of_turn>model.
#   other              : anything else.
import rt
rt.check_import()
from exllamav3.models.gemma2 import Gemma2Model
from exllamav3.models.gemma3 import Gemma3Model, Gemma3TextModel
res = {}
for c in (Gemma2Model, Gemma3Model, Gemma3TextModel):
    s = c.default_chat_prompt(None, "Hello")
    head = s.split("<start_of_turn>model")[0]
    res[c.__name__] = dict(text=s, turn_starts=s.count("<start_of_turn>"), turn_ends=s.count("<end_of_turn>"), closed_before_model="<end_of_turn>" in head)
print(res, flush=True)
if all(not r["closed_before_model"] for r in res.values()): rt.report("stated_behaviour", **res)
elif all(r["closed_before_model"] for r in res.values()): rt.report("expected_behaviour", **res)
else: rt.report("other", **res)
