from __future__ import annotations

from textwrap import dedent, indent

from orchestrator.schemas import CandidateSpec


def _slippage_setup_line(var_name: str, spec: CandidateSpec, indent_spaces: int = 16) -> str:
    slippage_bps = float(spec.parameters.get("slippage_bps", 0.0))
    if slippage_bps <= 0:
        return ""
    slippage_pct = slippage_bps / 10000.0
    return " " * indent_spaces + f"{var_name}.set_slippage_model(ConstantSlippageModel({slippage_pct}))\n"


def render_strategy(spec: CandidateSpec) -> str:
    if spec.family == "buy_and_hold":
        return _render_buy_and_hold(spec)
    if spec.family == "equal_weight_buy_and_hold":
        return _render_equal_weight_buy_and_hold(spec)
    if spec.family == "sma_crossover":
        return _render_sma_crossover(spec)
    if spec.family == "sma_regime":
        return _render_sma_regime(spec)
    if spec.family == "donchian_regime":
        return _render_donchian_regime(spec)
    if spec.family == "dual_momentum":
        return _render_dual_momentum(spec)
    if spec.family == "rotation_rsi":
        return _render_rotation_rsi(spec)
    if spec.family == "gap_reversal_intraday":
        return _render_gap_reversal_intraday(spec)
    if spec.family == "day2_breakout_intraday":
        return _render_day2_breakout_intraday(spec)
    if spec.family == "bsl_reversal_intraday":
        return _render_bsl_reversal_intraday(spec)
    if spec.family == "gap_reversal_scanner_intraday":
        return _render_gap_reversal_scanner_intraday(spec)
    if spec.family == "bsl_reversal_scanner_intraday":
        return _render_bsl_reversal_scanner_intraday(spec)
    if spec.family == "regime_router_scanner_intraday":
        return _render_regime_router_scanner_intraday(spec)
    if spec.family == "vwap_reclaim_scanner_intraday":
        return _render_vwap_reclaim_scanner_intraday(spec)
    if spec.family == "failed_breakdown_reclaim_scanner_intraday":
        return _render_failed_breakdown_reclaim_scanner_intraday(spec)
    raise ValueError(f"Unsupported strategy family: {spec.family}")


def _render_buy_and_hold(spec: CandidateSpec) -> str:
    symbol = spec.symbols[0]
    position_size = float(spec.parameters.get("position_size", 1.0))
    slippage_line = _slippage_setup_line("security", spec)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                security = self.add_equity("{symbol}", Resolution.DAILY)
{slippage_line}                self.symbol = security.symbol
                self._entered = False

            def on_data(self, data: Slice):
                if self._entered:
                    return
                if self.symbol not in data.bars:
                    return

                self.set_holdings(self.symbol, {position_size})
                self._entered = True
        """
    )


def _render_equal_weight_buy_and_hold(spec: CandidateSpec) -> str:
    symbol_list = ", ".join(f'"{symbol}"' for symbol in spec.symbols)
    total_size = float(spec.parameters.get("position_size", 1.0))
    weight = total_size / max(len(spec.symbols), 1)
    slippage_line = _slippage_setup_line("security", spec, indent_spaces=20)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                self.symbols = []
                for ticker in [{symbol_list}]:
                    security = self.add_equity(ticker, Resolution.DAILY)
{slippage_line}                    self.symbols.append(security.symbol)
                self.target_weight = {weight}
                self._entered = False

            def on_data(self, data: Slice):
                if self._entered:
                    return
                if any(symbol not in data.bars for symbol in self.symbols):
                    return

                for symbol in self.symbols:
                    self.set_holdings(symbol, self.target_weight, True)
                self._entered = True
        """
    )


def _render_sma_crossover(spec: CandidateSpec) -> str:
    symbol = spec.symbols[0]
    fast = int(spec.parameters["fast"])
    slow = int(spec.parameters["slow"])
    slippage_line = _slippage_setup_line("security", spec)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                security = self.add_equity("{symbol}", Resolution.DAILY)
{slippage_line}                self.symbol = security.symbol
                self.fast = self.sma(self.symbol, {fast}, Resolution.DAILY)
                self.slow = self.sma(self.symbol, {slow}, Resolution.DAILY)
                self.set_warm_up({slow}, Resolution.DAILY)
                self._prev_above = None

            def on_data(self, data: Slice):
                if self.is_warming_up:
                    return
                if not (self.fast.is_ready and self.slow.is_ready):
                    return
                if self.symbol not in data.bars:
                    return

                above = self.fast.current.value > self.slow.current.value
                if self._prev_above is None:
                    self._prev_above = above
                    if above:
                        self.set_holdings(self.symbol, 1.0)
                    return

                if above != self._prev_above:
                    if above:
                        self.set_holdings(self.symbol, 1.0)
                    else:
                        self.liquidate(self.symbol)

                self._prev_above = above
        """
    )


def _render_dual_momentum(spec: CandidateSpec) -> str:
    lookback = int(spec.parameters.get("lookback", 126))
    rebalance_days = int(spec.parameters.get("rebalance_days", 21))
    position_size = float(spec.parameters.get("position_size", 1.0))
    offensive_a, offensive_b, defensive = spec.symbols
    slippage_a = _slippage_setup_line("security_a", spec)
    slippage_b = _slippage_setup_line("security_b", spec)
    slippage_def = _slippage_setup_line("security_def", spec)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        from datetime import timedelta
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                security_a = self.add_equity("{offensive_a}", Resolution.DAILY)
{slippage_a}                self.offensive_a = security_a.symbol
                security_b = self.add_equity("{offensive_b}", Resolution.DAILY)
{slippage_b}                self.offensive_b = security_b.symbol
                security_def = self.add_equity("{defensive}", Resolution.DAILY)
{slippage_def}                self.defensive = security_def.symbol

                self.roc_a = self.roc(self.offensive_a, {lookback}, Resolution.DAILY)
                self.roc_b = self.roc(self.offensive_b, {lookback}, Resolution.DAILY)
                self.roc_def = self.roc(self.defensive, {lookback}, Resolution.DAILY)
                self.set_warm_up({lookback}, Resolution.DAILY)

                self.rebalance_days = {rebalance_days}
                self.position_size = {position_size}
                self.current_target = None
                self.pending_target = None
                self.next_rebalance_date = None

            def on_data(self, data: Slice):
                if self.is_warming_up:
                    return
                if not (self.roc_a.is_ready and self.roc_b.is_ready and self.roc_def.is_ready):
                    return
                if self.offensive_a not in data.bars or self.offensive_b not in data.bars or self.defensive not in data.bars:
                    return

                invested_symbols = [
                    symbol for symbol in [self.offensive_a, self.offensive_b, self.defensive]
                    if self.portfolio[symbol].invested
                ]
                current_invested = invested_symbols[0] if invested_symbols else None

                if self.pending_target is not None:
                    if current_invested is None:
                        self.set_holdings(self.pending_target, self.position_size)
                        self.current_target = self.pending_target
                        self.pending_target = None
                    return

                if self.next_rebalance_date is not None and self.time.date() < self.next_rebalance_date:
                    return

                scores = {{
                    self.offensive_a: self.roc_a.current.value,
                    self.offensive_b: self.roc_b.current.value,
                }}
                best_offensive = max(scores, key=scores.get)
                best_offensive_score = scores[best_offensive]
                defensive_score = self.roc_def.current.value

                if best_offensive_score > 0 and best_offensive_score >= defensive_score:
                    target = best_offensive
                elif defensive_score > 0:
                    target = self.defensive
                else:
                    target = None

                if target != current_invested:
                    if target is None:
                        self.liquidate()
                        self.current_target = None
                    elif current_invested is None:
                        self.set_holdings(target, self.position_size, True)
                        self.current_target = target
                    else:
                        self.pending_target = target
                        self.current_target = None
                        self.liquidate()
                else:
                    self.current_target = current_invested

                self.next_rebalance_date = self.time.date() + timedelta(days=self.rebalance_days)
        """
    )


