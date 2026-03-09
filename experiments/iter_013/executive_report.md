# Iteration `iter_013` Executive Report

## Decision

Promote two intraday BSL deployment branches and keep one gap branch as secondary:

- `High-beta BSL aggressive`: `NVDA/TSLA` with `3m` confirmation, `240m` hold, and `vwap_exit` disabled
- `High-beta BSL clean`: `NVDA/TSLA` with `3m` confirmation, `300m` hold, and `vwap_exit` enabled
- `Core large-cap BSL clean`: `AAPL/MSFT/AMZN/META` with `5m` confirmation and `150m` hold
- `High-beta gap`: keep as secondary, not primary

Do not narrow the core branch all the way down to `AMZN/META`. Do not reopen broad gap research outside the high-beta basket.

## Sample Coverage

- Candidates: `121/121 completed`
- Sample: `2025-01-02` to `2026-03-06` (`2026 YTD`)
- Benchmark: `VOO buy-and-hold`
- New baselines added: `equal_weight_buy_and_hold` baskets
- Order-event validation: `121` order-event files inspected, `0` invalid orders
- Total official experiment count to date: `1407`

## Basket Passive Baselines

| Passive Basket | Return % | Drawdown % |
| --- | ---: | ---: |
| `NVDA/TSLA equal-weight buy-and-hold` | `1.997` | `25.5` |
| `AAPL/MSFT/AMZN/META equal-weight buy-and-hold` | `1.643` | `9.8` |
| `AMZN/META equal-weight buy-and-hold` | `3.327` | `18.9` |
| `AMZN/META/MSFT equal-weight buy-and-hold` | `-0.958` | `11.4` |

These baselines materially changed the quality of the conclusions. The best intraday branches were not just beating single names; they were beating their natural basket alternatives by a wide margin.

## Recommended Candidate Set

| Branch | Structure | Return % | Drawdown % | Trades | Why Keep It |
| --- | --- | ---: | ---: | ---: | --- |
| `High-beta BSL aggressive` | `NVDA/TSLA + QQQ/SMH + 3m + 240m + no vwap exit` | `16.787` | `4.8` | `20` | Highest raw-return intraday row |
| `High-beta BSL clean` | `NVDA/TSLA + QQQ/XLK/SMH + 3m + 300m + vwap exit` | `13.215` | `2.0` | `21` | Best clean risk-adjusted profile |
| `Core BSL clean` | `AAPL/MSFT/AMZN/META + QQQ/XLK + 5m + 150m + vwap exit` | `10.899` | `1.6` | `22` | Best large-cap non-high-beta branch |
| `Gap high-beta secondary` | `NVDA/TSLA + QQQ/XLK + 2m + 90m + vwap exit` | `10.418` | `5.5` | `51` | Reproducible specialist gap branch |

## Main Findings

- `High-beta BSL` improved materially from `iter_012`.
  - Best raw return rose from `12.098%` to `16.787%`
  - Best clean profile rose from roughly `12.1% / 2.0%` to `13.215% / 2.0%`
- `Core BSL` also improved materially.
  - Best row rose from `7.406% / 2.4%` to `10.899% / 1.6%`
- Narrowing the core basket to `AMZN/META` did not improve the branch.
- `Gap high-beta` reproduced but did not overtake `BSL high-beta`.
- Daily controls still dominated the whole campaign leaderboard.

## Recommendation

Next round should not reopen a broad search. It should do one of two things:

1. `Deployment validation`
   Keep the four candidate branches above, add more history, and test stability.
2. `Sleeve construction`
   Start researching a portfolio that combines:
   - validated daily control
   - one clean intraday BSL sleeve
   - optional aggressive intraday sleeve

The current evidence no longer supports equal budget across many intraday families. `BSL` is the main branch now.
