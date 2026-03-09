# region imports
from AlgorithmImports import *
# endregion


class SmaCrossover(QCAlgorithm):
    """
    Simple SMA 50/200 golden-cross / death-cross strategy.
    - BUY  when fast SMA crosses above slow SMA
    - SELL when fast SMA crosses below slow SMA

    Data is sourced from Polygon (pre-adjusted OHLCV, stored locally).
    Run `python setup.py` first to download data.
    """

    def initialize(self):
        # ── Backtest period (must match the data you downloaded) ──────────
        self.set_start_date(2022, 1, 1)
        self.set_end_date(2024, 12, 31)
        self.set_cash(100_000)

        # ── Universe ──────────────────────────────────────────────────────
        self.symbol = self.add_equity("AAPL", Resolution.DAILY).symbol

        # ── Indicators ────────────────────────────────────────────────────
        self.fast = self.sma(self.symbol, 50,  Resolution.DAILY)
        self.slow = self.sma(self.symbol, 200, Resolution.DAILY)

        # Warm-up: pre-fill indicators before the backtest start date
        self.set_warm_up(200, Resolution.DAILY)

        # Track previous cross state to detect crossovers
        self._prev_above: bool | None = None

    # ------------------------------------------------------------------
    def on_data(self, data: Slice):
        if self.is_warming_up:
            return
        if not (self.fast.is_ready and self.slow.is_ready):
            return
        if self.symbol not in data.bars:
            return

        price = data.bars[self.symbol].close
        fast_val = self.fast.current.value
        slow_val = self.slow.current.value
        above = fast_val > slow_val

        # Detect crossover
        if self._prev_above is not None and above != self._prev_above:
            if above:
                # Golden cross → enter long
                self.set_holdings(self.symbol, 1.0)
                self.log(
                    f"GOLDEN CROSS  | BUY  {self.symbol.value} @ {price:.2f} "
                    f"| SMA50={fast_val:.2f} SMA200={slow_val:.2f}"
                )
            else:
                # Death cross → exit
                self.liquidate(self.symbol)
                self.log(
                    f"DEATH  CROSS  | SELL {self.symbol.value} @ {price:.2f} "
                    f"| SMA50={fast_val:.2f} SMA200={slow_val:.2f}"
                )

        self._prev_above = above

    # ------------------------------------------------------------------
    def on_end_of_algorithm(self):
        self.log("=== Final Portfolio ===")
        self.log(f"Total Portfolio Value : {self.portfolio.total_portfolio_value:,.2f}")
        self.log(f"Total Profit          : {self.portfolio.total_profit:,.2f}")
