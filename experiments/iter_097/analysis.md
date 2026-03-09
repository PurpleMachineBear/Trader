# Iteration 097 Analysis

## Sample Coverage

- Recent broad window: `2025-01-02` to `2026-03-06`
- Earlier aggregate window: `2024-01-02` to `2025-12-31`
- Cloud project: `Cloud_Earnings_Research`
- New question under test: whether known cloud event-basket aliases remain useful when embedded as static event sleeves inside the master

## Decision

Static basket aliasing inside the master is real. It is not just a standalone cloud-swing artifact.

The strongest aggregate row is now `enterprise4 after_close`. It beat the canonical `platform5 any` sleeve on both the recent broad and `2024_2025` aggregate windows. `platform5 after_close` also improved on the canonical `platform5 any` row. `software3` did not transfer its earlier hostile-window story into the master aggregate windows.

Do not promote anything yet. The right next step is explicit split-window validation, because these aggregate wins could still be mostly a `2025` effect.

## Process Check

- The broad canary matched the remembered `iter_094 candidate_02` exactly:
  - `60.602%`, `Sharpe 2.068`, `DD 9.9%`, `124` orders
- This means the alias comparison is being made on a stable cloud-to-master control path.

## Summary Table

| Candidate | Window | Static Sleeve | Return | Sharpe | Drawdown | Orders |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `candidate_01` | broad | `platform5 any` canary | `60.602%` | `2.068` | `9.9%` | `124` |
| `candidate_02` | broad | `platform5 any` control | `60.602%` | `2.068` | `9.9%` | `124` |
| `candidate_03` | broad | `enterprise4 any` | `61.024%` | `2.077` | `10.5%` | `102` |
| `candidate_04` | broad | `software3 any` | `57.948%` | `1.961` | `10.5%` | `89` |
| `candidate_05` | broad | `platform5 after_close` | `61.219%` | `2.094` | `9.9%` | `123` |
| `candidate_06` | broad | `enterprise4 after_close` | `61.714%` | `2.105` | `10.5%` | `97` |
| `candidate_07` | `2024_2025` | `platform5 any` control | `62.646%` | `1.362` | `5.4%` | `442` |
| `candidate_08` | `2024_2025` | `enterprise4 any` | `62.688%` | `1.369` | `5.4%` | `407` |
| `candidate_09` | `2024_2025` | `software3 any` | `60.997%` | `1.329` | `5.4%` | `387` |
| `candidate_10` | `2024_2025` | `enterprise4 after_close` | `63.334%` | `1.388` | `5.4%` | `403` |

## Benchmark Table

### Recent broad: versus `VOO`, local master, and cloud master control

| Static Sleeve | Delta vs `VOO` Return | Delta vs local master Return | Delta vs cloud master control Return | Delta vs cloud master control Drawdown |
| --- | ---: | ---: | ---: | ---: |
| `platform5 any` | `+46.139` | `+1.456` | `+1.426` | `-1.0` |
| `enterprise4 any` | `+46.561` | `+1.878` | `+1.848` | `-0.4` |
| `software3 any` | `+43.485` | `-1.198` | `-1.228` | `-0.4` |
| `platform5 after_close` | `+46.756` | `+2.073` | `+2.043` | `-1.0` |
| `enterprise4 after_close` | `+47.251` | `+2.568` | `+2.538` | `-0.4` |

### Earlier aggregate: versus local/cloud control

| Static Sleeve | Delta vs local master Return | Delta vs cloud master control Return | Delta vs cloud master control Drawdown |
| --- | ---: | ---: | ---: |
| `platform5 any` | `+0.608` | `+2.391` | `-0.9` |
| `enterprise4 any` | `+0.650` | `+2.433` | `-0.9` |
| `software3 any` | `-1.041` | `+0.742` | `-0.9` |
| `enterprise4 after_close` | `+1.296` | `+3.079` | `-0.9` |

## Useful

- `enterprise4 after_close` is the strongest aggregate static alias inside the master.
- `platform5 after_close` is also a real refinement over `platform5 any` on the recent broad window.
- `software3` did not survive the transfer from standalone cloud swing into the master aggregate windows.

## Not Useful

- Aggregate basket wins alone are still ambiguous.
- `software3` should stop being treated as the leading hostile-window master alias until split validation says otherwise.

## Invalid

- None.

## Next

- Run split-window validation across `2024`, `2025`, and `2026 YTD`.
- Specifically test whether:
  - `enterprise4 after_close` is only a `2025` positive-window alias
  - `platform5 any` remains the best all-weather control
  - `software3` loses its hostile-window story once embedded in the master
