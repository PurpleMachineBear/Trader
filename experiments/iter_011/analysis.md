# Iteration `iter_011` Analysis

## Scope

- Raw candidates: `81`
- Status: `81/81 completed` after retry
- Sample: `2025-06-02` to `2026-03-06` (`2026 YTD`, latest completed trading day before `2026-03-07`)
- Theme: first systematic intraday pilot for abstracted long setups inspired by `BSL`, `gap reversal`, and `day-2 breakout`
- Benchmark: `VOO buy-and-hold`
- Controls carried forward: `QQQ/VOO/GLD 126/7`, `TQQQ/VOO/GLD 126/7 0.75x`
- Process check: `57` order-event files inspected, `0` invalid orders

## Executive Read

This round did not produce an intraday family that beat the best daily controls or the strongest passive references on the whole sample. That is the blunt truth.

But it did produce one useful research result:

- `bsl_reversal_intraday` on `MSFT` is the only new family branch that clearly deserves continued work.

Everything else is weaker:

- `gap_reversal_intraday` is only marginally interesting on `AAPL`
- `day2_breakout_intraday` is not a priority right now
- `TQQQ` was a poor intraday long target in this translation

## Activation Table

| Family | Count | Active Count | Activation Rate | Avg Return % (Active) | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `bsl_reversal_intraday` | `24` | `18` | `75.0%` | `0.247` | Best new family; still weak overall, but not dead |
| `gap_reversal_intraday` | `24` | `18` | `75.0%` | `-0.930` | Triggered often enough, but average active performance was negative |
| `day2_breakout_intraday` | `24` | `12` | `50.0%` | `-0.309` | Too sparse and too weak in this pilot |

Interpretation:

- Intraday pilot rounds cannot be read from `score` alone.
- Activation rate matters because some strict rows simply never traded.
- The new report format now includes activation for exactly this reason.

## Best Intraday Rows

| Family | Candidate | Symbol | Return % | Sharpe | Drawdown % | Trades | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `bsl_reversal_intraday` | `candidate_077` | `MSFT` | `5.400` | `-0.204` | `0.6` | `8` | Best new strategy result of the round |
| `bsl_reversal_intraday` | `candidate_074` | `MSFT` | `3.813` | `-0.685` | `1.1` | `8` | Same symbol cluster confirms the branch is real enough to continue |
| `bsl_reversal_intraday` | `candidate_075` | `MSFT` | `3.463` | `-0.819` | `0.9` | `6` | The `MSFT` BSL cluster is the main keeper |
| `gap_reversal_intraday` | `candidate_023` | `AAPL` | `1.967` | `-2.157` | `0.5` | `3` | Positive but too low-frequency to trust yet |
| `gap_reversal_intraday` | `candidate_025` | `AAPL` | `1.393` | `-1.900` | `0.8` | `9` | Better evidence quality than `candidate_023`, still not a strong edge |
| `day2_breakout_intraday` | `candidate_049` | `AAPL` | `0.423` | `-2.072` | `2.0` | `13` | Best day-2 row, but not strong enough |

## Same-Symbol Passive Baseline Table

| Active Structure | Passive Baseline | Score Delta | Excess Return % | Drawdown Delta % | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| `MSFT bsl_reversal_intraday 8d / 60m entry` (`candidate_077`) | `MSFT buy-and-hold` (`candidate_006`) | `127.791` | `16.691` | `-28.3` | Strongest same-symbol win of the round |
| `MSFT bsl_reversal_intraday 10d / 90m entry` (`candidate_074`) | `MSFT buy-and-hold` (`candidate_006`) | `77.104` | `15.104` | `-27.8` | Confirms the `MSFT` BSL theme |
| `AAPL gap_reversal_intraday` (`candidate_023`) | `AAPL buy-and-hold` (`candidate_005`) | `-331.249` | `-25.749` | `-13.2` | Positive on its own, but badly lagged passive AAPL in this sample |
| `AAPL day2_breakout_intraday` (`candidate_049`) | `AAPL buy-and-hold` (`candidate_005`) | `-327.293` | `-27.293` | `-11.7` | Not competitive |
| `XLK bsl_reversal_intraday` (`candidate_081`) | `XLK buy-and-hold` (`candidate_007`) | `-424.964` | `-16.864` | `-10.3` | Not good enough |

Interpretation:

- `MSFT` is the only symbol where the new intraday branch clearly beat its own passive baseline.
- `AAPL` had tradable behavior, but passive `AAPL` was still much stronger over this sample.

## Useful

- Minute data support is now real, not hypothetical. The project can now research intraday families locally with Polygon-backed LEAN minute data.
- `bsl_reversal_intraday` is the only new family worth continuing immediately.
- The best branch was:
  - `MSFT`
  - shorter downtrend lookbacks (`8-15` days)
  - lenient gap filters (`gap_min -0.02 to -0.005`)
  - early entry windows (`60-90` minutes)
- `gap_reversal_intraday` on `AAPL` is worth a secondary follow-up, but only as a second-tier branch.
- Carryover daily controls did their job:
  - `QQQ/VOO/GLD 126/7` still outperformed the new intraday families on the whole sample
  - the old framework remains the quality bar

## Not Useful

- `day2_breakout_intraday` is not a priority family after this pilot.
- `TQQQ` was a poor target for these translated long intraday motifs.
- Broad ETFs like `SPY` rarely produced interesting results under the current filters. The family logic seems more at home on single-name tech.
- Strict gap and premarket filters often produced zero-trade rows without compensating quality.

## Invalid Or Process Issues

- There was no strategy-level execution bug after the initial smoke round.
- First pass had `4` process-level failures; all were fixed by `--only-failed --jobs 2`.
- `0` invalid orders were found in all available order-event files.
- The existing composite score is too unstable for low-trade intraday pilots because Sharpe can turn sharply negative even when raw return is positive and drawdown is tiny.

## Experiment Design Problems

- This pilot used `1-minute` entry logic. That gave fidelity, but also high noise.
- The current sample `2025-06-02` to `2026-03-06` is too short and too trend-sensitive to judge intraday alpha cleanly against strong passive symbols like `AAPL`.
- The current parameter grid was still too broad for a first real minute round. Too many rows were either zero-trade or obviously dominated.
- Mixing daily controls and intraday candidates in one score ranking is useful for orientation, but not for final judgment. Intraday families need their own pilot criteria.

## What To Change Next

- Keep `bsl_reversal_intraday`, but narrow the symbol set to:
  - `MSFT`
  - `AAPL`
  - `QQQ`
  - optional `XLK`
- Demote or temporarily drop:
  - `day2_breakout_intraday`
  - `TQQQ` intraday long translations
  - `SPY` intraday long translations
- Add a structural improvement, not just more threshold sweeps:
  - `5-minute` confirmation instead of pure `1-minute` trigger noise
  - midday cutoff / no-lunch entry filter
  - alternate exit logic beyond immediate VWAP loss
- Keep same-symbol passive baselines in every future intraday round.

## Next Round

- Continue the overall campaign, but split the research budget:
  - daily validated controls remain one track
  - intraday minute research becomes a separate track
- The next intraday round should be an exploit round around:
  - `MSFT bsl_reversal_intraday`
  - `AAPL gap_reversal_intraday`
- The next intraday round should be smaller and sharper than this pilot. The correct move is not another wide `81`-candidate spray.