def _render_sma_regime(spec: CandidateSpec) -> str:
    symbol = spec.symbols[0]
    fast = int(spec.parameters["fast"])
    slow = int(spec.parameters["slow"])
    entry_buffer_pct = float(spec.parameters.get("entry_buffer_pct", 0.0))
    trailing_stop_pct = float(spec.parameters.get("trailing_stop_pct", 0.0))
    max_holding_days = int(spec.parameters.get("max_holding_days", 0))
    cooldown_days = int(spec.parameters.get("cooldown_days", 0))
    position_size = float(spec.parameters.get("position_size", 1.0))
    slippage_line = _slippage_setup_line("security", spec)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        from datetime import timedelta
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                security = self.add_equity("{symbol}", Resolution.DAILY)
{slippage_line}                self.symbol = security.symbol
                self.fast = self.sma(self.symbol, {fast}, Resolution.DAILY)
                self.slow = self.sma(self.symbol, {slow}, Resolution.DAILY)
                self.set_warm_up({slow}, Resolution.DAILY)

                self.entry_buffer_pct = {entry_buffer_pct}
                self.trailing_stop_pct = {trailing_stop_pct}
                self.max_holding_days = {max_holding_days}
                self.cooldown_days = {cooldown_days}
                self.position_size = {position_size}

                self.entry_date = None
                self.highest_close = None
                self.cooldown_until = None

            def on_data(self, data: Slice):
                if self.is_warming_up:
                    return
                if not (self.fast.is_ready and self.slow.is_ready):
                    return
                if self.symbol not in data.bars:
                    return

                close = data.bars[self.symbol].close
                slow_value = self.slow.current.value
                if slow_value <= 0:
                    return

                above = self.fast.current.value > slow_value
                spread_pct = (self.fast.current.value / slow_value) - 1.0
                invested = self.portfolio[self.symbol].invested

                if invested:
                    self.highest_close = close if self.highest_close is None else max(self.highest_close, close)
                    exit_reason = None

                    if self.trailing_stop_pct > 0 and close <= self.highest_close * (1.0 - self.trailing_stop_pct):
                        exit_reason = "trailing_stop"
                    elif self.max_holding_days > 0 and self.entry_date is not None:
                        if (self.time.date() - self.entry_date).days >= self.max_holding_days:
                            exit_reason = "time_stop"
                    elif not above:
                        exit_reason = "trend_exit"

                    if exit_reason is not None:
                        self.liquidate(self.symbol, tag=exit_reason)
                        self.entry_date = None
                        self.highest_close = None
                        if self.cooldown_days > 0:
                            self.cooldown_until = self.time.date() + timedelta(days=self.cooldown_days)
                        return

                if invested:
                    return

                if self.cooldown_until is not None and self.time.date() < self.cooldown_until:
                    return

                if above and spread_pct >= self.entry_buffer_pct:
                    self.set_holdings(self.symbol, self.position_size)
                    self.entry_date = self.time.date()
                    self.highest_close = close
        """
    )


def _render_donchian_regime(spec: CandidateSpec) -> str:
    symbol = spec.symbols[0]
    entry_lookback = int(spec.parameters["entry_lookback"])
    exit_lookback = int(spec.parameters["exit_lookback"])
    trailing_stop_pct = float(spec.parameters.get("trailing_stop_pct", 0.0))
    max_holding_days = int(spec.parameters.get("max_holding_days", 0))
    position_size = float(spec.parameters.get("position_size", 1.0))
    slippage_line = _slippage_setup_line("security", spec)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        from collections import deque
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                security = self.add_equity("{symbol}", Resolution.DAILY)
{slippage_line}                self.symbol = security.symbol
                self.entry_lookback = {entry_lookback}
                self.exit_lookback = {exit_lookback}
                self.trailing_stop_pct = {trailing_stop_pct}
                self.max_holding_days = {max_holding_days}
                self.position_size = {position_size}
                self.set_warm_up(max(self.entry_lookback, self.exit_lookback), Resolution.DAILY)

                self.entry_date = None
                self.highest_close = None
                self.previous_highs = deque(maxlen=self.entry_lookback)
                self.previous_lows = deque(maxlen=self.exit_lookback)

            def on_data(self, data: Slice):
                if self.symbol not in data.bars:
                    return

                bar = data.bars[self.symbol]
                close = bar.close
                breakout_level = max(self.previous_highs) if len(self.previous_highs) == self.entry_lookback else None
                exit_level = min(self.previous_lows) if len(self.previous_lows) == self.exit_lookback else None

                if self.is_warming_up:
                    self.previous_highs.append(bar.high)
                    self.previous_lows.append(bar.low)
                    return

                invested = self.portfolio[self.symbol].invested
                if invested:
                    self.highest_close = close if self.highest_close is None else max(self.highest_close, close)
                    exit_reason = None

                    if self.trailing_stop_pct > 0 and close <= self.highest_close * (1.0 - self.trailing_stop_pct):
                        exit_reason = "trailing_stop"
                    elif self.max_holding_days > 0 and self.entry_date is not None:
                        if (self.time.date() - self.entry_date).days >= self.max_holding_days:
                            exit_reason = "time_stop"
                    elif exit_level is not None and close < exit_level:
                        exit_reason = "channel_exit"

                    if exit_reason is not None:
                        self.liquidate(self.symbol, tag=exit_reason)
                        self.entry_date = None
                        self.highest_close = None

                if (not invested) and breakout_level is not None and close > breakout_level:
                    self.set_holdings(self.symbol, self.position_size)
                    self.entry_date = self.time.date()
                    self.highest_close = close

                self.previous_highs.append(bar.high)
                self.previous_lows.append(bar.low)
        """
    )


