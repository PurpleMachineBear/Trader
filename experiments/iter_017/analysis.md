# Iteration `iter_017` Analysis

## Decision

Freeze the paper-trading shortlist around three roles:

- `Primary daily engine`: `QQQ/VOO/GLD dual_momentum 126/7`
- `Primary intraday engine`: `fixed NVDA/TSLA aggressive BSL`
- `Secondary aggressive intraday engine`: `dynamic high-beta BSL pool 1`

Keep one optional conservative version:

- `fixed NVDA/TSLA aggressive BSL risk 1.00%`

Do not promote:

- `core clean BSL`
- `core clean BSL risk 1.00%`
- any `gap` branch

## Sample Coverage

- Candidates: `27/27 completed`
- Windows:
  - `2024-01-02` to `2024-12-31`
  - `2025-01-02` to `2025-12-31`
  - `2026-01-02` to `2026-03-06`
- Benchmark: `VOO buy-and-hold slip 1bps`
- Frozen candidates under test:
  - daily control
  - high-beta passive basket
  - core passive basket
  - dynamic high-beta BSL pool 1
  - fixed aggressive BSL
  - fixed core clean BSL
  - conservative `risk 1.00%` sleeves
- Process validation: `2` initial Docker race failures, both recovered cleanly via `--only-failed`
- Total official experiment count to date: `1529`

## Stability Summary

| Structure | 2024 Return / DD | 2025 Return / DD | 2026 YTD Return / DD | Stability Judgment |
| --- | --- | --- | --- | --- |
| `QQQ/VOO/GLD dual_momentum 126/7` | `2.639 / 9.2` | `55.407 / 7.1` | `16.769 / 14.1` | Strong full-sample leader, but not all-weather |
| `Dynamic high-beta BSL pool 1` | `1.676 / 7.7` | `15.072 / 6.6` | `3.683 / 3.3` | Positive in all windows, but unstable and 2024-weak |
| `Fixed NVDA/TSLA aggressive BSL` | `5.056 / 4.2` | `7.982 / 5.5` | `3.443 / 1.2` | Best intraday stability profile |
| `Fixed core clean BSL` | `-1.931 / 2.7` | `7.304 / 1.5` | `-1.079 / 1.7` | Not stable enough |
| `Fixed aggressive BSL risk 1.00%` | `0.655 / 1.6` | `2.815 / 0.8` | `1.740 / 0.6` | Valid conservative sleeve |
| `Core clean BSL risk 1.00%` | `-0.263 / 0.6` | `4.275 / 0.9` | `-0.458 / 0.7` | Too weak even as conservative sleeve |

## What Was Useful

- `Fixed NVDA/TSLA aggressive BSL` was the most stable intraday branch. It stayed positive in all three windows with moderate drawdown and manageable trade count.
- `Dynamic high-beta BSL pool 1` also stayed positive in all three windows. It kept the higher-upside profile, especially in `2025`, so it still belongs in the paper set.
- `Fixed aggressive BSL risk 1.00%` is the first conservative sleeve that stayed positive in all three windows while keeping drawdown near `1%`.
- The round successfully separated `paper-worthy intraday branches` from `interesting but not stable enough branches`.

## What Was Not Useful

- `Fixed core clean BSL` failed the stability test. It only worked in `2025` and was negative in both `2024` and `2026 YTD`.
- `Core clean BSL risk 1.00%` also failed the stability test. Lower drawdown did not rescue the branch.
- Neither passive basket baseline justified replacing the daily control or the main intraday shortlist, but they did show something important:
  - the intraday high-beta branches were not dominant in `2024`
  - they became much more useful in `2025` and `2026 YTD`

## Important Interpretation

This round materially changed the intraday hierarchy.

Before `iter_017`, it was still plausible to keep `core clean BSL` in the main paper set because the full-sample drawdown was attractive.

After `iter_017`, that is no longer the right decision. The branch is too dependent on the `2025` window.

The high-beta branch split is now clearer:

- `Fixed aggressive BSL` is the more stable paper engine
- `Dynamic high-beta BSL pool 1` is the higher-upside but more regime-sensitive paper engine

That is a cleaner deployment structure than trying to keep too many branches alive.

## Invalid Or Misleading

- Short `YTD` windows can inflate Sharpe and the default composite score. `candidate_24` looks extraordinary on score because the `2026 YTD` sample is short and the drawdown is tiny.
- For this round, stability should be judged by:
  - positive or negative window count
  - return / drawdown by window
  - whether the branch survives multiple regimes
- not by the best single-window score alone

## Recommendation

The paper-trading freeze set should now be:

1. `QQQ/VOO/GLD dual_momentum 126/7`
2. `NVDA/TSLA fixed aggressive BSL`
3. `NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO dynamic high-beta BSL pool 1`
4. optional `NVDA/TSLA fixed aggressive BSL risk 1.00%` as the conservative version
5. `VOO buy-and-hold` kept as a passive benchmark

Do not start paper with `core clean BSL` or any `gap` branch.

If we start paper next, the correct operational framing is:

- one daily control
- one fixed intraday engine
- one dynamic intraday engine in shadow or smaller paper allocation

That is enough evidence to stop broad research and move into paper deployment preparation.
