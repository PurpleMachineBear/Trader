# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta, time
# endregion


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_float(value: str | None, default: float) -> float:
    if value is None or value == "":
        return default
    return float(value)


def _parse_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default
    return int(float(value))


class DualMomentumCoreSleeve:
    def __init__(self, algo: QCAlgorithm):
        self.algo = algo
        self.allocation = _parse_float(algo.get_parameter("core_allocation"), 0.75)
        self.lookback = _parse_int(algo.get_parameter("core_lookback"), 126)
        self.rebalance_days = _parse_int(algo.get_parameter("core_rebalance_days"), 7)

        qqq = algo.add_equity("QQQ", Resolution.MINUTE, extended_market_hours=True)
        qqq.set_slippage_model(ConstantSlippageModel(0.0001))
        self.qqq = qqq.symbol

        voo = algo.add_equity("VOO", Resolution.DAILY)
        voo.set_slippage_model(ConstantSlippageModel(0.0001))
        self.voo = voo.symbol

        gld = algo.add_equity("GLD", Resolution.DAILY)
        gld.set_slippage_model(ConstantSlippageModel(0.0001))
        self.gld = gld.symbol

        algo.set_benchmark(self.voo)

        self.roc_qqq = algo.roc(self.qqq, self.lookback, Resolution.DAILY)
        self.roc_voo = algo.roc(self.voo, self.lookback, Resolution.DAILY)
        self.roc_gld = algo.roc(self.gld, self.lookback, Resolution.DAILY)

        self.core_symbols = [self.qqq, self.voo, self.gld]
        self.current_target = None
        self.pending_target = None
        self.next_rebalance_date = None
        self.rebalance_requested = False

        algo.schedule.on(
            algo.date_rules.every_day(self.qqq),
            algo.time_rules.after_market_open(self.qqq, 1),
            self.request_rebalance,
        )

    def _decision_reason(
        self,
        target: Symbol | None,
        best_offensive: Symbol,
        best_offensive_score: float,
        defensive_score: float,
    ) -> str:
        if target is None:
            return (
                "cash_all_negative "
                f"best_offensive={best_offensive.value}:{best_offensive_score:.3f} "
                f"gld={defensive_score:.3f}"
            )
        if target == self.gld:
            return (
                "defensive_wins "
                f"best_offensive={best_offensive.value}:{best_offensive_score:.3f} "
                f"gld={defensive_score:.3f}"
            )
        return (
            "offensive_wins "
            f"target={target.value}:{best_offensive_score:.3f} "
            f"gld={defensive_score:.3f}"
        )

    def _theoretical_target(self) -> tuple[Symbol | None, Symbol, float, float]:
        scores = [
            (self.qqq, self.roc_qqq.current.value),
            (self.voo, self.roc_voo.current.value),
        ]
        best_offensive, best_offensive_score = max(scores, key=lambda item: item[1])
        defensive_score = self.roc_gld.current.value

        if best_offensive_score > 0 and best_offensive_score >= defensive_score:
            target = best_offensive
        elif defensive_score > 0:
            target = self.gld
        else:
            target = None
        return target, best_offensive, best_offensive_score, defensive_score

    def log_snapshot(self, tag: str):
        if not (self.roc_qqq.is_ready and self.roc_voo.is_ready and self.roc_gld.is_ready):
            self.algo.log(f"[CORE] snapshot={tag} indicators_not_ready")
            return

        target, best_offensive, best_offensive_score, defensive_score = self._theoretical_target()
        target_value = target.value if target is not None else "CASH"
        decision_reason = self._decision_reason(
            target=target,
            best_offensive=best_offensive,
            best_offensive_score=best_offensive_score,
            defensive_score=defensive_score,
        )
        self.algo.log(
            f"[CORE] snapshot={tag} target={target_value} reason={decision_reason} "
            f"roc_qqq={self.roc_qqq.current.value:.3f} "
            f"roc_voo={self.roc_voo.current.value:.3f} "
            f"roc_gld={self.roc_gld.current.value:.3f}"
        )

    def request_rebalance(self):
        self.rebalance_requested = True

    def _current_invested(self):
        for symbol in self.core_symbols:
            if self.algo.portfolio[symbol].invested:
                return symbol
        return None

    def _liquidate_core(self):
        for symbol in self.core_symbols:
            if self.algo.portfolio[symbol].invested:
                self.algo.liquidate(symbol, tag="core_rebalance")

    def _set_target(self, symbol: Symbol):
        target_allocation = self.algo.cap_target_allocation(symbol, self.allocation, "core")
        if target_allocation <= 0:
            self.algo.log(
                f"[CORE] skipped target={symbol.value} requested_alloc={self.allocation:.2f} "
                "reason=exposure_cap"
            )
            self.current_target = None
            return

        self.algo.set_holdings(symbol, target_allocation, False, tag="core_target")
        self.current_target = symbol
        self.algo.log(
            f"[CORE] target={symbol.value} alloc={target_allocation:.2f} "
            f"roc_qqq={self.roc_qqq.current.value:.3f} "
            f"roc_voo={self.roc_voo.current.value:.3f} "
            f"roc_gld={self.roc_gld.current.value:.3f}"
        )

    def on_data(self):
        if self.pending_target is not None and self._current_invested() is None:
            self._set_target(self.pending_target)
            self.pending_target = None
            return

        if not self.rebalance_requested:
            return
        self.rebalance_requested = False

        if self.algo.is_warming_up:
            return
        if not (self.roc_qqq.is_ready and self.roc_voo.is_ready and self.roc_gld.is_ready):
            return
        if self.next_rebalance_date is not None and self.algo.time.date() < self.next_rebalance_date:
            return

        target, best_offensive, best_offensive_score, defensive_score = self._theoretical_target()

        decision_reason = self._decision_reason(
            target=target,
            best_offensive=best_offensive,
            best_offensive_score=best_offensive_score,
            defensive_score=defensive_score,
        )

        current_invested = self._current_invested()
        if target != current_invested:
            if target is None:
                self._liquidate_core()
                self.current_target = None
                self.algo.log(f"[CORE] target=CASH reason={decision_reason}")
            elif current_invested is None:
                self._set_target(target)
            else:
                self.pending_target = target
                self.current_target = None
                self._liquidate_core()
                self.algo.log(
                    f"[CORE] rotate_from={current_invested.value} "
                    f"to={target.value} reason={decision_reason}"
                )
        else:
            held_value = current_invested.value if current_invested is not None else "CASH"
            self.algo.log(
                f"[CORE] hold={held_value} reason={decision_reason} "
                f"roc_qqq={self.roc_qqq.current.value:.3f} "
                f"roc_voo={self.roc_voo.current.value:.3f} "
                f"roc_gld={self.roc_gld.current.value:.3f}"
            )

        self.next_rebalance_date = self.algo.time.date() + timedelta(days=self.rebalance_days)


