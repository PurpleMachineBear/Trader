# Iter 084 Executive Report

This round shows that `estimate availability` matters, but it is not the full explanation for the cloud event branch.

`platform5 pre1 hold3` remained the winner in both windows. On the recent broad sample, the control returned `100.059%`; the `estimate required` subset returned `75.473%`; the `estimate missing` subset only `14.095%`. On `2024-2025`, the same pattern held: control `93.491%`, `estimate required` `64.370%`, `estimate missing` `5.254%`.

The useful conclusion is that the branch mainly lives in ordinary covered earnings events, not in estimate-missing names. But requiring estimates still leaves money on the table, so estimate presence by itself is only a partial quality signal. The next cloud work should move to richer covered-event metadata, not more binary estimate or report-time filters.
