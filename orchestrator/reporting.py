#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import statistics
from pathlib import Path


@dataclass
class CandidateRow:
    candidate_id: str
    structure: str
    window: str
    family: str
    role: str
    bucket: str
    score: float
    net_profit_pct: float
    sharpe_ratio: float
    max_drawdown_pct: float
    trade_count: float
    total_orders: float


@dataclass
class YearlySeries:
    returns: dict[str, float]
    latest_timestamp: datetime | None


def compute_score(metrics: dict) -> float:
    return (
        float(metrics.get("sharpe_ratio", 0.0)) * 100.0
        - float(metrics.get("max_drawdown_pct", 0.0)) * 2.0
        + float(metrics.get("net_profit_pct", 0.0))
    )


def classify_bucket(candidate: dict) -> str:
    family = candidate.get("family", "")
    tags = set(candidate.get("tags", []))
    if family in {"buy_and_hold", "equal_weight_buy_and_hold"}:
        return "passive"
    if family.endswith("_scanner_intraday"):
        return "intraday_scanner"
    if family.endswith("_intraday"):
        return "intraday_single"
    if "leveraged" in tags:
        return "leveraged"
    if family == "dual_momentum":
        return "non_leveraged_rotation"
    if family == "sma_regime":
        return "trend"
    return family or "other"


