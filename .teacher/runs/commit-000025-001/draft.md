# 825408b22bf032e38321c37d6925394cf93293c1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/825408b22bf032e38321c37d6925394cf93293c1) · [Evidence ledger](draft.json)

Fixes negative minute remainders in duration formatting and omits zero minutes from hour-bearing output.

- [Format complete hours and remaining minutes](#runtime)

## Problem

human_time rounded minutes and hours independently before subtracting hours, allowing positive durations to display negative minutes. [source; call_2ef9297fb3d24464b262310bb0b934a7]

## Reasoning

Removing the two +30 offsets makes each division by 60 count complete units after the initial seconds rounding. Subtracting complete hours then leaves a nonnegative minute remainder for nonnegative inputs. [source; call_675c7ada97c8466fb362e033496fcf81, call_2ef9297fb3d24464b262310bb0b934a7]

## Impact

The located direct caller formats conversion's remaining-time estimate: the latest module duration multiplied by the number of remaining modules. The patch changes its display, not the estimate calculation or quantization. [source; call_3eb72a872a0b4d82aa1132a0a5127b0c, call_10e64627bb1c4a21b4e83a81b2ca0026, call_675c7ada97c8466fb362e033496fcf81]

## Source Notes

The earlier timing entry recorded the negative-minute observation in human_time. [ancestor; call_763d9cf2923d4892aeade10d397b84db]

Inspection of the parent implementation and task diff shows that the offending upward hour rounding is removed, rather than carried over. [source; call_2ef9297fb3d24464b262310bb0b934a7, call_675c7ada97c8466fb362e033496fcf81]

<a id="runtime"></a>

## Format complete hours and remaining minutes

human_time retains round(seconds), then computes complete minutes and hours using 60 seconds per minute and 60 minutes per hour. It omits the minute component when an hour-bearing duration has zero remaining minutes; the minute-only and '< 1 minute' branches remain. [source; call_675c7ada97c8466fb362e033496fcf81, call_2ef9297fb3d24464b262310bb0b934a7]

The transcription changes 1800 seconds from '1 hour, -30 minute' to '30 minutes', 5400 to '1 hour, 30 minutes', and 3600 to '1 hour'. Its decomposition check passed for every integer second from 0 through 86400. [execution; call_338564e5996e41de9ff72c43430632ac]

The display now favors complete minutes over nearest-minute rounding, although the retained seconds rounding still affects boundaries: the transcription reports '< 1 minute' at 59.4 seconds and '1 minute' at 59.5 seconds. [execution; call_338564e5996e41de9ff72c43430632ac]

## Uncertainty and limits

Validation used a scalar transcription, not the repository implementation or a conversion run.

The caller search establishes literal in-tree usage, not external or dynamic consumers.
