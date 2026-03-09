# Iteration 094 Analysis

## Sample Coverage

- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Cloud project: `Cloud_Earnings_Research`
- New style under test: `master_portfolio + independent event sleeve`

## Decision

The independent event sleeve is a real improvement over the ungated cloud master on both aggregate windows.

This is the first downstream integration that actually helped after the earlier count-based event-state gates failed. The effect is not tiny: all tested sleeve variants beat the cloud master control on both aggregate windows, and all of them remained well above `VOO`.

Do not promote it yet. Move immediately to split-window validation before changing the frozen production master.

## Summary Table

| Candidate | Window | Structure | Return | Sharpe | Drawdown | Orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `candidate_01` | broad | `control` | `59.176%` | `1.836` | `10.9%` | `55` |
| `candidate_02` | broad | `platform5 sleeve 10%` | `60.602%` | `2.068` | `9.9%` | `124` |
| `candidate_03` | broad | `platform5 sleeve 15%` | `60.797%` | `2.139` | `9.5%` | `127` |
| `candidate_04` | broad | `enterprise4 sleeve 10%` | `61.024%` | `2.077` | `10.5%` | `102` |
| `candidate_05` | `2024_2025` | `control` | `60.255%` | `1.224` | `6.3%` | `341` |
| `candidate_06` | `2024_2025` | `platform5 sleeve 10%` | `62.646%` | `1.362` | `5.4%` | `442` |
| `candidate_07` | `2024_2025` | `platform5 sleeve 15%` | `63.993%` | `1.390` | `6.1%` | `446` |
| `candidate_08` | `2024_2025` | `enterprise4 sleeve 10%` | `62.688%` | `1.369` | `5.4%` | `407` |

## Benchmark Table

### Recent broad: versus `VOO`, local master, and cloud control

| Structure | Delta vs `VOO` Return | Delta vs local master Return | Delta vs cloud control Return | Delta vs cloud control Drawdown |
| --- | ---: | ---: | ---: | ---: |
| `control` | `+44.713` | `+0.030` | `+0.000` | `+0.0` |
| `platform5 sleeve 10%` | `+46.139` | `+1.456` | `+1.426` | `-1.0` |
| `platform5 sleeve 15%` | `+46.334` | `+1.651` | `+1.621` | `-1.4` |
| `enterprise4 sleeve 10%` | `+46.561` | `+1.878` | `+1.848` | `-0.4` |

### Earlier aggregate: versus `VOO`, local master, and cloud control

| Structure | Delta vs `VOO` Return | Delta vs local master Return | Delta vs cloud control Return | Delta vs cloud control Drawdown |
| --- | ---: | ---: | ---: | ---: |
| `control` | `+15.655` | `-1.783` | `+0.000` | `+0.0` |
| `platform5 sleeve 10%` | `+18.046` | `+0.608` | `+2.391` | `-0.9` |
| `platform5 sleeve 15%` | `+19.393` | `+1.955` | `+3.738` | `-0.2` |
| `enterprise4 sleeve 10%` | `+18.088` | `+0.650` | `+2.433` | `-0.9` |

## Useful

- The event sleeve succeeded where event-state gates failed.
- `platform5 10%`, `platform5 15%`, and `enterprise4 10%` all improved the master on both aggregate windows.
- The broad control invariance check matched `iter_093` exactly, so this round is not a refactor artifact.

## Not Useful

- None of the tested sleeves is obviously dominant on aggregate windows alone.
- Aggregate improvement is not enough to decide promotion because the sleeve could still be only a `2025` amplifier.

## Invalid

- None.

## Next

- Run explicit split-window validation on `2024`, `2025`, and `2026 YTD`.
- Keep the production `IB` paper master unchanged until the event sleeve survives hostile/current split checks.
