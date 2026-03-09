# LEAN Strategy Roadmap

Last updated: `2026-03-09`

## Current Position

- Official completed experiments: `2183`
- Daily track leaders:
  - `GLD 18/110 + 189d time stop`
  - `QQQ/VOO/GLD dual_momentum 126/7`
- Aggressive daily branch leaders:
  - `TQQQ/VOO/GLD 126/7 1.0x` as the raw-return leader
  - `QLD/VOO/GLD 126/7` as the cleaner leveraged compromise
- Intraday track leaders:
  - `NVDA/TSLA high-beta BSL aggressive` as the main stable paper intraday engine
  - `NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO dynamic high-beta BSL pool 1` as the more aggressive secondary intraday engine
- Range-regime exploratory branches:
  - `NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO dynamic high-beta BSL 120m hold` as a current-regime branch
  - `NVDA/AMD/MU/TSM/MRVL/AVGO` semis-only `failed_breakdown_reclaim` as a shadow range-regime branch
  - `AMZN/META/NVDA/TSLA growth4 BSL pool2` as a large-cap current-regime shadow reference
  - `NVDA/AVGO/AMD/MU/MRVL/TSM/MSFT hardware7 failed_breakdown next-gen pool2` as the strongest large-cap alternative shadow branch
- `AAPL/MSFT/CRM/NOW/ORCL platform5 pre1 hold3 earnings basket` as the current cloud-only event-aware large-cap lead
  - `MSFT/CRM/NOW/ORCL enterprise4 pre1 hold3 earnings basket` as the positive-window cloud-only shadow alias
  - `CRM/NOW/ORCL software3 pre1 hold3 earnings basket` as the hostile-window cloud-only alias
- `AAPL/MSFT/NFLX/CRM/ADBE/NOW/ORCL platform7 pre1 hold3 earnings basket` as the broader event-aware control
- `AAPL/MSFT/CRM/NOW/ORCL platform5 pre1 intraday BSL` as the current cloud-only event-aware intraday shadow control
  - current QuantConnect-only event metadata is exhausted on this lane:
    - `after_close` filtering is behaviorally inert
    - `estimate required` is harmful
    - simple exit/risk overlays are also exhausted:
      - shorter holds and lower targets reduce drawdown but also reduce return
    - future work should move to downstream integration or richer external metadata
- Cloud-to-master integration verdict:
  - `platform5 pre1` event state is now validated as a shadow input for a master-style portfolio
  - hard count gates and the tested simple allocation tilt do not improve the current master
  - keep the production `IB` paper master unchanged
  - a separate cloud event sleeve does improve the master on aggregate windows, but split-window validation shows it is a `positive-window shadow sleeve`, not an all-weather production upgrade
  - static aliasing inside the master is real:
    - `enterprise4 after_close` is the cleanest positive-window static alias
    - `platform5 any 10%` remains the canonical all-window control
  - coarse positive-regime proxies are now also exhausted:
    - `offensive_only` improves hostile `2024` but weakens `2025`, `2026 YTD`, and `2024_2025`
    - `min_active_events=2` is broadly harmful
  - reduced `enterprise4 after_close` allocations are also exhausted:
    - `7.5%` is the best small-size compromise, but still loses to `platform5 any 10%` in hostile/current windows
    - `5%` gives up too much positive-window edge without producing cleaner risk
  - current best classification:
    - `platform5` / `enterprise4` event sleeves may be revisited as regime-specific overlays
    - they should not replace or unconditionally augment the frozen master
- Conservative sleeve candidates:
  - `NVDA/TSLA high-beta BSL aggressive risk 1.00%`
- Demoted from paper track:
  - large-cap bullish daily regime gates
  - large-cap simple regime router
  - narrowed `AMZN/TSLA` large-cap aliases as promotion candidates
  - large-cap `BSL` basket expansion as a main research direction
  - `NVDA/TSLA fixed aggressive BSL + daily_loss 0.75%` as a non-universal overlay
  - `dynamic high-beta gap`
  - `fixed high-beta gap`
  - `AAPL/MSFT/AMZN/META core BSL clean`
  - `AAPL/MSFT/AMZN/META core BSL clean risk 1.00%`
