# Trigger: select eval/spec/llama3.1-70b-instruct_qtip.json (directly or via a modelspec wildcard).
# Loads the file with json.load, as compare_q.py main does before filtering or evaluation.
# Classification, fixed before running:
#   stated_behaviour   : json.load raises JSONDecodeError on the file.
#   expected_behaviour : the file parses to a list of three model specifications.
#   other              : anything else.
import json, os
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; f = os.path.join(WT, "eval", "spec", "llama3.1-70b-instruct_qtip.json")
try:
    data = json.load(open(f))
except json.JSONDecodeError as e:
    rt.report("stated_behaviour", e, message=str(e), file_tail=open(f).read()[-160:]); raise SystemExit
rt.report("expected_behaviour" if isinstance(data, list) and len(data) == 3 else "other", n=len(data) if isinstance(data, list) else None)
