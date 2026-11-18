# Decision: the author may run ahead while a request is under review

Recorded by Fable (reviewer) on 2026-11-17, about 00:05 UTC.

## The user's words

Asked "Let the author run up to three commits ahead of my reviews?", the user answered:

> the only thing im worried about is you falling out of cache hits on your input tokens with that. I would
> allow the runner to go ahead while you are reviewing, but i guess i dont want you waiting for 2 or 3 to stack
> up, if you understand

## What is decided (my reading, stated so the user can correct it)

1. The author no longer has to wait for a verdict before starting the next teacher run. While a request is
   awaiting or under review it may prepare and run the next position, and file that request when it finishes.
2. The reviewer does not batch. Each request is reviewed as soon as it arrives, oldest first. Nothing waits
   for others to accumulate.
3. Safety cap (mine, to bound rework): at most **three** requests may be without a verdict at once. At three
   the author stops starting runs until one is decided.
4. A run started ahead is authored without the entries of positions still under review. Its request must say
   so and name them ("ran ahead of N, M"). If the reviewer finds that a missing entry mattered, or an earlier
   position is rejected and its retry changes what a later entry should say, the reviewer asks for that later
   position to be rerun. Approval order stays ascending: a position is recorded as approved only after every
   earlier position is.
5. Everything else stands: one teacher session at a time, ancestor retrieval scope only, ledger items filed
   with the next request, nothing committed or pushed.

If the walk tooling cannot do this as it is (journal states, packet preparation from a partly approved
history), the author files an implementation request first and keeps to one at a time until it is accepted.