- Compliance constraint:
  - `GOOG` and `GOOGL` remain blocklisted

## Higher-Level Gaps

The research is no longer blocked by idea generation. It is now blocked by evidence quality and deployment realism.

What still needs to be hardened:

- `Macro shock regime`
  - The current environment can no longer be treated as a generic high-volatility tape.
  - The active hypothesis is an `oil shock + growth scare + Fed constraint` regime:
    - war / geopolitical escalation pushes energy higher
    - growth data weakens at the same time
    - policy flexibility becomes worse, not better
  - This matters because:
    - `daily core` may need explicit risk-budget logic when `GLD` / defensive legs are already active
    - `intraday` should prefer failed-breakdown / reclaim behavior over breakout assumptions in this regime
    - event sleeves should not be promoted off aggregate results if the macro tape is overriding event quality
  - The next macro question is not only `which strategy wins`.
    - It is `which top-level regime variables explain when beta, gold-defense, intraday reversal, and event sleeves should be emphasized or de-emphasized`.

- `Premarket planning`
  - We still lack a formal stage that turns overnight news, earnings, macro events, and key levels into a daily watchlist and scenario map.
  - A first manual helper now exists at `orchestrator/premarket_planner.py`, but it is still a standalone tool rather than an integrated daily research stage.
- `Event regime`
  - Earnings and catalyst days are not yet modeled explicitly in the intraday stack.
  - Current Polygon access is not enough for Benzinga earnings data, so a full earnings calendar layer needs either a higher entitlement or a separate source.
- QuantConnect `Upcoming Earnings` is available to the account but is marked `CloudOnly`, so it cannot be assumed available inside the local executor loop without a cloud-backed research lane.
  - The cloud-backed lane at `/Users/chenchien/lean/Cloud_Earnings_Research` is operational now.
  - Do not treat a cloud batch as valid if the required `lean cloud push` timed out or failed before code-dependent candidates were launched; rerun the affected batch after a confirmed successful push.
  - The next bottleneck in that lane is richer event metadata, not more basket permutation, hard trailing-return state slicing, simple `QQQ/XLK` tape gating, binary `estimate required/missing` filters, report-time-conditioned hold schedules, or hard rolling quality floors.
  - For the production master specifically, simple count-based event-state gating and simple count-based event-state tilts are now exhausted.
  - For the cloud event sleeve itself, coarse `offensive_only` and same-day `min_active_events` proxies are also exhausted.
  - The next question for this lane is no longer “how to force the sleeve into all windows” or “what is the right static sleeve size”.
    - It is “how to detect the positive event regime that makes the sleeve worth turning on”.
- `Data integrity`
  - A reusable local audit now exists at `/Users/chenchien/lean/orchestrator/data_audit.py`.
  - Active daily-factor mismatches have been repaired for the main daily, master, and intraday reference symbols.
  - A known local rename-history caveat remains for `META` daily data because the series contains a large internal gap.
- `Macro / cross-asset data`
  - Current local research is strong on equities, equity ETFs, minute bars, and cloud earnings events.
  - It is still weak on explicit macro-state inputs such as:
    - oil / energy shock proxies
    - rates / duration shock proxies
    - volatility / credit-stress proxies
    - macro event calendar tags
  - This does not block the current paper master.
    - It does block serious regime-aware research on whether the master should de-risk or reweight in war / inflation shock environments.
  - The first implementation path should prefer locally obtainable proxies before buying new feeds:
    - `USO`, `XLE`, `GLD`, `TLT`, `IEF`, `HYG`, `LQD`, `UUP`, `VIXY`-style ETF proxies where available
    - QuantConnect cloud datasets for economic events
    - existing Polygon minute / news where already entitled
  - Only buy richer metadata if the proxy-based regime work proves directionally useful first.