def _render_rotation_rsi(spec: CandidateSpec) -> str:
    high = float(spec.parameters["high_rsi"])
    low = float(spec.parameters["low_rsi"])
    qqq_weight = float(spec.parameters.get("neutral_qqq_weight", 0.5))
    voo_weight = float(spec.parameters.get("neutral_voo_weight", 0.5))
    qqq_symbol, voo_symbol = spec.symbols
    slippage_qqq = _slippage_setup_line("qqq_security", spec)
    slippage_voo = _slippage_setup_line("voo_security", spec)
    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            HIGH_RSI = {high}
            LOW_RSI = {low}

            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                qqq_security = self.add_equity("{qqq_symbol}", Resolution.DAILY)
{slippage_qqq}                self.qqq = qqq_security.symbol
                voo_security = self.add_equity("{voo_symbol}", Resolution.DAILY)
{slippage_voo}                self.voo = voo_security.symbol
                self._rsi = self.rsi(self.qqq, 14, MovingAverageType.WILDERS, Resolution.DAILY)
                self.set_warm_up(20, Resolution.DAILY)
                self._regime = None

            def on_data(self, data: Slice):
                if self.is_warming_up or not self._rsi.is_ready:
                    return
                if self.qqq not in data.bars or self.voo not in data.bars:
                    return

                rsi_val = self._rsi.current.value
                if rsi_val > self.HIGH_RSI:
                    regime = "voo"
                elif rsi_val < self.LOW_RSI:
                    regime = "qqq"
                else:
                    regime = "neutral"

                if regime == self._regime:
                    return

                self._regime = regime
                if regime == "voo":
                    self.set_holdings(self.qqq, 0.0)
                    self.set_holdings(self.voo, 1.0)
                elif regime == "qqq":
                    self.set_holdings(self.voo, 0.0)
                    self.set_holdings(self.qqq, 1.0)
                else:
                    self.set_holdings(self.qqq, {qqq_weight})
                    self.set_holdings(self.voo, {voo_weight})
        """
    )


def _render_intraday_single_symbol_long(
    spec: CandidateSpec,
    *,
    qualification_code: str,
    entry_code: str,
    min_history_days: int,
) -> str:
    symbol = spec.symbols[0]
    opening_range_minutes = int(spec.parameters.get("opening_range_minutes", 5))
    max_entry_minutes = int(spec.parameters.get("max_entry_minutes", 90))
    force_exit_minutes_before_close = int(spec.parameters.get("force_exit_minutes_before_close", 5))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    risk_reward = float(spec.parameters.get("risk_reward", 2.0))
    stop_buffer_pct = float(spec.parameters.get("stop_buffer_pct", 0.001))
    position_size = float(spec.parameters.get("position_size", 1.0))
    risk_per_trade_pct = float(spec.parameters.get("risk_per_trade_pct", 0.0))
    max_daily_loss_pct = float(spec.parameters.get("max_daily_loss_pct", 0.0))
    max_daily_trades = int(spec.parameters.get("max_daily_trades", 0))
    max_holding_minutes = int(spec.parameters.get("max_holding_minutes", 0))
    use_vwap_exit = bool(spec.parameters.get("use_vwap_exit", True))
    slippage_line = _slippage_setup_line("security", spec)

    qualification_block = indent(dedent(qualification_code).strip(), " " * 16)
    entry_block = indent(dedent(entry_code).strip(), " " * 16)

    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        from datetime import time
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                security = self.add_equity("{symbol}", Resolution.MINUTE, extended_market_hours=True)
{slippage_line}                self.symbol = security.symbol

                self.position_size = {position_size}
                self.opening_range_minutes = {opening_range_minutes}
                self.max_entry_minutes = {max_entry_minutes}
                self.force_exit_minutes_before_close = {force_exit_minutes_before_close}
                self.volume_lookback_days = {volume_lookback_days}
                self.risk_reward = {risk_reward}
                self.stop_buffer_pct = {stop_buffer_pct}
                self.risk_per_trade_pct = {risk_per_trade_pct}
                self.max_daily_loss_pct = {max_daily_loss_pct}
                self.max_daily_trades = {max_daily_trades}
                self.min_history_days = {min_history_days}
                self.max_daily_history = max(self.min_history_days + 10, self.volume_lookback_days + 10, 40)
                self.max_holding_minutes = {max_holding_minutes}
                self.use_vwap_exit = {str(use_vwap_exit)}

                self.current_day = None
                self.daily_summaries = []
                self.entry_price = None
                self.stop_price = None
                self.target_price = None
                self.entry_time = None
                self.daily_start_equity = float(self.portfolio.total_portfolio_value)
                self.daily_entry_count = 0
                self._reset_intraday_state()

            def _reset_intraday_state(self):
                self.premarket_high = None
                self.premarket_low = None
                self.premarket_volume = 0.0

                self.regular_open = None
                self.regular_high = None
                self.regular_low = None
                self.regular_close = None
                self.regular_volume = 0.0

                self.opening_range_high = None
                self.opening_range_low = None
                self.session_high = None
                self.session_low = None

                self.vwap_price_volume = 0.0
                self.vwap_volume = 0.0

                self.trade_taken = False
                self.day_qualified = None
                self.prev_day = None
                self.avg_volume = 0.0
                self.gap_pct = 0.0
                self.premarket_vol_ratio = 0.0
                self.prev_day_return = 0.0
                self.prev_close_position = 0.0
                self.key_level = None
                self.pullback_seen = False
                self.flush_seen = False

                self.entry_price = None
                self.stop_price = None
                self.target_price = None
                self.entry_time = None
                self.daily_start_equity = float(self.portfolio.total_portfolio_value)
                self.daily_entry_count = 0

            def _roll_day(self, new_date):
                if self.current_day is not None and self.regular_open is not None and self.regular_close is not None:
                    summary = {{
                        "date": self.current_day,
                        "open": self.regular_open,
                        "high": self.regular_high,
                        "low": self.regular_low,
                        "close": self.regular_close,
                        "volume": self.regular_volume,
                    }}
                    self.daily_summaries.append(summary)
                    if len(self.daily_summaries) > self.max_daily_history:
                        self.daily_summaries = self.daily_summaries[-self.max_daily_history:]

                self.current_day = new_date
                self._reset_intraday_state()

            def _is_premarket(self):
                current_time = self.time.time()
                return time(4, 0) <= current_time < time(9, 30)

            def _is_regular(self):
                current_time = self.time.time()
                return time(9, 30) <= current_time < time(16, 0)

            def _minutes_from_open(self):
                return (self.time.hour * 60 + self.time.minute) - (9 * 60 + 30)

            def _minutes_to_close(self):
                return (16 * 60) - (self.time.hour * 60 + self.time.minute)

            def _session_vwap(self):
                if self.vwap_volume <= 0:
                    return self.regular_close or 0.0
                return self.vwap_price_volume / self.vwap_volume

            def _daily_loss_breached(self):
                if self.max_daily_loss_pct <= 0 or self.daily_start_equity <= 0:
                    return False
                return float(self.portfolio.total_portfolio_value) <= self.daily_start_equity * (1.0 - self.max_daily_loss_pct)

            def _entries_available(self):
                if self.max_daily_trades > 0 and self.daily_entry_count >= self.max_daily_trades:
                    return False
                if self._daily_loss_breached():
                    return False
                return True

            def _avg_regular_volume(self, lookback_days):
                if len(self.daily_summaries) < lookback_days:
                    return 0.0
                sample = self.daily_summaries[-lookback_days:]
                return sum(item["volume"] for item in sample) / float(lookback_days)

            def _recent_return(self, lookback_days):
                if len(self.daily_summaries) < lookback_days + 1:
                    return 0.0
                start_close = self.daily_summaries[-(lookback_days + 1)]["close"]
                end_close = self.daily_summaries[-1]["close"]
                if start_close <= 0:
                    return 0.0
                return (end_close / start_close) - 1.0

            def _qualifies_today(self):
                if self.day_qualified is not None:
                    return self.day_qualified

{qualification_block}

            def _enter_long(self, price, stop_reference, tag):
                if stop_reference is None:
                    return
                if not self._entries_available():
                    return
                stop_price = stop_reference * (1.0 - self.stop_buffer_pct)
                risk = price - stop_price
                if risk <= max(price * 0.001, 0.01):
                    return

                if self.risk_per_trade_pct > 0:
                    portfolio_value = float(self.portfolio.total_portfolio_value)
                    risk_budget = portfolio_value * self.risk_per_trade_pct
                    max_notional = portfolio_value * self.position_size
                    quantity = int(min(risk_budget / risk, max_notional / price))
                    if quantity <= 0:
                        return
                    self.market_order(self.symbol, quantity, tag=tag)
                else:
                    self.set_holdings(self.symbol, self.position_size, True)
                self.entry_price = price
                self.stop_price = stop_price
                self.target_price = price + risk * self.risk_reward if self.risk_reward > 0 else None
                self.entry_time = self.time
                self.trade_taken = True
                self.daily_entry_count += 1

            def _manage_position(self, bar):
                if not self.portfolio[self.symbol].invested:
                    return False

                price = bar.close
                if self._daily_loss_breached():
                    self.liquidate(self.symbol, tag="daily_loss_kill")
                    return True

                if self.stop_price is not None and price <= self.stop_price:
                    self.liquidate(self.symbol, tag="stop_loss")
                    return True

                if self.target_price is not None and price >= self.target_price:
                    self.liquidate(self.symbol, tag="profit_target")
                    return True

                if self.entry_time is not None and self.max_holding_minutes > 0:
                    held_minutes = (self.time - self.entry_time).total_seconds() / 60.0
                    if held_minutes >= self.max_holding_minutes:
                        self.liquidate(self.symbol, tag="time_exit")
                        return True

                if self._minutes_to_close() <= self.force_exit_minutes_before_close:
                    self.liquidate(self.symbol, tag="eod_exit")
                    return True

                if self.use_vwap_exit:
                    vwap = self._session_vwap()
                    if vwap > 0 and price < vwap:
                        self.liquidate(self.symbol, tag="vwap_loss")
                        return True

                return False

            def _maybe_enter(self, bar):
{entry_block}

            def on_data(self, data: Slice):
                if self.symbol not in data.bars:
                    return

                if self.current_day != self.time.date():
                    self._roll_day(self.time.date())

                bar = data.bars[self.symbol]

                if self._is_premarket():
                    self.premarket_high = bar.high if self.premarket_high is None else max(self.premarket_high, bar.high)
                    self.premarket_low = bar.low if self.premarket_low is None else min(self.premarket_low, bar.low)
                    self.premarket_volume += float(bar.volume)
                    return

                if not self._is_regular():
                    if self.portfolio[self.symbol].invested and self._minutes_to_close() <= self.force_exit_minutes_before_close:
                        self.liquidate(self.symbol, tag="eod_exit")
                    return

                self.regular_open = bar.open if self.regular_open is None else self.regular_open
                self.regular_high = bar.high if self.regular_high is None else max(self.regular_high, bar.high)
                self.regular_low = bar.low if self.regular_low is None else min(self.regular_low, bar.low)
                self.regular_close = bar.close
                self.regular_volume += float(bar.volume)

                self.session_high = bar.high if self.session_high is None else max(self.session_high, bar.high)
                self.session_low = bar.low if self.session_low is None else min(self.session_low, bar.low)
                self.vwap_price_volume += float(bar.close) * float(bar.volume)
                self.vwap_volume += float(bar.volume)

                minutes_from_open = self._minutes_from_open()
                if minutes_from_open < self.opening_range_minutes:
                    self.opening_range_high = bar.high if self.opening_range_high is None else max(self.opening_range_high, bar.high)
                    self.opening_range_low = bar.low if self.opening_range_low is None else min(self.opening_range_low, bar.low)

                if self._manage_position(bar):
                    return

                if self.trade_taken:
                    return

                if minutes_from_open < self.opening_range_minutes:
                    return

                if minutes_from_open > self.max_entry_minutes:
                    return

                if len(self.daily_summaries) < self.min_history_days:
                    return

                if not self._entries_available():
                    return

                if not self._qualifies_today():
                    return

                self._maybe_enter(bar)
        """
    )