class FixedAggressiveBSLSleeve:
    def __init__(self, algo: QCAlgorithm, core_sleeve: DualMomentumCoreSleeve):
        self.algo = algo
        self.core_sleeve = core_sleeve
        self.allocation = _parse_float(algo.get_parameter("intraday_allocation"), 0.20)
        self.enable_trading = _parse_bool(algo.get_parameter("enable_intraday"), True)
        self.max_portfolio_daily_loss_pct = _parse_float(
            algo.get_parameter("portfolio_intraday_disable_pct"),
            0.0,
        )
        self.max_intraday_daily_loss_pct = _parse_float(
            algo.get_parameter("intraday_daily_loss_pct_total"),
            0.0,
        )

        self.opening_range_minutes = 5
        self.max_entry_minutes = 120
        self.force_exit_minutes_before_close = 5
        self.volume_lookback_days = 20
        self.risk_reward = 2.0
        self.stop_buffer_pct = 0.001
        self.confirm_hold_minutes = 3
        self.max_holding_minutes = 240
        self.use_vwap_exit = False
        self.selection_pool_size = 1
        self.context_require_above_vwap = True
        self.context_require_above_open = False
        self.context_min_positive = 2
        self.min_prev_close = 20.0
        self.max_prev_close = 2000.0
        self.min_avg_dollar_volume = 250000000.0
        self.min_premarket_dollar_volume = 1000000.0
        self.downtrend_lookback_days = 15
        self.downtrend_return_max = -0.05
        self.gap_min = -0.005
        self.premarket_vol_ratio_min = 0.004
        self.morning_flush_pct = 0.003

        self.symbol_by_ticker = {symbol.value: symbol for symbol in core_sleeve.core_symbols}
        for ticker in ["NVDA", "TSLA", "SMH"]:
            if ticker in self.symbol_by_ticker:
                continue
            security = algo.add_equity(ticker, Resolution.MINUTE, extended_market_hours=True)
            security.set_slippage_model(ConstantSlippageModel(0.0001))
            self.symbol_by_ticker[ticker] = security.symbol

        self.tradable_symbols = [self.symbol_by_ticker["NVDA"], self.symbol_by_ticker["TSLA"]]
        self.context_symbols = [self.symbol_by_ticker["QQQ"], self.symbol_by_ticker["SMH"]]
        self.symbols = list(self.symbol_by_ticker.values())
        self.max_daily_history = max(self.volume_lookback_days + 10, self.downtrend_lookback_days + 10, 60)

        self.current_day = None
        self.day_start_total_equity = float(algo.portfolio.total_portfolio_value)
        self.daily_summaries = {symbol: [] for symbol in self.symbols}
        self.state = {symbol: self._new_symbol_state() for symbol in self.symbols}
        self.watchlist_symbols = []
        self.entry_symbol = None
        self.stop_price = None
        self.target_price = None
        self.entry_time = None
        self.trade_taken = False

        self._bootstrap_daily_history()

    def _new_symbol_state(self):
        return {
            "premarket_high": None,
            "premarket_low": None,
            "premarket_volume": 0.0,
            "regular_open": None,
            "regular_high": None,
            "regular_low": None,
            "regular_close": None,
            "regular_volume": 0.0,
            "opening_range_high": None,
            "opening_range_low": None,
            "session_high": None,
            "session_low": None,
            "vwap_price_volume": 0.0,
            "vwap_volume": 0.0,
            "qualified": None,
            "rank_score": None,
            "gap_pct": 0.0,
            "premarket_vol_ratio": 0.0,
            "avg_dollar_volume": 0.0,
            "premarket_dollar_volume": 0.0,
            "downtrend_return": 0.0,
            "flush_seen": False,
            "confirm_start": None,
            "key_level": None,
            "prev_day": None,
        }

    def _bootstrap_daily_history(self):
        for symbol in self.symbols:
            try:
                history = list(self.algo.history[TradeBar](symbol, self.max_daily_history, Resolution.DAILY))
            except Exception as exc:
                self.algo.log(f"[INTRADAY] daily history bootstrap failed for {symbol.value}: {exc}")
                history = []
            summaries = []
            for bar in history:
                summaries.append(
                    {
                        "date": bar.end_time.date(),
                        "open": float(bar.open),
                        "high": float(bar.high),
                        "low": float(bar.low),
                        "close": float(bar.close),
                        "volume": float(bar.volume),
                    }
                )
            self.daily_summaries[symbol] = summaries[-self.max_daily_history:]

    def _roll_day(self, new_date):
        if self.current_day is not None:
            for symbol in self.symbols:
                state = self.state[symbol]
                if state["regular_open"] is None or state["regular_close"] is None:
                    continue
                self.daily_summaries[symbol].append(
                    {
                        "date": self.current_day,
                        "open": state["regular_open"],
                        "high": state["regular_high"],
                        "low": state["regular_low"],
                        "close": state["regular_close"],
                        "volume": state["regular_volume"],
                    }
                )
                self.daily_summaries[symbol] = self.daily_summaries[symbol][-self.max_daily_history:]

        self.current_day = new_date
        self.day_start_total_equity = float(self.algo.portfolio.total_portfolio_value)
        self.state = {symbol: self._new_symbol_state() for symbol in self.symbols}
        self.watchlist_symbols = []
        self.entry_symbol = None
        self.stop_price = None
        self.target_price = None
        self.entry_time = None
        self.trade_taken = False

    def _is_premarket(self):
        current_time = self.algo.time.time()
        return time(4, 0) <= current_time < time(9, 30)

    def _is_regular(self):
        current_time = self.algo.time.time()
        return time(9, 30) <= current_time < time(16, 0)

    def _minutes_from_open(self):
        return (self.algo.time.hour * 60 + self.algo.time.minute) - (9 * 60 + 30)

    def _minutes_to_close(self):
        return (16 * 60) - (self.algo.time.hour * 60 + self.algo.time.minute)

    def _session_vwap(self, symbol: Symbol):
        state = self.state[symbol]
        if state["vwap_volume"] <= 0:
            return state["regular_close"] or 0.0
        return state["vwap_price_volume"] / state["vwap_volume"]

    def _intraday_unrealized_pnl(self):
        if self.entry_symbol is None:
            return 0.0
        holding = self.algo.portfolio[self.entry_symbol]
        if not holding.invested:
            return 0.0
        return float(holding.unrealized_profit)

    def _intraday_loss_breached(self):
        if self.max_intraday_daily_loss_pct <= 0:
            return False
        threshold = self.day_start_total_equity * self.max_intraday_daily_loss_pct
        return self._intraday_unrealized_pnl() <= -threshold

    def _portfolio_intraday_disabled(self):
        if self.max_portfolio_daily_loss_pct <= 0 or self.day_start_total_equity <= 0:
            return False
        return (
            float(self.algo.portfolio.total_portfolio_value)
            <= self.day_start_total_equity * (1.0 - self.max_portfolio_daily_loss_pct)
        )

    def _avg_regular_volume(self, symbol: Symbol, lookback_days: int):
        history = self.daily_summaries[symbol]
        if len(history) < lookback_days:
            return 0.0
        sample = history[-lookback_days:]
        return sum(item["volume"] for item in sample) / float(lookback_days)

    def _recent_return(self, symbol: Symbol, lookback_days: int):
        history = self.daily_summaries[symbol]
        if len(history) < lookback_days + 1:
            return 0.0
        start_close = history[-(lookback_days + 1)]["close"]
        end_close = history[-1]["close"]
        if start_close <= 0:
            return 0.0
        return (end_close / start_close) - 1.0

    def _qualifies(self, symbol: Symbol):
        state = self.state[symbol]
        if state["qualified"] is not None:
            return state["qualified"]

        history = self.daily_summaries[symbol]
        if len(history) < self.volume_lookback_days:
            state["qualified"] = False
            return False

        state["prev_day"] = history[-1]
        avg_volume = self._avg_regular_volume(symbol, self.volume_lookback_days)
        if avg_volume <= 0 or state["regular_open"] is None or state["prev_day"]["close"] <= 0:
            state["qualified"] = False
            return False

        state["avg_dollar_volume"] = avg_volume * state["prev_day"]["close"]
        state["premarket_dollar_volume"] = state["premarket_volume"] * max(
            state["regular_open"],
            state["prev_day"]["close"],
        )
        if not (self.min_prev_close <= state["prev_day"]["close"] <= self.max_prev_close):
            state["qualified"] = False
            return False
        if state["avg_dollar_volume"] < self.min_avg_dollar_volume:
            state["qualified"] = False
            return False
        if state["premarket_dollar_volume"] < self.min_premarket_dollar_volume:
            state["qualified"] = False
            return False

        state["gap_pct"] = (state["regular_open"] / state["prev_day"]["close"]) - 1.0
        state["premarket_vol_ratio"] = state["premarket_volume"] / avg_volume
        state["downtrend_return"] = self._recent_return(symbol, self.downtrend_lookback_days)
        state["key_level"] = max(state["prev_day"]["high"], state["prev_day"]["close"])
        state["qualified"] = (
            state["downtrend_return"] <= self.downtrend_return_max
            and state["gap_pct"] >= self.gap_min
            and state["premarket_vol_ratio"] >= self.premarket_vol_ratio_min
        )
        return state["qualified"]

    def _rank_score(self, symbol: Symbol):
        state = self.state[symbol]
        if state["rank_score"] is not None:
            return state["rank_score"]
        state["rank_score"] = abs(min(state["downtrend_return"], 0.0)) * max(
            state["premarket_vol_ratio"],
            0.0,
        )
        return state["rank_score"]

    def _select_watchlist(self):
        candidates = []
        for symbol in self.tradable_symbols:
            if not self._qualifies(symbol):
                continue
            score = self._rank_score(symbol)
            if score is None:
                continue
            candidates.append((score, symbol))
        if not candidates:
            return []
        candidates.sort(key=lambda item: item[0], reverse=True)
        return [symbol for _, symbol in candidates[:self.selection_pool_size]]

    def _entries_available(self):
        if not self.enable_trading:
            return False
        if self.trade_taken:
            return False
        if self.algo.master_trading_disabled():
            return False
        if self._portfolio_intraday_disabled():
            return False
        return True

    def _enter_long(self, symbol: Symbol, price: float, stop_reference: float):
        if stop_reference is None or not self._entries_available():
            return

        stop_price = stop_reference * (1.0 - self.stop_buffer_pct)
        risk = price - stop_price
        if risk <= max(price * 0.001, 0.01):
            return

        target_allocation = self.algo.cap_target_allocation(symbol, self.allocation, "intraday")
        if target_allocation <= 0:
            self.algo.log(
                f"[INTRADAY] skipped entry={symbol.value} requested_alloc={self.allocation:.2f} "
                "reason=exposure_cap"
            )
            return

        self.algo.set_holdings(symbol, target_allocation, False, tag="intraday_entry")
        self.entry_symbol = symbol
        self.stop_price = stop_price
        self.target_price = price + risk * self.risk_reward
        self.entry_time = self.algo.time
        self.trade_taken = True
        self.algo.log(
            f"[INTRADAY] entry={symbol.value} alloc={target_allocation:.2f} "
            f"price={price:.2f} stop={self.stop_price:.2f} target={self.target_price:.2f}"
        )

    def _manage_position(self, symbol: Symbol, bar: TradeBar):
        if self.entry_symbol != symbol or not self.algo.portfolio[symbol].invested:
            return False

        price = float(bar.close)
        exit_tag = None
        if self._intraday_loss_breached():
            exit_tag = "intraday_daily_loss_kill"
        elif self._portfolio_intraday_disabled():
            exit_tag = "portfolio_daily_loss_disable"
        elif self.stop_price is not None and price <= self.stop_price:
            exit_tag = "stop_loss"
        elif self.target_price is not None and price >= self.target_price:
            exit_tag = "profit_target"
        elif self.entry_time is not None:
            held_minutes = (self.algo.time - self.entry_time).total_seconds() / 60.0
            if held_minutes >= self.max_holding_minutes:
                exit_tag = "time_exit"
        if exit_tag is None and self._minutes_to_close() <= self.force_exit_minutes_before_close:
            exit_tag = "eod_exit"
        if exit_tag is None and self.use_vwap_exit:
            vwap = self._session_vwap(symbol)
            if vwap > 0 and price < vwap:
                exit_tag = "vwap_loss"

        if exit_tag is None:
            return False

        self.algo.liquidate(symbol, tag=exit_tag)
        self.algo.log(f"[INTRADAY] exit={symbol.value} reason={exit_tag} price={price:.2f}")
        return True

    def _context_allows_entry(self):
        positive_count = 0
        for symbol in self.context_symbols:
            state = self.state[symbol]
            price = state["regular_close"]
            if price is None:
                return False

            positive = True
            if self.context_require_above_vwap:
                vwap = self._session_vwap(symbol)
                if vwap <= 0 or price <= vwap:
                    positive = False
            if self.context_require_above_open:
                regular_open = state["regular_open"]
                if regular_open is None or price <= regular_open:
                    positive = False
            if positive:
                positive_count += 1

        required_count = self.context_min_positive or len(self.context_symbols)
        return positive_count >= required_count

    def _maybe_enter(self, symbol: Symbol, bar: TradeBar):
        state = self.state[symbol]
        if (
            state["session_low"] is None
            or state["regular_open"] is None
            or state["opening_range_low"] is None
            or state["key_level"] is None
        ):
            return

        if state["session_low"] <= state["regular_open"] * (1.0 - self.morning_flush_pct):
            state["flush_seen"] = True
        if not state["flush_seen"]:
            return

        levels = [
            level
            for level in [state["key_level"], state["opening_range_high"]]
            if level is not None
        ]
        if not levels:
            return

        breakout_level = max(levels)
        price = float(bar.close)
        vwap = self._session_vwap(symbol)
        if vwap <= 0 or price <= vwap or price <= breakout_level:
            state["confirm_start"] = None
            return

        if state["confirm_start"] is None:
            state["confirm_start"] = self.algo.time
            return

        held_above = (self.algo.time - state["confirm_start"]).total_seconds() / 60.0
        if held_above + 1e-9 < self.confirm_hold_minutes:
            return

        stop_reference = min(
            state["session_low"],
            state["opening_range_low"],
            state["prev_day"]["close"],
        )
        self._enter_long(symbol, price, stop_reference)

    def on_data(self, data: Slice):
        if self.current_day != self.algo.time.date():
            self._roll_day(self.algo.time.date())

        for symbol in self.symbols:
            if symbol not in data.bars:
                continue

            bar = data.bars[symbol]
            state = self.state[symbol]
            if self._is_premarket():
                state["premarket_high"] = bar.high if state["premarket_high"] is None else max(
                    state["premarket_high"],
                    bar.high,
                )
                state["premarket_low"] = bar.low if state["premarket_low"] is None else min(
                    state["premarket_low"],
                    bar.low,
                )
                state["premarket_volume"] += float(bar.volume)
                continue

            if not self._is_regular():
                if (
                    symbol in self.tradable_symbols
                    and self.algo.portfolio[symbol].invested
                    and self._minutes_to_close() <= self.force_exit_minutes_before_close
                ):
                    self.algo.liquidate(symbol, tag="eod_exit")
                continue

            state["regular_open"] = bar.open if state["regular_open"] is None else state["regular_open"]
            state["regular_high"] = bar.high if state["regular_high"] is None else max(state["regular_high"], bar.high)
            state["regular_low"] = bar.low if state["regular_low"] is None else min(state["regular_low"], bar.low)
            state["regular_close"] = bar.close
            state["regular_volume"] += float(bar.volume)
            state["session_high"] = bar.high if state["session_high"] is None else max(state["session_high"], bar.high)
            state["session_low"] = bar.low if state["session_low"] is None else min(state["session_low"], bar.low)
            state["vwap_price_volume"] += float(bar.close) * float(bar.volume)
            state["vwap_volume"] += float(bar.volume)

            minutes_from_open = self._minutes_from_open()
            if minutes_from_open < self.opening_range_minutes:
                state["opening_range_high"] = bar.high if state["opening_range_high"] is None else max(
                    state["opening_range_high"],
                    bar.high,
                )
                state["opening_range_low"] = bar.low if state["opening_range_low"] is None else min(
                    state["opening_range_low"],
                    bar.low,
                )

            if self._manage_position(symbol, bar):
                return

        if not self._is_regular():
            return
        if any(self.algo.portfolio[symbol].invested for symbol in self.tradable_symbols):
            return
        if not self._entries_available():
            return

        minutes_from_open = self._minutes_from_open()
        if minutes_from_open < self.opening_range_minutes or minutes_from_open > self.max_entry_minutes:
            return

        if not self.watchlist_symbols:
            self.watchlist_symbols = self._select_watchlist()
            if not self.watchlist_symbols:
                return

        if not self._context_allows_entry():
            return

        for symbol in self.watchlist_symbols:
            if symbol not in data.bars:
                continue
            self._maybe_enter(symbol, data.bars[symbol])
            if self.trade_taken or any(self.algo.portfolio[item].invested for item in self.tradable_symbols):
                return


