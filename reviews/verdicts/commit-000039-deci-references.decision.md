# Decision: re-author commit 39 with Deci's own repositories as reference evidence

Recorded by Fable (reviewer) on 2026-11-13.

## The user's words

Asked "Re-author commit 39 with Deci's own DeciLM models added to its reference evidence?", with my recommendation to do
so, the user answered:

> Yes, re-author 39

## Background

`reviews/verdicts/reference-discovery-implementation-001.md`, section "For the user". Commit 39 registers
`DeciLMForCausalLM`. Its reference evidence was drawn from the `nvidia` organisation only. The architecture's original
publisher, `Deci`, has repositories that declare the same string (`Deci/DeciLM-7B`, created 2023-12-10;
`Deci/DeciLM-7B-instruct`; `Deci/DeciLM-6b`) with a differently shaped configuration.

## What follows from it (my interpretation, not the user's words)

1. Run the accepted discovery tool for organisation `Deci`, architecture `DeciLMForCausalLM`, at commit 39's cutoff.
   Attach every match, configs and headers, alongside the four `nvidia` models already attached. Pins must be at or
   before the cutoff; verify them, do not take the repository names above on trust.
2. Author a fresh attempt 39/006 on the rebuilt packet. It is **unassisted**: commit 39's one reviewer-assisted attempt
   was 005, and no coverage request is issued for 006. Reference selection is administrative input and does not make a
   run assisted.
3. 39/005 stays the entry in force until 006 is reviewed. If 006 is approved it supersedes 005 for future retrieval; 005
   stays approved on record.
4. Later runs that read commit 39's entry (the request should list them; 72/002 is one) are not re-authored on this
   account. If 006 changes something a dependent relied on, say so in the request and I will raise it.
5. Order: finish and file whatever commit is in progress, then do 39/006, then resume the walk.
6. General rule from now on: reference discovery for a new architecture covers every organisation that officially
   publishes checkpoints declaring the registered string, the original publisher included. Which organisations count is
   recorded in the discovery report with a reason.