def _render_gap_reversal_intraday(spec: CandidateSpec) -> str:
    gap_up_pct_min = float(spec.parameters.get("gap_up_pct_min", 0.03))
    gap_up_pct_max = float(spec.parameters.get("gap_up_pct_max", 0.20))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.01))
    opening_pullback_pct = float(spec.parameters.get("opening_pullback_pct", 0.01))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))

    qualification_code = f"""
if len(self.daily_summaries) < self.min_history_days:
    self.day_qualified = False
    return False

self.prev_day = self.daily_summaries[-1]
self.avg_volume = self._avg_regular_volume(self.volume_lookback_days)
if self.avg_volume <= 0 or self.regular_open is None or self.prev_day["close"] <= 0:
    self.day_qualified = False
    return False

self.gap_pct = (self.regular_open / self.prev_day["close"]) - 1.0
self.premarket_vol_ratio = self.premarket_volume / self.avg_volume
self.day_qualified = (
    {gap_up_pct_min} <= self.gap_pct <= {gap_up_pct_max}
    and self.premarket_vol_ratio >= {premarket_vol_ratio_min}
)
return self.day_qualified
"""

    entry_code = f"""
if self.session_low is None or self.regular_open is None or self.opening_range_high is None or self.opening_range_low is None:
    return

if self.session_low <= self.regular_open * (1.0 - {opening_pullback_pct}):
    self.pullback_seen = True

if not self.pullback_seen:
    return

price = bar.close
vwap = self._session_vwap()
if vwap <= 0 or price <= vwap or price <= self.opening_range_high:
    return

stop_reference = min(self.session_low, self.opening_range_low)
self._enter_long(price, stop_reference, "gap_reversal_entry")
"""

    return _render_intraday_single_symbol_long(
        spec,
        qualification_code=qualification_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, 5),
    )


def _render_day2_breakout_intraday(spec: CandidateSpec) -> str:
    prior_day_return_min = float(spec.parameters.get("prior_day_return_min", 0.05))
    prior_day_close_position_min = float(spec.parameters.get("prior_day_close_position_min", 0.75))
    prior_day_volume_ratio_min = float(spec.parameters.get("prior_day_volume_ratio_min", 1.5))
    today_gap_min = float(spec.parameters.get("today_gap_min", -0.02))
    today_gap_max = float(spec.parameters.get("today_gap_max", 0.12))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.008))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))

    qualification_code = f"""
if len(self.daily_summaries) < self.min_history_days:
    self.day_qualified = False
    return False

self.prev_day = self.daily_summaries[-1]
self.avg_volume = self._avg_regular_volume(self.volume_lookback_days)
prev_range = max(self.prev_day["high"] - self.prev_day["low"], 0.01)
if self.avg_volume <= 0 or self.regular_open is None or self.prev_day["open"] <= 0 or self.prev_day["close"] <= 0:
    self.day_qualified = False
    return False

self.prev_day_return = (self.prev_day["close"] / self.prev_day["open"]) - 1.0
self.prev_close_position = (self.prev_day["close"] - self.prev_day["low"]) / prev_range
self.gap_pct = (self.regular_open / self.prev_day["close"]) - 1.0
self.premarket_vol_ratio = self.premarket_volume / self.avg_volume
self.day_qualified = (
    self.prev_day_return >= {prior_day_return_min}
    and self.prev_close_position >= {prior_day_close_position_min}
    and self.prev_day["volume"] >= self.avg_volume * {prior_day_volume_ratio_min}
    and {today_gap_min} <= self.gap_pct <= {today_gap_max}
    and self.premarket_vol_ratio >= {premarket_vol_ratio_min}
)
return self.day_qualified
"""

    entry_code = """
levels = [level for level in [self.premarket_high, self.opening_range_high] if level is not None]
if not levels or self.opening_range_low is None:
    return

breakout_level = max(levels)
price = bar.close
vwap = self._session_vwap()
if vwap <= 0 or price <= vwap or price <= breakout_level:
    return

stop_reference = min(self.opening_range_low, vwap)
self._enter_long(price, stop_reference, "day2_breakout_entry")
"""

    return _render_intraday_single_symbol_long(
        spec,
        qualification_code=qualification_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, 2),
    )


def _render_bsl_reversal_intraday(spec: CandidateSpec) -> str:
    downtrend_lookback_days = int(spec.parameters.get("downtrend_lookback_days", 20))
    downtrend_return_max = float(spec.parameters.get("downtrend_return_max", -0.08))
    gap_min = float(spec.parameters.get("gap_min", -0.01))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.006))
    morning_flush_pct = float(spec.parameters.get("morning_flush_pct", 0.005))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))

    qualification_code = f"""
if len(self.daily_summaries) < self.min_history_days:
    self.day_qualified = False
    return False

self.prev_day = self.daily_summaries[-1]
self.avg_volume = self._avg_regular_volume(self.volume_lookback_days)
if self.avg_volume <= 0 or self.regular_open is None or self.prev_day["close"] <= 0:
    self.day_qualified = False
    return False

self.gap_pct = (self.regular_open / self.prev_day["close"]) - 1.0
self.premarket_vol_ratio = self.premarket_volume / self.avg_volume
self.key_level = max(self.prev_day["high"], self.prev_day["close"])
downtrend_return = self._recent_return({downtrend_lookback_days})
self.day_qualified = (
    downtrend_return <= {downtrend_return_max}
    and self.gap_pct >= {gap_min}
    and self.premarket_vol_ratio >= {premarket_vol_ratio_min}
)
return self.day_qualified
"""

    entry_code = f"""
if self.session_low is None or self.regular_open is None or self.key_level is None or self.opening_range_low is None:
    return

if self.session_low <= self.regular_open * (1.0 - {morning_flush_pct}):
    self.flush_seen = True

if not self.flush_seen:
    return

levels = [level for level in [self.key_level, self.opening_range_high] if level is not None]
if not levels:
    return

breakout_level = max(levels)
price = bar.close
vwap = self._session_vwap()
if vwap <= 0 or price <= vwap or price <= breakout_level:
    return

stop_reference = min(self.session_low, self.opening_range_low, self.prev_day["close"])
self._enter_long(price, stop_reference, "bsl_reversal_entry")
"""

    return _render_intraday_single_symbol_long(
        spec,
        qualification_code=qualification_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, downtrend_lookback_days + 1),
    )


