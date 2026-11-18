# Trigger: call Dots1Model.default_chat_prompt("U") and compare with the single-user-message strings the
# ledger gives for the pinned Dots templates. The method takes self but does not use it, so None is passed.
import rt
rt.check_import()
from exllamav3.models.dots1 import Dots1Model
BODY = "<|userprompt|>U<|endofuserprompt|><|response|>"
BASE = "<|system|><|endofsystem|>" + BODY
INST = "<|system|>You are a helpful assistant.<|endofsystem|>" + BODY
p = Dots1Model.default_chat_prompt(None, "U")
notes = dict(prompt=p, equals_base_template=p == BASE, equals_instruction_template=p == INST)
if p in (BASE, INST): rt.report("expected_behaviour", **notes)
elif p.startswith("<|userprompt|>"): rt.report("stated_behaviour", **notes)
else: rt.report("other", **notes)
