# Trigger: compile a model configuration that uses the tie_word_embeddings key and expect update_config to force
# the setting true. exllamav3.conversion.quant_config.update_config (called by compile_model on the output
# config.json) is applied to {"tie_word_embeddings": False} and, for contrast, to {"tied_word_embeddings": False}.
# Classification, fixed before running:
#   stated_behaviour   : tie_word_embeddings stays False (only the tied_word_embeddings spelling is updated).
#   expected_behaviour : tie_word_embeddings becomes True.
#   other              : anything else.
import rt
rt.check_import()
from exllamav3.conversion.quant_config import update_config
a = {"tie_word_embeddings": False}; b = {"tied_word_embeddings": False}
update_config(a); update_config(b)
notes = dict(tie_word_embeddings_after=a, tied_word_embeddings_after=b)
print(notes, flush=True)
if a["tie_word_embeddings"] is False and b["tied_word_embeddings"] is True: rt.report("stated_behaviour", **notes)
elif a["tie_word_embeddings"] is True: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