def _render_intraday_scanner_long(
    spec: CandidateSpec,
    *,
    qualification_code: str,
    rank_score_code: str,
    entry_code: str,
    min_history_days: int,
) -> str:
    symbol_list = ", ".join(f'"{symbol}"' for symbol in spec.symbols)
    context_symbols = [str(symbol) for symbol in spec.parameters.get("context_symbols", [])]
    context_symbol_list = ", ".join(f'"{symbol}"' for symbol in context_symbols)
    opening_range_minutes = int(spec.parameters.get("opening_range_minutes", 5))
    max_entry_minutes = int(spec.parameters.get("max_entry_minutes", 90))
    force_exit_minutes_before_close = int(spec.parameters.get("force_exit_minutes_before_close", 5))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    risk_reward = float(spec.parameters.get("risk_reward", 2.0))
    stop_buffer_pct = float(spec.parameters.get("stop_buffer_pct", 0.001))
    position_size = float(spec.parameters.get("position_size", 1.0))
    risk_per_trade_pct = float(spec.parameters.get("risk_per_trade_pct", 0.0))
    max_daily_loss_pct = float(spec.parameters.get("max_daily_loss_pct", 0.0))
    max_daily_trades = int(spec.parameters.get("max_daily_trades", 0))
    confirm_hold_minutes = int(spec.parameters.get("confirm_hold_minutes", 3))
    max_holding_minutes = int(spec.parameters.get("max_holding_minutes", 180))
    use_vwap_exit = bool(spec.parameters.get("use_vwap_exit", True))
    selection_pool_size = int(spec.parameters.get("selection_pool_size", 1))
    min_prev_close = float(spec.parameters.get("min_prev_close", 20.0))
    max_prev_close = float(spec.parameters.get("max_prev_close", 2000.0))
    min_avg_dollar_volume = float(spec.parameters.get("min_avg_dollar_volume", 250000000.0))
    min_premarket_dollar_volume = float(spec.parameters.get("min_premarket_dollar_volume", 1000000.0))
    rank_relative_premarket_dollar_volume_weight = float(
        spec.parameters.get("rank_relative_premarket_dollar_volume_weight", 0.0)
    )
    rank_relative_key_level_distance_weight = float(
        spec.parameters.get("rank_relative_key_level_distance_weight", 0.0)
    )
    context_require_above_vwap = bool(spec.parameters.get("context_require_above_vwap", True))
    context_require_above_open = bool(spec.parameters.get("context_require_above_open", True))
    context_min_positive = int(spec.parameters.get("context_min_positive", len(context_symbols)))
    regime_symbols = [str(symbol) for symbol in spec.parameters.get("regime_symbols", [])]
    regime_symbol_list = ", ".join(f'"{symbol}"' for symbol in regime_symbols)
    regime_lookback_days = int(spec.parameters.get("regime_lookback_days", 0))
    regime_return_min = float(spec.parameters.get("regime_return_min", 0.0))
    regime_min_positive = int(spec.parameters.get("regime_min_positive", len(regime_symbols) if regime_symbols else 0))

    qualification_block = indent(dedent(qualification_code).strip(), " " * 16)
    rank_score_block = indent(dedent(rank_score_code).strip(), " " * 16)
    entry_block = indent(dedent(entry_code).strip(), " " * 16)
    slippage_line = _slippage_setup_line("security", spec, indent_spaces=20)

    return dedent(
        f"""\
        # region imports
        from AlgorithmImports import *
        from datetime import timedelta, time
        # endregion


        class GeneratedStrategy(QCAlgorithm):
            def initialize(self):
                self.set_start_date(*map(int, "{spec.start_date}".split("-")))
                self.set_end_date(*map(int, "{spec.end_date}".split("-")))
                self.set_cash({spec.cash})

                self.symbol_by_ticker = {{}}
                for ticker in [{symbol_list}{", " if context_symbol_list else ""}{context_symbol_list}{", " if regime_symbol_list else ""}{regime_symbol_list}]:
                    if ticker in self.symbol_by_ticker:
                        continue
                    security = self.add_equity(
                        ticker,
                        Resolution.MINUTE,
                        extended_market_hours=True,
                    )
{slippage_line}                    self.symbol_by_ticker[ticker] = security.symbol

                self.tradable_symbols = [self.symbol_by_ticker[ticker] for ticker in [{symbol_list}]]
                self.context_symbols = [self.symbol_by_ticker[ticker] for ticker in [{context_symbol_list}]]
                self.regime_symbols = [self.symbol_by_ticker[ticker] for ticker in [{regime_symbol_list}]]
                self.symbols = list(self.symbol_by_ticker.values())

                self.position_size = {position_size}
                self.opening_range_minutes = {opening_range_minutes}
                self.max_entry_minutes = {max_entry_minutes}
                self.force_exit_minutes_before_close = {force_exit_minutes_before_close}
                self.volume_lookback_days = {volume_lookback_days}
                self.risk_reward = {risk_reward}
                self.stop_buffer_pct = {stop_buffer_pct}
                self.risk_per_trade_pct = {risk_per_trade_pct}
                self.max_daily_loss_pct = {max_daily_loss_pct}
                self.max_daily_trades = {max_daily_trades}
                self.min_history_days = {min_history_days}
                self.max_daily_history = max(self.min_history_days + 10, self.volume_lookback_days + 10, 60)
                self.confirm_hold_minutes = {confirm_hold_minutes}
                self.max_holding_minutes = {max_holding_minutes}
                self.use_vwap_exit = {str(use_vwap_exit)}
                self.selection_pool_size = max({selection_pool_size}, 1)
                self.min_prev_close = {min_prev_close}
                self.max_prev_close = {max_prev_close}
                self.min_avg_dollar_volume = {min_avg_dollar_volume}
                self.min_premarket_dollar_volume = {min_premarket_dollar_volume}
                self.rank_relative_premarket_dollar_volume_weight = {rank_relative_premarket_dollar_volume_weight}
                self.rank_relative_key_level_distance_weight = {rank_relative_key_level_distance_weight}
                self.context_require_above_vwap = {str(context_require_above_vwap)}
                self.context_require_above_open = {str(context_require_above_open)}
                self.context_min_positive = {context_min_positive}
                self.regime_lookback_days = {regime_lookback_days}
                self.regime_return_min = {regime_return_min}
                self.regime_min_positive = {regime_min_positive}

                self.current_day = None
                self.daily_summaries = {{symbol: [] for symbol in self.symbols}}
                self.state = {{symbol: self._new_symbol_state() for symbol in self.symbols}}
                self.watchlist_symbols = []
                self.entry_symbol = None
                self.entry_price = None
                self.stop_price = None
                self.target_price = None
                self.entry_time = None
                self.trade_taken = False
                self.daily_start_equity = float(self.portfolio.total_portfolio_value)
                self.daily_entry_count = 0

            def _new_symbol_state(self):
                return {{
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
                    "pullback_seen": False,
                    "flush_seen": False,
                    "confirm_start": None,
                    "key_level": None,
                    "key_level_distance_pct": 0.0,
                    "prev_day": None,
                }}

            def _roll_day(self, new_date):
                if self.current_day is not None:
                    for symbol in self.symbols:
                        state = self.state[symbol]
                        if state["regular_open"] is not None and state["regular_close"] is not None:
                            summary = {{
                                "date": self.current_day,
                                "open": state["regular_open"],
                                "high": state["regular_high"],
                                "low": state["regular_low"],
                                "close": state["regular_close"],
                                "volume": state["regular_volume"],
                            }}
                            self.daily_summaries[symbol].append(summary)
                            if len(self.daily_summaries[symbol]) > self.max_daily_history:
                                self.daily_summaries[symbol] = self.daily_summaries[symbol][-self.max_daily_history:]

                self.current_day = new_date
                self.state = {{symbol: self._new_symbol_state() for symbol in self.symbols}}
                self.watchlist_symbols = []
                self.entry_symbol = None
                self.entry_price = None
                self.stop_price = None
                self.target_price = None
                self.entry_time = None
                self.trade_taken = False
                self.daily_start_equity = float(self.portfolio.total_portfolio_value)
                self.daily_entry_count = 0

            def _is_premarket(self):
                current_time = self.time.time()
                return time(4, 0) <= current_time < time(9, 30)

            def _is_regular(self):
                current_time = self.time.time()
                return time(9, 30) <= current_time < time(16, 0)

            def _minutes_from_open(self):
                return (self.time.hour * 60 + self.time.minute) - (9 * 60 + 30)

            def _minutes_to_close(self):
                return (16 * 60) - (self.time.hour * 60 + self.time.minute)

            def _session_vwap(self, symbol):
                state = self.state[symbol]
                if state["vwap_volume"] <= 0:
                    return state["regular_close"] or 0.0
                return state["vwap_price_volume"] / state["vwap_volume"]

            def _daily_loss_breached(self):
                if self.max_daily_loss_pct <= 0 or self.daily_start_equity <= 0:
                    return False
                return float(self.portfolio.total_portfolio_value) <= self.daily_start_equity * (1.0 - self.max_daily_loss_pct)

            def _entries_available(self):
                if self.max_daily_trades > 0 and self.daily_entry_count >= self.max_daily_trades:
                    return False
                if self._daily_loss_breached():
                    return False
                return True

            def _avg_regular_volume(self, symbol, lookback_days):
                history = self.daily_summaries[symbol]
                if len(history) < lookback_days:
                    return 0.0
                sample = history[-lookback_days:]
                return sum(item["volume"] for item in sample) / float(lookback_days)

            def _recent_return(self, symbol, lookback_days):
                history = self.daily_summaries[symbol]
                if len(history) < lookback_days + 1:
                    return 0.0
                start_close = history[-(lookback_days + 1)]["close"]
                end_close = history[-1]["close"]
                if start_close <= 0:
                    return 0.0
                return (end_close / start_close) - 1.0

            def _qualifies(self, symbol):
                state = self.state[symbol]
                if state["qualified"] is not None:
                    return state["qualified"]

{qualification_block}

            def _select_watchlist(self):
                candidates = []
                for symbol in self.tradable_symbols:
                    if self._qualifies(symbol):
                        score = self._rank_score(symbol)
                        if score is None:
                            continue
                        state = self.state[symbol]
                        candidates.append({{
                            "score": score,
                            "ticker": symbol.value,
                            "symbol": symbol,
                            "premarket_dollar_volume": float(state["premarket_dollar_volume"] or 0.0),
                            "key_level_distance_pct": float(state["key_level_distance_pct"] or 0.0),
                        }})
                if not candidates:
                    return []

                if self.rank_relative_premarket_dollar_volume_weight > 0 and len(candidates) > 1:
                    ranked = sorted(candidates, key=lambda item: (item["premarket_dollar_volume"], item["ticker"]))
                    denominator = max(len(ranked) - 1, 1)
                    for index, item in enumerate(ranked):
                        item["score"] *= 1.0 + self.rank_relative_premarket_dollar_volume_weight * (index / denominator)

                if self.rank_relative_key_level_distance_weight > 0 and len(candidates) > 1:
                    ranked = sorted(candidates, key=lambda item: (item["key_level_distance_pct"], item["ticker"]))
                    denominator = max(len(ranked) - 1, 1)
                    for index, item in enumerate(ranked):
                        item["score"] /= 1.0 + self.rank_relative_key_level_distance_weight * (index / denominator)

                # Keep watchlist selection stable when scores tie so symbol order does not leak into research results.
                candidates.sort(key=lambda item: (-item["score"], item["ticker"]))
                return [item["symbol"] for item in candidates[:self.selection_pool_size]]

            def _rank_score(self, symbol):
                state = self.state[symbol]
                if state["rank_score"] is not None:
                    return state["rank_score"]

{rank_score_block}

            def _enter_long(self, symbol, price, stop_reference, tag):
                if stop_reference is None:
                    return
                if not self._entries_available():
                    return
                stop_price = stop_reference * (1.0 - self.stop_buffer_pct)
                risk = price - stop_price
                if risk <= max(price * 0.001, 0.01):
                    return

                if self.risk_per_trade_pct > 0:
                    portfolio_value = float(self.portfolio.total_portfolio_value)
                    risk_budget = portfolio_value * self.risk_per_trade_pct
                    max_notional = portfolio_value * self.position_size
                    quantity = int(min(risk_budget / risk, max_notional / price))
                    if quantity <= 0:
                        return
                    self.market_order(symbol, quantity, tag=tag)
                else:
                    self.set_holdings(symbol, self.position_size, True)
                self.entry_symbol = symbol
                self.entry_price = price
                self.stop_price = stop_price
                self.target_price = price + risk * self.risk_reward if self.risk_reward > 0 else None
                self.entry_time = self.time
                self.trade_taken = True
                self.daily_entry_count += 1

            def _manage_position(self, symbol, bar):
                if self.entry_symbol != symbol or not self.portfolio[symbol].invested:
                    return False

                price = bar.close
                if self._daily_loss_breached():
                    self.liquidate(symbol, tag="daily_loss_kill")
                    return True

                if self.stop_price is not None and price <= self.stop_price:
                    self.liquidate(symbol, tag="stop_loss")
                    return True

                if self.target_price is not None and price >= self.target_price:
                    self.liquidate(symbol, tag="profit_target")
                    return True

                if self.entry_time is not None and self.max_holding_minutes > 0:
                    held_minutes = (self.time - self.entry_time).total_seconds() / 60.0
                    if held_minutes >= self.max_holding_minutes:
                        self.liquidate(symbol, tag="time_exit")
                        return True

                if self._minutes_to_close() <= self.force_exit_minutes_before_close:
                    self.liquidate(symbol, tag="eod_exit")
                    return True

                if self.use_vwap_exit:
                    vwap = self._session_vwap(symbol)
                    if vwap > 0 and price < vwap:
                        self.liquidate(symbol, tag="vwap_loss")
                        return True

                return False

            def _context_allows_entry(self):
                if not self.context_symbols:
                    return True

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

            def _regime_positive_count(self):
                if not self.regime_symbols or self.regime_lookback_days <= 0:
                    return len(self.regime_symbols)

                positive_count = 0
                for symbol in self.regime_symbols:
                    history = self.daily_summaries[symbol]
                    if len(history) < self.regime_lookback_days + 1:
                        return None

                    regime_return = self._recent_return(symbol, self.regime_lookback_days)
                    if regime_return >= self.regime_return_min:
                        positive_count += 1

                return positive_count

            def _regime_allows_entry(self):
                if not self.regime_symbols or self.regime_lookback_days <= 0:
                    return True
                if self.regime_min_positive < 0:
                    return True

                positive_count = self._regime_positive_count()
                if positive_count is None:
                    return False

                required_count = self.regime_min_positive or len(self.regime_symbols)
                return positive_count >= required_count

            def _maybe_enter(self, symbol, bar):
                state = self.state[symbol]
{entry_block}

            def on_data(self, data: Slice):
                if self.current_day != self.time.date():
                    self._roll_day(self.time.date())

                for symbol in self.symbols:
                    if symbol not in data.bars:
                        continue

                    bar = data.bars[symbol]
                    state = self.state[symbol]

                    if self._is_premarket():
                        state["premarket_high"] = bar.high if state["premarket_high"] is None else max(state["premarket_high"], bar.high)
                        state["premarket_low"] = bar.low if state["premarket_low"] is None else min(state["premarket_low"], bar.low)
                        state["premarket_volume"] += float(bar.volume)
                        continue

                    if not self._is_regular():
                        if self.portfolio[symbol].invested and self._minutes_to_close() <= self.force_exit_minutes_before_close:
                            self.liquidate(symbol, tag="eod_exit")
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
                        state["opening_range_high"] = bar.high if state["opening_range_high"] is None else max(state["opening_range_high"], bar.high)
                        state["opening_range_low"] = bar.low if state["opening_range_low"] is None else min(state["opening_range_low"], bar.low)

                    if self._manage_position(symbol, bar):
                        return

                if self.trade_taken or any(self.portfolio[symbol].invested for symbol in self.tradable_symbols):
                    return

                if not self._is_regular():
                    return

                minutes_from_open = self._minutes_from_open()
                if minutes_from_open < self.opening_range_minutes or minutes_from_open > self.max_entry_minutes:
                    return

                if not self._entries_available():
                    return

                if not self.watchlist_symbols:
                    self.watchlist_symbols = self._select_watchlist()
                    if not self.watchlist_symbols:
                        return

                if not self._context_allows_entry():
                    return

                if not self._regime_allows_entry():
                    return

                for symbol in self.watchlist_symbols:
                    if symbol not in data.bars:
                        continue
                    self._maybe_enter(symbol, data.bars[symbol])
                    if self.trade_taken or any(self.portfolio[item].invested for item in self.tradable_symbols):
                        return
        """
    )


