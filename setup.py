#!/usr/bin/env python3
"""
Setup script for LEAN backtest environment.
1. Downloads market-hours and symbol-properties from LEAN GitHub
2. Downloads OHLCV data from Polygon and converts it to LEAN daily/minute equity format
"""

import os
import json
import zipfile
import requests
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY", "")


# ---------------------------------------------------------------------------
# Infrastructure files (market hours, symbol properties)
# ---------------------------------------------------------------------------

LEAN_RAW = "https://raw.githubusercontent.com/QuantConnect/Lean/master/Data"
INFRA_FILES = [
    "market-hours/market-hours-database.json",
    "symbol-properties/symbol-properties-database.csv",
    "alternative/interest-rate/usa/interest-rate.csv",
]


def download_lean_infrastructure(data_dir: Path) -> None:
    print("=== Downloading LEAN infrastructure files ===")
    for rel in INFRA_FILES:
        target = data_dir / rel
        if target.exists():
            print(f"  [skip] {rel}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"  Downloading {rel} ...", end=" ", flush=True)
        r = requests.get(f"{LEAN_RAW}/{rel}", timeout=30)
        r.raise_for_status()
        target.write_bytes(r.content)
        print("OK")


# ---------------------------------------------------------------------------
# Polygon → LEAN equity format
# ---------------------------------------------------------------------------

NY_TZ = ZoneInfo("America/New_York")


def fetch_polygon_bars(symbol: str, start: str, end: str, *, multiplier: int, timespan: str) -> list[dict]:
    """Fetch Polygon aggregate bars (handles pagination)."""
    if not POLYGON_API_KEY:
        raise EnvironmentError("POLYGON_API_KEY environment variable is not set")

    all_results = []
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/"
        f"{start}/{end}"
        f"?adjusted=true&sort=asc&limit=50000&apiKey={POLYGON_API_KEY}"
    )

    while url:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        payload = r.json()
        status = payload.get("status", "")
        if status not in ("OK", "DELAYED"):
            raise ValueError(f"Polygon API error: {payload}")
        all_results.extend(payload.get("results", []))
        url = payload.get("next_url")  # pagination
        if url:
            url += f"&apiKey={POLYGON_API_KEY}"

    return all_results


def _scaled_ohlcv_line(timestamp: str | int, open_price: float, high_price: float, low_price: float, close_price: float, volume: float) -> str:
    o = int(round(open_price * 10000))
    h = int(round(high_price * 10000))
    lo = int(round(low_price * 10000))
    c = int(round(close_price * 10000))
    v = int(volume)
    return f"{timestamp},{o},{h},{lo},{c},{v}"


def _read_zip_lines(zip_path: Path) -> list[str]:
    if not zip_path.exists():
        return []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        if not names:
            return []
        return zf.read(names[0]).decode("utf-8").splitlines()


def write_lean_daily_zip(symbol: str, bars: list[dict], data_dir: Path) -> Path:
    """
    Convert Polygon bars to LEAN's daily equity CSV format and write as ZIP.

    LEAN daily equity CSV (no header):
        yyyyMMdd 00:00,open*10000,high*10000,low*10000,close*10000,volume
    """
    lines_by_timestamp: dict[str, str] = {}
    sym_lower = symbol.lower()

    daily_dir = data_dir / "equity" / "usa" / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    zip_path = daily_dir / f"{sym_lower}.zip"

    for line in _read_zip_lines(zip_path):
        timestamp = line.split(",", 1)[0]
        lines_by_timestamp[timestamp] = line

    for bar in bars:
        dt = datetime.utcfromtimestamp(bar["t"] / 1000)
        date_str = dt.strftime("%Y%m%d 00:00")
        lines_by_timestamp[date_str] = _scaled_ohlcv_line(
            date_str,
            bar["o"],
            bar["h"],
            bar["l"],
            bar["c"],
            bar["v"],
        )

    csv_content = "\n".join(
        lines_by_timestamp[timestamp]
        for timestamp in sorted(lines_by_timestamp.keys())
    )
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{sym_lower}.csv", csv_content)
    return zip_path


