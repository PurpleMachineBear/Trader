# Iteration `iter_006` Executive Report

## Decision

Continue. Batch 1 materially improved the research process and produced a new leading configuration on the extended `2022-01-01` to `2026-03-06` sample.

## Winner

`candidate_171` won the round: `QQQ/VOO/GLD dual_momentum` with `126-day` lookback and `10-day` rebalance.

- Net profit: `188.741%`
- Sharpe ratio: `1.150`
- Max drawdown: `13.9%`
- Composite score: `275.941`
- Trades: `20`

## What Changed

- The sample was extended through `2026-03-06`, so the results now include `2025` and `2026 YTD`.
- The ETF universe was widened to include `TQQQ`, `GLD`, `IEF`, `DIA`, and `XLK`.
- A new `donchian_regime` family was added.
- The research process exposed and fixed two real workflow defects:
  - `--jobs 10` created avoidable Docker race failures on large batches
  - `dual_momentum` originally used a same-bar rotation pattern that created invalid orders

## Summary Table

| Candidate | Description | Score | Return % | Sharpe | Drawdown % |
| --- | --- | ---: | ---: | ---: | ---: |
| `candidate_171` | `QQQ/VOO/GLD dual_momentum`, `126d`, `10d` | `275.941` | `188.741` | `1.150` | `13.9` |
| `candidate_172` | `QQQ/VOO/GLD dual_momentum`, `126d`, `21d` | `267.574` | `184.074` | `1.111` | `13.8` |
| `candidate_046` | `GLD sma_regime`, `30/150`, `252d` | `257.801` | `175.601` | `1.100` | `13.9` |
| `candidate_045` | `GLD sma_regime`, `50/200`, `252d` | `245.365` | `167.765` | `1.052` | `13.8` |
| `candidate_170` | `QQQ/VOO/GLD dual_momentum`, `126d`, `5d` | `244.572` | `168.072` | `1.041` | `13.8` |
| `candidate_004` | `GLD buy-and-hold` | `241.126` | `180.326` | `1.028` | `21.0` |

## Yearly Return Table

| Candidate | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
| --- | ---: | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `-20.26%` | `24.33%` | `23.36%` | `16.39%` | `-1.39%` |
| `GLD buy-and-hold` | `0.44%` | `12.69%` | `26.65%` | `63.67%` | `19.48%` |
| `SPY 40/180 + 252d` | `0.00%` | `19.06%` | `24.51%` | `13.46%` | `-0.13%` |
| `QQQ 40/180 + 252d` | `0.00%` | `37.98%` | `27.34%` | `17.95%` | `-2.41%` |
| `QQQ/VOO/GLD 126d/10d` | `-7.44%` | `37.67%` | `23.70%` | `53.16%` | `19.60%` |

## Key Findings

- The strongest new edge came from using `GLD` as the defensive leg in rotation, not from continuing to rely on `TLT`.
- `GLD` itself was strong enough to dominate the single-asset leaderboard in passive, SMA, and Donchian forms.
- `QQQ` trend timing remained strong and still beat passive `QQQ`, so the prior growth-trend finding survived the longer sample.
- Timed `TQQQ` is viable as a high-octane explore path, but its drawdown profile is still much worse than the top GLD and rotation winners.

## Main Risks

- The current best results are concentrated in a `GLD`-favorable regime, so the next step needs stricter validation rather than immediately expanding the search space again.
- The best `TQQQ` and `rotation_rsi` variants still carry drawdowns that are too large for a primary control role.
- A heterogeneous universe makes single-benchmark interpretation fragile. The next round needs more symbol-native passive references.

## Recommendation For Next Round

- Keep `VOO buy-and-hold` as the common benchmark.
- Keep `QQQ 40/180 + 252-day time stop` as the aggressive trend control.
- Promote `QQQ/VOO/GLD dual_momentum` as the main cross-family control.
- Add same-symbol passive references for the main single-asset ETFs.
- Focus the next batch on:
  - `QQQ/VOO/GLD` exploit variants near the winning parameter cluster
  - `GLD` trend refinement
  - selective `TQQQ` timing tests
  - less budget on fresh `TLT` and `IEF` sweeps
