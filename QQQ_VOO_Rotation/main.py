# region imports
from AlgorithmImports import *
# endregion


class QQQVOORotation(QCAlgorithm):
    """
    Rotation strategy: QQQ ↔ VOO based on RSI(14) of QQQ.

    Signal logic (uses QQQ RSI as market temperature):
      RSI > HIGH_RSI  → "overbought / high point"  → 100% VOO  (defensive)
      RSI < LOW_RSI   → "oversold  / low point"    → 100% QQQ  (aggressive)
      Otherwise       → 50/50 neutral               → rebalance to equal weight

    Benchmark: pure VOO buy-and-hold tracked on a separate chart.
    """

    HIGH_RSI = 65   # overbought threshold
    LOW_RSI  = 40   # oversold  threshold

    def initialize(self):
        self.set_start_date(2025, 1, 2)
        self.set_end_date(2026, 3, 4)
        self.set_cash(100_000)

        self.qqq = self.add_equity("QQQ", Resolution.DAILY).symbol
        self.voo = self.add_equity("VOO", Resolution.DAILY).symbol

        # RSI on QQQ as the "temperature" signal
        # Use a distinct name to avoid shadowing QCAlgorithm.rsi() method
        self._rsi = self.rsi(self.qqq, 14, MovingAverageType.WILDERS, Resolution.DAILY)

        # Warmup: need at least 14 bars before backtest start
        self.set_warm_up(20, Resolution.DAILY)

        # Track current regime to log only on change
        self._regime = "neutral"   # "qqq" | "voo" | "neutral"

        # ── Charts ──────────────────────────────────────────────────────
        ret_chart = Chart("Returns (%)")
        ret_chart.add_series(Series("Rotation", SeriesType.LINE, 0, "%"))
        ret_chart.add_series(Series("Pure VOO", SeriesType.LINE, 0, "%"))
        self.add_chart(ret_chart)

        rsi_chart = Chart("QQQ RSI")
        rsi_chart.add_series(Series("RSI",            SeriesType.LINE, 0))
        rsi_chart.add_series(Series("High threshold", SeriesType.LINE, 0))
        rsi_chart.add_series(Series("Low threshold",  SeriesType.LINE, 0))
        self.add_chart(rsi_chart)

        # Benchmark tracking
        self._voo_entry  = None
        self._cash_start = 100_000.0

    # ------------------------------------------------------------------
    def on_data(self, data: Slice):
        if self.is_warming_up:
            return
        if not self._rsi.is_ready:
            return
        if self.qqq not in data.bars or self.voo not in data.bars:
            return

        voo_price = data.bars[self.voo].close
        rsi_val   = self._rsi.current.value

        # Capture VOO entry price on first real bar
        if self._voo_entry is None:
            self._voo_entry = voo_price

        # ── Regime decision ──────────────────────────────────────────
        if rsi_val > self.HIGH_RSI:
            target_regime = "voo"
        elif rsi_val < self.LOW_RSI:
            target_regime = "qqq"
        else:
            target_regime = "neutral"

        if target_regime != self._regime:
            self._regime = target_regime
            if target_regime == "voo":
                self.set_holdings(self.qqq, 0.0)
                self.set_holdings(self.voo, 1.0)
                self.log(f"HIGH POINT → 100% VOO | RSI={rsi_val:.1f} | "
                         f"QQQ={data.bars[self.qqq].close:.2f} VOO={voo_price:.2f}")
            elif target_regime == "qqq":
                self.set_holdings(self.voo, 0.0)
                self.set_holdings(self.qqq, 1.0)
                self.log(f"LOW  POINT → 100% QQQ | RSI={rsi_val:.1f} | "
                         f"QQQ={data.bars[self.qqq].close:.2f} VOO={voo_price:.2f}")
            else:
                self.set_holdings(self.qqq, 0.5)
                self.set_holdings(self.voo, 0.5)
                self.log(f"NEUTRAL    → 50/50     | RSI={rsi_val:.1f} | "
                         f"QQQ={data.bars[self.qqq].close:.2f} VOO={voo_price:.2f}")

        # ── Plot returns ─────────────────────────────────────────────
        rotation_ret = (self.portfolio.total_portfolio_value / self._cash_start - 1) * 100
        voo_ret      = (voo_price / self._voo_entry - 1) * 100
        self.plot("Returns (%)", "Rotation", rotation_ret)
        self.plot("Returns (%)", "Pure VOO", voo_ret)
        self.plot("QQQ RSI", "RSI",            rsi_val)
        self.plot("QQQ RSI", "High threshold", self.HIGH_RSI)
        self.plot("QQQ RSI", "Low threshold",  self.LOW_RSI)

    # ------------------------------------------------------------------
    def on_end_of_algorithm(self):
        voo_price = self.securities[self.voo].price
        voo_ret   = (voo_price / self._voo_entry - 1) * 100 if self._voo_entry else 0

        rotation_val = self.portfolio.total_portfolio_value
        rotation_ret = (rotation_val / self._cash_start - 1) * 100

        self.log("=" * 50)
        self.log(f"  Rotation strategy : ${rotation_val:,.0f}  ({rotation_ret:+.2f}%)")
        self.log(f"  Pure VOO B&H      : ${100_000 * (1 + voo_ret/100):,.0f}  ({voo_ret:+.2f}%)")
        self.log(f"  Alpha vs VOO      : {rotation_ret - voo_ret:+.2f}%")
        self.log("=" * 50)
