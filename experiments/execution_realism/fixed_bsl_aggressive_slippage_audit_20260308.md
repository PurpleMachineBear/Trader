# Fixed BSL Aggressive Slippage Audit

## Scope

- Candidate: `iter_018 / candidate_05`
- Structure: `NVDA/TSLA fixed aggressive BSL`
- Sample: `2025-01-02` to `2026-03-06`
- Baseline backtest slippage: `1 bp`

Source artifacts:

- `/Users/chenchien/lean/experiments/iter_018/candidate_05/spec.json`
- `/Users/chenchien/lean/experiments/iter_018/candidate_05/backtest/1221427987-order-events.json`
- `/Users/chenchien/lean/experiments/iter_018/candidate_05/backtest/1221427987-summary.json`

## Baseline

- End equity: `$116,302.69`
- Net profit: `16.303%`
- Max drawdown: `4.8%`
- Total filled orders: `40`
- Trade count: `20`
- Turnover notional: `$4,269,300.00`
- Average order notional: `$106,732.50`
- Average round-trip notional: `$213,465.00`
- Filled-order fees: `$87.75`

Turnover mix:

- `TSLA`: `$3,002,177.80` (`70.3%`)
- `NVDA`: `$1,267,122.20` (`29.7%`)

## Fill Quality Notes

- All `40` filled orders include the LEAN warning `No quote information available ... order filled using TradeBar data`.
- This means the backtest is already using a simplified fill model on minute bars, not quote-driven bid/ask execution.
- The sensitivity table below is therefore a first-order stress test, not a broker-accurate execution replay.

## Sensitivity Table

Assumption:

- Baseline already includes `1 bp` slippage.
- Additional cost at a higher slippage level is estimated as:
  - `(target_bps - 1) * turnover_notional / 10,000`

| Total Slippage | Extra Cost vs Baseline | Adjusted End Equity | Adjusted Net Profit |
| --- | ---: | ---: | ---: |
| `1 bp` | `$0.00` | `$116,302.69` | `16.303%` |
| `2 bp` | `$426.93` | `$115,875.76` | `15.876%` |
| `5 bp` | `$1,707.72` | `$114,594.97` | `14.595%` |
| `10 bp` | `$3,842.37` | `$112,460.32` | `12.460%` |

## Interpretation

- The strategy is not hypersensitive to small slippage changes. It remains solidly positive at `2 bp` and `5 bp`.
- The estimated break-even slippage is about `39.19 bp` total, which is far above the current `1 bp` research assumption.
- Against the same-sample `VOO buy-and-hold` baseline from `iter_018 candidate_01`:
  - `VOO` return: `14.463%`
  - fixed BSL at `5 bp` still slightly leads on raw return: `14.595%`
  - fixed BSL at `10 bp` falls behind on raw return: `12.460%`
- Even in the harsher `10 bp` stress, the strategy still carries a much lower validated drawdown profile than `VOO` (`4.8%` vs `19.0%` baseline backtest drawdown).

## Decision Use

- This result supports keeping `NVDA/TSLA fixed aggressive BSL` in the paper shortlist.
- It does **not** yet justify promoting it as a high-frequency live sleeve without further work on:
  - paper/live fill drift logging
  - quote-aware execution checks
  - latency and partial-fill monitoring
