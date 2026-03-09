# iter_070 Analysis

## Objective

Use QuantConnect `Upcoming Earnings` in a cloud-backed lane to test whether different large-cap buckets behave materially better when selection is explicitly restricted to earnings-event windows.

## Sample Coverage

- `2025-01-02` to `2026-03-06`
- Cloud project: `Cloud_Earnings_Research`

## Summary Table

| Candidate | Bucket | Mode | Return | Sharpe | Drawdown | Trades | Backtest |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `candidate_01` | `growth4` | `pre1` | `-18.069%` | `-0.741` | `20.2%` | `32` | `2bcca96f1945a041c5a33ebdbc84c06e` |
| `candidate_02` | `growth4` | `day0` | `-33.029%` | `-1.584` | `33.3%` | `38` | `c49b08d5a5021ec821c0827cb9eab90e` |
| `candidate_03` | `platform7` | `pre1` | `38.970%` | `0.641` | `19.3%` | `50` | `ca0e8b1ee38e11e5fbfe52b0721bd7c5` |
| `candidate_04` | `platform7` | `day0` | `8.430%` | `0.086` | `23.1%` | `58` | `d7d4c6e13b12d7985580b4bb74f3ee51` |
| `candidate_05` | `hardware7` | `pre1` | `-53.876%` | `-1.250` | `57.2%` | `55` | `91997143a3780343ea833b8caf7bd135` |
| `candidate_06` | `hardware7` | `day0` | `-58.931%` | `-1.830` | `60.4%` | `57` | `691d14e41a6a8c2218875c7a6107304f` |

## Comparison Against Local Context

- Same sample local `platform7` passive baseline from `iter_068` / `iter_069`: `-1.170%`
- Same sample local non-event `platform7 BSL` best row from `iter_069`: `-4.847%`
- Same sample local `growth4 BSL next-gen`: `21.595%`

## Useful

- `platform7 pre1` was the clear winner. This is the first strong evidence that the adjacent platform-style large-cap bucket may need explicit earnings timing rather than another non-event `BSL` selector tweak.
- `platform7 day0` stayed positive, but it was much weaker than `pre1`.
- The cloud-only `Upcoming Earnings` lane is now operational. QuantConnect data is sufficient for the first event-aware branch study.

## Not Useful

- `growth4` earnings baskets were clearly negative. The original `growth4` edge does not look like a simple earnings-event basket.
- `hardware7` earnings baskets were catastrophic in both `pre1` and `day0`. This bucket is not a candidate for a naive earnings-basket promotion.
- These are daily event baskets, not deployable strategies. They are evidence about branch habitat, not paper-ready promotion candidates.

## Conclusion

The first cloud event-aware round strongly suggests that `platform7` is an event-driven large-cap branch, while `growth4` and `hardware7` are not. This is exactly the type of separation the local transfer rounds could not explain. The immediate implication is that future large-cap event-aware work should focus on `platform7 pre1` style selection rather than buying richer news data right away.

## Next

- Open a second cloud round around `platform7` only:
  - `pre1`, `pre2`, `pre3`
  - `hold 1`, `hold 2`, `hold 3`
  - optionally `post1`
- Keep `growth4` and `hardware7` out of the next cloud earnings round unless a different event logic is being tested.
- Do not buy Polygon Benzinga yet. QuantConnect `Upcoming Earnings` is enough to establish the first-order event branch map.