def format_structure(candidate: dict) -> str:
    family = candidate.get("family", "")
    symbols = "/".join(candidate.get("symbols", []))
    parameters = candidate.get("parameters", {})
    slippage_bps = parameters.get("slippage_bps")
    risk_per_trade_pct = parameters.get("risk_per_trade_pct")
    max_daily_loss_pct = parameters.get("max_daily_loss_pct")
    max_daily_trades = parameters.get("max_daily_trades")
    slippage_suffix = f" slip {slippage_bps:g}bps" if slippage_bps else ""
    risk_suffix = f" risk {risk_per_trade_pct * 100:.2f}%" if risk_per_trade_pct else ""
    daily_loss_suffix = f" daily_loss {max_daily_loss_pct * 100:.2f}%" if max_daily_loss_pct else ""
    daily_trades_suffix = f" max_trades {int(max_daily_trades)}" if max_daily_trades else ""

    if family == "buy_and_hold":
        return f"{symbols} buy-and-hold{slippage_suffix}{risk_suffix}{daily_loss_suffix}{daily_trades_suffix}"

    if family == "equal_weight_buy_and_hold":
        size = parameters.get("position_size")
        suffix = f" {size:g}x" if size is not None else ""
        return f"{symbols} equal-weight buy-and-hold{suffix}{slippage_suffix}{risk_suffix}{daily_loss_suffix}{daily_trades_suffix}"

    if family == "dual_momentum":
        lookback = parameters.get("lookback")
        rebalance = parameters.get("rebalance_days")
        size = parameters.get("position_size")
        parts = [symbols, "dual_momentum", f"{lookback}/{rebalance}"]
        if size is not None:
            parts.append(f"{size:g}x")
        if slippage_bps:
            parts.append(f"slip {slippage_bps:g}bps")
        if risk_per_trade_pct:
            parts.append(f"risk {risk_per_trade_pct * 100:.2f}%")
        if max_daily_loss_pct:
            parts.append(f"daily_loss {max_daily_loss_pct * 100:.2f}%")
        if max_daily_trades:
            parts.append(f"max_trades {int(max_daily_trades)}")
        return " ".join(str(part) for part in parts)

    if family == "sma_regime":
        fast = parameters.get("fast")
        slow = parameters.get("slow")
        holding_days = parameters.get("max_holding_days")
        size = parameters.get("position_size")
        parts = [symbols, "sma_regime", f"{fast}/{slow}"]
        if holding_days is not None:
            parts.append(f"+ {holding_days}d")
        if size is not None:
            parts.append(f"{size:g}x")
        if slippage_bps:
            parts.append(f"slip {slippage_bps:g}bps")
        if risk_per_trade_pct:
            parts.append(f"risk {risk_per_trade_pct * 100:.2f}%")
        if max_daily_loss_pct:
            parts.append(f"daily_loss {max_daily_loss_pct * 100:.2f}%")
        if max_daily_trades:
            parts.append(f"max_trades {int(max_daily_trades)}")
        return " ".join(str(part) for part in parts)

    if family.endswith("_scanner_intraday"):
        ctx = "/".join(parameters.get("context_symbols", []))
        ctx_min_positive = parameters.get("context_min_positive")
        ctx_require_above_vwap = parameters.get("context_require_above_vwap")
        ctx_require_above_open = parameters.get("context_require_above_open")
        regime = "/".join(parameters.get("regime_symbols", []))
        regime_lookback_days = parameters.get("regime_lookback_days")
        regime_return_min = parameters.get("regime_return_min")
        regime_min_positive = parameters.get("regime_min_positive")
        confirm = parameters.get("confirm_hold_minutes")
        max_hold = parameters.get("max_holding_minutes")
        max_entry = parameters.get("max_entry_minutes")
        pool = parameters.get("selection_pool_size")
        max_key_level_distance_pct = parameters.get("max_key_level_distance_pct")
        rank_premarket_dollar_volume_scale = parameters.get("rank_premarket_dollar_volume_scale")
        rank_key_level_distance_penalty = parameters.get("rank_key_level_distance_penalty")
        rank_relative_premarket_dollar_volume_weight = parameters.get("rank_relative_premarket_dollar_volume_weight")
        rank_relative_key_level_distance_weight = parameters.get("rank_relative_key_level_distance_weight")
        family_label = family.replace("_intraday", "")
        parts = [symbols, family_label]
        if pool:
            parts.append(f"pool {pool}")
        if ctx:
            parts.append(f"ctx {ctx}")
        if ctx_min_positive is not None:
            parts.append(f"ctx+ {int(ctx_min_positive)}")
        if ctx_require_above_vwap:
            parts.append("ctx_vwap")
        if ctx_require_above_open:
            parts.append("ctx_open")
        if regime:
            regime_part = f"regime {regime}"
            if regime_lookback_days:
                regime_part += f" {int(regime_lookback_days)}d"
            if regime_return_min is not None:
                regime_part += f" >= {float(regime_return_min) * 100:.1f}%"
            parts.append(regime_part)
        if regime_min_positive is not None and regime and int(regime_min_positive) >= 0:
            parts.append(f"reg+ {int(regime_min_positive)}")
        if confirm:
            parts.append(f"conf {confirm}m")
        if max_entry:
            parts.append(f"entry {max_entry}m")
        if max_hold:
            parts.append(f"hold {max_hold}m")
        if max_key_level_distance_pct:
            parts.append(f"keydist <= {float(max_key_level_distance_pct) * 100:.1f}%")
        if rank_premarket_dollar_volume_scale:
            parts.append(f"pm$ {float(rank_premarket_dollar_volume_scale) / 1_000_000:.1f}m")
        if rank_key_level_distance_penalty:
            parts.append(f"keypen {float(rank_key_level_distance_penalty) * 100:.1f}%")
        if rank_relative_premarket_dollar_volume_weight:
            parts.append(f"relpm {float(rank_relative_premarket_dollar_volume_weight):.2f}")
        if rank_relative_key_level_distance_weight:
            parts.append(f"relkey {float(rank_relative_key_level_distance_weight):.2f}")
        if slippage_bps:
            parts.append(f"slip {slippage_bps:g}bps")
        if risk_per_trade_pct:
            parts.append(f"risk {risk_per_trade_pct * 100:.2f}%")
        if max_daily_loss_pct:
            parts.append(f"daily_loss {max_daily_loss_pct * 100:.2f}%")
        if max_daily_trades:
            parts.append(f"max_trades {int(max_daily_trades)}")
        return " ".join(str(part) for part in parts)

    if family in {"gap_reversal_intraday", "day2_breakout_intraday", "bsl_reversal_intraday"}:
        max_hold = parameters.get("max_holding_minutes")
        family_label = family.replace("_intraday", "")
        parts = [symbols, family_label]
        if max_hold:
            parts.append(f"hold {max_hold}m")
        if slippage_bps:
            parts.append(f"slip {slippage_bps:g}bps")
        if risk_per_trade_pct:
            parts.append(f"risk {risk_per_trade_pct * 100:.2f}%")
        if max_daily_loss_pct:
            parts.append(f"daily_loss {max_daily_loss_pct * 100:.2f}%")
        if max_daily_trades:
            parts.append(f"max_trades {int(max_daily_trades)}")
        return " ".join(str(part) for part in parts)

    if parameters:
        return f"{symbols} {family} {json.dumps(parameters, sort_keys=True)}"
    return f"{symbols} {family}".strip()


def sample_window(candidate: dict) -> str:
    start_date = candidate.get("start_date", "")
    end_date = candidate.get("end_date", "")
    if not start_date or not end_date:
        return "-"
    return f"{start_date}..{end_date}"