class MasterPaperPortfolio(QCAlgorithm):
    def initialize(self):
        start_date = self.get_parameter("start_date") or "2025-01-02"
        end_date = self.get_parameter("end_date") or "2026-03-06"
        starting_cash = _parse_int(self.get_parameter("cash"), 100000)

        self.set_start_date(*map(int, start_date.split("-")))
        self.set_end_date(*map(int, end_date.split("-")))
        self.set_cash(starting_cash)
        self.start_date_anchor = datetime.strptime(start_date, "%Y-%m-%d").date()

        self.max_total_exposure_pct = min(
            max(_parse_float(self.get_parameter("max_total_exposure_pct"), 0.95), 0.0),
            1.0,
        )
        self.max_portfolio_daily_loss_pct = max(
            _parse_float(self.get_parameter("portfolio_daily_loss_pct_total"), 0.0),
            0.0,
        )
        self.master_kill_switch_active = False
        self.master_kill_reason = None
        self.risk_day = None
        self.day_start_total_equity = float(starting_cash)
        self.warmup_snapshot_logged = False

        self.core = DualMomentumCoreSleeve(self)
        self.intraday = FixedAggressiveBSLSleeve(self, self.core)
        self.tracked_symbols = list(dict.fromkeys(self.core.core_symbols + self.intraday.symbols))

        warmup_days = max(self.core.lookback, self.intraday.volume_lookback_days + 5)
        self.set_warm_up(warmup_days, Resolution.DAILY)

        self.log(
            "[MASTER] initialized "
            f"core_alloc={self.core.allocation:.2f} "
            f"intraday_alloc={self.intraday.allocation:.2f} "
            f"intraday_enabled={self.intraday.enable_trading} "
            f"portfolio_daily_loss_pct_total={self.max_portfolio_daily_loss_pct:.4f} "
            f"max_total_exposure_pct={self.max_total_exposure_pct:.2f} "
            f"intraday_daily_loss_pct_total={self.intraday.max_intraday_daily_loss_pct:.4f} "
            f"portfolio_intraday_disable_pct={self.intraday.max_portfolio_daily_loss_pct:.4f}"
        )

    def _roll_risk_day(self):
        current_date = self.time.date()
        if self.risk_day == current_date:
            return

        previous_kill = self.master_kill_switch_active
        self.risk_day = current_date
        self.day_start_total_equity = float(self.portfolio.total_portfolio_value)
        self.master_kill_switch_active = False
        self.master_kill_reason = None
        if (not self.is_warming_up and current_date >= self.start_date_anchor) or previous_kill:
            self.log(
                f"[RISK] new_day={current_date.isoformat()} "
                f"start_equity={self.day_start_total_equity:.2f} "
                f"kill_switch_reset={previous_kill}"
            )

    def master_trading_disabled(self) -> bool:
        return self.master_kill_switch_active

    def total_absolute_exposure_pct(self, exclude_symbols: list[Symbol] | None = None) -> float:
        if self.portfolio.total_portfolio_value <= 0:
            return 0.0

        excluded = set(exclude_symbols or [])
        exposure_value = 0.0
        for symbol in self.tracked_symbols:
            if symbol in excluded:
                continue
            exposure_value += abs(float(self.portfolio[symbol].holdings_value))
        return exposure_value / float(self.portfolio.total_portfolio_value)

    def cap_target_allocation(self, symbol: Symbol, requested_allocation: float, sleeve_name: str) -> float:
        requested = max(requested_allocation, 0.0)
        if requested <= 0:
            return 0.0
        if self.max_total_exposure_pct <= 0:
            return requested

        other_exposure = self.total_absolute_exposure_pct(exclude_symbols=[symbol])
        available = max(0.0, self.max_total_exposure_pct - other_exposure)
        capped = min(requested, available)

        if (requested - capped) > 1e-6:
            self.log(
                f"[RISK] exposure_cap sleeve={sleeve_name} symbol={symbol.value} "
                f"requested={requested:.2f} capped={capped:.2f} "
                f"other_exposure={other_exposure:.2f} max_total={self.max_total_exposure_pct:.2f}"
            )
        return capped

    def _portfolio_daily_loss_breached(self) -> bool:
        if self.max_portfolio_daily_loss_pct <= 0 or self.day_start_total_equity <= 0:
            return False
        return (
            float(self.portfolio.total_portfolio_value)
            <= self.day_start_total_equity * (1.0 - self.max_portfolio_daily_loss_pct)
        )

    def _activate_master_kill_switch(self, reason: str):
        if self.master_kill_switch_active:
            return

        self.master_kill_switch_active = True
        self.master_kill_reason = reason
        self.liquidate(tag=reason)
        self.log(
            f"[RISK] master_kill_switch reason={reason} "
            f"equity={self.portfolio.total_portfolio_value:.2f} "
            f"exposure={self.total_absolute_exposure_pct():.2f}"
        )

    def on_data(self, data: Slice):
        self._roll_risk_day()
        if not self.is_warming_up and not self.warmup_snapshot_logged:
            self.core.log_snapshot("post_warmup")
            self.warmup_snapshot_logged = True
        if self._portfolio_daily_loss_breached():
            self._activate_master_kill_switch("master_daily_loss_kill")
        if self.master_trading_disabled():
            return

        self.core.on_data()
        self.intraday.on_data(data)

    def on_order_event(self, order_event: OrderEvent):
        if order_event.status != OrderStatus.FILLED:
            return
        security = self.securities[order_event.symbol]
        order = self.transactions.get_order_by_id(order_event.order_id)
        order_tag = order.tag if order is not None else "-"
        self.log(
            f"[ORDER] symbol={order_event.symbol.value} "
            f"qty={order_event.fill_quantity:.0f} "
            f"price={order_event.fill_price:.2f} "
            f"tag={order_tag} "
            f"holdings={security.holdings.quantity:.0f}"
        )

    def on_end_of_algorithm(self):
        self.log(
            "[MASTER] final "
            f"equity={self.portfolio.total_portfolio_value:.2f} "
            f"cash={self.portfolio.cash:.2f} "
            f"master_kill_reason={self.master_kill_reason or '-'}"
        )
