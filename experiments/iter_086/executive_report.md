`platform5 pre1 hold3` stayed canonical again. Hard rolling quality floors did not clean up the cloud branch; they materially damaged it.

The strongest result is negative but useful:
- broad control `any`: `100.059%`, `DD 10.1%`
- broad `any floor min1`: `76.840%`, `DD 17.8%`
- broad `required control`: `75.473%`, `DD 10.1%`
- broad `required floor min1`: `47.445%`, `DD 17.1%`

The same pattern held on `2024_2025`, so this is not a recent-window artifact. The decision is to stop spending near-term budget on cloud selector mechanics. The next valuable work is richer event metadata, or using the cloud branch as an event-state reference for intraday integration rather than continuing to tune the swing selector itself.