def _render_gap_reversal_scanner_intraday(spec: CandidateSpec) -> str:
    gap_up_pct_min = float(spec.parameters.get("gap_up_pct_min", 0.01))
    gap_up_pct_max = float(spec.parameters.get("gap_up_pct_max", 0.12))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.004))
    opening_pullback_pct = float(spec.parameters.get("opening_pullback_pct", 0.003))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    min_prev_close = float(spec.parameters.get("min_prev_close", 20.0))
    max_prev_close = float(spec.parameters.get("max_prev_close", 2000.0))
    min_avg_dollar_volume = float(spec.parameters.get("min_avg_dollar_volume", 250000000.0))
    min_premarket_dollar_volume = float(spec.parameters.get("min_premarket_dollar_volume", 1000000.0))

    qualification_code = f"""
history = self.daily_summaries[symbol]
if len(history) < self.min_history_days:
    state["qualified"] = False
    return False

state["prev_day"] = history[-1]
avg_volume = self._avg_regular_volume(symbol, self.volume_lookback_days)
if avg_volume <= 0 or state["regular_open"] is None or state["prev_day"]["close"] <= 0:
    state["qualified"] = False
    return False

state["avg_dollar_volume"] = avg_volume * state["prev_day"]["close"]
state["premarket_dollar_volume"] = state["premarket_volume"] * max(state["regular_open"], state["prev_day"]["close"])
if not ({min_prev_close} <= state["prev_day"]["close"] <= {max_prev_close}):
    state["qualified"] = False
    return False
if state["avg_dollar_volume"] < {min_avg_dollar_volume}:
    state["qualified"] = False
    return False
if state["premarket_dollar_volume"] < {min_premarket_dollar_volume}:
    state["qualified"] = False
    return False

state["gap_pct"] = (state["regular_open"] / state["prev_day"]["close"]) - 1.0
state["premarket_vol_ratio"] = state["premarket_volume"] / avg_volume
state["qualified"] = (
    {gap_up_pct_min} <= state["gap_pct"] <= {gap_up_pct_max}
    and state["premarket_vol_ratio"] >= {premarket_vol_ratio_min}
)
return state["qualified"]
"""

    rank_score_code = """
state["rank_score"] = state["gap_pct"] * max(state["premarket_vol_ratio"], 0.0)
return state["rank_score"]
"""

    entry_code = f"""
if state["session_low"] is None or state["regular_open"] is None or state["opening_range_high"] is None or state["opening_range_low"] is None:
    return

if state["session_low"] <= state["regular_open"] * (1.0 - {opening_pullback_pct}):
    state["pullback_seen"] = True

if not state["pullback_seen"]:
    return

price = bar.close
vwap = self._session_vwap(symbol)
breakout_level = state["opening_range_high"]
if vwap <= 0 or price <= vwap or price <= breakout_level:
    state["confirm_start"] = None
    return

if state["confirm_start"] is None:
    state["confirm_start"] = self.time
    return

held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
if held_above + 1e-9 < self.confirm_hold_minutes:
    return

stop_reference = min(state["session_low"], state["opening_range_low"])
self._enter_long(symbol, price, stop_reference, "gap_scanner_entry")
"""

    return _render_intraday_scanner_long(
        spec,
        qualification_code=qualification_code,
        rank_score_code=rank_score_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, 5),
    )


