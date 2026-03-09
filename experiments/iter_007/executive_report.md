# Iteration `iter_007` Executive Report

## Decision

Continue. Batch 2 confirmed that the `GLD` defensive thesis is robust and narrowed the winning parameter cluster materially.

## Winners

Raw-return winner:

- `candidate_101`: `TQQQ/VOO/GLD dual_momentum`, `126-day` lookback, `7-day` rebalance
- Net profit: `412.001%`
- Sharpe ratio: `1.076`
- Max drawdown: `33.4%`
- Composite score: `452.801`

Control-grade winner:

- `candidate_022`: `QQQ/VOO/GLD dual_momentum`, `126-day` lookback, `7-day` rebalance
- Net profit: `224.389%`
- Sharpe ratio: `1.316`
- Max drawdown: `13.9%`
- Composite score: `328.189`

## What Changed

- The batch added native passive references for the major single-asset ETFs.
- The exploit grid concentrated on `GLD` defensive rotations instead of spending equal budget on `TLT` and `IEF`.
- The round confirmed that leverage now needs a separate interpretation layer. The best `TQQQ/*/GLD` variants are too strong to ignore, but too different from the control-grade set to mix casually.

## Summary Table

| Candidate | Description | Score | Return % | Sharpe | Drawdown % |
| --- | --- | ---: | ---: | ---: | ---: |
| `candidate_101` | `TQQQ/VOO/GLD`, `126d`, `7d` | `452.801` | `412.001` | `1.076` | `33.4` |
| `candidate_081` | `TQQQ/QQQ/GLD`, `126d`, `7d` | `423.825` | `386.725` | `1.039` | `33.4` |
| `candidate_022` | `QQQ/VOO/GLD`, `126d`, `7d` | `328.189` | `224.389` | `1.316` | `13.9` |
| `candidate_041` | `QQQ/SPY/GLD`, `126d`, `7d` | `327.778` | `224.178` | `1.314` | `13.9` |
| `candidate_061` | `QQQ/XLK/GLD`, `126d`, `7d` | `313.789` | `217.589` | `1.240` | `13.9` |
| `candidate_135` | `GLD 20/120 + 189d` | `260.720` | `178.620` | `1.097` | `13.8` |

## Key Findings

- `GLD` defensive rotation is now the dominant cross-family theme of the campaign.
- The best unleveraged rotation variants converged on `126-day` lookback and `7-14` day rebalance across multiple offensive pairs.
- The best leveraged variants used the same core timing logic but pushed return much higher with materially larger drawdowns.
- Passive references improved interpretation: `GLD` remained strong on its own, while active `GLD` timing mainly improved risk rather than raw return.
- The old `QQQ/VOO/TLT` control is now clearly second-tier.

## Main Risks

- Leveraged and unleveraged candidates now occupy different risk classes, so a single headline winner can be misleading.
- The campaign is still operating on one continuous historical window. The next phase needs stricter validation structure.
- `rotation_rsi` remains too turnover-heavy to promote despite some strong absolute returns.

## Recommendation For Next Round

- Split the research into two explicit tracks:
  - non-leveraged `GLD` defensive rotation
  - leveraged `TQQQ/*/GLD` rotation with risk scaling
- Keep one legacy `TLT` control to confirm continued underperformance.
- Add targeted risk overlays through `position_size` rather than immediately widening the symbol universe again.
