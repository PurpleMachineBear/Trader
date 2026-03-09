#!/usr/bin/env python3
"""
Build a simple premarket watchlist from Polygon minute bars and news.

This is intentionally lightweight:
- Computes premarket gap and dollar volume from 1-minute bars
- Pulls recent headlines for each ticker
- Outputs a ranked Markdown watchlist for human review or future automation
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests


POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY", "")
NY_TZ = ZoneInfo("America/New_York")
PREMARKET_START = time(4, 0)
REGULAR_OPEN = time(9, 30)


@dataclass
class PremarketSummary:
    ticker: str
    prev_close: float
    premarket_last: float
    gap_pct: float
    premarket_high: float
    premarket_low: float
    premarket_volume: float
    premarket_dollar_volume: float
    rank_score: float
    news_items: list[dict]


def _require_key() -> str:
    if not POLYGON_API_KEY:
        raise EnvironmentError("POLYGON_API_KEY environment variable is not set")
    return POLYGON_API_KEY


def _polygon_get(url: str, *, params: dict | None = None) -> dict:
    key = _require_key()
    merged = dict(params or {})
    merged["apiKey"] = key
    response = requests.get(url, params=merged, timeout=30)
    response.raise_for_status()
    payload = response.json()
    status = payload.get("status", "")
    if status not in ("OK", "DELAYED"):
        raise ValueError(f"Polygon API error for {url}: {json.dumps(payload)[:500]}")
    return payload


def fetch_snapshot_batch(tickers: list[str]) -> dict[str, dict]:
    payload = _polygon_get(
        "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers",
        params={"tickers": ",".join(sorted(set(tickers)))},
    )
    return {
        item["ticker"].upper(): item
        for item in payload.get("tickers", [])
        if item.get("ticker")
    }


def fetch_minute_bars_for_date(ticker: str, target_date: date) -> list[dict]:
    payload = _polygon_get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/minute/{target_date.isoformat()}/{target_date.isoformat()}",
        params={
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
        },
    )
    return payload.get("results", [])


def fetch_news(ticker: str, *, limit: int, since: datetime) -> list[dict]:
    payload = _polygon_get(
        "https://api.polygon.io/v2/reference/news",
        params={
            "ticker": ticker.upper(),
            "limit": limit,
            "published_utc.gte": since.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "sort": "published_utc",
            "order": "desc",
        },
    )
    return payload.get("results", [])


def summarize_ticker(ticker: str, target_date: date, snapshot: dict, news_limit: int) -> PremarketSummary | None:
    prev_close = float(snapshot.get("prevDay", {}).get("c") or 0.0)
    if prev_close <= 0:
        return None

    bars = fetch_minute_bars_for_date(ticker, target_date)
    premarket_bars = []
    for bar in bars:
        dt_local = datetime.fromtimestamp(bar["t"] / 1000, tz=timezone.utc).astimezone(NY_TZ)
        if PREMARKET_START <= dt_local.time() < REGULAR_OPEN:
            premarket_bars.append(bar)

    if not premarket_bars:
        return None

    premarket_last = float(premarket_bars[-1]["c"])
    premarket_high = max(float(bar["h"]) for bar in premarket_bars)
    premarket_low = min(float(bar["l"]) for bar in premarket_bars)
    premarket_volume = sum(float(bar["v"]) for bar in premarket_bars)
    premarket_dollar_volume = sum(float(bar["c"]) * float(bar["v"]) for bar in premarket_bars)
    gap_pct = (premarket_last / prev_close) - 1.0
    rank_score = abs(gap_pct) * premarket_dollar_volume
    news_items = fetch_news(
        ticker,
        limit=news_limit,
        since=datetime.combine(target_date - timedelta(days=2), time(0, 0), tzinfo=NY_TZ),
    )

    return PremarketSummary(
        ticker=ticker.upper(),
        prev_close=prev_close,
        premarket_last=premarket_last,
        gap_pct=gap_pct,
        premarket_high=premarket_high,
        premarket_low=premarket_low,
        premarket_volume=premarket_volume,
        premarket_dollar_volume=premarket_dollar_volume,
        rank_score=rank_score,
        news_items=news_items,
    )


def render_markdown(target_date: date, summaries: list[PremarketSummary]) -> str:
    lines = [
        f"# Premarket Watchlist {target_date.isoformat()}",
        "",
        f"Generated from Polygon minute bars and recent news at `{datetime.now(NY_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}`.",
        "",
        "## Ranked Table",
        "",
        "| Rank | Ticker | Gap % | Premarket $Vol | Premarket Vol | Premarket Range | Rank Score |",
        "| ---: | --- | ---: | ---: | ---: | --- | ---: |",
    ]

    for idx, summary in enumerate(sorted(summaries, key=lambda item: item.rank_score, reverse=True), start=1):
        lines.append(
            "| "
            f"{idx} | {summary.ticker} | {summary.gap_pct * 100:.2f}% | "
            f"${summary.premarket_dollar_volume:,.0f} | {summary.premarket_volume:,.0f} | "
            f"{summary.premarket_low:.2f} - {summary.premarket_high:.2f} | {summary.rank_score:,.0f} |"
        )

    for summary in sorted(summaries, key=lambda item: item.rank_score, reverse=True):
        lines.extend(
            [
                "",
                f"## {summary.ticker}",
                "",
                f"- Prev close: `{summary.prev_close:.2f}`",
                f"- Premarket last: `{summary.premarket_last:.2f}`",
                f"- Gap: `{summary.gap_pct * 100:.2f}%`",
                f"- Premarket high/low: `{summary.premarket_high:.2f}` / `{summary.premarket_low:.2f}`",
                f"- Premarket volume: `{summary.premarket_volume:,.0f}`",
                f"- Premarket dollar volume: `${summary.premarket_dollar_volume:,.0f}`",
            ]
        )
        if summary.news_items:
            lines.append("- Recent headlines:")
            for item in summary.news_items:
                published = item.get("published_utc", "")
                title = item.get("title", "Untitled")
                url = item.get("article_url", "")
                lines.append(f"  - `{published}` [{title}]({url})")
        else:
            lines.append("- Recent headlines: none found in the lookback window")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Polygon-backed premarket watchlist")
    parser.add_argument(
        "--tickers",
        required=True,
        help="Comma-separated ticker list, for example NVDA,AMD,MU,TSM,MRVL,AVGO",
    )
    parser.add_argument(
        "--date",
        default=datetime.now(NY_TZ).date().isoformat(),
        help="Market date in YYYY-MM-DD, default is today's New York date",
    )
    parser.add_argument(
        "--news-limit",
        type=int,
        default=2,
        help="Number of recent headlines to include per ticker",
    )
    parser.add_argument(
        "--output",
        help="Optional output Markdown path",
    )
    parser.add_argument(
        "--json-output",
        help="Optional output JSON path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = date.fromisoformat(args.date)
    tickers = [ticker.strip().upper() for ticker in args.tickers.split(",") if ticker.strip()]
    if not tickers:
        raise ValueError("At least one ticker is required")

    snapshots = fetch_snapshot_batch(tickers)
    summaries: list[PremarketSummary] = []
    missing = []
    for ticker in tickers:
        snapshot = snapshots.get(ticker)
        if snapshot is None:
            missing.append(ticker)
            continue
        summary = summarize_ticker(ticker, target_date, snapshot, args.news_limit)
        if summary is None:
            missing.append(ticker)
            continue
        summaries.append(summary)

    markdown = render_markdown(target_date, summaries)
    json_payload = {
        "date": target_date.isoformat(),
        "generated_at": datetime.now(NY_TZ).isoformat(),
        "tickers": [
            {
                "ticker": summary.ticker,
                "prev_close": summary.prev_close,
                "premarket_last": summary.premarket_last,
                "gap_pct": summary.gap_pct,
                "premarket_high": summary.premarket_high,
                "premarket_low": summary.premarket_low,
                "premarket_volume": summary.premarket_volume,
                "premarket_dollar_volume": summary.premarket_dollar_volume,
                "rank_score": summary.rank_score,
                "news": [
                    {
                        "published_utc": item.get("published_utc"),
                        "title": item.get("title"),
                        "article_url": item.get("article_url"),
                        "tickers": item.get("tickers", []),
                    }
                    for item in summary.news_items
                ],
            }
            for summary in sorted(summaries, key=lambda item: item.rank_score, reverse=True)
        ],
        "missing_or_inactive": missing,
    }
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown)
        print(f"wrote {output_path}")
    else:
        print(markdown)

    if args.json_output:
        json_path = Path(args.json_output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(json_payload, indent=2) + "\n")
        print(f"wrote {json_path}")

    if missing:
        print("missing_or_inactive:", ",".join(missing))


if __name__ == "__main__":
    main()
