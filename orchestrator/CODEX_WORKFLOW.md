# Codex Research Workflow

Use this workflow for multi-round strategy research in this repository.

## Principle

Codex owns reasoning. Local scripts own execution.

- Codex writes plans
- Executor runs plans
- Codex analyzes results
- Executor does not decide winners

## Round Loop

### 1. Planning

Codex writes `plan.json` for the round.

The plan should usually contain:

- `iteration`
- `thesis`
- `benchmark`
- `universe`
- optional `research_memory`
- `candidates`

The `universe` block should usually contain:

- `name`
- `selection_rule`
- `allowed_symbols`
- `validation_symbols`
- `blocklist`

The `benchmark` block should usually contain:

- `symbol`
- `family`
- `purpose`

When scanner families rotate across multiple tradable symbols, the plan should also usually include equal-weight passive basket candidates for the main baskets under study.

Each candidate should include:

- `candidate_id`
- `family`
- `role`
- `hypothesis`
- `parameters`
- `symbols`
- `start_date`
- `end_date`
- `cash`
- `notes`

### 2. Execution

Run:

```bash
python orchestrator/run_loop.py --plan path/to/plan.json
```

This produces:

- per-candidate `result.json`
- iteration-level `results.json`
- LEAN backtest artifacts under each candidate folder

The executor should reject plans whose candidate symbols violate the plan `blocklist` or fall outside the declared allowed universe.

### 3. Analysis

Codex reads:

- `results.json`
- candidate `result.json`
- if needed, `*-summary.json`, `*-log.txt`, or order event files
- for rotation or allocation families, the latest `*-order-events.json` to verify there are no invalid orders

Codex then writes:

- an executive summary
- a technical analysis
- a round memory update
- a roadmap update when the strategic or deployment picture changed
- a decision on whether to continue

For large batches, Codex should not wait until the very end of all planned experiments before reporting. Write checkpoint summaries after each batch or meaningful milestone.

### 4. Next Round

Codex proposes the next `plan.json` based on:

- return quality
- drawdown
- trade count
- stability of the edge
- whether the result looks symbol-specific

When a round materially changes the strategic direction, deployment readiness, or operational blockers, update `/Users/chenchien/lean/ROADMAP.md` in the same pass as the round analysis.

## Default Candidate Mix

For a normal 5-candidate round, prefer:

- 2 exploit candidates
- 2 explore candidates
- 1 control candidate

## Executive Report Template

Unless the user asks otherwise, each executive report should cover:

- decision
- what changed
- winner
- key metrics
- main risks
- recommendation for next round

Preferred report structure for serious rounds:

- `Sample Coverage`: absolute start date, absolute end date, and whether the latest year is partial `YTD`
- `Summary Table`: candidate, family, role, score, return, Sharpe, drawdown, trades
- `Unique Structure Table`: deduplicated by strategy structure so repeated aliases do not crowd out the shortlist
- `Benchmark Table`: each key candidate versus the benchmark on excess return, Sharpe delta, and drawdown delta
- `Passive Baseline Table`: when single-asset active candidates matter, compare them to the same symbol's passive buy-and-hold baseline
- `Yearly Return Table`: benchmark, control, winner, and other key candidates by calendar year plus current-year-to-date when data is available
- `Risk Bucket Table`: when leveraged and unleveraged candidates are mixed, summarize each bucket separately instead of relying on one combined ranking
- `Activation Table`: for intraday or sparse-trigger families, report how many candidates actually traded and the average return of active rows
- `Intraday Quality Table`: for minute-family rounds, rank active intraday rows by return, drawdown, and return/drawdown instead of relying only on Sharpe-based score
- `Selection Distribution`: for scanner families, inspect top order-event files and show which symbols the winning scanners actually traded
- `Dynamic Watchlist Comparison`: for rounds that test broader premarket watchlists, compare dynamic-watchlist winners directly against the carryover fixed-basket controls
- `Knob Sensitivity Table`: for narrow branch-study rounds, compare the base branch to each filter variant across windows so isolated one-window wins do not get over-promoted
- `Stability Table`: for validation rounds, aggregate the same strategy structure across windows with average, median, min, and max score
- `Useful / Not Useful / Invalid / Next`

For scanner-based rounds, the readable structure label must include materially behavior-changing gates such as:

- `selection_pool_size`
- `context_min_positive`
- `context_require_above_vwap`
- `context_require_above_open`
- materially different entry or holding windows

For serious rounds, add an `analysis.md` that explicitly states:

- what was useful
- what was not useful
- what was invalid due to data/process errors
- what to test next

## Guardrails

- Do not treat low-trade results as strong evidence.
- Do not treat high-return, high-drawdown results as automatic winners.
- Keep one control candidate in serious comparison rounds.
- Keep one benchmark candidate or one explicit benchmark reference in serious comparison rounds.
- Treat universe definition as first-class strategy design, not as cosmetic metadata.
- Prefer reporting on the most recent available date rather than arbitrarily stopping at an older year if current data is available.
- Prefer local symbols with data already present unless the user explicitly expands the dataset.
- Do not assume QuantConnect alternative datasets are locally testable. If a required dataset is marked `CloudOnly`, treat it as a separate cloud-backed research lane instead of silently mixing it into the local executor loop.
- For cloud-backed lanes, do not assume a successful cloud backtest means the latest local code is running. If `lean cloud push` failed, treat the cloud project as potentially stale until a fresh push succeeds.
- If a cloud push times out or fails before a batch that depends on new code changes, treat the entire affected batch as stale and rerun it from scratch after a confirmed successful push.
- If `lean cloud push` reports `Invalid credentials` but `lean whoami`, `authenticate`, and `projects/read` still work, test whether `projects/update` is failing on non-code metadata such as `description`. For now, prefer empty local `config.json.description` values in cloud-backed research projects and keep narrative notes in `README.md`.
- For cloud-backed batch research, pace submissions conservatively. QuantConnect can return `Too many backtest requests; please slow down.` if several backtests are launched too quickly in sequence. Retry failed cloud candidates with deliberate spacing instead of treating the rate-limit as a strategy failure.
- For heterogeneous universes, compare single-asset winners both to the common benchmark and to the same symbol's passive buy-and-hold baseline when available.
- Write tables using readable structure labels, not only raw `candidate_id`, and exclude failed runs from aggregate tables unless the point is to document process failure.
- For intraday pilot rounds, do not rely on score alone. Report trade activation rate and inspect whether zero-trade candidates simply over-filtered the sample.
- For scanner-based rounds, compare winning baskets to a same-sample basket passive baseline when possible; single-name passive references are not sufficient once the scanner can rotate across multiple names.
- Before adding a local same-basket passive baseline for symbols that recently entered through a cloud-only or recent-window lane, inspect the local daily ZIP and factor-file start dates for every basket name. If the local files start later than the validation window, backfill them first instead of silently accepting a truncated passive baseline.
- After repairing a previously invalid local same-basket passive baseline, rerun the affected earlier-window comparison before carrying forward hostile-window promotion claims from the cloud lane. The repaired passive check can materially downgrade a branch that only looked strong against an invalid baseline.
- For rename-sensitive equities or symbols with historical ticker changes, inspect local daily files for large internal date gaps as well as late starts. A symbol can have the right first date but still be unusable for older local validation if the rename path is broken.
- For dynamic-watchlist rounds, include the watchlist pool size in readable structure labels so `pool 1`, `pool 3`, and `pool 5` are not collapsed into one apparent structure.
- For scanner-based rounds, readable structure labels must also include materially different context gates so `ctx+ 1` and `ctx+ 2` are not merged into one apparent structure.
- For subwindow validation rounds, include the sample window in row-level tables and keep a structure-level stability table so the same strategy is not judged from only its single best window.
- For short YTD validation windows, do not over-rank candidates on Sharpe or the default composite score alone. Short samples can inflate both; use positive-window count and return/drawdown by window as the primary judgment.
- For cloud-only event branches, short YTD windows can also have extremely low trade counts. Treat near-zero-trade YTD wins as sparse evidence, not promotion evidence.
- For cloud event-aware rounds, if a filtered row such as `after_close` is identical to the unfiltered row in a validation window, treat that filter as inert for that window and stop tuning it as though it explained the result.
- For cloud event-aware rounds, if a simple tape-state gate such as `QQQ/XLK positive` or `QQQ/XLK weak` underperforms the canonical control across both the recent and earlier validation windows, stop spending budget on that coarse gate and move to richer event metadata instead.
- For cloud event-aware rounds, if report-time-conditioned hold variants all underperform the fixed-hold canonical control across both the recent and earlier validation windows, stop spending budget on hold-schedule micro-tuning and move to richer metadata instead.
- For cloud event-aware rounds, if a hard rolling symbol-quality floor materially reduces both return and drawdown quality on the canonical branch across the recent and earlier validation windows, treat selector mechanics as exhausted for that lane and move to richer metadata or a downstream integration test instead.
- When a cloud research project is extended to a new strategy style or major code path, rerun the canonical carryover control immediately and treat any material drift versus the remembered control as a process caveat until invariance is explained. Do not silently compare post-refactor rows to older cloud results as though nothing changed.
- For cloud event-aware intraday pilots, if `failed_breakdown` is inactive across both the recent and earlier validation windows while `BSL` is at least active, stop spending budget on event-aware `failed_breakdown` and treat the lane as `BSL`-only until new metadata suggests otherwise.
- For cloud event-aware intraday pilots, if removing the inherited recent-weakness assumption materially improves both recent and earlier windows, promote the relaxed branch to the new control and stop tuning recent-return scoring when `absolute` and `none` score modes collapse to the same path.
- For cloud event-aware intraday pilots, if increasing `selection_pool_size` is inert across windows and dropping the minute context gate helps only one window, keep the smaller pooled context-gated row as canonical and move to downstream integration or risk/exit work instead of more selector tuning.
- For cloud event-aware intraday pilots, if `report_time_filter=after_close` is behaviorally identical to `any` across windows and `estimate_mode=required` is materially worse than the canonical control, stop spending budget on the current QuantConnect event metadata for that lane and move to downstream integration, richer external metadata, or risk/exit work.
- For cloud event-aware intraday pilots, if shorter holds or lower profit targets only reduce drawdown while also reducing return across both recent and earlier windows, keep the canonical control unchanged and stop spending budget on simple exit/risk micro-tuning for that lane.
- For cloud-to-master integration rounds, if hard event-state gates materially reduce intraday order count across both recent and earlier windows while also underperforming the ungated master control, keep the event state as a shadow reference and do not promote it into the production master as an activation rule.
- For cloud-to-master integration rounds, if a simple event-state allocation tilt preserves activation but still underperforms the ungated master across both recent and earlier windows, stop spending budget on count-based master tilts and move to richer metadata or shadow-branch promotion logic instead.
- For cloud-to-master integration rounds, if an independent event sleeve improves only aggregate windows, do not promote it yet. Require hostile/current split-window validation before treating it as a production master upgrade.
- For cloud-to-master integration rounds, if split-window validation shows an event sleeve is neutral in the hostile window, strongest in the positive window, and weaker in the sparse current window, classify it as a `positive-window shadow sleeve` rather than an all-weather master improvement.
- For cloud event-sleeve regime-detection rounds, if a proxy such as `offensive_only` improves the hostile split but materially weakens the positive split and the aggregate validation window, classify it as a hostile-window cleaner only, not a positive-regime detector.
- For cloud event-sleeve regime-detection rounds, if same-day event breadth proxies such as `min_active_events >= 2` underperform the canonical sleeve control across hostile, positive, and current windows, stop spending budget on coarse breadth gates and move to richer metadata.
- When parsing QuantConnect CLI backtest tables, do not rely on naive label searches because rows like `Net Profit`, `Sharpe Ratio`, and `Drawdown` can appear more than once. Parse the saved table cells structurally from the `cloud_runs` logs before writing `results.json`.
- For cloud event-aware basket refinements, if a narrower basket wins an extended aggregate window but does not also improve the recent broad sample, keep the broader control as canonical and require explicit hostile/current split-window validation before promotion.
- For sparse cloud current-window validations, if multiple basket variants collapse to the same few trades or same symbol path, treat the window as non-discriminating and do not use it to decide basket promotion.
- When a cloud basket-discovery campaign already yields a clear hostile-window alias, a clear positive-window alias, and a stable canonical control, stop basket permutation work and move to richer metadata or state detection instead of squeezing the same symbol set further.
- For branch-promotion rounds on new scanner sub-universes, require at least one hostile earlier window in addition to the recent positive windows that motivated the branch.
- For longer-horizon intraday validation rounds, pair the broad sample with explicit `2024`, `2025`, and current-year `YTD` splits when data is available. A broad positive row alone is not enough to promote a recent-regime branch.
- Do not promote a new branch into the frozen paper set when each tested filter wins only one window and none improves the base across all windows. Keep it shadow or regime-specific instead.
- Treat invalid orders in rotation families as a process bug until proven otherwise, not as harmless noise.
- When leveraged and unleveraged candidates are mixed in the same round, do not rely only on one composite score. Use drawdown ceilings or separate risk buckets so raw return does not dominate the ranking.
- When report tooling is corrected mid-round, regenerate the affected tables before final analysis so stale aliases do not survive into memory or roadmap updates.
- For routed or regime-conditioned branches, broad-sample improvement is not sufficient for promotion. Require explicit split-window validation before updating roadmap or frozen deployment status.
- Treat zero-trade or near-zero-trade routed windows as informative failures, not neutral rows.
- When a narrowed watchlist variant produces the same current-window result as the broader control, keep the broader control as canonical unless cross-window validation clearly favors the narrowed branch.
- After any change to ranking or watchlist tie-breaking logic, rerun at least one canonical control with reversed symbol order or another direct invariance check before trusting new scanner results.
- When a new scanner branch wins the broad sample, require a direct head-to-head by subwindow against the old family control before promotion.
- When a selector upgrade is introduced, validate it separately inside each family of interest. A ranking change that helps `BSL` can still hurt `failed_breakdown`, and vice versa.

