# Iteration `iter_016` Analysis

## Decision

Do not replace the current paper shortlist with risk-sized versions.

Keep:

- `No-risk-sizing dynamic high-beta BSL pool 1`
- `No-risk-sizing fixed NVDA/TSLA aggressive BSL`
- `No-risk-sizing fixed clean/core clean BSL` as the main paper track

Demote risk-sized variants to:

- `conservative sleeve candidates`
- not `primary paper candidates`

## Sample Coverage

- Candidates: `24/24 completed`
- Sample: `2024-01-02` to `2026-03-06` (`2026 YTD`)
- Benchmark: `VOO buy-and-hold slip 1bps`
- Daily control: `QQQ/VOO/GLD dual_momentum 126/7 slip 1bps`
- Intraday controls: frozen no-risk-sizing paper shortlist from `iter_015`
- Sizing variable tested: `risk_per_trade_pct = 0.50% / 0.75% / 1.00%`
- Slippage stress: `1bps` on the whole round, plus selected `2bps` conservative rows
- Total official experiment count to date: `1502`

## Winner Table

| Branch | Candidate | Structure | Return % | Drawdown % | Trades | Comment |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `Daily control` | `candidate_02` | `QQQ/VOO/GLD dual_momentum 126/7 slip 1bps` | `92.392` | `13.9` | `11` | Still the main daily paper engine |
| `Dynamic intraday control` | `candidate_05` | `dynamic high-beta BSL pool 1, no risk sizing` | `24.695` | `7.3` | `66` | Best intraday return row remains the no-risk control |
| `Fixed aggressive control` | `candidate_06` | `fixed NVDA/TSLA aggressive BSL, no risk sizing` | `20.995` | `5.8` | `35` | Best fixed intraday control |
| `Fixed clean control` | `candidate_07` | `fixed NVDA/TSLA clean BSL, no risk sizing` | `13.949` | `4.5` | `39` | Cleaner but lower-return sleeve |
| `Core clean control` | `candidate_08` | `fixed core BSL clean, no risk sizing` | `8.049` | `2.6` | `30` | Lowest-drawdown no-risk control |
| `Best risk-sized dynamic row` | `candidate_11` | `dynamic high-beta BSL, risk 1.00%` | `6.466` | `3.4` | `66` | Drawdown improved, return collapsed |
| `Best risk-sized fixed row` | `candidate_16` | `fixed aggressive BSL, risk 1.00%` | `7.295` | `1.6` | `35` | Good drawdown control, weak raw return |

## What The Round Actually Showed

This was not a family test. It was a capital-model test.

The main question was:

- can stop-based `risk_per_trade_pct` make the intraday paper candidates more deployable without breaking their economics?

The answer was:

- it materially reduces drawdown
- it also materially reduces raw return
- under the current objective, the no-risk-sizing controls still win

## Useful

- `risk_per_trade_pct` clearly works as a drawdown suppressor.
- `1.00%` risk sizing was the least bad conservative setting across the tested range. It was better than `0.75%`, which was better than `0.50%`.
- `Fixed core clean BSL` became a very low-drawdown conservative sleeve under risk sizing, reaching only `0.7%` drawdown at `1.00%` risk.
- `Fixed aggressive BSL` also became a viable conservative sleeve at `1.00%` risk with only `1.6%` drawdown.

## Not Useful

- None of the risk-sized versions beat their corresponding no-risk-sizing controls on return.
- `0.50%` risk sizing de-risked far too aggressively. It removed too much of the sleeve economics.
- `0.75%` risk sizing still gave up too much return to become the default paper model.
- The new sizing logic did not produce a better primary paper candidate than the current no-risk controls.

## Invalid Or Misleading

- The standard score formula becomes even less useful once risk sizing compresses both drawdown and return. Several risk-sized rows are operationally interesting even though the score is heavily negative.
- This round should therefore be interpreted by deployment role:
  - `primary paper candidate`
  - `conservative sleeve candidate`
  - not by one combined ranking alone

## Recommendation For Next Round

Do not continue sweeping sizing numbers. The next meaningful step is stability validation across windows for the frozen shortlist.

Use two paper tracks:

1. `Primary paper track`
   - no-risk-sizing dynamic high-beta BSL pool 1
   - no-risk-sizing fixed aggressive BSL
   - daily `QQQ/VOO/GLD dual_momentum`
2. `Conservative sleeve track`
   - `fixed core clean BSL risk 1.00%`
   - optionally `fixed aggressive BSL risk 1.00%`

The main conclusion from `iter_016` is:

- risk sizing is useful
- but not for choosing the main paper winner
- it is useful for defining a separate conservative sleeve
