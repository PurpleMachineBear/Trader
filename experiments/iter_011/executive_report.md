# Iteration `iter_011` Executive Report

## Decision

Continue the campaign, but do not scale the new intraday families broadly yet. Only the `MSFT` branch of the BSL-inspired reversal setup showed enough signal to justify the next round.

## Sample Coverage

- Candidates: `81/81 completed`
- Sample: `2025-06-02` to `2026-03-06` (`2026 YTD`)
- Universe: `SPY`, `QQQ`, `TQQQ`, `AAPL`, `MSFT`, `XLK`
- Benchmark: `VOO buy-and-hold`
- Data fidelity: first official minute-data round

## What Changed

- The repository now supports local LEAN minute data from Polygon.
- Three new long intraday strategy families were added:
  - `gap_reversal_intraday`
  - `day2_breakout_intraday`
  - `bsl_reversal_intraday`
- The workflow and report format were upgraded to include `Activation Table` reporting because intraday pilots need to show which candidates actually traded.

## Winners

Overall round winners were still passive or previously validated daily controls:

| Structure | Score | Return % | Sharpe | Drawdown % |
| --- | ---: | ---: | ---: | ---: |
| `AAPL buy-and-hold` | `116.516` | `27.716` | `1.162` | `13.7` |
| `VOO buy-and-hold` | `82.723` | `13.523` | `0.792` | `5.0` |
| `QQQ/VOO/GLD 126/7` | `80.704` | `21.304` | `0.872` | `13.9` |

Best new intraday branch:

| Structure | Candidate | Return % | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: |
| `MSFT bsl_reversal_intraday` | `candidate_077` | `5.400` | `0.6` | `8` |
| `MSFT bsl_reversal_intraday` | `candidate_074` | `3.813` | `1.1` | `8` |
| `MSFT bsl_reversal_intraday` | `candidate_075` | `3.463` | `0.9` | `6` |

## Activation Table

| Family | Activation Rate | Avg Return % (Active) | Verdict |
| --- | ---: | ---: | --- |
| `bsl_reversal_intraday` | `75.0%` | `0.247` | Keep |
| `gap_reversal_intraday` | `75.0%` | `-0.930` | Demote to secondary branch |
| `day2_breakout_intraday` | `50.0%` | `-0.309` | Drop from priority queue |

## Main Findings

- `1-minute` data was necessary to test these setups with any fidelity. Daily data would not have been enough.
- Translating the discretionary setup ideas into systematic rules was feasible.
- The best new result came from `MSFT`, not from the broad ETFs.
- `AAPL` gap reversal produced some positive rows, but still badly lagged passive `AAPL`.
- `TQQQ` was not a good target for these new long intraday motifs.

## Main Risks

- This was still a short sample.
- The current score function is not a reliable primary ranking tool for low-trade intraday pilots.
- Most new intraday candidates did not beat their own passive baseline over this window.

## Recommendation

- Keep daily validated controls unchanged.
- Continue intraday research only on:
  - `MSFT bsl_reversal_intraday`
  - `AAPL gap_reversal_intraday`
- In the next intraday round, improve structure rather than spray more thresholds:
  - add `5-minute` confirmation
  - add better exit logic
  - narrow the symbol set