def load_results(iteration_dir: Path) -> tuple[dict, list[CandidateRow]]:
    results = json.loads((iteration_dir / "results.json").read_text())
    plan = json.loads((iteration_dir / "plan.json").read_text())
    candidate_by_id = {
        item["candidate_id"]: item
        for item in plan.get("candidates", [])
    }

    rows = []
    for result in results["results"]:
        if result.get("status") != "completed":
            continue
        candidate = candidate_by_id.get(result["candidate_id"], {})
        metrics = result.get("metrics", {})
        rows.append(
            CandidateRow(
                candidate_id=result["candidate_id"],
                structure=format_structure(candidate),
                window=sample_window(candidate),
                family=metrics.get("family", ""),
                role=candidate.get("role", ""),
                bucket=classify_bucket(candidate),
                score=compute_score(metrics),
                net_profit_pct=float(metrics.get("net_profit_pct", 0.0)),
                sharpe_ratio=float(metrics.get("sharpe_ratio", 0.0)),
                max_drawdown_pct=float(metrics.get("max_drawdown_pct", 0.0)),
                trade_count=float(metrics.get("trade_count", 0.0)),
                total_orders=float(metrics.get("total_orders", 0.0)),
            )
        )
    rows.sort(key=lambda row: row.score, reverse=True)
    return plan, rows


def unique_rows(rows: list[CandidateRow]) -> list[CandidateRow]:
    seen = set()
    selected = []
    for row in rows:
        if row.structure in seen:
            continue
        seen.add(row.structure)
        selected.append(row)
    return selected


