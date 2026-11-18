# Trigger: an uncached evaluation with nonempty valid data and no model spec containing out_logits.
import re
import rt, cqcli as c
rt.check_import()
rc, t = c.run("compare_q.py", "-d", c.DATA, "-m", c.SPEC)
et, s = c.tb(t); ppl = re.findall(r"Perplexity: ([\d.]+)", t)
if et == "ZeroDivisionError": rt.report("stated_behaviour", etype=et, esite=s, returncode=rc)
elif et: rt.report("other", etype=et, esite=s, returncode=rc, tail=t[-400:])
elif rc == 0 and ppl: rt.report("expected_behaviour", perplexity=ppl[-1])
else: rt.report("did_not_run", returncode=rc, tail=t[-400:])
