# region imports
from AlgorithmImports import *
# endregion


class VooBuyAndHoldBenchmark(QCAlgorithm):
    def initialize(self) -> None:
        start_date = self.get_parameter("start_date") or "2025-01-02"
        end_date = self.get_parameter("end_date") or "2026-03-06"
        starting_cash = int(float(self.get_parameter("cash") or 100000))

        self.set_start_date(*map(int, start_date.split("-")))
        self.set_end_date(*map(int, end_date.split("-")))
        self.set_cash(starting_cash)

        security = self.add_equity("VOO", Resolution.DAILY)
        security.set_slippage_model(ConstantSlippageModel(0.0001))
        self.symbol = security.symbol
        self.set_benchmark(self.symbol)

        self.invested_once = False

    def on_data(self, data: Slice) -> None:
        if self.invested_once:
            return
        if self.is_warming_up or self.symbol not in data.bars:
            return
        self.set_holdings(self.symbol, 1.0)
        self.invested_once = True
