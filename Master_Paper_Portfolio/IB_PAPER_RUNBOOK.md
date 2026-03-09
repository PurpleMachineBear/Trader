# IB Paper Runbook

This runbook is for the deployed `Master_Paper_Portfolio` algorithm when it is connected to `Interactive Brokers` with `QuantConnect` as the live data provider.

## Deployment Shape

- Strategy: `QQQ/VOO/GLD dual_momentum` core + `NVDA/TSLA fixed aggressive BSL` intraday sleeve
- Brokerage: `Interactive Brokers`
- Data provider: `QuantConnect`
- Safe status command:

```bash
lean cloud status "Master_Paper_Portfolio"
```

Do not use `lean cloud status --verbose` for routine checks. It can print plaintext brokerage authentication metadata.

## Recommended Paper Parameters

- `core_allocation=0.75`
- `intraday_allocation=0.20`
- `max_total_exposure_pct=0.95`
- `portfolio_daily_loss_pct_total=0.015`
- `intraday_daily_loss_pct_total=0.0075`
- `portfolio_intraday_disable_pct=0.01`

## Sunday IB Check

1. Watch for the `IB Key` re-authentication prompt after the scheduled weekly restart.
2. Approve the restart on the `IBKR Mobile` app.
3. Confirm the deployment returns to `Running`.
4. If QuantConnect sends a `Connect` or `Stop` email, handle it before the next market session.

## Monday Pre-Open Check

1. Confirm the deployment status is still `Running`.
2. Confirm the brokerage still shows `Interactive Brokers`.
3. Confirm the data provider still shows `QuantConnect`.
4. Open the live logs and verify there is no new brokerage sync or authentication error.
5. Confirm the account equity roughly matches the expected IB paper cash and mark-to-market state.

## What To Watch Each Session

- Whether the core sleeve changes target unexpectedly outside its rebalance rhythm.
- Whether the intraday sleeve logs a watchlist and then either enters once or stays flat.
- Whether the master risk layer logs:
  - `[RISK] new_day=...`
  - `[RISK] exposure_cap ...`
  - `[RISK] master_kill_switch ...`
- Whether order logs show abnormal fills, rejections, or repeated liquidations.

## Stop / Disable Conditions

Stop trading for the day and inspect logs if any of these happen:

- repeated brokerage sync or authentication errors
- unexpected orders outside `QQQ`, `VOO`, `GLD`, `NVDA`, `TSLA`, `SMH`
- master kill switch activation
- multiple intraday entries on the same day
- exposure above the intended sleeve budget

## Restart Protocol

Use this order:

1. Check the live logs.
2. If there is a brokerage/auth problem, fix the broker state first.
3. If the issue is strategy-side and you must redeploy, push code and redeploy once.
4. Do not churn multiple redeploys during market hours unless the current deployment is clearly broken.

## Secret Handling

- Treat QuantConnect deployment metadata as sensitive.
- Do not paste brokerage credentials into notes, reports, or chat.
- Do not use verbose cloud status output in screen shares or recordings.
