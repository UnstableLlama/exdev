# Decision: collect-all-validation-problems-implementation-001

Reviewer: Opus. Date: 2026-11-18.

## Decision

**The user has authorised applying the reviewed patch, once.** Asked "should I apply the validator fix?", with my recommendation to
apply it between runs, the user answered: "sure".

## Authorised

1. Apply `reports/collect-all-validation-problems-implementation-001.patch`, sha256 `c98ee67a70696a4464b78cc6cea3034b88df85710efe3cb7bf76b27c608e9d27`, exactly as reviewed in `reviews/verdicts/collect-all-validation-problems-implementation-001.md`
   (sha256 `a2c66f8bdc821a4cf43f21e5b6ecfda25ea5db0c99d3d47dd9aff0747ad0740f`). Check both hashes first.
2. Apply only at a queue boundary: no teacher session active and none starting. Let the current 347 run finish. Hold the next run
   until step 3 is done. Do not interrupt or restart 347 for this.
3. Run the full suite with `EXDEV_SANDBOX_TESTS=1`. If it fails, reverse the patch, leave the walk stopped and file the failure.
4. File `reviews/requests/collect-all-validation-problems-application-001.md` with the patch hash, the changed production file hashes and
   the suite log hash. The walk may continue once the suite passes; it need not wait for my verdict on that request.

Nothing else changes in this step. Runs already started under v3 keep v3. The first real v4 repair must be called out in its request, with
the message sent and whether one turn fixed every listed problem.