- `Execution realism`
  - A first slippage audit now exists for the fixed `NVDA/TSLA` aggressive BSL paper candidate.
  - Intraday results still need paper/live fill-drift logging, quote-aware checks, and latency assumptions before live interpretation is strong enough.
  - Dynamic scanners with high cancellation churn need order-management review before they are trusted in paper or live deployment.
- `Risk architecture`
  - The master paper algorithm now has first-pass account-level daily loss and max-exposure guards.
  - We still need better sleeve-level realized PnL accounting, more explicit portfolio heat tracking, and better gap-through handling.
- `Regime routing`
  - The intraday stack now has evidence for both all-weather and range-regime branches, but no formal router that decides when to prefer one over the other.
- `Out-of-sample quality`
  - Approved high-beta intraday minute validation now reaches `2024-01-02`.
  - Earlier-than-`2024` minute history is no longer a blocking gap for the current paper intraday sleeve, but it remains optional future hardening for pre-`2024` regime studies.
- `Portfolio construction`
  - The next meaningful step is not more isolated winners. It is a sleeve design that combines daily controls and intraday sleeves.
- `Operational readiness`
  - A first IB paper runbook now exists for the frozen master deployment.
  - We still need monitoring artifacts, alert discipline, and a tighter deployment acceptance checklist.

## Strategic View

The portfolio should be treated as two engines:

- `Core engine`
  - Daily strategies that carry medium-term return and benchmark-relative outperformance.
- `Tactical sleeve`
  - Intraday strategies that aim for low-drawdown alpha and diversification, not necessarily for maximum raw return versus the strongest beta ETF.

This matters because the current intraday evidence is strongest as a sleeve, not yet as a standalone replacement for the best daily or high-beta passive exposures.

The `iter_014` conclusion changes one key design choice:

- `Ticker selection should be dynamic`
- `Dynamic selection should be bucketed`
- `One giant mixed watchlist is not the right operating model`

The `iter_015` and `iter_016` conclusions change the paper-deployment view:

- `BSL survived longer sample and slippage`
- `gap did not`
- `risk sizing is for conservative sleeves, not for the main paper winner`

The `iter_017` conclusion finishes the paper-shortlist freeze:

- `fixed aggressive BSL` is the stable intraday paper engine
- `dynamic high-beta BSL` stays, but as the more aggressive secondary engine
- `core clean BSL` is no longer in the approved paper set

The `iter_018` conclusion adds one more layer:

- `range-regime` intraday branches do exist
- they currently look real only inside `2026 YTD`
- they should be validated as regime branches, not promoted directly into the frozen all-weather paper set

The `iter_019` to `iter_021` conclusion sharpens that view:

- `dynamic vwap_reclaim` and `dynamic BSL 120m` still look too window-specific for promotion
- `semis-only failed_breakdown_reclaim` is the first new range-regime branch with real `2025` plus `2026` evidence
- but it failed the hostile `2024` window and therefore stays `shadow only`, not paper-approved

The `iter_022` conclusion adds a separate aggressive-daily track:

- `TQQQ/VOO/GLD 126/7 1.0x` still leads raw return after fixing the stale `TQQQ` factor file
- `QLD/VOO/GLD 126/7` is the best leveraged compromise tested so far
- this branch should be researched separately from the current paper master, not merged into it yet

The `iter_023` conclusion closes the longer-horizon intraday question:

- `NVDA/TSLA` fixed aggressive BSL stayed positive in `2024`, `2025`, and `2026 YTD`, so it remains the main all-weather intraday paper sleeve
- `fixed BSL + daily_loss 0.75%` did not generalize and should not replace the base sleeve
- `dynamic high-beta BSL 120m` still looks recent-regime-specific
- `semis-only failed_breakdown_reclaim` is real, but still belongs in the `shadow/range-regime` lane because `2024` stayed hostile
- the approved high-beta minute universe is now validated back to `2024-01-02`

The `iter_024` and `iter_025` large-cap campaign changes the large-cap view:

