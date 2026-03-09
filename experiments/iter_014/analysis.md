# Iteration `iter_014` Analysis

## Decision

Do not hard-code a daily watchlist, but do not replace it with one giant mixed universe either.

The evidence now supports:

- `Dynamic watchlists inside structured buckets`
- `High-beta dynamic watchlists` as the first real upgrade over fixed intraday baskets
- `Fixed core large-cap BSL` as the current core intraday control
- `Event bucket dynamic watchlists` as not ready

## Sample Coverage

- Candidates: `49/49 completed`
- Sample: `2025-01-02` to `2026-03-06` (`2026 YTD`)
- Benchmark: `VOO buy-and-hold`
- Cross-family control: `QQQ/VOO/GLD dual_momentum 126/7`
- Universe: `30` approved symbols, blocklisting `GOOG/GOOGL`
- Dynamic watchlist variable tested: `selection_pool_size = 1 / 3 / 5`
- Order validation: `0` invalid orders
- Total official experiment count to date: `1456`

## Winner Table

| Branch | Candidate | Structure | Return % | Drawdown % | Trades | Comment |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `Daily control` | `candidate_02` | `QQQ/VOO/GLD dual_momentum 126/7` | `38.452` | `13.8` | `4` | Still the highest full-round return leader |
| `BSL score winner` | `candidate_17` | `high-beta dynamic BSL, pool 1, QQQ/SMH` | `24.757` | `6.7` | `37` | Best composite score among intraday rows |
| `BSL raw-return winner` | `candidate_18` | `high-beta dynamic BSL, pool 3, QQQ/SMH` | `26.245` | `7.2` | `51` | Best raw-return BSL row |
| `Gap winner` | `candidate_34` | `high-beta dynamic gap, pool 5, QQQ/XLK` | `22.886` | `5.7` | `103` | Best gap row and best dynamic gap quality |
| `Fixed BSL control` | `candidate_08` | `fixed NVDA/TSLA aggressive BSL` | `16.787` | `4.8` | `20` | Prior control, now clearly surpassed |
| `Fixed core control` | `candidate_09` | `fixed AAPL/MSFT/AMZN/META clean BSL` | `10.899` | `1.6` | `22` | Core branch still better than wider core watchlists |
| `Benchmark` | `candidate_01` | `VOO buy-and-hold` | `14.473` | `19.0` | `0` | Passive benchmark |

## Fixed Vs Dynamic

| Comparison | Fixed Control | Best Dynamic Row | Return Delta % | Drawdown Delta % | Conclusion |
| --- | --- | --- | ---: | ---: | --- |
| `High-beta BSL aggressive` | `candidate_08` | `candidate_18` | `+9.458` | `+2.4` | Dynamic high-beta BSL clearly improved |
| `High-beta gap` | `candidate_10` | `candidate_34` | `+12.468` | `+0.2` | Dynamic high-beta gap clearly improved |
| `Core BSL clean` | `candidate_09` | `candidate_23` | `-4.300` | `+0.7` | Dynamic core watchlist did not beat fixed core basket |
| `High-beta BSL clean` | `candidate_07` | `candidate_14` | `-13.296` | `+4.6` | Broadening the clean high-beta branch was a failure |

## Watchlist Selection Distribution

The dynamic winners were not fake upgrades. They actually rotated into new names beyond the old two-name baskets.

| Candidate | Main Symbols Traded |
| --- | --- |
| `candidate_18` | `NVDA 10`, `TSLA 10`, `AMD 10`, `MRVL 8`, `AVGO 7`, `MU 5`, `TSM 1` |
| `candidate_34` | `AMD 18`, `MU 17`, `TSLA 17`, `NVDA 16`, `AVGO 16`, `TSM 11`, `MRVL 8` |
| `candidate_39` | Mostly `MU/MRVL/TSLA/TSM/AMD/AVGO/NVDA`, with only small `ORCL/NFLX/AMZN/META/CRM` participation |

This is the main answer to the ticker-selection question:

- `Ticker choice should not be manually written each day`
- `Ticker choice should come from a broad approved bucket`
- `The bucket itself still matters`
- `The best dynamic watchlists were still specialized high-beta/semiconductor universes, not giant mixed universes`

## Yearly Return Table

| Structure | 2025 | 2026 YTD |
| --- | ---: | ---: |
| `VOO buy-and-hold` | `16.08%` | `-1.39%` |
| `QQQ/VOO/GLD dual_momentum 126/7` | `16.06%` | `19.29%` |
| `candidate_17 high-beta dynamic BSL` | `15.70%` | `7.83%` |
| `candidate_18 high-beta dynamic BSL` | `11.98%` | `12.74%` |
| `candidate_34 high-beta dynamic gap` | `16.72%` | `5.28%` |
| `candidate_08 fixed high-beta aggressive BSL` | `8.30%` | `7.84%` |
| `candidate_09 fixed core clean BSL` | `7.63%` | `3.04%` |

## Useful

- `Dynamic high-beta BSL aggressive` worked. The broad high-beta watchlist beat the fixed `NVDA/TSLA` aggressive control by a wide margin.
- `Dynamic high-beta gap` worked even better than expected. Pool sizes above `1` helped this branch materially.
- `Broad master universe + daily watchlist pool` is the right abstraction, but only inside the right bucket.
- `QQQ/SMH` remained the strongest context for dynamic high-beta BSL.
- `QQQ/XLK` remained the strongest context for dynamic high-beta gap.

## Not Useful

- `Dynamic high-beta BSL clean` failed across the board. The extra names degraded the cleaner exit profile.
- `Dynamic core BSL` did not beat the fixed `AAPL/MSFT/AMZN/META` control.
- `Dynamic combined BSL` was mostly a failure, especially once pool size rose above `1`.
- `Event bucket` branches were not ready. Gap and BSL rows on `XOM/CVX/OXY/LMT/EXPE/OKTA` were mostly negative.
- `Pool 5` was not universally better. It helped gap more than BSL, and hurt core/combined branches.

## Invalid Or Risky

- No process failures or invalid orders were found.
- Execution realism is still not solved. Order-event files show LEAN warnings that fills used `TradeBar` data when quote data was unavailable. That does not invalidate the round, but it is a reason to stay conservative about paper/live expectations.

## Next

The next round should not reopen the whole search space. It should do three focused things:

1. Keep `fixed core clean BSL` as the core intraday control.
2. Promote two dynamic high-beta branches:
   - `dynamic high-beta BSL aggressive`
   - `dynamic high-beta gap`
3. Add the next missing layer:
   - `earnings / catalyst regime`
   - `premarket planning engine`
   - `portfolio-level risk caps`

The strategic conclusion is now clearer:

- `Watchlists should be dynamic`
- `Dynamic watchlists should be bucketed`
- `High-beta is the first bucket where the dynamic approach clearly pays`
- `Core large-cap remains better as a tighter fixed basket for now`