## Large-Scale Research

For rounds or campaigns larger than roughly 100 candidates:

- split the work into batches
- keep one stable benchmark and one stable control across batches
- checkpoint after each batch with a short written report
- update `experiments/research_memory.md` after each batch, not only at the campaign end
- avoid blindly expanding parameter grids if prior batches already show a family is dominated
- for optimization-heavy rounds, report both raw candidate count and deduplicated unique-structure count
- new minute-data families should pass a smoke round before entering a large batch
- prefer a stable concurrency setting below the Docker or LEAN failure threshold; if process-level failures appear, retry only failed candidates at lower concurrency before analyzing results
- clear or overwrite prior candidate `backtest/` artifacts before reruns so the latest summary and order-event files are unambiguous

## Current Tooling

- Strategy template renderer: `orchestrator/templates.py`
- Executor entrypoint: `orchestrator/run_loop.py`
- Plan schema reference: `orchestrator/PLAN_SCHEMA.md`
- Premarket watchlist helper: `orchestrator/premarket_planner.py`

## Paper Deployment Notes

When a shortlisted strategy is promoted from research to QuantConnect Paper:

- ensure the local project `config.json` includes `algorithm-language`, not only `local-id`
- ensure [lean.json](/Users/chenchien/lean/lean.json) points at the real QuantConnect `job-organization-id`, not `local`
- for non-interactive paper deploys, pass `--data-provider-live QuantConnect` explicitly along with brokerage, node, restart, and notification flags
- remember that QuantConnect live trading ignores `SetStartDate`, `SetEndDate`, and `SetCash`; paper/live behavior is driven by the current deployment time and live brokerage state, not the backtest sample window
- do not use `lean cloud status --verbose` as a routine monitoring command because it can print plaintext brokerage authentication metadata. Treat verbose cloud status output as secret material and never echo credentials back into notes, reports, or chat.