- no tested large-cap dynamic BSL branch is ready as an all-weather promotion candidate
- `growth4 BSL + strict context` is the only large-cap branch worth deeper work, but only as a `current/range-regime` lane
- core large-cap BSL still behaves like a weak `AMZN/META`-led branch, not a stable broad mega-cap engine
- future large-cap work should compare directly against same-basket passive baselines and tune inside the regime-specific lane instead of reopening all-window promotion debates

The `iter_026` to `iter_033` campaign closes the first large-cap regime-aware selection pass:

- `growth4 BSL pool2` became the canonical large-cap current-regime reference
- positive daily regime gates hurt the large-cap lane and are now deprioritized
- a simple large-cap regime router improved the broad sample but failed split-window validation, so it stays demoted
- narrowing the basket down to `AMZN/TSLA` improved `2025` but was materially worse in hostile `2024` and did not improve `2026 YTD`
- the current large-cap lane is now understood as a shadow/current-regime branch, not as a near-term paper-promotion candidate

The `iter_034` to `iter_063` campaign closes the first large-cap audit and selective-extension pass:

- deterministic watchlist tie-breaking did not change the canonical `growth4 BSL pool2` result, so prior large-cap conclusions were not a symbol-order artifact
- expanding `BSL` into larger or more stable-looking large-cap baskets was mostly negative
- `hardware7 failed_breakdown` became the first large-cap alternative branch worth keeping after validation and slippage stress
- but it still lost to the old `growth4 failed_breakdown` control in hostile `2024`, so it remains a shadow/regime branch rather than an all-weather promotion candidate
- the large-cap lane should now shift away from more basket permutations and toward ranking, filtering, event-awareness, and context design

The `iter_064` to `iter_067` selector campaign refines that conclusion:

- large-cap `BSL` can improve materially when dynamic selection emphasizes premarket dollar volume and key-level proximity
- the new `growth4` selector improved the broad sample and especially `2025`, but it did not create a stronger `2026 YTD` branch than the old current-regime control
- the same selector logic improved `hardware7 failed_breakdown` across `2024`, `2025`, and `2026 YTD`
- but even the improved hardware7 branch still failed to beat the old `growth4 failed_breakdown` hostile-window reference in `2024`
- therefore the selector campaign upgraded the large-cap shadow lane, not the frozen paper set

The `iter_068` adjacent transfer check closes the immediate anti-overfit question:

- the improved `growth4 BSL` selector does not generalize to the nearby `AAPL/MSFT/NFLX/CRM/ADBE/NOW/ORCL` platform bucket
- both the old and new selectors were clearly negative there, while the original `growth4` reference stayed strongly positive on the same sample
- this means the current selector is still habitat-specific rather than a general large-cap BSL engine
- the next large-cap lane should move to event-aware or catalyst-aware ranking, not more adjacent bucket transfer tests

The `iter_069` normalization check narrows that conclusion further:

- bucket-relative ranking can slightly improve a real habitat such as `growth4`
- but it does not rescue `platform7`
- therefore the adjacent-bucket failure is not mainly a simple absolute-threshold scaling problem

The `iter_070` first cloud event-aware round changes the large-cap roadmap:

- `platform7` became strongly positive when the cloud lane restricted it to `pre1` earnings-event names
- `growth4` and `hardware7` were both clearly negative under the same naive event-basket logic
- this is the first strong evidence that `platform7` is an event-driven large-cap branch rather than a generic non-event `BSL` branch
- the next cloud round should focus on `platform7 pre-earnings` timing rather than broad bucket expansion
- QuantConnect `Upcoming Earnings` is sufficient for this next step, so a Polygon Benzinga purchase is not yet justified by current bottlenecks

The `iter_071` to `iter_073` cloud refinement campaign sharpens that verdict:

- `platform7` is not just an event bucket; it is a narrow `pre1` branch whose best tested timing is `pre1 hold3`
- `post1` was negative and `pre3` was weak, so the branch is anticipation-led rather than a generic event carry basket
- changing `max_names` did not improve the branch, which means ranking breadth is not the main bottleneck
- removing `NFLX` and `ADBE` mattered a lot; `platform5 pre1 hold3` became the strongest cloud-only event-aware large-cap shadow branch
- the branch still stays shadow-only because the `2026 YTD` validation was too sparse, not because the `2025` window failed

