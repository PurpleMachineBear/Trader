#!/usr/bin/env python3
"""
After-tax return analysis for QQQ/VOO Rotation vs Pure VOO B&H.

Short-term capital gain : held < 365 days  → taxed as ordinary income
Long-term  capital gain : held >= 365 days → preferential rate (0/15/20%)

Usage:
  python tax_analysis.py [--st-rate 0.32] [--lt-rate 0.15]
"""

import json
import argparse
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────────

def ts_to_dt(ts: float) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def holding_days(buy_dt: datetime, sell_dt: datetime) -> int:
    return (sell_dt - buy_dt).days


# ── FIFO lot tracker ──────────────────────────────────────────────────────────

class FIFOTracker:
    def __init__(self):
        # symbol → list of [buy_dt, price, qty_remaining]
        self.lots: dict[str, list] = defaultdict(list)
        self.realized: list[dict]  = []   # realized trade records

    def buy(self, symbol: str, dt: datetime, price: float, qty: float):
        self.lots[symbol].append([dt, price, qty])

    def sell(self, symbol: str, dt: datetime, price: float, qty: float):
        qty_to_sell = abs(qty)
        symbol_lots = self.lots[symbol]

        while qty_to_sell > 1e-9 and symbol_lots:
            lot = symbol_lots[0]
            buy_dt, buy_price, lot_qty = lot

            matched = min(qty_to_sell, lot_qty)
            days    = holding_days(buy_dt, dt)
            gain    = (price - buy_price) * matched
            term    = "long" if days >= 365 else "short"

            self.realized.append({
                "symbol":    symbol,
                "buy_date":  buy_dt.date(),
                "sell_date": dt.date(),
                "days":      days,
                "term":      term,
                "qty":       matched,
                "buy_price": buy_price,
                "sell_price": price,
                "gain":      gain,
            })

            qty_to_sell -= matched
            lot[2]      -= matched
            if lot[2] < 1e-9:
                symbol_lots.pop(0)

    def unrealized_value(self, prices: dict[str, float]) -> float:
        total = 0.0
        for sym, lots in self.lots.items():
            if sym in prices:
                total += sum(l[2] * prices[sym] for l in lots)
        return total

    def unrealized_gains(self, prices: dict[str, float],
                         sell_date: datetime) -> tuple[float, float]:
        """Returns (short_gain, long_gain) for all remaining lots if sold now."""
        st, lt = 0.0, 0.0
        for sym, lots in self.lots.items():
            if sym not in prices:
                continue
            for buy_dt, buy_price, qty in lots:
                days = holding_days(buy_dt, sell_date)
                gain = (prices[sym] - buy_price) * qty
                if days >= 365:
                    lt += gain
                else:
                    st += gain
        return st, lt

    def summary(self):
        st_gains = sum(r["gain"] for r in self.realized if r["term"] == "short")
        lt_gains = sum(r["gain"] for r in self.realized if r["term"] == "long")
        st_loss  = sum(r["gain"] for r in self.realized if r["term"] == "short" and r["gain"] < 0)
        lt_loss  = sum(r["gain"] for r in self.realized if r["term"] == "long"  and r["gain"] < 0)
        return {
            "short_gains": st_gains,
            "long_gains":  lt_gains,
            "short_losses": st_loss,
            "long_losses":  lt_loss,
            "trades": len(self.realized),
        }


# ── main ──────────────────────────────────────────────────────────────────────