def _render_bsl_reversal_scanner_intraday(spec: CandidateSpec) -> str:
    downtrend_lookback_days = int(spec.parameters.get("downtrend_lookback_days", 10))
    downtrend_return_max = float(spec.parameters.get("downtrend_return_max", -0.03))
    gap_min = float(spec.parameters.get("gap_min", -0.01))
    gap_max = float(spec.parameters.get("gap_max", 1.0))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.003))
    morning_flush_pct = float(spec.parameters.get("morning_flush_pct", 0.002))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    min_prev_close = float(spec.parameters.get("min_prev_close", 20.0))
    max_prev_close = float(spec.parameters.get("max_prev_close", 2000.0))
    min_avg_dollar_volume = float(spec.parameters.get("min_avg_dollar_volume", 250000000.0))
    min_premarket_dollar_volume = float(spec.parameters.get("min_premarket_dollar_volume", 1000000.0))
    max_key_level_distance_pct = float(spec.parameters.get("max_key_level_distance_pct", 0.0))
    rank_premarket_dollar_volume_scale = float(spec.parameters.get("rank_premarket_dollar_volume_scale", 0.0))
    rank_key_level_distance_penalty = float(spec.parameters.get("rank_key_level_distance_penalty", 0.0))

    qualification_code = f"""
history = self.daily_summaries[symbol]
if len(history) < self.min_history_days:
    state["qualified"] = False
    return False

state["prev_day"] = history[-1]
avg_volume = self._avg_regular_volume(symbol, self.volume_lookback_days)
if avg_volume <= 0 or state["regular_open"] is None or state["prev_day"]["close"] <= 0:
    state["qualified"] = False
    return False

state["avg_dollar_volume"] = avg_volume * state["prev_day"]["close"]
state["premarket_dollar_volume"] = state["premarket_volume"] * max(state["regular_open"], state["prev_day"]["close"])
if not ({min_prev_close} <= state["prev_day"]["close"] <= {max_prev_close}):
    state["qualified"] = False
    return False
if state["avg_dollar_volume"] < {min_avg_dollar_volume}:
    state["qualified"] = False
    return False
if state["premarket_dollar_volume"] < {min_premarket_dollar_volume}:
    state["qualified"] = False
    return False

state["gap_pct"] = (state["regular_open"] / state["prev_day"]["close"]) - 1.0
state["premarket_vol_ratio"] = state["premarket_volume"] / avg_volume
state["downtrend_return"] = self._recent_return(symbol, {downtrend_lookback_days})
state["key_level"] = max(state["prev_day"]["high"], state["prev_day"]["close"])
state["key_level_distance_pct"] = abs((state["regular_open"] / state["key_level"]) - 1.0) if state["key_level"] > 0 else 0.0
if {max_key_level_distance_pct} > 0 and state["key_level_distance_pct"] > {max_key_level_distance_pct}:
    state["qualified"] = False
    return False
state["qualified"] = (
    state["downtrend_return"] <= {downtrend_return_max}
    and {gap_min} <= state["gap_pct"] <= {gap_max}
    and state["premarket_vol_ratio"] >= {premarket_vol_ratio_min}
)
return state["qualified"]
"""

    rank_score_code = f"""
score = abs(min(state["downtrend_return"], 0.0)) * max(state["premarket_vol_ratio"], 0.0)
if {rank_premarket_dollar_volume_scale} > 0:
    score *= 1.0 + min(state["premarket_dollar_volume"] / {rank_premarket_dollar_volume_scale}, 10.0)
if {rank_key_level_distance_penalty} > 0:
    score /= 1.0 + (state["key_level_distance_pct"] / {rank_key_level_distance_penalty})
state["rank_score"] = score
return state["rank_score"]
"""

    entry_code = f"""
if state["session_low"] is None or state["regular_open"] is None or state["opening_range_low"] is None or state["key_level"] is None:
    return

if state["session_low"] <= state["regular_open"] * (1.0 - {morning_flush_pct}):
    state["flush_seen"] = True

if not state["flush_seen"]:
    return

levels = [level for level in [state["key_level"], state["opening_range_high"]] if level is not None]
if not levels:
    return

breakout_level = max(levels)
price = bar.close
vwap = self._session_vwap(symbol)
if vwap <= 0 or price <= vwap or price <= breakout_level:
    state["confirm_start"] = None
    return

if state["confirm_start"] is None:
    state["confirm_start"] = self.time
    return

held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
if held_above + 1e-9 < self.confirm_hold_minutes:
    return

stop_reference = min(state["session_low"], state["opening_range_low"], state["prev_day"]["close"])
self._enter_long(symbol, price, stop_reference, "bsl_scanner_entry")
"""

    return _render_intraday_scanner_long(
        spec,
        qualification_code=qualification_code,
        rank_score_code=rank_score_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, downtrend_lookback_days + 1),
    )


def _render_regime_router_scanner_intraday(spec: CandidateSpec) -> str:
    weak_lookback_days = int(spec.parameters.get("weak_lookback_days", 10))
    weak_return_max = float(spec.parameters.get("weak_return_max", -0.03))
    gap_min = float(spec.parameters.get("gap_min", -0.015))
    gap_max = float(spec.parameters.get("gap_max", 0.01))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.004))
    bsl_morning_flush_pct = float(spec.parameters.get("bsl_morning_flush_pct", 0.003))
    failed_morning_flush_pct = float(spec.parameters.get("failed_morning_flush_pct", 0.003))
    breakdown_buffer_pct = float(spec.parameters.get("breakdown_buffer_pct", 0.001))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    router_regime_min_positive = int(spec.parameters.get("router_regime_min_positive", 2))
    min_prev_close = float(spec.parameters.get("min_prev_close", 20.0))
    max_prev_close = float(spec.parameters.get("max_prev_close", 2000.0))
    min_avg_dollar_volume = float(spec.parameters.get("min_avg_dollar_volume", 250000000.0))
    min_premarket_dollar_volume = float(spec.parameters.get("min_premarket_dollar_volume", 1000000.0))

    qualification_code = f"""
history = self.daily_summaries[symbol]
if len(history) < self.min_history_days:
    state["qualified"] = False
    return False

state["prev_day"] = history[-1]
avg_volume = self._avg_regular_volume(symbol, self.volume_lookback_days)
if avg_volume <= 0 or state["regular_open"] is None or state["prev_day"]["close"] <= 0:
    state["qualified"] = False
    return False

state["avg_dollar_volume"] = avg_volume * state["prev_day"]["close"]
state["premarket_dollar_volume"] = state["premarket_volume"] * max(state["regular_open"], state["prev_day"]["close"])
if not ({min_prev_close} <= state["prev_day"]["close"] <= {max_prev_close}):
    state["qualified"] = False
    return False
if state["avg_dollar_volume"] < {min_avg_dollar_volume}:
    state["qualified"] = False
    return False
if state["premarket_dollar_volume"] < {min_premarket_dollar_volume}:
    state["qualified"] = False
    return False

state["gap_pct"] = (state["regular_open"] / state["prev_day"]["close"]) - 1.0
state["premarket_vol_ratio"] = state["premarket_volume"] / avg_volume
state["downtrend_return"] = self._recent_return(symbol, {weak_lookback_days})
state["qualified"] = (
    state["downtrend_return"] <= {weak_return_max}
    and {gap_min} <= state["gap_pct"] <= {gap_max}
    and state["premarket_vol_ratio"] >= {premarket_vol_ratio_min}
)
return state["qualified"]
"""

    rank_score_code = """
state["rank_score"] = (
    abs(min(state["downtrend_return"], 0.0))
    * max(state["premarket_vol_ratio"], 0.0)
)
return state["rank_score"]
"""

    entry_code = f"""
if state["session_low"] is None or state["regular_open"] is None or state["opening_range_low"] is None or state["prev_day"] is None:
    return

regime_positive_count = self._regime_positive_count()
if regime_positive_count is None:
    return

strong_regime = regime_positive_count >= max({router_regime_min_positive}, 1)
price = bar.close
vwap = self._session_vwap(symbol)
if vwap <= 0:
    state["confirm_start"] = None
    return

if strong_regime:
    if state["session_low"] <= state["regular_open"] * (1.0 - {bsl_morning_flush_pct}):
        state["flush_seen"] = True

    if not state["flush_seen"]:
        return

    levels = [level for level in [state["prev_day"]["high"], state["prev_day"]["close"], state["opening_range_high"]] if level is not None]
    if not levels:
        return

    breakout_level = max(levels)
    if price <= vwap or price <= breakout_level:
        state["confirm_start"] = None
        return

    if state["confirm_start"] is None:
        state["confirm_start"] = self.time
        return

    held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
    if held_above + 1e-9 < self.confirm_hold_minutes:
        return

    stop_reference = min(state["session_low"], state["opening_range_low"], state["prev_day"]["close"])
    self._enter_long(symbol, price, stop_reference, "router_bsl_entry")
    return

flush_level = min(
    state["regular_open"] * (1.0 - {failed_morning_flush_pct}),
    state["prev_day"]["low"] * (1.0 - {breakdown_buffer_pct})
)
if state["session_low"] <= flush_level:
    state["flush_seen"] = True

if not state["flush_seen"]:
    return

if price <= vwap or price <= state["prev_day"]["low"]:
    state["confirm_start"] = None
    return

if state["confirm_start"] is None:
    state["confirm_start"] = self.time
    return

held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
if held_above + 1e-9 < self.confirm_hold_minutes:
    return

stop_reference = min(state["session_low"], state["opening_range_low"])
self._enter_long(symbol, price, stop_reference, "router_failed_breakdown_entry")
"""

    return _render_intraday_scanner_long(
        spec,
        qualification_code=qualification_code,
        rank_score_code=rank_score_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, weak_lookback_days + 1),
    )