The `iter_074` report-time round sharpens the quality story further:

- the platform event branch is mostly an `after_close` anticipation setup
- `platform7` improves materially when filtered to `after_close`
- `platform5` still does best with `any`, which means sparse `before_open` events can add value even though they are not the main driver
- the next step should be symbol-specific event quality rather than another global filter sweep

The `iter_075` and `iter_076` symbol-quality rounds close that selector branch for now:

- additive rolling quality bonuses were completely inert
- hard rolling quality floors did move the broad `platform7` branch, but only slightly
- the best floor variant still remained far below `platform5 pre1 hold3`
- the cloud lane now looks more constrained by event-history depth and metadata richness than by another round of ranking micro-tuning

The `iter_077` earlier-window validation materially upgrades the cloud event branch:

- `platform5 pre1 hold3` was positive in hostile `2024`, so the branch is no longer just a `2025` artifact
- the broader `platform7` control remained deeply negative in `2024`, confirming that basket quality, not just event timing, is the structural driver
- `platform5` also remained strong across the combined `2024_2025` window
- the next cloud question is whether the branch is really an even narrower enterprise-software habitat rather than a general `platform5` basket

The `iter_078` habitat-refinement round narrows that answer:

- removing `AAPL` improved the extended `2024_2025` window, so the true branch likely is narrower than `platform5`
- the pure `software3` basket was too narrow because it materially weakened the recent broad sample
- `enterprise4` is the only narrower alias worth carrying forward, but it still does not beat `platform5` across both the extended and recent windows
- the next decision needs an explicit hostile/current split rather than another broad aggregate

The `iter_079` split-window validation resolves that follow-up:

- `enterprise4` does not improve the hostile `2024` window, so it should not replace `platform5` as the main cloud control
- `software3` is the strongest hostile-window alias
- `2026 YTD` is too sparse and too symbol-concentrated to decide basket promotion
- the next useful basket comparison is explicit `2025`, not more current-window tuning

The `iter_080` `2025` round closes the first cloud basket-discovery campaign:

- `enterprise4` is the best clean positive-window refinement
- `software3` remains the hostile-window refinement
- `platform5` stays canonical because it is the least fragile cross-window control
- future progress in this cloud lane is now more likely to come from richer event metadata than from more basket permutations

The `iter_081` passive-baseline round adds a key anti-story check:

- on the clean recent broad sample, passive `platform7` and passive `platform5` were both flat-to-negative
- the corresponding cloud event branches were strongly positive
- this materially increases confidence that the cloud branch contains real event-timing edge, not just a lucky underlying basket
- local earlier-window passive comparisons remain blocked by stale `CRM/NOW/ORCL` factor coverage and should not be treated as valid until repaired

The `iter_082` to `iter_086` event-state rounds close the next layer of simple explanations:

- hard pre-event return gates did not improve the canonical cloud branch
- simple `QQQ/XLK` tape-state gates also underperformed the canonical control
- estimate availability is informative, but only as a partial quality clue; the ungated control still wins
- report-time-conditioned hold schedules failed in both the recent broad and `2024_2025` windows
- hard rolling symbol-quality floors materially damaged `platform5` instead of cleaning it up
- the cloud lane should now stop near-term selector-mechanics tuning and either move to richer metadata or act as an event-quality reference for intraday integration

The `iter_087` repaired passive-baseline recheck refines the cloud-branch claim:

- `platform5` still has a strong two-year event edge versus its same-basket passive baseline on `2024_2025`
- `platform5` did not beat same-basket passive in `2024` alone
- `platform7` failed the repaired earlier-window passive checks and should be treated as demoted
- the cloud lane should now be described as a useful two-year event-edge reference, not as a clear hostile-window passive-beater

