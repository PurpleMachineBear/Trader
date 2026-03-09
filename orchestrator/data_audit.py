#!/usr/bin/env python3
"""
Local data integrity audit for LEAN research symbols.

Checks:
- daily zip existence and first/last dates
- factor file existence and first date
- whether factor start is later than the daily start
- minute directory existence and first/last dates where requested
"""

from __future__ import annotations

import argparse
import json
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "equity" / "usa"


@dataclass
class DailyAudit:
    symbol: str
    daily_exists: bool
    daily_first: str | None
    daily_last: str | None
    daily_count: int
    max_gap_days: int
    factor_exists: bool
    factor_first: str | None
    factor_mismatch: bool
    large_gap: bool


@dataclass
class MinuteAudit:
    symbol: str
    minute_exists: bool
    minute_first: str | None
    minute_last: str | None
    minute_count: int


def _read_daily(symbol: str) -> tuple[bool, str | None, str | None, int, int]:
    path = DATA_DIR / "daily" / f"{symbol.lower()}.zip"
    if not path.exists():
        return False, None, None, 0, 0
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        if not names:
            return True, None, None, 0, 0
        lines = zf.read(names[0]).decode("utf-8").splitlines()
    if not lines:
        return True, None, None, 0, 0
    dates = [line.split(",", 1)[0].split()[0] for line in lines]
    max_gap_days = 0
    parsed = [datetime.strptime(value[:8], "%Y%m%d").date() for value in dates]
    for previous, current in zip(parsed, parsed[1:]):
        max_gap_days = max(max_gap_days, (current - previous).days)
    return True, dates[0], dates[-1], len(lines), max_gap_days


def _read_factor(symbol: str) -> tuple[bool, str | None]:
    path = DATA_DIR / "factor_files" / f"{symbol.lower()}.csv"
    if not path.exists():
        return False, None
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    if not lines:
        return True, None
    return True, lines[0].split(",", 1)[0]


def _read_minute(symbol: str) -> tuple[bool, str | None, str | None, int]:
    folder = DATA_DIR / "minute" / symbol.lower()
    if not folder.exists():
        return False, None, None, 0
    files = sorted(path.name for path in folder.glob("*_trade.zip"))
    if not files:
        return True, None, None, 0
    return True, files[0][:8], files[-1][:8], len(files)


def audit_symbols(symbols: list[str], check_minute: bool) -> tuple[list[DailyAudit], list[MinuteAudit]]:
    daily_rows: list[DailyAudit] = []
    minute_rows: list[MinuteAudit] = []
    for symbol in symbols:
        daily_exists, daily_first, daily_last, daily_count, max_gap_days = _read_daily(symbol)
        factor_exists, factor_first = _read_factor(symbol)
        factor_mismatch = False
        large_gap = max_gap_days > 10
        if daily_exists and daily_first and factor_exists and factor_first:
            expected = (
                datetime.strptime(daily_first[:8], "%Y%m%d").date() - timedelta(days=1)
            ).strftime("%Y%m%d")
            factor_mismatch = factor_first[:8] > expected
        daily_rows.append(
            DailyAudit(
                symbol=symbol,
                daily_exists=daily_exists,
                daily_first=daily_first,
                daily_last=daily_last,
                daily_count=daily_count,
                max_gap_days=max_gap_days,
                factor_exists=factor_exists,
                factor_first=factor_first,
                factor_mismatch=factor_mismatch,
                large_gap=large_gap,
            )
        )

        if check_minute:
            minute_exists, minute_first, minute_last, minute_count = _read_minute(symbol)
            minute_rows.append(
                MinuteAudit(
                    symbol=symbol,
                    minute_exists=minute_exists,
                    minute_first=minute_first,
                    minute_last=minute_last,
                    minute_count=minute_count,
                )
            )
    return daily_rows, minute_rows


def render_markdown(
    daily_rows: list[DailyAudit],
    minute_rows: list[MinuteAudit],
    *,
    title: str,
) -> str:
    lines = [f"# {title}", ""]
    lines.append("## Daily Coverage")
    lines.append("")
    lines.append("| Symbol | Daily First | Daily Last | Bars | Max Gap (days) | Factor First | Status |")
    lines.append("| --- | --- | --- | ---: | ---: | --- | --- |")
    for row in daily_rows:
        status = "OK"
        if not row.daily_exists:
            status = "missing_daily"
        elif not row.factor_exists:
            status = "missing_factor"
        elif row.factor_mismatch:
            status = "factor_after_daily_start"
        elif row.large_gap:
            status = "large_internal_gap"
        lines.append(
            f"| {row.symbol} | {row.daily_first or '-'} | {row.daily_last or '-'} | "
            f"{row.daily_count} | {row.max_gap_days} | {row.factor_first or '-'} | {status} |"
        )

    if minute_rows:
        lines.append("")
        lines.append("## Minute Coverage")
        lines.append("")
        lines.append("| Symbol | Minute First | Minute Last | Files | Status |")
        lines.append("| --- | --- | --- | ---: | --- |")
        for row in minute_rows:
            status = "OK" if row.minute_exists and row.minute_count > 0 else "missing_minute"
            lines.append(
                f"| {row.symbol} | {row.minute_first or '-'} | {row.minute_last or '-'} | "
                f"{row.minute_count} | {status} |"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit local LEAN data coverage for research symbols.")
    parser.add_argument("--symbols", nargs="+", required=True, help="Ticker symbols to audit.")
    parser.add_argument("--check-minute", action="store_true", help="Also inspect minute coverage.")
    parser.add_argument("--markdown-out", help="Optional markdown report output path.")
    parser.add_argument("--json-out", help="Optional JSON report output path.")
    parser.add_argument("--title", default="Data Integrity Audit", help="Markdown report title.")
    args = parser.parse_args()

    symbols = [symbol.upper() for symbol in args.symbols]
    daily_rows, minute_rows = audit_symbols(symbols, check_minute=args.check_minute)

    payload = {
        "daily": [row.__dict__ for row in daily_rows],
        "minute": [row.__dict__ for row in minute_rows],
    }

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, indent=2) + "\n")
    markdown = render_markdown(daily_rows, minute_rows, title=args.title)
    if args.markdown_out:
        Path(args.markdown_out).write_text(markdown)
    else:
        print(markdown, end="")


if __name__ == "__main__":
    main()
