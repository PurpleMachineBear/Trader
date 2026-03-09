# Iteration `iter_017` Executive Report

## Decision

Freeze the paper shortlist.

Approved for paper-track use:

- `QQQ/VOO/GLD dual_momentum 126/7`
- `NVDA/TSLA fixed aggressive BSL`
- `NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO dynamic high-beta BSL pool 1`
- optional `NVDA/TSLA fixed aggressive BSL risk 1.00%` as the conservative version

Do not approve:

- `core clean BSL`
- `core clean BSL risk 1.00%`
- `gap`

## What Changed

This round stopped optimizing and instead validated the frozen shortlist across separate `2024`, `2025`, and `2026 YTD` windows.

That was the right move. It showed that the shortlist should get smaller:

- `fixed aggressive BSL` is the stable intraday branch
- `dynamic high-beta BSL` is still good, but more regime-sensitive
- `core clean BSL` is not stable enough for the paper set

## Key Findings

| Branch | 2024 | 2025 | 2026 YTD | Conclusion |
| --- | ---: | ---: | ---: | --- |
| `QQQ/VOO/GLD dual_momentum 126/7` | `2.639%` | `55.407%` | `16.769%` | Strong daily engine, but not all-weather |
| `Fixed NVDA/TSLA aggressive BSL` | `5.056%` | `7.982%` | `3.443%` | Best intraday stability |
| `Dynamic high-beta BSL pool 1` | `1.676%` | `15.072%` | `3.683%` | Higher upside, less stable |
| `Fixed aggressive BSL risk 1.00%` | `0.655%` | `2.815%` | `1.740%` | Good conservative sleeve |
| `Fixed core clean BSL` | `-1.931%` | `7.304%` | `-1.079%` | Reject for paper |
| `Core clean BSL risk 1.00%` | `-0.263%` | `4.275%` | `-0.458%` | Reject for paper |

## What Was Useful

- `Fixed aggressive BSL` survived all three windows.
- `Dynamic high-beta BSL` also survived all three windows and still offers the higher-upside intraday branch.
- `Fixed aggressive BSL risk 1.00%` is the only conservative sleeve that stayed positive across all tested windows.

## What Was Not Useful

- `Core clean BSL` did not survive the stability test.
- `Core clean BSL risk 1.00%` also failed the stability test.
- The paper set should not keep extra branches alive just because one full-sample row looked clean.

## Recommendation

The first paper deployment set should be small:

1. `QQQ/VOO/GLD dual_momentum 126/7`
2. `NVDA/TSLA fixed aggressive BSL`
3. `VOO buy-and-hold` as passive benchmark

Optional:

- run `dynamic high-beta BSL pool 1` in shadow or with smaller paper emphasis
- run `fixed aggressive BSL risk 1.00%` only if you want a conservative comparison sleeve

The research is now good enough to stop broad strategy search and move into paper-trading preparation.