def render_summary_table(rows: list[CandidateRow], top_n: int | None = None) -> str:
    selected = rows if top_n is None else rows[:top_n]
    lines = [
        "| Candidate | Window | Structure | Bucket | Role | Score | Return % | Sharpe | Drawdown % | Trades | Orders |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in selected:
        lines.append(
            f"| {row.candidate_id} | {row.window} | {row.structure} | {row.bucket} | {row.role or '-'} | "
            f"{row.score:.3f} | {row.net_profit_pct:.3f} | {row.sharpe_ratio:.3f} | "
            f"{row.max_drawdown_pct:.3f} | {row.trade_count:.0f} | {row.total_orders:.0f} |"
        )
    return "\n".join(lines)


def render_stability_table(rows: list[CandidateRow]) -> str:
    grouped: dict[str, list[CandidateRow]] = {}
    for row in rows:
        grouped.setdefault(row.structure, []).append(row)

    ranked = sorted(
        grouped.items(),
        key=lambda item: (
            statistics.mean(row.score for row in item[1]),
            statistics.median(row.net_profit_pct for row in item[1]),
        ),
        reverse=True,
    )

    lines = [
        "| Structure | Windows | Avg Score | Median Score | Min Score | Max Score | Avg Return % | Avg Drawdown % | Best Window | Worst Window |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for structure, structure_rows in ranked:
        best_row = max(structure_rows, key=lambda row: row.score)
        worst_row = min(structure_rows, key=lambda row: row.score)
        lines.append(
            f"| {structure} | {len(structure_rows)} | "
            f"{statistics.mean(row.score for row in structure_rows):.3f} | "
            f"{statistics.median(row.score for row in structure_rows):.3f} | "
            f"{min(row.score for row in structure_rows):.3f} | "
            f"{max(row.score for row in structure_rows):.3f} | "
            f"{statistics.mean(row.net_profit_pct for row in structure_rows):.3f} | "
            f"{statistics.mean(row.max_drawdown_pct for row in structure_rows):.3f} | "
            f"{best_row.window} | {worst_row.window} |"
        )
    return "\n".join(lines)


def render_unique_structure_table(rows: list[CandidateRow], top_n: int | None = None) -> str:
    selected = unique_rows(rows)
    if top_n is not None:
        selected = selected[:top_n]
    lines = [
        "| Structure | Candidate | Bucket | Role | Score | Return % | Sharpe | Drawdown % | Trades |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in selected:
        lines.append(
            f"| {row.structure} | {row.candidate_id} | {row.bucket} | {row.role or '-'} | "
            f"{row.score:.3f} | {row.net_profit_pct:.3f} | {row.sharpe_ratio:.3f} | "
            f"{row.max_drawdown_pct:.3f} | {row.trade_count:.0f} |"
        )
    return "\n".join(lines)


def render_family_table(rows: list[CandidateRow]) -> str:
    grouped: dict[str, list[CandidateRow]] = {}
    for row in rows:
        grouped.setdefault(row.family, []).append(row)

    lines = [
        "| Family | Count | Avg Score | Median Score | Avg Return % | Avg Sharpe | Avg Drawdown % |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for family, family_rows in sorted(
        grouped.items(),
        key=lambda item: statistics.mean(row.score for row in item[1]),
        reverse=True,
    ):
        lines.append(
            f"| {family} | {len(family_rows)} | "
            f"{statistics.mean(row.score for row in family_rows):.3f} | "
            f"{statistics.median(row.score for row in family_rows):.3f} | "
            f"{statistics.mean(row.net_profit_pct for row in family_rows):.3f} | "
            f"{statistics.mean(row.sharpe_ratio for row in family_rows):.3f} | "
            f"{statistics.mean(row.max_drawdown_pct for row in family_rows):.3f} |"
        )
    return "\n".join(lines)


def render_bucket_table(rows: list[CandidateRow]) -> str:
    grouped: dict[str, list[CandidateRow]] = {}
    for row in rows:
        grouped.setdefault(row.bucket, []).append(row)

    lines = [
        "| Bucket | Count | Avg Score | Median Score | Avg Return % | Avg Sharpe | Avg Drawdown % | Best Structure |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for bucket, bucket_rows in sorted(
        grouped.items(),
        key=lambda item: statistics.mean(row.score for row in item[1]),
        reverse=True,
    ):
        best_row = max(bucket_rows, key=lambda row: row.score)
        lines.append(
            f"| {bucket} | {len(bucket_rows)} | "
            f"{statistics.mean(row.score for row in bucket_rows):.3f} | "
            f"{statistics.median(row.score for row in bucket_rows):.3f} | "
            f"{statistics.mean(row.net_profit_pct for row in bucket_rows):.3f} | "
            f"{statistics.mean(row.sharpe_ratio for row in bucket_rows):.3f} | "
            f"{statistics.mean(row.max_drawdown_pct for row in bucket_rows):.3f} | "
            f"{best_row.structure} |"
        )
    return "\n".join(lines)


def render_activation_table(rows: list[CandidateRow]) -> str:
    grouped: dict[str, list[CandidateRow]] = {}
    for row in rows:
        grouped.setdefault(row.family, []).append(row)

    lines = [
        "| Family | Count | Active Count | Activation Rate | Avg Return % (Active) | Best Active Structure |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for family, family_rows in sorted(grouped.items(), key=lambda item: item[0]):
        active_rows = [
            row for row in family_rows
            if row.trade_count > 0 or row.total_orders > 1
        ]
        activation_rate = (len(active_rows) / len(family_rows)) if family_rows else 0.0
        avg_active_return = (
            statistics.mean(row.net_profit_pct for row in active_rows)
            if active_rows else 0.0
        )
        best_active = (
            max(active_rows, key=lambda row: row.net_profit_pct).structure
            if active_rows else "-"
        )
        lines.append(
            f"| {family} | {len(family_rows)} | {len(active_rows)} | "
            f"{activation_rate * 100:.1f}% | {avg_active_return:.3f} | {best_active} |"
        )
    return "\n".join(lines)


def render_intraday_quality_table(rows: list[CandidateRow], top_n: int | None = None) -> str:
    intraday_rows = [
        row for row in rows
        if row.bucket in {"intraday_single", "intraday_scanner"} and row.trade_count > 0
    ]
    intraday_rows.sort(
        key=lambda row: (
            row.net_profit_pct / max(row.max_drawdown_pct, 0.1),
            row.net_profit_pct,
            -row.max_drawdown_pct,
        ),
        reverse=True,
    )
    if top_n is not None:
        intraday_rows = intraday_rows[:top_n]

    lines = [
        "| Structure | Candidate | Bucket | Return % | Drawdown % | Return/Drawdown | Trades |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in intraday_rows:
        ratio = row.net_profit_pct / max(row.max_drawdown_pct, 0.1)
        lines.append(
            f"| {row.structure} | {row.candidate_id} | {row.bucket} | "
            f"{row.net_profit_pct:.3f} | {row.max_drawdown_pct:.3f} | "
            f"{ratio:.3f} | {row.trade_count:.0f} |"
        )
    return "\n".join(lines)


def render_benchmark_table(rows: list[CandidateRow], benchmark_candidate_id: str, top_n: int | None = None) -> str:
    benchmark = next(row for row in rows if row.candidate_id == benchmark_candidate_id)
    selected = unique_rows(rows)
    if top_n is not None:
        selected = selected[:top_n]
    lines = [
        "| Structure | Candidate | Score Delta | Excess Return % | Sharpe Delta | Drawdown Delta % |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in selected:
        lines.append(
            f"| {row.structure} | {row.candidate_id} | "
            f"{row.score - benchmark.score:.3f} | "
            f"{row.net_profit_pct - benchmark.net_profit_pct:.3f} | "
            f"{row.sharpe_ratio - benchmark.sharpe_ratio:.3f} | "
            f"{row.max_drawdown_pct - benchmark.max_drawdown_pct:.3f} |"
        )
    return "\n".join(lines)


def _annual_returns(candidate_dir: Path) -> YearlySeries:
    result_files = [
        path for path in candidate_dir.glob("[0-9]*.json")
        if not path.name.endswith("-summary.json") and not path.name.endswith("-order-events.json")
    ]
    if not result_files:
        return YearlySeries(returns={}, latest_timestamp=None)
    packet = json.loads(result_files[0].read_text())
    chart = packet["charts"]["Strategy Equity"]["series"]["Equity"]["values"]

    by_year: dict[str, list[float]] = {}
    latest_timestamp = None
    for point in chart:
        ts = int(point[0])
        equity = float(point[1])
        timestamp = datetime.fromtimestamp(ts, tz=timezone.utc)
        latest_timestamp = timestamp
        year = timestamp.strftime("%Y")
        by_year.setdefault(year, [equity, equity])
        by_year[year][1] = equity

    returns = {}
    for year, (first_eq, last_eq) in by_year.items():
        if first_eq == 0:
            continue
        returns[year] = (last_eq / first_eq) - 1.0
    return YearlySeries(returns=returns, latest_timestamp=latest_timestamp)


def render_yearly_table(iteration_dir: Path, rows: list[CandidateRow]) -> str:
    yearly_by_candidate: dict[str, YearlySeries] = {}
    year_set = set()
    latest_timestamps = []
    for row in rows:
        series = _annual_returns(iteration_dir / row.candidate_id / "backtest")
        yearly_by_candidate[row.candidate_id] = series
        year_set.update(series.returns.keys())
        if series.latest_timestamp is not None:
            latest_timestamps.append(series.latest_timestamp)

    years = sorted(year_set)
    latest_timestamp = max(latest_timestamps) if latest_timestamps else None
    year_labels = list(years)
    if latest_timestamp is not None and year_labels:
        latest_year = latest_timestamp.strftime("%Y")
        if latest_timestamp.month != 12 or latest_timestamp.day != 31:
            year_labels = [
                f"{year} YTD" if year == latest_year else year
                for year in year_labels
            ]

    header = "| Candidate | " + " | ".join(year_labels) + " |"
    divider = "| --- | " + " | ".join("---:" for _ in year_labels) + " |"
    lines = [header, divider]
    for row in rows:
        series = yearly_by_candidate[row.candidate_id]
        cells = [
            f"{series.returns.get(year, 0.0) * 100:.2f}%"
            if year in series.returns else "-"
            for year in years
        ]
        lines.append(f"| {row.structure} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render markdown tables for a research iteration.")
    parser.add_argument("--iteration-dir", required=True, help="Path to an iteration directory.")
    parser.add_argument("--benchmark-candidate", required=True, help="Candidate id to use as the benchmark row.")
    parser.add_argument("--top-n", type=int, default=5, help="How many rows to include in summary tables.")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir)
    _, rows = load_results(iteration_dir)
    top_unique_rows = unique_rows(rows)[:args.top_n]

    print("## Summary Table")
    print()
    print(render_summary_table(rows, top_n=args.top_n))
    print()
    print("## Unique Structure Table")
    print()
    print(render_unique_structure_table(rows, top_n=args.top_n))
    print()
    print("## Family Table")
    print()
    print(render_family_table(rows))
    print()
    print("## Risk Bucket Table")
    print()
    print(render_bucket_table(rows))
    print()
    print("## Activation Table")
    print()
    print(render_activation_table(rows))
    print()
    print("## Intraday Quality Table")
    print()
    print(render_intraday_quality_table(rows, top_n=args.top_n))
    print()
    print("## Stability Table")
    print()
    print(render_stability_table(rows))
    print()
    print("## Benchmark Table")
    print()
    print(render_benchmark_table(rows, args.benchmark_candidate, top_n=args.top_n))
    print()
    print("## Yearly Return Table")
    print()
    print(render_yearly_table(iteration_dir, top_unique_rows))


if __name__ == "__main__":
    main()
