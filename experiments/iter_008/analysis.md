# Iteration `iter_008` Analysis

## Scope

- Candidates: `201`
- Status: `201/201 completed`
- Sample: `2022-01-01` to `2026-03-06`
- Focus: explicit `position_size` testing for leveraged and unleveraged GLD-defensive strategies
- Benchmark: `VOO buy-and-hold`

## Summary Table

| Candidate | Description | Score | Return % | Sharpe | Drawdown % | Trades |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `candidate_006` | `TQQQ/VOO/GLD`, `126d`, `7d`, `1.00x` | `452.801` | `412.001` | `1.076` | `33.4` | `10` |
| `candidate_097` | `TQQQ/SPY/GLD`, `126d`, `7d`, `1.00x` | `452.678` | `411.878` | `1.076` | `33.4` | `10` |
| `candidate_057` | `TQQQ/QQQ/GLD`, `126d`, `7d`, `1.00x` | `423.825` | `386.725` | `1.039` | `33.4` | `9` |
| `candidate_005` | `QQQ/VOO/GLD`, `126d`, `7d`, `1.00x` | `328.189` | `224.389` | `1.316` | `13.9` | `21` |
| `candidate_017` | `TQQQ/VOO/GLD`, `126d`, `7d`, `0.75x` | `307.248` | `267.848` | `0.952` | `27.9` | `10` |
| `candidate_096` | `TQQQ/SPY/GLD`, `126d`, `7d`, `0.75x` | `307.156` | `267.756` | `0.952` | `27.9` | `10` |
| `candidate_008` | `GLD 20/120 + 189d`, `1.00x` | `260.720` | `178.620` | `1.097` | `13.8` | `6` |
| `candidate_198` | `TQQQ/VOO/GLD`, `126d`, `7d`, `0.33x` | `121.522` | `91.722` | `0.608` | `15.5` | `10` |

## Family Table

| Family | Count | Avg Score | Median Score | Avg Return % | Avg Sharpe | Avg Drawdown % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `dual_momentum` | `155` | `194.785` | `183.206` | `177.406` | `0.747` | `28.662` |
| `sma_regime` | `27` | `136.714` | `124.252` | `125.592` | `0.648` | `26.852` |
| `donchian_regime` | `15` | `88.793` | `74.246` | `99.326` | `0.537` | `32.140` |
| `buy_and_hold` | `4` | `30.437` | `2.776` | `70.087` | `0.419` | `40.800` |

## Position-Size Table

| Position Size | Count | Avg Score | Median Score | Avg Return % | Avg Drawdown % |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.33` | `4` | `106.545` | `118.700` | `83.470` | `15.475` |
| `0.50` | `46` | `97.705` | `95.287` | `95.109` | `24.287` |
| `0.67` | `34` | `159.569` | `144.528` | `157.566` | `32.421` |
| `0.75` | `44` | `167.110` | `169.553` | `161.898` | `31.491` |
| `1.00` | `40` | `248.231` | `239.937` | `242.273` | `37.545` |

## Useful

- Full-size leveraged `TQQQ/*/GLD` rotations remained the strongest raw-return configurations even after being stress-tested against explicit position sizing.
- `0.75` size was the best leveraged compromise tested. It reduced drawdown materially versus full size while retaining a large share of the score and return edge.
- The offensive proxy mattered less than expected inside the leveraged bucket. `TQQQ/VOO/GLD`, `TQQQ/SPY/GLD`, and `TQQQ/QQQ/GLD` all behaved very similarly around the winning `126-day`, `7-day` cluster.
- The non-leveraged control still mattered. `QQQ/VOO/GLD 126/7` remained the best control-grade strategy with much lower drawdown than the leveraged winners.
- `GLD 20/120 + 189-day time stop` stayed the best single-asset active GLD configuration and remained useful as the clean single-asset reference strategy.

## Not Useful

- `0.50` and `0.33` position sizes de-risked too aggressively. They cut drawdown, but gave up too much return and score versus the `0.75` bucket.
- Risk-scaled `QQQ/VOO/TLT` variants still did not challenge the GLD-defensive cluster. Lower sizing did not rescue the legacy defensive path.
- Leveraged Donchian tests on `TQQQ` remained weaker than leveraged dual-momentum even after sizing was added.

## Invalid Or Process Issues

- No template-level execution issue appeared.
- The latest `dual_momentum` order-event files still showed `0` invalid orders.
- A small set of process-level failures appeared on the first pass and were cleared by the standard retry flow.

## Interpretation

- The campaign now has three distinct classes:
  - raw-return leader: full-size leveraged `TQQQ/*/GLD`
  - deployable leveraged compromise: `0.75` sized `TQQQ/*/GLD`
  - control-grade non-leveraged leader: `QQQ/*/GLD`
- That split is more valuable than a single headline winner because it maps directly to different risk appetites.

## Next Round

- Stop widening the parameter grid again.
- Use the next batch for subperiod validation of:
  - `QQQ/VOO/GLD 126/7`
  - `QQQ/SPY/GLD 126/7`
  - `QQQ/XLK/GLD 126/7`
  - `TQQQ/VOO/GLD 126/7` at `1.00x` and `0.75x`
  - `GLD 20/120 + 189d`
- Keep one `QQQ/VOO/TLT` legacy control in the validation batch to verify continued inferiority.
