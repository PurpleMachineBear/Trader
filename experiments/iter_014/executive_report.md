# Iteration `iter_014` Executive Report

## Decision

Stop treating ticker choice as a hand-written watchlist. Move to `dynamic daily watchlists`, but only inside structured buckets.

Promote:

- `Dynamic high-beta BSL aggressive`
- `Dynamic high-beta gap`

Keep:

- `Fixed core clean BSL` as the core intraday control
- `QQQ/VOO/GLD dual_momentum 126/7` as the cross-family daily control

Do not promote:

- `Dynamic core watchlists`
- `Dynamic event watchlists`
- `Dynamic mixed-universe BSL`

## What Changed

This round upgraded the intraday scanner from a single selected symbol to a `top-N daily watchlist pool`, added liquidity and premarket-dollar-volume filters, and expanded the approved minute-data universe to a broader liquid master set.

That was the right change. The results show the system can now decide tickers dynamically instead of relying on a manually frozen basket.

## Key Findings

| Branch | Best Row | Return % | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: |
| `Daily control` | `QQQ/VOO/GLD dual_momentum 126/7` | `38.452` | `13.8` | `4` |
| `Dynamic high-beta BSL` | `candidate_18` | `26.245` | `7.2` | `51` |
| `Dynamic high-beta gap` | `candidate_34` | `22.886` | `5.7` | `103` |
| `Fixed high-beta BSL control` | `candidate_08` | `16.787` | `4.8` | `20` |
| `Fixed core BSL control` | `candidate_09` | `10.899` | `1.6` | `22` |
| `VOO benchmark` | `candidate_01` | `14.473` | `19.0` | `0` |

## What Was Useful

- Dynamic high-beta watchlists clearly improved the aggressive BSL branch.
- Dynamic high-beta watchlists improved the gap branch even more.
- The winner rows actually traded `AMD`, `MU`, `MRVL`, `AVGO`, and `TSM`, not just `NVDA` and `TSLA`.

## What Was Not Useful

- Dynamic core watchlists did not beat the fixed `AAPL/MSFT/AMZN/META` control.
- Event-driven watchlists on `XOM/CVX/OXY/LMT/EXPE/OKTA` were not good enough.
- Large mixed-universe BSL was mostly a downgrade.

## Recommendation

Next round should focus on:

1. `Dynamic high-beta BSL aggressive`
2. `Dynamic high-beta gap`
3. `Fixed core clean BSL`

And add:

- `earnings / catalyst regime`
- `premarket planning engine`
- `portfolio-level risk caps`

The key conclusion is simple: `ticker selection should be dynamic, but not universal`. The profitable version is `bucketed dynamic selection`, not a giant mixed watchlist.
