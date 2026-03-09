# Iteration `iter_010` Executive Report

## Decision

Stop broad search. The campaign has now completed `1004` official experiments, and the marginal value of more local grid expansion is falling. The next phase should be validation and deployment selection, not another same-family sweep.

## Sample Coverage

- Batch size: `201/201 completed`
- Unique structures: `193`
- Sample: `2022-01-01` to `2026-03-06` (`2026 YTD`, latest completed trading day before `2026-03-07`)
- Benchmark: `VOO buy-and-hold`
- Process status: `0` invalid order events after inspecting all round order-event files

## Deployment Shortlist

| Strategy | Bucket | Score | Return % | Sharpe | Drawdown % | Excess Return vs VOO % |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `TQQQ/VOO/GLD dual_momentum 126/7 1.0x` | `leveraged` | `452.801` | `412.001` | `1.076` | `33.4` | `371.630` |
| `TQQQ/SPY/GLD dual_momentum 126/7 1.0x` | `leveraged` | `452.678` | `411.878` | `1.076` | `33.4` | `371.507` |
| `TQQQ/VOO/GLD dual_momentum 126/7 0.75x` | `leveraged` | `307.248` | `267.848` | `0.952` | `27.9` | `227.477` |
| `QQQ/VOO/GLD dual_momentum 126/7` | `non-leveraged` | `328.189` | `224.389` | `1.316` | `13.9` | `184.018` |
| `QQQ/SPY/GLD dual_momentum 126/7` | `non-leveraged` | `327.778` | `224.178` | `1.314` | `13.9` | `183.807` |
| `QQQ/XLK/GLD dual_momentum 126/7` | `non-leveraged` | `313.789` | `217.589` | `1.240` | `13.9` | `177.218` |
| `GLD sma_regime 18/110 + 189d` | `single-asset trend` | `277.323` | `189.423` | `1.155` | `13.8` | `149.052` |

## What Changed

- The previously validated leaders stayed on top after final refinement. This is confirmation, not a new family discovery.
- `GLD` trend refinement did improve materially: `18/110 + 189d` is now the best single-asset active GLD configuration.
- `QQQ/XLK/GLD 126/7` improved slightly over the earlier `126/14` tech-tilted control.
- The report format is now clearer:
  - batch reports distinguish raw candidate count from unique structures
  - rankings are shown by structure, not only by `candidate_id`
  - leverage is treated as its own risk bucket

## Yearly Return Table

| Strategy | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
| --- | ---: | ---: | ---: | ---: | ---: |
| `VOO buy-and-hold` | `-20.26%` | `24.33%` | `23.36%` | `16.39%` | `-1.39%` |
| `GLD buy-and-hold` | `0.44%` | `12.69%` | `26.65%` | `63.67%` | `19.48%` |
| `QQQ/VOO/GLD 126/7` | `0.82%` | `38.00%` | `24.00%` | `57.38%` | `19.48%` |
| `TQQQ/VOO/GLD 126/7 1.0x` | `0.82%` | `100.59%` | `61.88%` | `29.28%` | `20.98%` |
| `TQQQ/VOO/GLD 126/7 0.75x` | `0.65%` | `74.32%` | `48.32%` | `22.15%` | `15.73%` |
| `GLD sma_regime 18/110 + 189d` | `4.10%` | `11.68%` | `25.74%` | `64.75%` | `20.17%` |

## Main Risks

- The raw-return winners still live in a materially higher drawdown bucket than the non-leveraged controls.
- The research sample is now current through `2026-03-06`, but it still only starts in `2022`. That is not enough by itself for deployment confidence.
- Continuing to expand the same parameter grid will create more bookkeeping than insight.

## Recommendation

- Keep three separate final tracks:
  - `leveraged`: `TQQQ/*/GLD 126/7`
  - `non-leveraged`: `QQQ/*/GLD 126/7`
  - `single-asset trend`: `GLD 18/110 + 189d`
- Do not spend the next batch on more `126` micro-tuning.
- Use the next batch for longer-history validation, rolling windows, and additional execution-stress checks.