def write_lean_minute_zip(symbol: str, bars: list[dict], data_dir: Path) -> list[Path]:
    """
    Convert Polygon minute bars to LEAN minute equity format.

    LEAN minute equity path:
        data/equity/usa/minute/{symbol}/{yyyyMMdd}_trade.zip
    Internal CSV name:
        {yyyyMMdd}_{symbol}_minute_trade.csv
    CSV rows:
        milliseconds_since_midnight,open*10000,high*10000,low*10000,close*10000,volume
    """
    sym_lower = symbol.lower()
    minute_dir = data_dir / "equity" / "usa" / "minute" / sym_lower
    minute_dir.mkdir(parents=True, exist_ok=True)

    grouped_lines: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for bar in bars:
        dt_utc = datetime.fromtimestamp(bar["t"] / 1000, tz=timezone.utc)
        dt_local = dt_utc.astimezone(NY_TZ)
        date_key = dt_local.strftime("%Y%m%d")
        milliseconds = (
            ((dt_local.hour * 60 + dt_local.minute) * 60 + dt_local.second) * 1000
            + (dt_local.microsecond // 1000)
        )
        grouped_lines[date_key].append(
            (
                milliseconds,
                _scaled_ohlcv_line(
                    milliseconds,
                    bar["o"],
                    bar["h"],
                    bar["l"],
                    bar["c"],
                    bar["v"],
                ),
            )
        )

    written_paths = []
    for date_key, rows in sorted(grouped_lines.items()):
        zip_path = minute_dir / f"{date_key}_trade.zip"
        entry_name = f"{date_key}_{sym_lower}_minute_trade.csv"
        rows_by_ms: dict[int, str] = {}
        for line in _read_zip_lines(zip_path):
            milliseconds_str = line.split(",", 1)[0]
            rows_by_ms[int(milliseconds_str)] = line
        for milliseconds, line in rows:
            rows_by_ms[milliseconds] = line
        csv_content = "\n".join(
            rows_by_ms[milliseconds]
            for milliseconds in sorted(rows_by_ms.keys())
        )
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(entry_name, csv_content)
        written_paths.append(zip_path)

    return written_paths


def write_map_file(symbol: str, data_dir: Path) -> Path:
    """
    Minimal map file telling LEAN the ticker has never changed.
    Format: yyyyMMdd,SYMBOL
    """
    map_dir = data_dir / "equity" / "usa" / "map_files"
    map_dir.mkdir(parents=True, exist_ok=True)
    path = map_dir / f"{symbol.lower()}.csv"
    path.write_text(f"19980101,{symbol.upper()}\n20500101,{symbol.upper()}\n")
    return path


def write_factor_file(symbol: str, first_timestamp_ms: int, first_close: float, data_dir: Path) -> Path:
    """
    Factor file: tells LEAN there are no splits/dividends.
    Polygon data is already adjusted, so we keep all factors at 1.

    Format (no header): yyyyMMdd,price_factor,split_factor,reference_price
    - First row: day before data starts, reference price = first close price
    - Terminal row: far-future sentinel
    The reference_price must be non-zero to avoid LEAN's precision-check warning.
    """
    factor_dir = data_dir / "equity" / "usa" / "factor_files"
    factor_dir.mkdir(parents=True, exist_ok=True)
    path = factor_dir / f"{symbol.lower()}.csv"

    first_dt = datetime.fromtimestamp(first_timestamp_ms / 1000, tz=timezone.utc)
    # One calendar day before first bar
    from datetime import timedelta
    start_date = (first_dt - timedelta(days=1)).strftime("%Y%m%d")

    # Never let a later minute backfill overwrite an earlier daily factor start.
    # The factor file only needs an earliest usable reference row plus the sentinel,
    # so keep the earliest known start if the file already exists.
    if path.exists():
        lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
        if lines:
            first_existing = lines[0].split(",")
            if len(first_existing) >= 4 and first_existing[0] < start_date:
                start_date = first_existing[0]
                try:
                    first_close = float(first_existing[3])
                except ValueError:
                    pass

    lines = [
        f"{start_date},1,1,{first_close:.4f}",
        f"20500101,1,1,{first_close:.4f}",
    ]
    path.write_text("\n".join(lines) + "\n")
    return path


def download_equity_daily(symbol: str, start: str, end: str, data_dir: Path) -> None:
    sym = symbol.upper()
    print(f"\n  [{sym}] Fetching from Polygon ({start} → {end}) ...", end=" ", flush=True)
    bars = fetch_polygon_bars(sym, start, end, multiplier=1, timespan="day")
    print(f"{len(bars)} bars")
    if not bars:
        raise ValueError("No bars returned from Polygon")

    zip_path = write_lean_daily_zip(sym, bars, data_dir)
    map_path = write_map_file(sym, data_dir)
    fac_path = write_factor_file(sym, bars[0]["t"], bars[0]["c"], data_dir)

    print(f"    data  -> {zip_path}")
    print(f"    map   -> {map_path}")
    print(f"    factor-> {fac_path}")


def download_equity_minute(symbol: str, start: str, end: str, data_dir: Path) -> None:
    sym = symbol.upper()
    print(f"\n  [{sym}] Fetching minute bars from Polygon ({start} → {end}) ...", end=" ", flush=True)
    bars = fetch_polygon_bars(sym, start, end, multiplier=1, timespan="minute")
    print(f"{len(bars)} bars")
    if not bars:
        raise ValueError("No minute bars returned from Polygon")

    zip_paths = write_lean_minute_zip(sym, bars, data_dir)
    map_path = write_map_file(sym, data_dir)
    fac_path = write_factor_file(sym, bars[0]["t"], bars[0]["c"], data_dir)

    print(f"    files -> {len(zip_paths)} daily minute archives")
    if zip_paths:
        print(f"    first -> {zip_paths[0]}")
        print(f"    last  -> {zip_paths[-1]}")
    print(f"    map   -> {map_path}")
    print(f"    factor-> {fac_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download LEAN infrastructure + Polygon market data"
    )
    parser.add_argument(
        "--symbols", nargs="+", default=["AAPL", "SPY"],
        help="Ticker symbols to download (default: AAPL SPY)"
    )
    parser.add_argument(
        "--start", default="2022-01-01",
        help="Start date YYYY-MM-DD (default: 2022-01-01)"
    )
    parser.add_argument(
        "--end", default="2024-12-31",
        help="End date YYYY-MM-DD (default: 2024-12-31)"
    )
    parser.add_argument(
        "--resolution",
        choices=["daily", "minute", "both"],
        default="daily",
        help="Which LEAN data resolution(s) to download (default: daily)",
    )
    args = parser.parse_args()

    data_dir = Path(__file__).parent / "data"

    download_lean_infrastructure(data_dir)

    print("\n=== Downloading market data from Polygon ===")
    for sym in args.symbols:
        try:
            if args.resolution in ("daily", "both"):
                download_equity_daily(sym, args.start, args.end, data_dir)
            if args.resolution in ("minute", "both"):
                download_equity_minute(sym, args.start, args.end, data_dir)
        except Exception as exc:
            print(f"    ERROR: {exc}")

    print("\n=== Setup complete ===")
    print("Next steps:")
    print("  1. Edit SMA_Crossover/main.py to adjust symbols/dates")
    print("  2. Run: lean backtest SMA_Crossover")