The `iter_088` to `iter_091` cloud intraday integration campaign now has a stable stopping point:

- `platform5 pre1 intraday BSL` is a real but sparse cloud-only intraday shadow branch
- removing the inherited recent-weakness assumption was the only material improvement
- increasing watchlist breadth was inert
- dropping the minute context gate was mixed and not promotion-worthy
- `after_close` filtering is inert and `estimate required` is harmful
- therefore the current QuantConnect event metadata is exhausted for this intraday lane
- the next productive step is no longer metadata slicing inside QC; it is either downstream integration, richer external metadata, or risk/exit work on the canonical branch

The `iter_092` follow-up narrows that further:

- the canonical cloud intraday branch is not being obviously held back by a too-slow hold or too-high target
- `hold120`, `rr1.5`, and `rr1.5 + hold120` all compressed drawdown but also reduced return in both windows
- that means simple risk/exit micro-tuning is exhausted too
- the cloud intraday lane should now be treated as mapped enough for its current evidence level; future progress should come from broader integration or richer external metadata, not more internal knob turning

The `2026-03-08` deployment-hardening pass adds three practical conclusions:

- the frozen master now has first-pass portfolio-level daily loss and max-exposure controls
- the IB paper deployment now has an explicit runbook instead of ad hoc operator memory
- the fixed `NVDA/TSLA` aggressive BSL edge survives a simple `1/2/5/10 bp` slippage audit, but it still should be treated as a sleeve with execution risk, not as a high-frequency live engine

## Research Priorities

### Phase 1: Research Hardening

Target window: `2026-03-07` to `2026-03-15`

- Validate the new `range-regime` branches on earlier choppy windows:
  - `fixed BSL + daily_loss 0.75%`
  - `dynamic high-beta BSL 120m hold`
  - `semis-only failed_breakdown_reclaim`
- Deprioritize `dynamic vwap_reclaim 120m hold` until a better regime or event layer explains the `2026`-only strength.
- Deprioritize more local large-cap micro-grids until there is a richer event or premarket layer to justify them.
- Deprioritize more cloud selector-mechanics tuning inside `platform5` until a richer event-metadata source or a concrete intraday-integration test is ready.
- The first concrete cloud intraday-integration test is now complete:
  - `iter_088` showed `platform5 pre1 intraday BSL` is real but sparse, `failed_breakdown` is inactive, and `after_close` is inert
  - `iter_089` showed the real bottleneck was the inherited `recent weakness` assumption; removing it improved the branch materially in both windows
  - `iter_090` showed `pool3` is inert and dropping the `QQQ/XLK` minute context gate is only a mixed split-window alias
  - implication: stop cloud intraday selector micro-tuning and treat the no-weakness `pool2 ctx+1` row as the canonical cloud intraday shadow reference
- A new process caveat exists in the cloud lane:
  - after extending `Cloud_Earnings_Research` to support intraday mode, the carryover recent-broad swing control changed materially and the drift reproduced on rerun
  - until the invariance gap is isolated, compare new cloud intraday results to same-code controls inside the post-refactor project, not directly to older remembered cloud swing rows
- Deprioritize more large-cap basket permutations. The `034-063` campaign showed that basket-level exploration has mostly reached diminishing returns.
- Inspect dynamic scanner order churn:
  - explain why some profitable rows still generate heavy cancellation counts
  - decide whether the behavior is acceptable for paper trading
- Add a basic intraday regime router:
  - separate `all-weather` BSL from `range-regime` reclaim / failed-breakdown branches
  - do not reopen the current simple large-cap router until a richer event or premarket state is available
