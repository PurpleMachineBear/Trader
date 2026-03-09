# Iteration `iter_013` Analysis

## What Changed

This round was a focused exploit pass, not a broad search. It added one new tool and used it immediately:

- new family: `equal_weight_buy_and_hold`

That let the round compare scanner branches against their natural passive baskets instead of only against single-name buy-and-hold rows.

## Intraday Quality Table

| Structure | Return % | Drawdown % | Return/Drawdown | Trades | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `AAPL/MSFT/AMZN/META BSL + QQQ/XLK + 5m + 150m` | `10.899` | `1.6` | `6.812` | `22` | Best core large-cap clean row |
| `NVDA/TSLA BSL + QQQ/XLK/SMH + 3m + 300m` | `13.215` | `2.0` | `6.607` | `21` | Best high-beta clean row |
| `AAPL/MSFT/AMZN/META BSL + QQQ/SMH + 5m + 150m` | `10.918` | `1.7` | `6.422` | `22` | Same core branch held up under a second context |
| `AMZN/META/MSFT BSL + QQQ/XLK + 5m + 150m` | `10.112` | `1.6` | `6.320` | `21` | Narrowed core basket was good, but not clearly better than `core4` |
| `NVDA/TSLA BSL + SPY/QQQ/IWM + 3m + 240m` | `12.098` | `2.0` | `6.049` | `21` | Stable high-beta carryover branch |
| `NVDA/TSLA BSL + QQQ/SMH + 3m + 300m` | `13.171` | `2.2` | `5.987` | `20` | Strong hybrid of return and control |
| `NVDA/TSLA BSL + QQQ/SMH + 3m + 240m` | `11.832` | `2.0` | `5.916` | `20` | Clean branch, reproducible from `iter_012` |
| `NVDA/TSLA BSL + QQQ/XLK/SMH + 3m + 240m` | `11.804` | `2.0` | `5.902` | `21` | Hybrid context worked, not just the old contexts |
| `NVDA/TSLA gap + QQQ/XLK + 2m + 90m` | `10.418` | `5.5` | `1.894` | `51` | Best gap row, but clearly lower quality than BSL |

## Useful

### 1. Basket passive baselines confirmed real alpha

The strongest scanner branches decisively beat their natural passive baskets:

| Structure | Return % | Drawdown % | Passive Basket | Basket Return % | Basket Drawdown % |
| --- | ---: | ---: | --- | ---: | ---: |
| `NVDA/TSLA BSL + QQQ/SMH + 3m + 240m + no vwap exit` | `16.787` | `4.8` | `NVDA/TSLA equal-weight` | `1.997` | `25.5` |
| `NVDA/TSLA BSL + QQQ/XLK/SMH + 3m + 300m + vwap exit` | `13.215` | `2.0` | `NVDA/TSLA equal-weight` | `1.997` | `25.5` |
| `AAPL/MSFT/AMZN/META BSL + QQQ/XLK + 5m + 150m` | `10.899` | `1.6` | `AAPL/MSFT/AMZN/META equal-weight` | `1.643` | `9.8` |
| `AMZN/META/MSFT BSL + QQQ/XLK + 5m + 150m` | `10.112` | `1.6` | `AMZN/META/MSFT equal-weight` | `-0.958` | `11.4` |

This is the most important new evidence in the round. The scanner branches are now beating the right passive comparator, not just a conveniently weak single-name baseline.

### 2. `High-beta BSL` improved again

The high-beta branch now has two valid deployment styles:

- `Aggressive`
  - `candidate_038`
  - `QQQ/SMH`, `3m`, `240m`, `risk_reward 2.0`, `vwap_exit False`
  - `16.787%` return, `4.8%` drawdown, `20` trades
- `Clean`
  - `candidate_045`
  - `QQQ/XLK/SMH`, `3m`, `300m`, `risk_reward 2.5`, `vwap_exit True`
  - `13.215%` return, `2.0%` drawdown, `21` trades

That is a real engineering decision now, not a vague research idea.

### 3. `Core BSL` improved without needing an extreme basket reduction

The best core rows were:

- `candidate_047`: `10.899%`, `1.6%` drawdown, `22` trades
- `candidate_051`: `10.918%`, `1.7%` drawdown, `22` trades
- `candidate_059`: `10.112%`, `1.6%` drawdown, `21` trades
- `candidate_063`: `10.135%`, `1.7%` drawdown, `21` trades

Selection distribution showed the same theme as `iter_012`:

- `candidate_047`: `AMZN 10`, `META 7`, `MSFT 3`, `AAPL 2`
- `candidate_059`: `AMZN 10`, `META 8`, `MSFT 3`

The branch is still powered by `AMZN/META`, but `core4` remained competitive enough that cutting down to `AMZN/META` alone was not worth it.

### 4. `Gap high-beta` reproduced but did not displace `BSL`

Focused gap results were stable:

- `candidate_082`: `10.418%`, `5.5%` drawdown, `51` trades
- `candidate_083`: `9.936%`, `4.0%` drawdown, `37` trades
- `candidate_084`: `9.381%`, `3.9%` drawdown, `37` trades

The branch remained useful, but still lower quality than the best BSL rows. That is why it stays secondary.

## Not Useful

- `AMZN/META` alone did not beat `core4` or `AMZN/META/MSFT`. The basket became too narrow.
- `All6` confirmation rows were positive, but still inferior to the dedicated `high-beta` or `core4` branches.
- Turning off `vwap_exit` on the core branch added drawdown without the same payoff that it delivered in `high-beta`.

## Invalid Or Misleading

- `4` candidates failed during the main pass, but all were Docker/container race noise and all completed on low-concurrency retry.
- The standard score still mixes daily and intraday tracks poorly. The new `Intraday Quality Table` remains the better primary ranking tool for minute branches.

## Process Notes

- Final status: `121/121 completed`
- Order-event files inspected: `121`
- Invalid orders: `0`

## Next

### Promote these branches

- `High-beta BSL aggressive`
  - `NVDA/TSLA`
  - `QQQ/SMH`
  - `3m`
  - `240m`
  - `vwap_exit False`
- `High-beta BSL clean`
  - `NVDA/TSLA`
  - `QQQ/XLK/SMH`
  - `3m`
  - `300m`
  - `vwap_exit True`
- `Core BSL clean`
  - `AAPL/MSFT/AMZN/META`
  - `QQQ/XLK` or `QQQ/SMH`
  - `5m`
  - `150m`
  - `vwap_exit True`

### Keep only as secondary

- `High-beta gap`
  - still valid
  - still useful
  - but clearly second-tier behind `BSL`

### Most professional next step

Do not run another parameter spray immediately. The next meaningful upgrade is to research a two-sleeve or three-sleeve portfolio:

- one validated daily control
- one clean intraday BSL sleeve
- optional aggressive intraday BSL sleeve

That would move the repo from “best standalone strategies” toward “actual deployable portfolio construction.”
