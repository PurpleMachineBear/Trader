# Plan Schema

Codex writes a `plan.json` for each round. The executor consumes it without adding strategy judgment.

## Shape

```json
{
  "iteration": "iter_001",
  "thesis": "Cross-family ETF and stock research should compare against a fixed passive benchmark and a stable active control.",
  "benchmark": {
    "symbol": "VOO",
    "family": "buy_and_hold",
    "purpose": "Primary passive benchmark"
  },
  "universe": {
    "name": "core_us_macro_v2",
    "selection_rule": "Fixed liquid US ETFs, defensive ETFs, and approved mega-cap stocks",
    "allowed_symbols": ["SPY", "VOO", "QQQ", "TQQQ", "IWM", "DIA", "TLT", "IEF", "GLD", "AAPL", "MSFT"],
    "validation_symbols": ["SPY", "VOO", "QQQ", "TQQQ", "IWM", "DIA", "TLT", "IEF", "GLD", "AAPL", "MSFT"],
    "blocklist": ["GOOG", "GOOGL"]
  },
  "research_memory": {
    "memory_path": "experiments/research_memory.md",
    "carry_forward_findings": [
      "Pure SMA window search produced diminishing returns after iter_003."
    ]
  },
  "candidates": [
    {
      "candidate_id": "candidate_01",
      "family": "donchian_regime",
      "role": "explore",
      "hypothesis": "A 55/20 Donchian channel may produce a more active but still disciplined trend profile on QQQ.",
      "parameters": {
        "entry_lookback": 55,
        "exit_lookback": 20,
        "max_holding_days": 252
      },
      "symbols": ["QQQ"],
      "universe_name": "core_us_macro_v2",
      "benchmark_symbol": "VOO",
      "validation_symbols": ["SPY", "VOO", "TQQQ"],
      "tags": ["trend", "breakout", "daily"],
      "start_date": "2022-01-01",
      "end_date": "2026-03-06",
      "cash": 100000,
      "notes": ["Written by Codex."]
    }
  ]
}
```

## Supported Families

- `buy_and_hold`
- `equal_weight_buy_and_hold`
- `sma_crossover`
- `sma_regime`
- `donchian_regime`
- `dual_momentum`
- `rotation_rsi`
- `gap_reversal_intraday`
- `day2_breakout_intraday`
- `bsl_reversal_intraday`
- `gap_reversal_scanner_intraday`
- `bsl_reversal_scanner_intraday`
- `vwap_reclaim_scanner_intraday`
- `failed_breakdown_reclaim_scanner_intraday`

## Data Fidelity Note

- The three `*_intraday` families require local minute data in LEAN format.
- The two `*_scanner_intraday` families also support optional `context_symbols` parameters so broad-market or sector proxies can gate entries.
- The two `*_scanner_intraday` families can also use a broader master universe with dynamic daily watchlists instead of a manually frozen ticker basket.
- Useful scanner parameters include:
  - `selection_pool_size`: keep the top `N` premarket-qualified names in the watchlist and let the first valid intraday trigger enter
  - `min_prev_close` and optional `max_prev_close`: price-floor and price-cap filters
  - `min_avg_dollar_volume`: liquidity floor using recent regular-session dollar volume
  - `min_premarket_dollar_volume`: premarket activity floor so thin names do not dominate the watchlist
  - `gap_max`: optional cap on the opening gap when the branch should stay near the reclaim zone instead of chasing large dislocations
  - `max_key_level_distance_pct`: optional filter so the opening price must remain reasonably close to the key reclaim or breakdown level
  - `rank_premarket_dollar_volume_scale`: optional ranking boost for heavier premarket dollar volume
  - `rank_key_level_distance_penalty`: optional ranking penalty for symbols opening too far from the key level
  - `rank_relative_premarket_dollar_volume_weight`: optional bucket-relative ranking weight that rewards the heaviest premarket dollar volume names among the already-qualified candidates
  - `rank_relative_key_level_distance_weight`: optional bucket-relative ranking weight that prefers the names opening closest to the key reclaim or breakdown level among the already-qualified candidates
  - `slippage_bps`: optional constant slippage in basis points for paper-readiness or execution-stress validation
  - `risk_per_trade_pct`: optional stop-based risk budget for intraday position sizing; use it only in deployment-validation rounds because it materially changes the capital model
  - `max_daily_loss_pct`: optional intraday engine-level daily loss cap that blocks new entries and can force a kill-switch exit after the threshold is breached
  - `max_daily_trades`: optional cap on actual entries per day for intraday engines when overtrading risk matters
- QuantConnect alternative datasets marked `CloudOnly` should not be assumed available inside the local executor loop. If an event-aware plan depends on such a dataset, either move that branch to a cloud-backed workflow or use a locally available substitute.
- They are intended to be research translations of discretionary setups, not literal copies of scanner/news rules.
- Plans using these families should usually:
  - keep a same-symbol passive baseline
  - or, for broader watchlist universes, keep a same-universe equal-weight passive basket baseline
  - keep one carryover benchmark or daily control
  - report activation rate, because zero-trade rows can dominate naive score rankings
  - for validation rounds, repeat the same shortlisted structures across multiple date windows so stability can be judged directly instead of from one full-sample row
