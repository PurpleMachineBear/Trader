# iter_063 Analysis

## Objective

Close the `iter_034` to `iter_063` large-cap campaign by comparing the old `growth4 failed_breakdown` control and the new `hardware7 failed_breakdown` branch directly across `2024`, `2025`, and `2026 YTD`.

## Campaign Summary

The 30-round campaign answered three separate questions:

1. Was prior large-cap dynamic research contaminated by ranking or symbol-order bugs?
2. Could a better large-cap basket rescue the `BSL` lane?
3. If not, was there another large-cap family worth keeping as a shadow branch?

The answers were:

- `No` on the bug question. The deterministic tie-break fix did not change the canonical `growth4 BSL pool2` result.
- `No` on the `BSL` basket-rescue question. Larger or more stable-looking large-cap baskets mostly weakened the branch.
- `Yes, but only partially` on the alternative-family question. `hardware7 failed_breakdown` became a real large-cap shadow branch, but not an all-weather promotion candidate.

## Window Table

| Window | `growth4 failed_breakdown` | `hardware7 failed_breakdown` | Decision |
| --- | ---: | ---: | --- |
| `2024` | `5.858%` return, `2.5%` DD | `0.754%` return, `3.6%` DD | Old control still better |
| `2025` | `0.652%` return, `2.6%` DD | `15.598%` return, `2.7%` DD | New hardware7 branch clearly better |
| `2026 YTD` | `-2.099%` return, `2.1%` DD | `1.581%` return, `2.2%` DD | New hardware7 branch better |

## Stress / Knob Findings

- `hardware7 failed_breakdown` stayed positive on the broad sample at both `3 bps` and `5 bps` slippage.
- `pool1` and `90-minute` variants were acceptable, but neither improved the base `pool2 / 120m` branch enough to replace it.
- This means the branch itself is real, but the local knobs are already close to diminishing returns.

## Useful

- The large-cap campaign successfully closed the symbol-order bug question.
- The campaign also ruled out a large amount of low-value basket exploration on the `BSL` side.
- `hardware7 failed_breakdown` is now the main large-cap alternative shadow branch worth carrying forward.

## Not Useful

- Large-cap `BSL` basket expansion did not create a stronger branch than the old `growth4` control.
- Broad-sample wins alone were not enough. Without the final head-to-head round, `hardware7 failed_breakdown` could have been over-promoted despite its weak `2024`.

## Next

- Keep `growth4 BSL pool2` as the canonical large-cap current-regime reference.
- Keep `hardware7 failed_breakdown` as the main large-cap alternative shadow branch.
- Stop spending more budget on large-cap basket permutations.
- If large-cap work continues, move to ranking, filter, event, and premarket design.
