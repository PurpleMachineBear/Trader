# Investment Committee Summary

Last updated: `2026-03-08`

## 1. Decision Snapshot

- Keep the current master portfolio as the frozen paper/live candidate.
- Do not promote any new large-cap intraday branch into the frozen set.
- Keep selected shadow branches alive for research only.

## 2. Deployable Set

| Strategy | Sample | Return | Sharpe | Drawdown | Status | Role |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `Master portfolio` | `2025-01-02` to `2026-03-06` | `59.146%` | `1.835` | `10.9%` | Deployable | Primary paper/live candidate |
| `QQQ/VOO/GLD dual_momentum 126/7` | approved control | see shortlist | approved | approved | Deployable | Primary daily engine |
| `NVDA/TSLA fixed aggressive BSL` | `2024-01-02` to `2026-03-06` | `20.995%` | `0.145` | `5.8%` | Deployable | Primary intraday sleeve |
| `VOO buy-and-hold` | `2024-01-02` to `2026-03-06` | `42.608%` | `0.574` | `18.8%` | Benchmark | Passive reference |

## 3. Shadow Set

| Strategy | Sample | Return | Sharpe | Drawdown | Why Keep |
| --- | --- | ---: | ---: | ---: | --- |
| `dynamic high-beta BSL 240m` | `2024-01-02` to `2026-03-06` | `24.695%` | `0.273` | `7.3%` | Real multi-symbol branch, but not yet validated enough to replace fixed `NVDA/TSLA` |
| `semis failed_breakdown_reclaim` | `2024-01-02` to `2026-03-06` | `19.632%` | `0.086` | `4.0%` | Strong regime-specific branch with low drawdown |
| `hardware7 failed_breakdown` | `2024` / `2025` / `2026 YTD` | mixed | mixed | low | Best new large-cap alternative branch, but not all-weather |
| `growth4 BSL pool2` | current-regime large-cap lane | mixed | mixed | low | Canonical large-cap current-regime reference |

## 4. Large-Cap Campaign Verdict

The `iter_034` to `iter_063` campaign closed three open questions:

1. Was large-cap scanner research distorted by symbol-order leakage?
2. Could a better large-cap basket rescue the `BSL` lane?
3. If not, was there another large-cap family worth keeping?

Answers:

- `No`: deterministic tie-break validation showed prior `growth4 BSL pool2` results were not a symbol-order artifact.
- `No`: larger or cleaner-looking large-cap `BSL` baskets mostly weakened the branch.
- `Yes, partially`: `hardware7 failed_breakdown` became a real large-cap shadow branch.

### Final Large-Cap Window Table

| Window | `growth4 failed_breakdown` | `hardware7 failed_breakdown` | Decision |
| --- | ---: | ---: | --- |
| `2024` | `5.858%` return, `2.5%` DD | `0.754%` return, `3.6%` DD | Old control still better |
| `2025` | `0.652%` return, `2.6%` DD | `15.598%` return, `2.7%` DD | `hardware7` clearly better |
| `2026 YTD` | `-2.099%` return, `2.1%` DD | `1.581%` return, `2.2%` DD | `hardware7` better |

Committee interpretation:

- `hardware7 failed_breakdown` is real.
- It is not all-weather.
- It should remain a shadow branch, not a frozen deployment candidate.

## 5. Rejected / Not Promoted

| Strategy / Direction | Decision | Why |
| --- | --- | --- |
| large-cap `BSL` basket expansion | Reject as primary direction | Mostly diluted edge |
| simple regime-router large-cap promotion | Reject | Broad sample improved, but split-window validation failed |
| `dynamic high-beta BSL 120m` | Reject for promotion | Too recent-regime-specific |
| `gap` branches | Rejected earlier | Did not survive stability checks |
| `core clean BSL` families | Rejected earlier | Too dependent on a favorable year |

## 6. What The Research Actually Says

- The deployable edge still comes from combining a daily core with a smaller intraday sleeve.
- Intraday strategies alone generally do not beat `VOO` on raw return across the broad sample.
- Intraday strategies still matter because they offer much lower drawdown and add tactical alpha inside the master portfolio.
- Large-cap dynamic selection is not solved by adding more symbols. It needs better ranking, event awareness, and premarket context.

## 7. Next Research Priorities

1. Improve `dynamic selection` with event-aware and premarket-aware ranking.
2. Add clearer regime gating for when to activate `failed_breakdown`-type shadow branches.
3. Continue high-risk daily research separately from the frozen master.
4. Avoid spending more budget on simple basket permutations.

## 8. Source Files

- Master summary: [1388520389-summary.json](/Users/chenchien/lean/Master_Paper_Portfolio/backtests/2026-03-07_20-34-53/1388520389-summary.json)
- Paper shortlist: [PAPER_TRADING_SHORTLIST.md](/Users/chenchien/lean/PAPER_TRADING_SHORTLIST.md)
- Intraday long-window validation: [iter_023 analysis](/Users/chenchien/lean/experiments/iter_023/analysis.md)
- Large-cap campaign analysis: [iter_063 analysis](/Users/chenchien/lean/experiments/iter_063/analysis.md)
- Large-cap campaign executive report: [iter_063 executive_report.md](/Users/chenchien/lean/experiments/iter_063/executive_report.md)
- Research memory: [research_memory.md](/Users/chenchien/lean/experiments/research_memory.md)
- Roadmap: [ROADMAP.md](/Users/chenchien/lean/ROADMAP.md)
