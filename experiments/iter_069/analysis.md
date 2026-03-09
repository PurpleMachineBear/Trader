# iter_069 Analysis

## Objective

Test whether bucket-relative ranking rescales the large-cap `BSL` selector better than absolute premarket-dollar-volume and key-level penalties, especially on the adjacent `platform7` bucket.

## Sample Coverage

- `2025-01-02` to `2026-03-06`

## Summary Table

| Structure | Role | Return | Sharpe | Drawdown | Trades |
| --- | --- | ---: | ---: | ---: | ---: |
| `VOO buy_and_hold` | benchmark | `14.463%` | `0.269` | `19.0%` | `0` |
| `platform7 equal_weight_buy_and_hold` | passive baseline | `-1.170%` | `-0.669` | `14.3%` | `0` |
| `growth4 BSL next-gen absolute pool2` | reference | `21.595%` | `1.036` | `3.9%` | `33` |
| `platform7 BSL absolute pool1` | control | `-4.847%` | `-2.459` | `5.3%` | `20` |
| `platform7 BSL relative pool1` | explore | `-9.713%` | `-2.555` | `10.1%` | `20` |
| `platform7 BSL relative pool2` | explore | `-6.671%` | `-1.978` | `8.3%` | `25` |
| `growth4 BSL relative pool2` | explore | `22.045%` | `1.071` | `2.9%` | `32` |

## Selection Distribution

- `platform7 absolute pool1`:
  - `NFLX -6465`, `AAPL -1325`, `NOW -785`, `ORCL +786`, `ADBE +845`, `MSFT +1080`, `CRM +1137`
- `platform7 relative pool1`:
  - `NFLX -6395`, `ORCL -3830`, `AAPL -1325`, `MSFT -729`, `NOW +709`, `ADBE +845`, `CRM +1137`
- `platform7 relative pool2`:
  - `NFLX -5153`, `ORCL -2569`, `AAPL -1325`, `NOW -760`, `CRM +321`, `ADBE +842`, `MSFT +2126`
- `growth4 relative pool2`:
  - `NVDA -1828`, `META +745`, `AMZN +6539`, `TSLA +16746`

## Useful

- Relative ranking did not damage the original `growth4` habitat. It improved the reference slightly from `21.595% / 3.9% DD` to `22.045% / 2.9% DD`.
- The test cleanly answered the scaling question: simple bucket-relative normalization is not enough to rescue `platform7`.

## Not Useful

- `platform7 relative pool1` was worse than the absolute control.
- `platform7 relative pool2` improved versus relative pool1, but it still remained clearly negative and still lagged the absolute pool1 control.
- Losses continued to concentrate in `NFLX`, with additional damage from `ORCL`, so this is not a simple absolute-threshold calibration miss.

## Conclusion

The adjacent-bucket failure is not mainly caused by absolute selector scales. Relative ranking can slightly improve a real habitat (`growth4`), but it does not turn `platform7` into a viable non-event `BSL` branch. That points the next large-cap step away from more selector scaling work and toward explicit `event-aware` selection.

## Next

- Keep `growth4 BSL next-gen` as the local large-cap current-regime reference.
- Do not spend another local round on more `platform7` selector scaling.
- Use the cloud earnings lane to test whether `platform7` is an event-driven branch instead of a generic non-event `BSL` bucket.
