# Trigger: eval/compare_q_logits.py reaches save_tensor after successful forwarding.
import os, re
from safetensors import safe_open
import rt, cqcli as c
rt.check_import()
out = os.path.join(c.TMP, "logits.safetensors")
rc, t = c.run("compare_q_logits.py", "-m", c.M, "-d", c.DATA, "-r", "2", "-rpb", "1", "-o", out)
et, s = c.tb(t); msg = re.findall(r"^ValueError: .*$", t, re.M)
if et == "ValueError" and "save_tensor" in t and msg and "tuple" in msg[-1]:
    rt.report("stated_behaviour", etype=et, esite=s, message=msg[-1], file_written=os.path.exists(out))
elif et: rt.report("other", etype=et, esite=s, returncode=rc, tail=t[-400:])
elif rc == 0 and os.path.exists(out):
    with safe_open(out, framework="pt") as f: k = sorted(f.keys()); sh = f.get_slice(k[0]).get_shape()
    rt.report("expected_behaviour" if k == ["tensor.0", "tensor.1"] else "other", keys=k, first_shape=sh)
else: rt.report("did_not_run", returncode=rc, tail=t[-400:])
