# Iteration `iter_012` Analysis

## What Changed

This round upgraded the intraday track in four ways:

- extended the minute sample from `2025-06-02` back to `2025-01-02`
- added scanner-based families with explicit `context_symbols`
- expanded the approved universe to `Mag7 ex-GOOG` plus ETF proxy context symbols
- added explicit time-based exits to the direct single-symbol intraday families

The round mixed:

- `4` validated daily controls / benchmark references
- `9` same-sample passive baselines
- `40` direct single-symbol intraday rows
- `148` scanner intraday rows

## Intraday Quality Table

| Structure | Return % | Drawdown % | Return/Drawdown | Trades | Observation |
| --- | ---: | ---: | ---: | ---: | --- |
| `NVDA/TSLA BSL scanner + SPY/QQQ/IWM + 3m confirm + 240m hold` | `12.098` | `2.0` | `6.049` | `21` | Best intraday quality row |
| `NVDA/TSLA BSL scanner + QQQ/SMH + 3m confirm + 240m hold` | `11.832` | `2.0` | `5.916` | `20` | Same branch stayed strong under a second context |
| `NVDA/TSLA BSL scanner + QQQ/XLK + 3m confirm + 240m hold` | `11.077` | `2.0` | `5.538` | `21` | Third context also worked; edge was not single-context noise |
| `AAPL/MSFT/AMZN/META BSL scanner + QQQ/XLK + 3m confirm + 240m hold` | `7.406` | `2.4` | `3.086` | `25` | Best core large-cap scanner row |
| `AAPL/MSFT/AMZN/META BSL scanner + QQQ/XLK + 5m confirm + 150m hold` | `4.625` | `1.6` | `2.891` | `18` | Stricter confirmation still held up |
| `AMZN BSL direct + 240m hold` | `5.640` | `2.2` | `2.564` | `15` | Strongest direct transfer |
| `AAPL/MSFT/AMZN/META BSL scanner + QQQ/SMH + 3m confirm + 240m hold` | `6.129` | `2.4` | `2.554` | `26` | Core4 BSL was not tied to one context only |
| `NVDA/TSLA gap scanner + QQQ/XLK + 2m confirm + 120m hold` | `9.936` | `4.0` | `2.484` | `37` | Best gap-quality compromise |
| `NVDA/TSLA gap scanner + QQQ/XLK + 3m confirm + 180m hold` | `9.381` | `3.9` | `2.405` | `37` | Similar branch, slightly lower return and drawdown |
| `MSFT BSL direct + 240m hold` | `2.753` | `1.3` | `2.118` | `10` | Old pilot still valid on the longer sample |

## Useful

### 1. `BSL` generalized beyond the original `MSFT` pilot

The strongest direct rows were:

- `AMZN BSL`: `5.640%` return, `2.2%` drawdown, `15` trades
- `TSLA BSL`: `4.673%` return, `4.2%` drawdown, `20` trades
- `MSFT BSL`: `2.753%` return, `1.3%` drawdown, `10` trades

Same-sample passive references over the same window were:

- `AMZN buy-and-hold`: `-4.204%` return, `31.0%` drawdown
- `MSFT buy-and-hold`: `-2.886%` return, `29.1%` drawdown
- `TSLA buy-and-hold`: `3.994%` return, `48.2%` drawdown

This is strong evidence that `BSL` is now a family edge, not a one-symbol accident.

### 2. `core4 BSL scanner` found the right expansion path

The best `core4` scanner rows were positive across all three context groups:

| Basket | Context | Count | Avg Return % | Best Return % |
| --- | --- | ---: | ---: | ---: |
| `AAPL/MSFT/AMZN/META` | `QQQ/XLK` | `7` | `2.574` | `7.406` |
| `AAPL/MSFT/AMZN/META` | `QQQ/SMH` | `6` | `2.071` | `6.129` |
| `AAPL/MSFT/AMZN/META` | `SPY/QQQ/IWM` | `6` | `1.790` | `4.706` |

