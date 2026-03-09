# Cloud Earnings Research

## Purpose

This project is the first cloud-backed research lane for `QuantConnect Upcoming Earnings`, which is available to the account but marked `CloudOnly` and therefore cannot be assumed usable inside the local `run_loop.py` workflow.

## Current Local Code

- `main.py` now supports three styles:
  - `strategy_style=swing`
  - `strategy_style=intraday`
  - `strategy_style=master_portfolio`
- The project still uses `EODHDUpcomingEarnings` as the event source, but it can now either:
  - rebalance a small multi-day event basket
  - or trade a minute-level intraday `BSL` / `failed_breakdown` pilot on qualified event days
  - or use the earnings basket as a shadow event-state input for a master-style `daily core + fixed NVDA/TSLA intraday sleeve` portfolio

## Current Cloud Status

- Cloud project created: `Cloud_Earnings_Research`
- Cloud project id: `28794465`
- Local code has been pushed successfully.
- First cloud-backed earnings smoke backtest:
  - backtest id: `40fc820bf9e780c5086640f26f98149e`
  - result: `-15.301%`, `19.3%` drawdown, `23` orders

## Important Operational Note

The earlier `Invalid credentials` push error was not actually caused by bad login state. The root cause was that `projects/update` returned a server `500` when the local project `config.json` included a non-empty `description`. The LEAN CLI surfaces that server-side failure as a generic credentials error.

Workaround:

- keep `config.json.description` empty for this project
- store explanatory text in this `README.md` instead of the project description field

## Current Research Status

- The swing lane already produced a real cloud-only event branch around `platform5 pre1 hold3`.
- The new intraday lane has also passed smoke and first formal rounds.
- The project now also supports a cloud-backed `master_portfolio` integration lane.
- The project now also supports an independent cloud event sleeve inside `master_portfolio`.
- The current cloud intraday control is:
  - `platform5 pre1 intraday BSL`
  - no recent-weakness requirement
  - `selection_pool_size = 2`
  - `QQQ/XLK` context with `context_min_positive = 1`

This branch is still a shadow/reference lane, not a frozen paper promotion candidate.

- The current cloud-to-master verdict is:
  - `platform5 pre1` event state can be wired into the master safely
  - but the tested count-based activation gates and the simple `0.30 / 0.10` tilt do not improve the ungated master
  - event state therefore remains a shadow reference, not a production master switch
  - a separate `event_sleeve_enabled=true` branch does improve the master on aggregate windows
  - split-window validation shows that sleeve is a `positive-window shadow sleeve`, not an all-weather production upgrade

## Current Master Event-Sleeve Knobs

The `master_portfolio` style now supports an optional cloud event swing sleeve through:

- `event_sleeve_enabled`
- `event_sleeve_bucket`
- `event_sleeve_event_mode`
- `event_sleeve_allocation`
- `event_sleeve_max_names`
- `event_sleeve_hold_days`
- `event_sleeve_lookback_days`
- `event_sleeve_min_avg_dollar_volume`
- `event_sleeve_report_time_filter`
- `event_sleeve_estimate_mode`

These knobs are meant for:

- testing a small event sleeve alongside the daily core and fixed `NVDA/TSLA` intraday sleeve
- comparing `platform5` and `enterprise4` event baskets as additive overlays
- validating whether the sleeve is broad enough to help outside a single favorable year

It now also supports simple regime-detection proxies for the event sleeve:

- `event_sleeve_core_state_filter`
  - `any`
  - `offensive_only`
- `event_sleeve_min_active_events`

Current verdict:

- these coarse proxies are not a usable positive-event regime detector
- `offensive_only` can clean up hostile `2024`, but it damages `2025` and aggregate windows
- `min_active_events >= 2` is broadly harmful
- keep `platform5 sleeve 10%` as the canonical cloud event-sleeve control

## Current Event-State Knobs

The cloud lane now supports simple pre-event state gating through backtest parameters:

- `recent_return_min`
- `recent_return_max`

These gates apply to the trailing `lookback_days` return before the event selection score is computed. They are intended for tests such as:

- pre-earnings pullback only
- flat/neutral pre-event state
- pre-event strength only

It also supports simple market/sector tape state gating:

- `context_symbols`
- `context_lookback_days`
- `context_return_threshold`
- `context_min_positive`
- `context_max_positive`

This allows tests such as:

- require `QQQ` and `XLK` both positive over the last `5` days
- require weak tape with zero positive context symbols
- combine `report_time_filter` with market/sector state

It now supports explicit estimate-state filters:

- `estimate_mode=any`
- `estimate_mode=required`
- `estimate_mode=missing`

This makes it possible to test whether the event edge is concentrated in names with published estimates, in names without estimates, or is indifferent to estimate availability.

It also supports report-time-conditioned holding rules:

- `hold_days`
- `hold_days_before_open`
- `hold_days_after_close`
- `hold_days_unknown`

These allow tests such as:

- keep the canonical `hold_days=3` default, but shorten `before_open` events to `1` day
- keep `after_close` events at `3` days while testing a `2` day `before_open` carry
- shorten only `after_close` events while leaving the fallback hold unchanged

## Current Intraday Knobs

The same project now supports event-aware intraday research through these parameters:

- `strategy_style=intraday`
- `intraday_family=bsl` or `intraday_family=failed_breakdown`
- `selection_pool_size`
- `require_recent_weakness`
- `recent_return_score_mode`
- `min_premarket_dollar_volume`
- `max_key_level_distance_pct`
- `rank_premarket_dollar_volume_scale`
- `rank_key_level_distance_penalty`
- `context_symbols`
- `context_min_positive`
- `context_require_above_vwap`

These are intended to answer questions such as:

- should the event intraday lane inherit the generic `weak-then-reclaim` assumption from local BSL research
- does the event lane need a broader watchlist pool
- does the minute `QQQ/XLK` tape gate help or just over-filter the event branch

## Important Process Note

After the project was extended from pure swing research into combined swing + intraday research, the carryover swing control changed materially on the recent broad window. The new result is stable across reruns, but it no longer matches the older remembered cloud control. Until that invariance gap is isolated, treat direct comparisons between pre-refactor and post-refactor cloud swing rows as stale.