## Deployment Acceptance

Before promoting a strategy from research winner to frozen paper deployment, complete these checks:

- add or confirm account-level risk controls:
  - daily loss cap
  - max exposure limit
  - no-new-entry kill switch after breach
- write or update a broker-specific runbook:
  - deployment steps
  - weekly restart / re-auth flow
  - monitoring checks
  - stop and redeploy protocol
- run an execution-realism pass on the promoted strategy:
  - inspect filled order events
  - estimate sensitivity to higher slippage assumptions
  - record whether the edge survives at reasonable paper/live stress levels
- keep the live/paper lane frozen while exploration continues elsewhere
- use safe status commands only; never rely on verbose cloud status as a normal monitoring tool

## Git Checkpoints

- Treat git commits as research checkpoints, not as an afterthought.
- Create a commit when a pass leaves the repository in a coherent state with code, reports, memory, and workflow notes aligned.
- Before any push:
  - review `git status`
  - ensure `.gitignore` is excluding local data, backtest artifacts, and scratch outputs
  - avoid mixing unrelated changes into the same commit
- It is acceptable to push directly to the configured main research remote when:
  - the current state is reproducible enough to checkpoint
  - there are no obvious secrets or accidental large artifacts staged
  - the push preserves a clear narrative of what changed
- If a pass is exploratory, half-finished, or process-invalidated, prefer another local commit later over pushing noisy history immediately.

## When Starting a New Session

If the user asks to continue the research loop:

1. Read the latest round folder under `experiments/`
2. Read the most recent `executive_report.md` if present
3. Read `experiments/research_memory.md`
4. Read the latest `results.json`
5. Decide whether the next action is:
   - write a new `plan.json`
   - run the executor
   - analyze fresh results
