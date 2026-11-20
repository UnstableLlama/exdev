# Trigger: call Gemma2Model.default_chat_prompt or Gemma3Model.default_chat_prompt with a nonempty system_prompt.
# The methods do not use self, so they are called on the classes directly (self=None) with prompt "Hello" and
# system_prompt "SYSTEM-TEXT-42". Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the returned prompts lack SYSTEM-TEXT-42 and contain the literal "{system_prompt}".
#   expected_behaviour : the returned prompts contain SYSTEM-TEXT-42.
#   other              : anything else.
import rt
rt.check_import()
from exllamav3.models.gemma2 import Gemma2Model
from exllamav3.models.gemma3 import Gemma3Model, Gemma3TextModel
out = {c.__name__: c.default_chat_prompt(None, "Hello", "SYSTEM-TEXT-42") for c in (Gemma2Model, Gemma3Model, Gemma3TextModel)}
notes = {k: dict(text=v, has_system=("SYSTEM-TEXT-42" in v), has_placeholder=("{system_prompt}" in v)) for k, v in out.items()}
print(notes, flush=True)
if all((not n["has_system"]) and n["has_placeholder"] for n in notes.values()): rt.report("stated_behaviour", **notes)
elif all(n["has_system"] for n in notes.values()): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
