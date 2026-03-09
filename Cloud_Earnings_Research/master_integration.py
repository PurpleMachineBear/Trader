# region imports
from AlgorithmImports import *
from datetime import datetime, timedelta, time
from typing import List, Optional
# endregion


def _parse_bool(value: Optional[str], default: bool) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_float(value: Optional[str], default: float) -> float:
    if value is None or value == "":
        return default
    return float(value)


def _parse_int(value: Optional[str], default: int) -> int:
    if value is None or value == "":
        return default
    return int(float(value))


class CloudDualMomentumCoreSleeve:
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

        current_invested = self._current_invested()
        if target != current_invested:
            if target is None:
                self._liquidate_core()
                self.current_target = None
                self.algo.log("[CORE] target=CASH")
            elif current_invested is None:
                self._set_target(target)
            else:
                self.pending_target = target
                self.current_target = None
                self._liquidate_core()

        self.next_rebalance_date = self.algo.time.date() + timedelta(days=self.rebalance_days)


class CloudEventAwareFixedAggressiveBSLSleeve:
    def __init__(self, algo: QCAlgorithm, core_sleeve: CloudDualMomentumCoreSleeve, state_bridge):
        self.algo = algo
        self.core_sleeve = core_sleeve
        self.state_bridge = state_bridge
        self.base_allocation = _parse_float(algo.get_parameter("intraday_allocation"), 0.20)
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
        self.risk_reward = _parse_float(algo.get_parameter("risk_reward"), 2.0)
        self.stop_buffer_pct = 0.001
        self.confirm_hold_minutes = 3
        self.max_holding_minutes = _parse_int(algo.get_parameter("max_holding_minutes"), 240)
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
            except Exception:
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
        if self.state_bridge.current_intraday_allocation() <= 0:
            return False
        return True

    def _enter_long(self, symbol: Symbol, price: float, stop_reference: float):
        if stop_reference is None or not self._entries_available():
            return

        stop_price = stop_reference * (1.0 - self.stop_buffer_pct)
        risk = price - stop_price
        if risk <= max(price * 0.001, 0.01):
            return

        requested_allocation = self.state_bridge.current_intraday_allocation()
        target_allocation = self.algo.cap_target_allocation(symbol, requested_allocation, "intraday")
        if target_allocation <= 0:
            self.algo.log(
                f"[INTRADAY] skipped entry={symbol.value} requested_alloc={requested_allocation:.2f} "
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
            f"price={price:.2f} stop={self.stop_price:.2f} target={self.target_price:.2f} "
            f"event_count={self.state_bridge.event_state_count}"
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


class CloudEventSwingSleeve:
    def __init__(self, algo: QCAlgorithm, master):
        self.algo = algo
        self.master = master
        self.enabled = _parse_bool(algo.get_parameter("event_sleeve_enabled"), False)
        self.bucket = (algo.get_parameter("event_sleeve_bucket") or "platform5").strip()
        self.event_mode = (algo.get_parameter("event_sleeve_event_mode") or "pre1").strip().lower()
        self.allocation = _parse_float(algo.get_parameter("event_sleeve_allocation"), 0.0)
        self.max_names = _parse_int(algo.get_parameter("event_sleeve_max_names"), 3)
        self.hold_days = _parse_int(algo.get_parameter("event_sleeve_hold_days"), 3)
        self.lookback_days = _parse_int(algo.get_parameter("event_sleeve_lookback_days"), 15)
        self.min_price = _parse_float(algo.get_parameter("event_sleeve_min_price"), 20.0)
        self.min_avg_dollar_volume = _parse_float(
            algo.get_parameter("event_sleeve_min_avg_dollar_volume"),
            150000000.0,
        )
        self.report_time_filter = (algo.get_parameter("event_sleeve_report_time_filter") or "any").strip().lower()
        self.estimate_mode = (algo.get_parameter("event_sleeve_estimate_mode") or "any").strip().lower()
        self.core_state_filter = (algo.get_parameter("event_sleeve_core_state_filter") or "any").strip().lower()
        self.min_active_events = _parse_int(algo.get_parameter("event_sleeve_min_active_events"), 1)
        self.max_daily_history = max(self.lookback_days + 10, 40)
        self.selection_log_count = 0
        self.last_rebalance_day = None
        self.rebalance_requested = False
        self.days_remaining = {}
        self.active_tickers = {}
        self.symbol_by_ticker = {}
        self.symbols = []

        if not self.enabled or self.allocation <= 0:
            self.enabled = False
            self.tickers = []
            return

        self.tickers = master.event_bucket_map.get(
            self.bucket,
            master.event_bucket_map["platform5"],
        )
        for ticker in self.tickers:
            security = algo.add_equity(
                ticker,
                Resolution.DAILY,
                data_normalization_mode=DataNormalizationMode.RAW,
            )
            security.set_slippage_model(ConstantSlippageModel(0.0001))
            self.symbol_by_ticker[ticker] = security.symbol
        self.symbols = list(self.symbol_by_ticker.values())

        anchor_symbol = self.symbols[0]
        algo.schedule.on(
            algo.date_rules.every_day(anchor_symbol),
            algo.time_rules.before_market_close(anchor_symbol, 3),
            self.request_rebalance,
        )

    def request_rebalance(self):
        self.rebalance_requested = True

    def _event_matches(self, today, report_date):
        delta = (report_date - today).days
        if self.event_mode == "pre1":
            return delta == 1
        if self.event_mode == "pre2":
            return delta == 2
        if self.event_mode == "pre3":
            return 1 <= delta <= 3
        if self.event_mode == "day0":
            return delta == 0
        if self.event_mode == "post1":
            return (today - report_date).days == 1
        if self.event_mode == "post2":
            return (today - report_date).days == 2
        return False

    def _report_time_matches(self, report_time: str) -> bool:
        if self.report_time_filter == "any":
            return True
        value = (report_time or "").strip().lower()
        if self.report_time_filter == "before_open":
            return "before" in value or "bmo" in value or "open" in value
        if self.report_time_filter == "after_close":
            return "after" in value or "amc" in value or "close" in value
        if self.report_time_filter == "unknown":
            return value == ""
        return True

    def _daily_rows(self, symbol: Symbol):
        try:
            history = list(self.algo.history[TradeBar](symbol, self.max_daily_history, Resolution.DAILY))
        except Exception:
            history = []
        rows = []
        for bar in history:
            rows.append(
                {
                    "close": float(bar.close),
                    "dollar_volume": float(bar.close * bar.volume),
                }
            )
        return rows

    def _avg_dollar_volume(self, rows, lookback_days: int):
        if len(rows) < lookback_days:
            return 0.0
        sample = rows[-lookback_days:]
        return sum(item["dollar_volume"] for item in sample) / float(lookback_days)

    def _recent_return(self, rows, lookback_days: int):
        if len(rows) < lookback_days + 1:
            return None
        start_close = rows[-(lookback_days + 1)]["close"]
        end_close = rows[-1]["close"]
        if start_close <= 0:
            return None
        return (end_close / start_close) - 1.0

    def _liquidate_expired(self, today):
        expired = []
        for ticker in list(self.days_remaining):
            self.days_remaining[ticker] -= 1
            if self.days_remaining[ticker] <= 0:
                expired.append(ticker)

        for ticker in expired:
            symbol = self.symbol_by_ticker[ticker]
            if self.algo.portfolio[symbol].invested:
                self.algo.liquidate(symbol, tag="event_sleeve_expired")
            self.days_remaining.pop(ticker, None)
            self.active_tickers.pop(ticker, None)
            self.algo.log(f"[EVENT_SLEEVE] expired={ticker} day={today.isoformat()}")

    def _core_state_allows_entries(self):
        if self.core_state_filter == "any":
            return True

        current_target = self.master.core.current_target
        if current_target is None:
            return False
        if self.core_state_filter == "offensive_only":
            return current_target in {self.master.core.qqq, self.master.core.voo}
        if self.core_state_filter == "qqq_only":
            return current_target == self.master.core.qqq
        return True

    def _select_candidates(self, today):
        candidates = []
        for ticker in self.tickers:
            symbol = self.symbol_by_ticker[ticker]
            security = self.algo.securities[symbol]
            if not security.has_data or float(security.price) < self.min_price:
                continue

            report_date = self.master.known_report_dates.get(ticker)
            if report_date is None or not self._event_matches(today, report_date):
                continue

            report_time = self.master.known_report_times.get(ticker, "")
            if not self._report_time_matches(report_time):
                continue

            estimate = self.master.known_estimates.get(ticker)
            if self.estimate_mode == "required" and estimate is None:
                continue
            if self.estimate_mode == "missing" and estimate is not None:
                continue

            rows = self._daily_rows(symbol)
            avg_dollar_volume = self._avg_dollar_volume(rows, 20)
            if avg_dollar_volume < self.min_avg_dollar_volume:
                continue

            recent_return = self._recent_return(rows, self.lookback_days)
            if recent_return is None:
                continue

            score = -recent_return
            candidates.append((score, ticker, symbol))

        candidates.sort(key=lambda item: (-item[0], item[1]))
        return candidates[: self.max_names]

    def _rebalance(self):
        if not self.enabled or self.allocation <= 0:
            return

        today = self.algo.time.date()
        if self.last_rebalance_day == today:
            return
        self.last_rebalance_day = today

        self._liquidate_expired(today)
        if self.algo.master_trading_disabled():
            return

        selected = self._select_candidates(today)
        if len(selected) < self.min_active_events:
            selected = []
        if not self._core_state_allows_entries():
            selected = []
        for _, ticker, _ in selected:
            if ticker not in self.days_remaining:
                self.days_remaining[ticker] = self.hold_days
                self.active_tickers[ticker] = str(today)

        desired_tickers = sorted(self.days_remaining.keys())
        desired_symbols = [self.symbol_by_ticker[ticker] for ticker in desired_tickers]

        for symbol in self.symbols:
            if self.algo.portfolio[symbol].invested and symbol not in desired_symbols:
                self.algo.liquidate(symbol, tag="event_sleeve_not_in_basket")

        if desired_symbols:
            requested_per_symbol = self.allocation / float(len(desired_symbols))
            for symbol in desired_symbols:
                target_allocation = self.algo.cap_target_allocation(symbol, requested_per_symbol, "event_sleeve")
                if target_allocation <= 0:
                    self.algo.log(
                        f"[EVENT_SLEEVE] skipped target={symbol.value} requested_alloc={requested_per_symbol:.2f} "
                        "reason=exposure_cap"
                    )
                    continue
                self.algo.set_holdings(symbol, target_allocation, False, tag="event_sleeve")

        self.selection_log_count += 1
        if self.selection_log_count <= 10:
            selected_tickers = ",".join(ticker for _, ticker, _ in selected) or "none"
            active_tickers = ",".join(desired_tickers) or "none"
            self.algo.log(
                f"[EVENT_SLEEVE] day={today.isoformat()} bucket={self.bucket} mode={self.event_mode} "
                f"alloc={self.allocation:.2f} core_filter={self.core_state_filter} "
                f"min_active={self.min_active_events} selected={selected_tickers} active={active_tickers}"
            )

    def on_data(self, data: Slice):
        if not self.enabled:
            return
        if not self.rebalance_requested:
            return
        self.rebalance_requested = False
        self._rebalance()


class CloudMasterEventIntegration:
    def __init__(self, algo: QCAlgorithm):
        self.algo = algo
        self.max_total_exposure_pct = min(
            max(_parse_float(algo.get_parameter("max_total_exposure_pct"), 0.95), 0.0),
            1.0,
        )
        self.max_portfolio_daily_loss_pct = max(
            _parse_float(algo.get_parameter("portfolio_daily_loss_pct_total"), 0.0),
            0.0,
        )
        self.master_kill_switch_active = False
        self.master_kill_reason = None
        self.risk_day = None
        self.day_start_total_equity = float(algo.portfolio.total_portfolio_value)

        self.event_bucket_map = {
            "platform5": ["AAPL", "MSFT", "CRM", "NOW", "ORCL"],
            "platform7": ["AAPL", "MSFT", "NFLX", "CRM", "ADBE", "NOW", "ORCL"],
            "enterprise4": ["MSFT", "CRM", "NOW", "ORCL"],
            "software3": ["CRM", "NOW", "ORCL"],
        }
        self.event_state_bucket = (algo.get_parameter("event_state_bucket") or "platform5").strip()
        self.event_state_tickers = self.event_bucket_map.get(
            self.event_state_bucket,
            self.event_bucket_map["platform5"],
        )
        self.event_state_mode = (algo.get_parameter("event_state_mode") or "off").strip().lower()
        self.event_state_event_mode = (algo.get_parameter("event_state_event_mode") or "pre1").strip().lower()
        self.event_state_min_count = _parse_int(algo.get_parameter("event_state_min_count"), 1)
        self.intraday_alloc_on = _parse_float(algo.get_parameter("intraday_event_alloc_on"), 0.20)
        self.intraday_alloc_off = _parse_float(algo.get_parameter("intraday_event_alloc_off"), 0.0)
        self.known_report_dates = {}
        self.known_report_times = {}
        self.known_estimates = {}
        self.event_state_count = 0
        self.event_state_active_tickers = []
        self.event_state_log_day = None

        # Expose shared risk hooks on the algorithm so reused sleeves can call them
        # without duplicating the master-specific plumbing.
        algo.cap_target_allocation = self.cap_target_allocation
        algo.master_trading_disabled = self.master_trading_disabled

        self.core = CloudDualMomentumCoreSleeve(algo)
        self.intraday = CloudEventAwareFixedAggressiveBSLSleeve(algo, self.core, self)
        self.event_sleeve = CloudEventSwingSleeve(algo, self)
        self.tracked_symbols = list(
            dict.fromkeys(self.core.core_symbols + self.intraday.symbols + self.event_sleeve.symbols)
        )

        warmup_days = max(self.core.lookback, self.intraday.volume_lookback_days + 5)
        algo.set_warm_up(warmup_days, Resolution.DAILY)
        algo.add_universe(EODHDUpcomingEarnings, self._select_event_universe)

        algo.log(
            "[CLOUD_MASTER] initialized "
            f"event_mode={self.event_state_mode} "
            f"event_bucket={self.event_state_bucket} "
            f"event_min_count={self.event_state_min_count} "
            f"intraday_on={self.intraday_alloc_on:.2f} "
            f"intraday_off={self.intraday_alloc_off:.2f} "
            f"event_sleeve_enabled={self.event_sleeve.enabled} "
            f"event_sleeve_bucket={self.event_sleeve.bucket if self.event_sleeve.enabled else '-'} "
            f"event_sleeve_alloc={self.event_sleeve.allocation if self.event_sleeve.enabled else 0.0:.2f}"
        )

    def _select_event_universe(self, earnings):
        tracked_tickers = set(self.event_state_tickers)
        tracked_tickers.update(self.event_sleeve.tickers)
        symbols = []
        for datum in earnings:
            ticker = datum.symbol.value
            if ticker not in tracked_tickers or datum.report_date is None:
                continue
            self.known_report_dates[ticker] = datum.report_date.date()
            self.known_report_times[ticker] = str(datum.report_time).strip() if datum.report_time is not None else ""
            self.known_estimates[ticker] = datum.estimate
            symbols.append(datum.symbol)
        return symbols

    def _event_matches(self, today, report_date):
        delta = (report_date - today).days
        if self.event_state_event_mode == "pre1":
            return delta == 1
        if self.event_state_event_mode == "pre2":
            return delta == 2
        if self.event_state_event_mode == "pre3":
            return 1 <= delta <= 3
        if self.event_state_event_mode == "day0":
            return delta == 0
        if self.event_state_event_mode == "post1":
            return (today - report_date).days == 1
        if self.event_state_event_mode == "post2":
            return (today - report_date).days == 2
        return False

    def _roll_risk_day(self):
        current_date = self.algo.time.date()
        if self.risk_day == current_date:
            return

        previous_kill = self.master_kill_switch_active
        self.risk_day = current_date
        self.day_start_total_equity = float(self.algo.portfolio.total_portfolio_value)
        self.master_kill_switch_active = False
        self.master_kill_reason = None
        if (not self.algo.is_warming_up) or previous_kill:
            self.algo.log(
                f"[RISK] new_day={current_date.isoformat()} "
                f"start_equity={self.day_start_total_equity:.2f} "
                f"kill_switch_reset={previous_kill}"
            )

    def _refresh_event_state(self):
        today = self.algo.time.date()
        active = []
        for ticker in self.event_state_tickers:
            report_date = self.known_report_dates.get(ticker)
            if report_date is None:
                continue
            if self._event_matches(today, report_date):
                active.append(ticker)
        self.event_state_active_tickers = sorted(active)
        self.event_state_count = len(active)
        if self.event_state_log_day != today:
            self.algo.log(
                f"[EVENT_STATE] day={today.isoformat()} mode={self.event_state_mode} "
                f"count={self.event_state_count} tickers={','.join(self.event_state_active_tickers) or 'none'}"
            )
            self.event_state_log_day = today

    def current_intraday_allocation(self):
        if self.event_state_mode == "off":
            return self.intraday_alloc_on
        active = self.event_state_count >= self.event_state_min_count
        if self.event_state_mode == "gate":
            return self.intraday_alloc_on if active else 0.0
        if self.event_state_mode == "tilt":
            return self.intraday_alloc_on if active else self.intraday_alloc_off
        return self.intraday_alloc_on

    def master_trading_disabled(self) -> bool:
        return self.master_kill_switch_active

    def total_absolute_exposure_pct(self, exclude_symbols: Optional[List[Symbol]] = None) -> float:
        if self.algo.portfolio.total_portfolio_value <= 0:
            return 0.0
        excluded = set(exclude_symbols or [])
        exposure_value = 0.0
        for symbol in self.tracked_symbols:
            if symbol in excluded:
                continue
            exposure_value += abs(float(self.algo.portfolio[symbol].holdings_value))
        return exposure_value / float(self.algo.portfolio.total_portfolio_value)

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
            self.algo.log(
                f"[RISK] exposure_cap sleeve={sleeve_name} symbol={symbol.value} "
                f"requested={requested:.2f} capped={capped:.2f} "
                f"other_exposure={other_exposure:.2f} max_total={self.max_total_exposure_pct:.2f}"
            )
        return capped

    def _portfolio_daily_loss_breached(self) -> bool:
        if self.max_portfolio_daily_loss_pct <= 0 or self.day_start_total_equity <= 0:
            return False
        return (
            float(self.algo.portfolio.total_portfolio_value)
            <= self.day_start_total_equity * (1.0 - self.max_portfolio_daily_loss_pct)
        )

    def _activate_master_kill_switch(self, reason: str):
        if self.master_kill_switch_active:
            return
        self.master_kill_switch_active = True
        self.master_kill_reason = reason
        self.algo.liquidate(tag=reason)
        self.algo.log(
            f"[RISK] master_kill_switch reason={reason} "
            f"equity={self.algo.portfolio.total_portfolio_value:.2f} "
            f"exposure={self.total_absolute_exposure_pct():.2f}"
        )

    def on_data(self, data: Slice):
        self._roll_risk_day()
        self._refresh_event_state()
        if self._portfolio_daily_loss_breached():
            self._activate_master_kill_switch("master_daily_loss_kill")
        if self.master_trading_disabled():
            return

        self.core.on_data()
        self.intraday.on_data(data)
        self.event_sleeve.on_data(data)

    def on_order_event(self, order_event: OrderEvent):
        if order_event.status != OrderStatus.FILLED:
            return
        security = self.algo.securities[order_event.symbol]
        order = self.algo.transactions.get_order_by_id(order_event.order_id)
        order_tag = order.tag if order is not None else "-"
        self.algo.log(
            f"[ORDER] symbol={order_event.symbol.value} "
            f"qty={order_event.fill_quantity:.0f} "
            f"price={order_event.fill_price:.2f} "
            f"tag={order_tag} "
            f"holdings={security.holdings.quantity:.0f}"
        )

    def on_end_of_algorithm(self):
        self.algo.log(
            "[CLOUD_MASTER] final "
            f"equity={self.algo.portfolio.total_portfolio_value:.2f} "
            f"cash={self.algo.portfolio.cash:.2f} "
            f"master_kill_reason={self.master_kill_reason or '-'} "
            f"event_count={self.event_state_count} "
            f"event_tickers={','.join(self.event_state_active_tickers) or 'none'} "
            f"event_sleeve_active={','.join(sorted(self.event_sleeve.days_remaining.keys())) or 'none'}"
        )