def analyze(backtest_dir: Path, st_rate: float, lt_rate: float):
    # ── load order events ────────────────────────────────────────────────────
    order_file = next(backtest_dir.glob("*-order-events.json"))
    events = json.loads(order_file.read_text())
    filled = sorted(
        [e for e in events if e["status"] == "filled"],
        key=lambda e: e["time"]
    )

    # ── load final prices from main result JSON ──────────────────────────────
    result_file = next(
        f for f in backtest_dir.glob("*.json")
        if "summary" not in f.name and "order" not in f.name
           and "monitor" not in f.name
    )
    result = json.loads(result_file.read_text())
    stats  = result.get("statistics", {})
    end_equity = float(stats.get("End Equity", 0) or
                       result.get("runtimeStatistics", {}).get("Equity", 100000))

    # ── replay trades through FIFO ───────────────────────────────────────────
    tracker = FIFOTracker()
    start_cash = 100_000.0
    fees = 0.0

    for e in filled:
        sym  = e["symbolValue"]
        dt   = ts_to_dt(e["time"])
        qty  = e["fillQuantity"]
        px   = e["fillPrice"]
        fee  = e.get("orderFeeAmount", 0) or 0
        fees += fee

        if qty > 0:
            tracker.buy(sym, dt, px, qty)
        else:
            tracker.sell(sym, dt, px, qty)

    # ── get last fill prices for unrealized calc ─────────────────────────────
    last_prices: dict[str, float] = {}
    for e in reversed(filled):
        sym = e["symbolValue"]
        if sym not in last_prices and e["fillPrice"] > 0:
            last_prices[sym] = e["fillPrice"]

    end_dt = ts_to_dt(filled[-1]["time"])

    # Unrealized gains on any residual open positions
    unreal_st, unreal_lt = tracker.unrealized_gains(last_prices, end_dt)

    summ = tracker.summary()

    # ── tax calculation for ROTATION strategy ────────────────────────────────
    # Realized
    real_st_tax = max(0, summ["short_gains"]) * st_rate
    real_lt_tax = max(0, summ["long_gains"])  * lt_rate
    # Unrealized (treated as sold at end date)
    unreal_st_tax = max(0, unreal_st) * st_rate
    unreal_lt_tax = max(0, unreal_lt) * lt_rate

    total_tax_rotation = real_st_tax + real_lt_tax + unreal_st_tax + unreal_lt_tax
    gross_gain_rotation = end_equity - start_cash
    after_tax_rotation  = gross_gain_rotation - total_tax_rotation

    # ── VOO B&H comparison ───────────────────────────────────────────────────
    # VOO B&H: buy on backtest start date, hold to end
    # Return: use the value logged by the algorithm (+12.73% for this run)
    # For a general solution, read it from the summary statistics.
    summary_file = next(backtest_dir.glob("*-summary.json"))
    summary = json.loads(summary_file.read_text())

    # Algorithm logged the VOO B&H return in the last log line
    log_file = next(backtest_dir.glob("*-log.txt"))
    log_text = log_file.read_text()
    import re
    m = re.search(r"Pure VOO B&H\s*:\s*\$[\d,]+\s*\(([+-][\d.]+)%\)", log_text)
    voo_pct   = float(m.group(1)) / 100 if m else 0.1273
    voo_gross = start_cash * voo_pct

    # Holding period: backtest start → backtest end
    # VOO B&H investor buys on day 1 and holds throughout
    backtest_start = datetime(2025, 1, 2, tzinfo=timezone.utc)
    voo_end        = ts_to_dt(filled[-1]["time"])
    voo_days       = holding_days(backtest_start, voo_end)
    voo_term       = "long" if voo_days >= 365 else "short"
    voo_rate       = lt_rate if voo_term == "long" else st_rate
    voo_tax        = max(0, voo_gross) * voo_rate
    after_tax_voo  = voo_gross - voo_tax

    # ── print report ─────────────────────────────────────────────────────────
    W = 58
    print("=" * W)
    print("  AFTER-TAX ANALYSIS  (2025-01-02 – 2026-03-04)")
    print(f"  Tax rates: Short-term {st_rate:.0%}  |  Long-term {lt_rate:.0%}")
    print("=" * W)

    print("\n── ROTATION STRATEGY ────────────────────────────────")
    print(f"  Gross gain              : ${gross_gain_rotation:>10,.2f}")
    print(f"  Realized short-term gain: ${summ['short_gains']:>10,.2f}  → tax ${real_st_tax:,.2f}")
    print(f"  Realized long-term  gain: ${summ['long_gains']:>10,.2f}  → tax ${real_lt_tax:,.2f}")
    print(f"  Unrealized ST gain      : ${unreal_st:>10,.2f}  → tax ${unreal_st_tax:,.2f}")
    print(f"  Unrealized LT gain      : ${unreal_lt:>10,.2f}  → tax ${unreal_lt_tax:,.2f}")
    print(f"  Total tax               : ${total_tax_rotation:>10,.2f}")
    print(f"  ── After-tax gain       : ${after_tax_rotation:>10,.2f}  "
          f"({after_tax_rotation/start_cash:+.2%})")
    print(f"  Trades: {summ['trades']}  |  Fees: ${fees:.2f}")

    print("\n── PURE VOO B&H ─────────────────────────────────────")
    print(f"  Holding period          : {voo_days} days → {voo_term.upper()}-TERM")
    print(f"  Gross gain              : ${voo_gross:>10,.2f}")
    print(f"  Tax ({voo_rate:.0%})              : ${voo_tax:>10,.2f}")
    print(f"  ── After-tax gain       : ${after_tax_voo:>10,.2f}  "
          f"({after_tax_voo/start_cash:+.2%})")
    print(f"  Trades: 1  |  Fees: $1.00")

    print("\n── COMPARISON ───────────────────────────────────────")
    alpha_gross   = gross_gain_rotation - voo_gross
    alpha_aftertax = after_tax_rotation - after_tax_voo
    print(f"  Gross alpha             : ${alpha_gross:>+10,.2f}  ({alpha_gross/start_cash:+.2%})")
    print(f"  After-tax alpha         : ${alpha_aftertax:>+10,.2f}  ({alpha_aftertax/start_cash:+.2%})")
    flip = alpha_gross > 0 and alpha_aftertax < 0
    print(f"  Tax drag flips winner?  : {'⚠ YES' if flip else 'No'}")
    print("=" * W)

    print("\n── TAX SENSITIVITY ──────────────────────────────────")
    print(f"  {'ST rate':>7}  {'LT rate':>7}  {'Rotation AT':>12}  {'VOO AT':>10}  {'Alpha':>8}")
    print(f"  {'-'*7}  {'-'*7}  {'-'*12}  {'-'*10}  {'-'*8}")
    for st in [0.22, 0.32, 0.37]:
        for lt in [0.15, 0.20]:
            r_tax = (max(0, summ["short_gains"]) + max(0, unreal_st)) * st + \
                    (max(0, summ["long_gains"])  + max(0, unreal_lt)) * lt
            v_tax = max(0, voo_gross) * (lt if voo_term == "long" else st)
            r_at  = gross_gain_rotation - r_tax
            v_at  = voo_gross - v_tax
            print(f"  {st:>7.0%}  {lt:>7.0%}  {r_at:>+12,.0f}  {v_at:>+10,.0f}  {r_at-v_at:>+8,.0f}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--st-rate", type=float, default=0.32,
                        help="Short-term capital gains rate (default 0.32)")
    parser.add_argument("--lt-rate", type=float, default=0.15,
                        help="Long-term capital gains rate (default 0.15)")
    parser.add_argument("--backtest-dir", type=str, default=None,
                        help="Path to backtest result directory (default: latest)")
    args = parser.parse_args()

    base = Path("QQQ_VOO_Rotation/backtests")
    if args.backtest_dir:
        backtest_dir = Path(args.backtest_dir)
    else:
        backtest_dir = sorted(base.iterdir())[-1]

    print(f"Analyzing: {backtest_dir}\n")
    analyze(backtest_dir, args.st_rate, args.lt_rate)