def _render_vwap_reclaim_scanner_intraday(spec: CandidateSpec) -> str:
    weak_lookback_days = int(spec.parameters.get("weak_lookback_days", 10))
    weak_return_max = float(spec.parameters.get("weak_return_max", -0.02))
    gap_min = float(spec.parameters.get("gap_min", -0.015))
    gap_max = float(spec.parameters.get("gap_max", 0.03))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.003))
    morning_flush_pct = float(spec.parameters.get("morning_flush_pct", 0.002))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    min_prev_close = float(spec.parameters.get("min_prev_close", 20.0))
    max_prev_close = float(spec.parameters.get("max_prev_close", 2000.0))
    min_avg_dollar_volume = float(spec.parameters.get("min_avg_dollar_volume", 250000000.0))
    min_premarket_dollar_volume = float(spec.parameters.get("min_premarket_dollar_volume", 1000000.0))
    require_above_open = bool(spec.parameters.get("require_above_open", False))

    qualification_code = f"""
history = self.daily_summaries[symbol]
if len(history) < self.min_history_days:
    state["qualified"] = False
    return False

state["prev_day"] = history[-1]
avg_volume = self._avg_regular_volume(symbol, self.volume_lookback_days)
if avg_volume <= 0 or state["regular_open"] is None or state["prev_day"]["close"] <= 0:
    state["qualified"] = False
    return False

state["avg_dollar_volume"] = avg_volume * state["prev_day"]["close"]
state["premarket_dollar_volume"] = state["premarket_volume"] * max(state["regular_open"], state["prev_day"]["close"])
if not ({min_prev_close} <= state["prev_day"]["close"] <= {max_prev_close}):
    state["qualified"] = False
    return False
if state["avg_dollar_volume"] < {min_avg_dollar_volume}:
    state["qualified"] = False
    return False
if state["premarket_dollar_volume"] < {min_premarket_dollar_volume}:
    state["qualified"] = False
    return False

state["gap_pct"] = (state["regular_open"] / state["prev_day"]["close"]) - 1.0
state["premarket_vol_ratio"] = state["premarket_volume"] / avg_volume
state["downtrend_return"] = self._recent_return(symbol, {weak_lookback_days})
state["qualified"] = (
    state["downtrend_return"] <= {weak_return_max}
    and {gap_min} <= state["gap_pct"] <= {gap_max}
    and state["premarket_vol_ratio"] >= {premarket_vol_ratio_min}
)
return state["qualified"]
"""

    rank_score_code = """
state["rank_score"] = (
    abs(min(state["downtrend_return"], 0.0))
    * max(state["premarket_vol_ratio"], 0.0)
)
return state["rank_score"]
"""

    entry_code = f"""
if state["session_low"] is None or state["regular_open"] is None or state["opening_range_low"] is None:
    return

if state["session_low"] <= state["regular_open"] * (1.0 - {morning_flush_pct}):
    state["flush_seen"] = True

if not state["flush_seen"]:
    return

price = bar.close
vwap = self._session_vwap(symbol)
if vwap <= 0 or price <= vwap:
    state["confirm_start"] = None
    return

if {str(require_above_open)} and price <= state["regular_open"]:
    state["confirm_start"] = None
    return

if state["confirm_start"] is None:
    state["confirm_start"] = self.time
    return

held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
if held_above + 1e-9 < self.confirm_hold_minutes:
    return

stop_reference = min(state["session_low"], state["opening_range_low"])
self._enter_long(symbol, price, stop_reference, "vwap_reclaim_entry")
"""

    return _render_intraday_scanner_long(
        spec,
        qualification_code=qualification_code,
        rank_score_code=rank_score_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, weak_lookback_days + 1),
    )


def _render_failed_breakdown_reclaim_scanner_intraday(spec: CandidateSpec) -> str:
    weak_lookback_days = int(spec.parameters.get("weak_lookback_days", 10))
    weak_return_max = float(spec.parameters.get("weak_return_max", -0.02))
    gap_min = float(spec.parameters.get("gap_min", -0.02))
    gap_max = float(spec.parameters.get("gap_max", 0.02))
    premarket_vol_ratio_min = float(spec.parameters.get("premarket_vol_ratio_min", 0.003))
    breakdown_buffer_pct = float(spec.parameters.get("breakdown_buffer_pct", 0.001))
    morning_flush_pct = float(spec.parameters.get("morning_flush_pct", 0.002))
    volume_lookback_days = int(spec.parameters.get("volume_lookback_days", 20))
    min_prev_close = float(spec.parameters.get("min_prev_close", 20.0))
    max_prev_close = float(spec.parameters.get("max_prev_close", 2000.0))
    min_avg_dollar_volume = float(spec.parameters.get("min_avg_dollar_volume", 250000000.0))
    min_premarket_dollar_volume = float(spec.parameters.get("min_premarket_dollar_volume", 1000000.0))
    max_key_level_distance_pct = float(spec.parameters.get("max_key_level_distance_pct", 0.0))
    rank_premarket_dollar_volume_scale = float(spec.parameters.get("rank_premarket_dollar_volume_scale", 0.0))
    rank_key_level_distance_penalty = float(spec.parameters.get("rank_key_level_distance_penalty", 0.0))

    qualification_code = f"""
history = self.daily_summaries[symbol]
if len(history) < self.min_history_days:
    state["qualified"] = False
    return False

state["prev_day"] = history[-1]
avg_volume = self._avg_regular_volume(symbol, self.volume_lookback_days)
if avg_volume <= 0 or state["regular_open"] is None or state["prev_day"]["close"] <= 0:
    state["qualified"] = False
    return False

state["avg_dollar_volume"] = avg_volume * state["prev_day"]["close"]
state["premarket_dollar_volume"] = state["premarket_volume"] * max(state["regular_open"], state["prev_day"]["close"])
if not ({min_prev_close} <= state["prev_day"]["close"] <= {max_prev_close}):
    state["qualified"] = False
    return False
if state["avg_dollar_volume"] < {min_avg_dollar_volume}:
    state["qualified"] = False
    return False
if state["premarket_dollar_volume"] < {min_premarket_dollar_volume}:
    state["qualified"] = False
    return False

state["gap_pct"] = (state["regular_open"] / state["prev_day"]["close"]) - 1.0
state["premarket_vol_ratio"] = state["premarket_volume"] / avg_volume
state["downtrend_return"] = self._recent_return(symbol, {weak_lookback_days})
state["key_level"] = state["prev_day"]["low"]
state["key_level_distance_pct"] = abs((state["regular_open"] / state["key_level"]) - 1.0) if state["key_level"] > 0 else 0.0
if {max_key_level_distance_pct} > 0 and state["key_level_distance_pct"] > {max_key_level_distance_pct}:
    state["qualified"] = False
    return False
state["qualified"] = (
    state["downtrend_return"] <= {weak_return_max}
    and {gap_min} <= state["gap_pct"] <= {gap_max}
    and state["premarket_vol_ratio"] >= {premarket_vol_ratio_min}
)
return state["qualified"]
"""

    rank_score_code = f"""
score = (
    abs(min(state["downtrend_return"], 0.0))
    * max(state["premarket_vol_ratio"], 0.0)
    * (1.0 + abs(min(state["gap_pct"], 0.0)))
)
if {rank_premarket_dollar_volume_scale} > 0:
    score *= 1.0 + min(state["premarket_dollar_volume"] / {rank_premarket_dollar_volume_scale}, 10.0)
if {rank_key_level_distance_penalty} > 0:
    score /= 1.0 + (state["key_level_distance_pct"] / {rank_key_level_distance_penalty})
state["rank_score"] = score
return state["rank_score"]
"""

    entry_code = f"""
if state["session_low"] is None or state["regular_open"] is None or state["opening_range_low"] is None or state["key_level"] is None:
    return

flush_level = min(
    state["regular_open"] * (1.0 - {morning_flush_pct}),
    state["key_level"] * (1.0 - {breakdown_buffer_pct})
)
if state["session_low"] <= flush_level:
    state["flush_seen"] = True

if not state["flush_seen"]:
    return

price = bar.close
vwap = self._session_vwap(symbol)
if vwap <= 0 or price <= vwap or price <= state["key_level"]:
    state["confirm_start"] = None
    return

if state["confirm_start"] is None:
    state["confirm_start"] = self.time
    return

held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
if held_above + 1e-9 < self.confirm_hold_minutes:
    return

stop_reference = min(state["session_low"], state["opening_range_low"])
self._enter_long(symbol, price, stop_reference, "failed_breakdown_reclaim_entry")
"""

    return _render_intraday_scanner_long(
        spec,
        qualification_code=qualification_code,
        rank_score_code=rank_score_code,
        entry_code=entry_code,
        min_history_days=max(volume_lookback_days, weak_lookback_days + 1),
    )