The top rows were mostly driven by `AMZN` and `META`, not by the old `MSFT` pilot names:

- `candidate_079`: `AMZN 11`, `META 9`, `MSFT 3`, `AAPL 2`
- `candidate_091`: `AMZN 11`, `META 9`, `MSFT 4`, `AAPL 2`

That matters. It means the better universe design was not “keep optimizing MSFT.” It was “let the scanner choose across a better large-cap basket.”

### 3. `NVDA/TSLA BSL scanner` became the main intraday exploit

High-beta BSL scanner rows were the strongest intraday family cluster in the whole round:

| Basket | Count | Avg Return % | Avg Drawdown % | Avg Trades | Best Return % |
| --- | ---: | ---: | ---: | ---: | ---: |
| `NVDA/TSLA` | `18` | `3.591` | `4.44` | `21.8` | `12.098` |

Top selection distribution was balanced enough to trust the basket:

- `candidate_121`: `TSLA 14`, `NVDA 7`
- `candidate_127`: `TSLA 14`, `NVDA 6`
- `candidate_115`: `TSLA 14`, `NVDA 7`

This was TSLA-led, but not TSLA-only.

### 4. `gap` was only valid in the high-beta basket

Gap behaved very differently by basket:

| Family Branch | Count | Avg Return % | Avg Drawdown % | Avg Trades | Verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| `gap scanner` on `NVDA/TSLA` | `18` | `4.723` | `4.88` | `37.6` | Keep |
| `gap scanner` on `all6` | `18` | `0.753` | `5.88` | `41.3` | Secondary only |
| `gap scanner` on `core4` | `19` | `-1.151` | `3.66` | `20.8` | Demote |
| `gap scanner` on `AAPL/MSFT` | `19` | `-1.303` | `1.78` | `9.1` | Drop |

The best `gap` row was `candidate_184`, and it traded both names:

- `NVDA 29`, `TSLA 22`

So the right interpretation is not “gap finally works everywhere.” The right interpretation is “gap is a high-beta specialist branch.”

## Not Useful

- Direct `gap` on `AAPL`, `AMZN`, `META`, and `TSLA` was a poor use of budget.
- Direct `BSL` on `META` stayed weak.
- `pilot_core BSL scanner` was clearly dominated by `core4` and `high_beta`.
- Broad `gap` grids without high-beta names diluted the signal and produced negative averages.

## Invalid Or Misleading

- The standard score formula still undervalues intraday rows with strong return/drawdown but modest Sharpe. The new `Intraday Quality Table` is a better primary ranking view for minute rounds.
- Basket scanners now need basket passive baselines. Comparing `NVDA/TSLA` scanner rows only to single-name passive references is informative but incomplete.

## Process Notes

- `201/201` finished cleanly after one Docker race retry.
- `0` invalid orders were found across `201` order-event files.
- `jobs 6` remained stable enough for this machine and workload.

## Next

### Primary Track: `BSL high-beta`

- Keep `NVDA/TSLA`
- Keep `3m confirm`
- Keep `240m hold`
- Refine target/stop logic instead of reopening a broad grid

### Secondary Track: `BSL core4`

- Keep `AAPL/MSFT/AMZN/META`
- Prioritize `QQQ/XLK` and `QQQ/SMH`
- Recognize `AMZN/META` as the main selection engine

### Exploratory Track: `gap high-beta`

- Keep only `NVDA/TSLA`
- Keep `QQQ/XLK` as the primary context
- Work around `2-3m` confirmation and `90-180m` holds

### Workflow Upgrades

- Add basket passive baselines such as `NVDA/TSLA equal-weight buy-and-hold`
- Add a `Selection Distribution` section for top scanner rows by default
- Extend intraday history earlier than `2025-01-02` before spending another large batch on micro-tuning