- For the large-cap lane, prioritize ranking and context work over more universe swaps:
  - event-aware or catalyst-aware watchlist ranking
  - better premarket score design
  - context filters that do more than simple bullish gating
  - validate selector changes separately for `BSL` and `failed_breakdown`; do not assume one ranking formula transfers cleanly across families
  - after `iter_068`, deprioritize more adjacent large-cap transfer baskets until an event-aware layer exists
  - after `iter_069`, deprioritize more local selector scaling rounds on `platform7`; the stronger next question is cloud event timing
  - after `iter_073`, prioritize earlier-window validation for `platform5 pre1 hold3` over more cloud micro-tuning
  - after `iter_074`, prioritize symbol-specific event quality scoring using `report_time` as one feature, not as the only filter
  - after `iter_076`, deprioritize more selector micro-tuning in the cloud platform lane until a richer event sample or richer metadata source is available
  - after `iter_077`, treat `platform5 pre1 hold3` as the canonical cloud control and test whether `AAPL` and possibly `MSFT` are diluting a narrower enterprise-software event branch
  - after `iter_078`, keep `enterprise4 pre1 hold3` only as a shadow alias until explicit hostile/current split windows show it improves both ends of the sample
  - after `iter_079`, keep `software3 pre1 hold3` only as a hostile-window alias unless it also proves itself in `2025`; do not use sparse `2026 YTD` cloud rows to settle basket promotion
  - after `iter_080`, stop near-term cloud basket permutation work and prioritize richer event metadata or state detection if the cloud lane continues
- Build a `Premarket Planning Engine`:
  - overnight news and earnings calendar
  - macro event calendar
  - premarket gap and volume ranking
  - key-level map
  - long/short scenario notes for the opening session
- Add `earnings/event regime` controls:
  - `skip earnings day +/- 1`
  - `only trade earnings day`
  - `only trade post-earnings day 1`
  - `only trade post-earnings day 2`
  - if the source is `CloudOnly`, move that branch to a cloud-backed workflow instead of pretending the local executor can test it
  - near-term cloud focus:
    - `platform7 pre1`
    - `platform7 pre2/pre3`
    - `platform7 hold 1/2/3`
    - optional `platform7 post1`
- Keep universes split by natural branch:
  - `high-beta`: `NVDA`, `TSLA`, then expand to names like `AMD`, `AVGO`, `MU`, `TSM`
  - `core large-cap`: `AAPL`, `MSFT`, `AMZN`, `META`, then expand to names like `ORCL`, `CRM`, `ADBE`, `NFLX`
- Keep the large-cap dynamic lane on `growth4` as the current canonical reference. Do not replace it with narrower `AMZN/TSLA` aliases unless a future event-aware layer proves a durable improvement.
- Keep `hardware7 failed_breakdown next-gen pool2` as the validated shadow large-cap branch, but do not treat it as a frozen or all-weather candidate while `2024` remains weaker than the old `growth4` hostile-window reference.
- Use dynamic watchlists inside each branch instead of manually frozen daily ticker lists.
- Add `futures-proxy / regime` context:
  - use `SPY`, `QQQ`, `IWM`, `SMH`, `XLK`, `TLT` style proxies before building full futures infrastructure
- Extend minute data earlier than `2024-01-02` only if an older hostile regime is needed for the next intraday validation question
- Add walk-forward and rolling-window validation to the top daily and intraday structures
- Add explicit passive references for the aggressive daily branch:
  - `TQQQ buy-and-hold`
  - `QLD buy-and-hold`
  - `SSO buy-and-hold`
- Add first portfolio-level risk rules:
  - max concurrent intraday exposure
  - max daily realized loss
  - max daily signal count
  - no new entries after daily loss threshold breach

### Phase 2: Sleeve Construction

Target window: `2026-03-09` to `2026-03-22`

- Build explicit sleeve candidates:
  - `daily control only`
  - `daily control + high-beta BSL clean`
  - `daily control + core BSL clean`
  - optional `daily control + aggressive BSL sleeve`
- Evaluate:
  - calendar-year returns
  - YTD returns
  - combined drawdown
  - trade count
  - capital usage and idle cash behavior
- Keep the passive references:
  - `VOO buy-and-hold`
  - same-basket equal-weight passive baseline where relevant

### Phase 3: Deployment Readiness

Target window: `2026-03-09` to `2026-03-23`

