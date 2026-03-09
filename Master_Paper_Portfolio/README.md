# Master Paper Portfolio

This project is the first deployable `master QCAlgorithm` for paper trading.

It combines two validated sleeves:

- `Core daily sleeve`: `QQQ/VOO/GLD dual_momentum 126/7`
- `Tactical intraday sleeve`: `NVDA/TSLA fixed aggressive BSL`

## Default Allocation

- `core_allocation = 0.75`
- `intraday_allocation = 0.20`
- implied cash reserve: `0.05`

## Why This Exists

The repo's current paper-trading shortlist is small enough that a single master algorithm is the most practical deployment shape:

- one QuantConnect paper host is enough
- sleeve behavior is easier to inspect in one account
- shared risk and allocation logic can be added without splitting infrastructure yet

## Runtime Parameters

You can override these as QuantConnect parameters or with `lean backtest --parameter ...`:

- `start_date`
- `end_date`
- `cash`
- `core_allocation`
- `core_lookback`
- `core_rebalance_days`
- `enable_intraday`
- `intraday_allocation`
- `portfolio_daily_loss_pct_total`
- `max_total_exposure_pct`
- `intraday_daily_loss_pct_total`
- `portfolio_intraday_disable_pct`

Recommended first paper values:

- `core_allocation=0.75`
- `intraday_allocation=0.20`
- `enable_intraday=true`
- `portfolio_daily_loss_pct_total=0`
- `max_total_exposure_pct=0.95`
- `intraday_daily_loss_pct_total=0`
- `portfolio_intraday_disable_pct=0`

If you want the more conservative `iter_018` overlay behavior, start with:

- `intraday_daily_loss_pct_total=0.0075`

If you want the first hardened paper profile, start with:

- `portfolio_daily_loss_pct_total=0.015`
- `max_total_exposure_pct=0.95`
- `intraday_daily_loss_pct_total=0.0075`
- `portfolio_intraday_disable_pct=0.01`

## Current Design

- The daily sleeve owns only `QQQ`, `VOO`, and `GLD`.
- The intraday sleeve trades only `NVDA` or `TSLA`.
- `QQQ` and `SMH` are used as intraday context filters.
- The intraday sleeve is limited to at most one trade per day by design.
- The master now supports account-level daily loss and total exposure caps before any new sleeve logic runs.

## What This Is Not Yet

- not a final live-trading portfolio router
- not a multi-sleeve dynamic watchlist engine
- not a broker-specific production deployment package

The next upgrade after paper validation should be:

- better sleeve-level PnL accounting
- optional dynamic high-beta shadow sleeve
- execution-model sensitivity checks against paper/live fills
