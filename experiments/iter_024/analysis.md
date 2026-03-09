# iter_024 Analysis

## Objective

Run a fresh `2024-01-02` to `2026-03-06` large-cap broad-sample sweep to find which mega-cap dynamic-selection branch deserves deeper regime-aware work.

## Sample Coverage

- Broad sample: `2024-01-02` to `2026-03-06`
- Universe focus:
  - core large-cap: `AAPL`, `MSFT`, `AMZN`, `META`
  - growth-heavy large-cap: `AMZN`, `META`, `NVDA`, `TSLA`
  - mixed mega-cap: `AAPL`, `MSFT`, `AMZN`, `META`, `NVDA`, `TSLA`

## Summary Table

| Structure | Return | Sharpe | Drawdown | Trades | Comment |
| --- | ---: | ---: | ---: | ---: | --- |
| `VOO buy-and-hold` | `42.608%` | `0.574` | `18.8%` | `0` | Broad passive benchmark |
| `core4 equal-weight passive` | `21.588%` | `0.141` | `14.2%` | `0` | Natural large-cap basket baseline |
| `core4 BSL + QQQ/XLK + 5m + 150m` | `5.347%` | `-0.860` | `6.2%` | `30` | Legacy core control stayed low-return |
| `core4 BSL + QQQ/SMH + 5m + 150m` | `5.540%` | `-0.839` | `6.0%` | `30` | Slightly better than `QQQ/XLK`, still weak |
| `core4 BSL + QQQ/XLK/SMH ctx+2 + 5m + 150m` | `5.358%` | `-0.853` | `6.8%` | `31` | Stronger regime gate did not help core4 |
| `all6 mega-cap BSL + ctx+2 + 5m + 150m` | `4.924%` | `-0.616` | `8.2%` | `53` | More activity, worse quality |
| `growth4 BSL + ctx+3 + 3m + 180m` | `10.232%` | `-0.351` | `6.1%` | `50` | Best active large-cap branch this round |
| `mega4 AMZN/META/MSFT/NVDA BSL + ctx+2 + 3m + 180m` | `1.934%` | `-0.949` | `10.0%` | `48` | NVDA-heavy version degraded badly |
| `all6 vwap_reclaim + ctx+2 + 120m` | `5.312%` | `-0.622` | `14.2%` | `202` | Too active for too little edge |
| `growth4 failed_breakdown_reclaim + ctx+2 + 120m` | `3.821%` | `-1.328` | `2.6%` | `31` | Clean drawdown, insufficient edge |

## Selection Distribution

- `core4 BSL + QQQ/XLK + 5m + 150m`:
  - `AMZN 12`, `META 10`, `AAPL 4`, `MSFT 4`
- `growth4 BSL + ctx+3 + 3m + 180m`:
  - `TSLA 18`, `NVDA 13`, `AMZN 10`, `META 9`
- `all6 mega-cap BSL + ctx+2 + 5m + 150m`:
  - `TSLA 17`, `NVDA 14`, `META 9`, `AMZN 9`, `AAPL 2`, `MSFT 2`
- `mega4 AMZN/META/MSFT/NVDA BSL + ctx+2 + 3m + 180m`:
  - `NVDA 21`, `META 12`, `AMZN 11`, `MSFT 4`

## Useful

- `growth4 BSL + ctx+3 + 3m + 180m` was the only active large-cap branch that looked worth deeper work. It was still far below passive return, but it was clearly better than the rest of the active large-cap field.
- Core large-cap BSL still behaves the same way as before: `AMZN/META` drive most of the activity while `AAPL/MSFT` add little. Stronger context alone did not solve the branch.
- The broad mixed mega-cap basket did not improve quality. Adding more names mainly increased activity through `TSLA/NVDA` without producing a better broad result.

## Not Useful

- `core4` regime tweaks around `QQQ/XLK`, `QQQ/SMH`, and `QQQ/XLK/SMH` were effectively all the same weak idea on the broad sample.
- `vwap_reclaim` and `failed_breakdown_reclaim` did not justify immediate large-cap promotion. They either traded too much for too little edge or stayed too weak on return.
- The `AMZN/META/MSFT/NVDA` basket over-concentrated into `NVDA` and degraded badly. Removing `TSLA` did not clean up the branch.

## Next

- Promote `growth4 BSL + ctx+3 + 3m + 180m` into a window-validation round.
- Carry one `core4` control into the next round to verify whether the broad-sample weakness is consistent across `2024`, `2025`, and `2026 YTD`.
- Add same-basket passive baselines for the growth-heavy branch in the next round so active large-cap alpha can be judged against its natural basket, not only against `VOO`.