- Freeze a small deployment shortlist
- Keep the aggressive daily branch out of the first paper master unless it passes a separate deployment-style validation track.
- Keep the frozen paper intraday sleeve on `NVDA/TSLA` fixed aggressive BSL unless a challenger stays positive across `2024`, `2025`, and current `YTD`.
- Create a paper-trading runbook:
  - expected behavior
  - restart procedure
  - broker/data outage procedure
  - alerts to watch
  - what to do when context filters fail or no trades appear
- Add operational logging for:
  - selected symbol
  - context gate state
  - entry timestamp
  - exit reason
  - rejected signals
- Define paper-trading acceptance criteria:
  - no process crashes
  - no invalid orders
  - expected activation rate
  - fill quality not grossly worse than modeled assumptions

## Paper Trading Decision

### QuantConnect Paper Trading

Recommendation: `Yes, feasible starting the week of 2026-03-09`, but only as an operational rehearsal and only after the gates below are closed.

Required gates:

- `LEAN CLI login`
- paid QuantConnect organization access
- live data provider configured
- paper candidate set frozen to `1-2` strategies
- runbook and alerting prepared
- explicit slippage assumptions added to research interpretation

Recommended first paper set:

- one daily control:
  - `QQQ/VOO/GLD dual_momentum 126/7`
- one intraday sleeve:
  - `NVDA/TSLA high-beta BSL aggressive`
- optional shadow intraday sleeve:
  - `NVDA/TSLA/AMD/MU/TSM/MRVL/AVGO dynamic high-beta BSL pool 1`

Do not start paper with the widest candidate set. The goal of the first paper week is to validate operations, not to optimize a dozen live branches simultaneously.

### Interactive Brokers Paper Trading

Recommendation: `Feasible in principle, but not the right first move on this machine`.

Decision:

- `Local IB paper on this Apple Silicon Mac`: `No-go`
- `QuantConnect Cloud + IB paper`: `Possible after account and data setup`
- `Separate x86 host + local IB Gateway`: `Possible, but more operational work than QuantConnect Paper`

Why local IB is not the right next step:

- this machine is `arm64`
- the current local LEAN + IB path does not support ARM-based Macs
- IB adds account, data-subscription, 2FA, restart, and session-management complexity before we have frozen the first production candidate set

IB prerequisites when we choose to pursue it:

- `IBKR Pro`, not Lite
- active market-data permissions for required assets if using IB data
- IB Key mobile authentication
- weekly restart window
- no competing IB session that steals the data feed

## Immediate Next Actions

1. Keep the paper shortlist frozen.
2. Keep `VOO` and same-basket passive baselines in every serious round.
3. Keep `fixed NVDA/TSLA aggressive BSL` as the main intraday paper engine and `dynamic high-beta BSL pool 1` as the secondary aggressive sleeve.
4. Treat `risk_per_trade_pct` rows as optional conservative sleeves, not as the default paper model.
5. Validate the new `range-regime` branches on earlier choppy windows before adding any of them to the paper set.
6. Inspect and reduce dynamic scanner cancellation churn before paper deployment.
7. Prepare QuantConnect Paper as the first deployment rehearsal for the week of `2026-03-09` using only the frozen shortlist.
8. Defer IB paper until either:
   - we switch to QuantConnect Cloud for IB, or
   - we provision an `x86_64` host for local IB Gateway.
9. Harden the repo for concurrent multi-agent research:
   - global `iter_XXX` claim/reservation workflow
   - branch-per-workstream discipline using `codex/<agent>/<topic>`
   - preserved artifact trail for abandoned or invalid concurrent rounds

## What Not To Do

- Do not merge all symbols into one giant scanner universe.
- Do not promote a short-window `2026 YTD` winner directly into the paper set without earlier-window validation.
- Do not judge intraday progress only by raw return against `SMH` or another high-beta ETF.
- Do not rely on paper-trading fills as proof of execution quality without explicit slippage modeling.
- Do not start with local IB paper on this `arm64` machine.
- Do not assume strategy-level stops alone are sufficient portfolio risk control.
