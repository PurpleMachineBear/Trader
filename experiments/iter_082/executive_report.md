# Iter 082 Executive Report

`platform5 pre1 hold3` stayed the clear winner. Adding hard pre-event state gates made the cloud earnings branch worse in every tested window.

On the recent broad sample `2025-01-02` to `2026-03-06`, the ungated control returned `100.059%` with `10.1%` drawdown. A mild pullback gate dropped that to `64.432%`, a deeper pullback gate to `15.600%`, and a strength-only gate to just `4.755%` with negative Sharpe. The earlier `2024-2025` aggregate told the same story: control `93.491%`, mild pullback `30.957%`, deeper pullback `18.352%`, strength-only `38.691%`.

The implication is useful: this branch is not a simple `pullback before earnings` trade, and it is not a pure `strength before earnings` continuation either. The current event edge depends on a richer mix of event states than trailing return alone. The next cloud research should move toward better event metadata and state detection, not more basket changes or more hard return gates.
