# Trigger: test_distribution with valid contiguous CUDA float32 input, ref_output of N bins (1 <= N <= 1024)
# and dist_output holding fewer than N float32 elements.
# To observe an overrun without writing outside a real allocation, dist_output is a contiguous view of the
# first M = 128 elements of a larger buffer filled with a sentinel; ref_output has N = 256 bins. If the kernel
# writes N floats through dist_output's pointer, the sentinel elements [M, N) change. The extension binding is
# called directly (no Python caller exists); the call matches the commit's binding arity (5 or 7 arguments).
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the call returns without error and sentinel elements beyond dist_output's size are
#                        overwritten.
#   expected_behaviour : the call is rejected with an exception before launch and the sentinel region is intact.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3.ext import exllamav3_ext as ext
M, N, SENT = 128, 256, -7.0
torch.manual_seed(0)
x = torch.randn(4096, dtype=torch.float, device="cuda:0")
big = torch.full((N + 64,), SENT, dtype=torch.float, device="cuda:0")
dist = big[:M]; ref = torch.zeros(N, dtype=torch.float, device="cuda:0")
nargs = ext.test_distribution.__doc__.split("\n")[0].count("arg")
print("binding arity", nargs, flush=True)
args = [x, dist, ref, -3.0, 3.0] + ([0, 0] if nargs >= 7 else [])
err = None
try:
    ext.test_distribution(*args); torch.cuda.synchronize()
except Exception as e:
    err = e
tail = big[M:N].cpu(); beyond = big[N:].cpu()
over = int((tail != SENT).sum()); over_beyond_N = int((beyond != SENT).sum())
notes = dict(binding_arity=nargs, sentinel_overwritten_in_M_to_N=over, sentinel_overwritten_beyond_N=over_beyond_N,
             exception_type=type(err).__name__ if err else None, message=(str(err).splitlines()[0] if err and str(err) else None))
if err is None and over > 0: rt.report("stated_behaviour", **notes)
elif err is not None and not isinstance(err, TypeError) and over == 0: rt.report("expected_behaviour", err, **notes)
elif isinstance(err, TypeError): rt.report("did_not_run", err, **notes)
else: rt.report("other", err, **notes)
