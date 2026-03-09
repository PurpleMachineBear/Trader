# Iteration `iter_015` Analysis

## Decision

Freeze the intraday paper shortlist around `BSL`, not `gap`.

Promote:

- `QQQ/VOO/GLD dual_momentum 126/7` as the daily paper control
- `Dynamic high-beta BSL pool 1` with `QQQ/SMH` context as the main intraday paper candidate
- `Fixed NVDA/TSLA aggressive BSL` as the secondary intraday control
- `Fixed NVDA/TSLA clean BSL` and `fixed core clean BSL` as lower-drawdown sleeve candidates

Demote:

- `Dynamic high-beta gap`
- `Fixed high-beta gap`

## Sample Coverage

- Candidates: `22/22 completed`
- Sample: `2024-01-02` to `2026-03-06` (`2026 YTD`)
- Benchmark: `VOO buy-and-hold slip 1bps`
- Daily control: `QQQ/VOO/GLD dual_momentum 126/7 slip 1bps`
- Intraday controls: fixed `NVDA/TSLA` aggressive and clean BSL, plus fixed core clean BSL
- Execution realism: explicit `1bps` and `2bps` slippage stress
- Order validation: no invalid orders in the final round state
- Total official experiment count to date: `1478`

## Winner Table

| Branch | Candidate | Structure | Return % | Drawdown % | Trades | Comment |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `Daily control` | `candidate_02` | `QQQ/VOO/GLD dual_momentum 126/7 slip 1bps` | `92.392` | `13.9` | `11` | Still the strongest overall paper-grade control |
| `Dynamic BSL winner` | `candidate_09` | `high-beta dynamic BSL pool 1, QQQ/SMH, 1bps` | `24.695` | `7.3` | `66` | Best dynamic intraday row over the longer sample |
| `Dynamic BSL slippage stress` | `candidate_12` | `high-beta dynamic BSL pool 1, QQQ/SMH, 2bps` | `23.066` | `7.5` | `66` | Survived slippage with only modest degradation |
| `Fixed aggressive control` | `candidate_06` | `fixed NVDA/TSLA aggressive BSL, 1bps` | `20.995` | `5.8` | `35` | Stronger than the old fixed clean branch |
| `Fixed clean control` | `candidate_05` | `fixed NVDA/TSLA clean BSL, 1bps` | `13.949` | `4.5` | `39` | Lower return but still viable as a cleaner sleeve |
| `Core clean control` | `candidate_08` | `fixed core BSL clean, 1bps` | `8.049` | `2.6` | `30` | Lower return, lower drawdown sleeve candidate |
| `Benchmark` | `candidate_01` | `VOO buy-and-hold, 1bps` | `42.608` | `18.8` | `0` | Passive benchmark |

## What Changed Versus `iter_014`

The key change was not a new family. It was a harder test:

- the minute sample was extended back to `2024-01-02`
- intraday candidates were forced through explicit `1bps` and `2bps` slippage
- the high-beta dynamic branch was compared against the same-basket passive baseline over the longer sample

That harder test materially changed one conclusion:

- `Dynamic high-beta BSL` survived
- `Dynamic high-beta gap` did not

## Useful

- `Dynamic high-beta BSL pool 1` survived the longer sample and remained the best intraday paper branch.
- `Pool 1` was clearly better than `pool 3` and `pool 5` once the sample was extended. The best dynamic result was no longer the broader watchlist pool; it was the tighter top-ranked daily selection.
- `1bps` versus `2bps` slippage did not break the dynamic high-beta BSL branch. The raw-return drop from `candidate_09` to `candidate_12` was modest.
- `Fixed NVDA/TSLA aggressive BSL` remained strong enough to keep as a secondary paper control.
- `Fixed clean` and `core clean` BSL kept their role as lower-drawdown sleeves, even if they were not return leaders.

## Not Useful

- `Dynamic high-beta gap` degraded badly over the longer sample. The best `gap` row returned only `4.065%` with `23.9%` drawdown, and several rows were negative.
- `Fixed high-beta gap` no longer looked attractive as a paper candidate. It was still positive, but clearly inferior to the BSL branches.
- `Pool 3` and `pool 5` dynamic BSL variants were not worth promoting. More names in the live watchlist diluted quality.
- The extended sample made it much harder to justify keeping `gap` on equal footing with `BSL`.

## Invalid Or Risky

- The first execution pass exposed a process bug: scanner slippage injection caused an indentation failure in generated `main.py` for some rows.
- That issue was fixed in the template renderer and the failed candidates were rerun cleanly with `--only-failed`.
- The final round state is valid, but this still matters operationally: deployment-readiness rounds need to be treated as process tests as much as strategy tests.

## Recommendation For Next Round

Do not keep searching across `gap` and `BSL` equally. The next round should narrow to:

1. `QQQ/VOO/GLD dual_momentum 126/7` as the daily paper control
2. `Dynamic high-beta BSL pool 1, QQQ/SMH` as the main intraday paper candidate
3. `Fixed NVDA/TSLA aggressive BSL` as secondary confirmation
4. `Fixed clean` and `core clean` BSL only if the goal is a lower-drawdown sleeve

Then test one thing that is more important than another parameter tweak:

- capital model and sizing realism

The main conclusion from `iter_015` is simple:

- `BSL` survived paper-style stress
- `gap` did not
- the paper set should now shrink, not grow
