# Iteration `iter_012` Executive Report

## Decision

Keep the validated daily controls unchanged. Promote `BSL scanner` as the main intraday research branch, with two separate deployment tracks:

- `NVDA/TSLA` high-beta scanner as the primary intraday exploit branch
- `AAPL/MSFT/AMZN/META` core large-cap scanner as the secondary, lower-volatility branch

Do not spend equal budget on broad `gap` research anymore. Only keep `gap scanner` inside the `NVDA/TSLA` high-beta bucket.

## Sample Coverage

- Candidates: `201/201 completed`
- Sample: `2025-01-02` to `2026-03-06` (`2026 YTD`)
- Universe: `AAPL`, `MSFT`, `AMZN`, `META`, `NVDA`, `TSLA`, `SPY`, `QQQ`, `IWM`, `XLK`, `SMH`, `VOO`, `GLD`, `TQQQ`
- Benchmark: `VOO buy-and-hold`
- Total official experiment count to date: `1286`
- Order-event validation: `201` order-event files inspected, `0` invalid orders

## Summary Table

| Structure | Role | Return % | Drawdown % | Trades | Verdict |
| --- | --- | ---: | ---: | ---: | --- |
| `GLD 18/110 + 189d` | daily control | `88.697` | `14.1` | `2` | Still the overall winner on the common sample |
| `QQQ/VOO/GLD 126/7` | daily control | `38.452` | `13.8` | `4` | Best non-leveraged cross-family control |
| `NVDA/TSLA BSL scanner + SPY/QQQ/IWM + 3m confirm + 240m hold` | intraday exploit | `12.098` | `2.0` | `21` | Best intraday quality row |
| `NVDA/TSLA gap scanner + QQQ/XLK + 2m confirm + 90m hold` | intraday explore | `10.418` | `5.5` | `51` | Best gap branch, but clearly high-beta only |
| `AAPL/MSFT/AMZN/META BSL scanner + QQQ/XLK + 3m confirm + 240m hold` | intraday exploit | `7.406` | `2.4` | `25` | Best core large-cap intraday branch |
| `VOO buy-and-hold` | benchmark | `14.473` | `19.0` | `0` | Passive benchmark |

## Main Findings

- `BSL` was the clear intraday winner. The edge generalized beyond the original `MSFT` pilot.
- The strongest intraday branch was not `AAPL/MSFT`; it was `NVDA/TSLA` under scanner selection and market-context filters.
- `core4 BSL scanner` worked because it mostly selected `AMZN` and `META`, not because `AAPL/MSFT` suddenly became great.
- `gap` was not universally broken. It was broken on `AAPL/MSFT` and mostly weak on `core4`, but it became a real branch on `NVDA/TSLA`.
- Daily controls still dominated the full leaderboard. The new intraday branches are promising sleeves, not replacements for the best daily systems.

## Useful

- `NVDA/TSLA BSL scanner`: top three rows returned `11.077%` to `12.098%` with only `2.0%` drawdown and `20-21` trades.
- `core4 BSL scanner`: best row returned `7.406%` with `2.4%` drawdown and `25` trades.
- Direct `BSL` transfer worked on `AMZN`, `TSLA`, and `MSFT`:
  - `AMZN BSL`: `5.640%` return, `2.2%` drawdown
  - `TSLA BSL`: `4.673%` return, `4.2%` drawdown
  - `MSFT BSL`: `2.753%` return, `1.3%` drawdown
- `NVDA/TSLA gap scanner` became a valid exploratory branch, especially with `QQQ/XLK` context.

## Not Useful

- `AAPL gap` remained weak even after the longer sample and better exits.
- `gap scanner` on `AAPL/MSFT` was decisively poor.
- `gap scanner` on `core4` improved a little, but average performance stayed negative.
- Direct `BSL` on `META` and direct `gap` on `META/TSLA` were poor uses of research budget.

## Recommendation

Run `iter_013` in three separated intraday tracks:

1. `BSL high-beta exploit`
   Focus on `NVDA/TSLA`, keep `240m` holds, and refine context plus stop/target logic.
2. `BSL core4 exploit`
   Keep `AAPL/MSFT/AMZN/META`, but recognize that `AMZN/META` are the real alpha carriers.
3. `Gap high-beta explore`
   Keep only `NVDA/TSLA` plus `QQQ/XLK` style context. Do not reopen broad `gap` grids.

Also add basket passive baselines for `NVDA/TSLA` and `core4`, because single-symbol passive references are no longer enough for scanner deployment decisions.
