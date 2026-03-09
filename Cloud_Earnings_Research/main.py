# region imports
from AlgorithmImports import *
from datetime import date, time, timedelta
# endregion


class CloudEarningsResearch(QCAlgorithm):

    def initialize(self) -> None:
        self.sample_window = (self.get_parameter("sample_window") or "broad").strip()
        if self.sample_window == "2024":
            self.set_start_date(2024, 1, 2)
            self.set_end_date(2024, 12, 31)
        elif self.sample_window == "2024_2025":
            self.set_start_date(2024, 1, 2)
            self.set_end_date(2025, 12, 31)
        elif self.sample_window == "2025":
            self.set_start_date(2025, 1, 2)
            self.set_end_date(2025, 12, 31)
        elif self.sample_window == "2026_ytd":
            self.set_start_date(2026, 1, 2)
            self.set_end_date(2026, 3, 6)
        else:
            self.set_start_date(2025, 1, 2)
            self.set_end_date(2026, 3, 6)

        self.set_cash(100000)
        self.settings.seed_initial_prices = True
        self.universe_settings.resolution = Resolution.DAILY
        self.universe_settings.data_normalization_mode = DataNormalizationMode.RAW

        self.strategy_style = (self.get_parameter("strategy_style") or "swing").strip().lower()
        if self.strategy_style == "master_portfolio":
            from master_integration import CloudMasterEventIntegration

            self.master_integration = CloudMasterEventIntegration(self)
            return

        self.bucket_map = {
            "growth4": ["AMZN", "META", "NVDA", "TSLA"],
            "platform7": ["AAPL", "MSFT", "NFLX", "CRM", "ADBE", "NOW", "ORCL"],
            "platform5": ["AAPL", "MSFT", "CRM", "NOW", "ORCL"],
            "enterprise4": ["MSFT", "CRM", "NOW", "ORCL"],
            "software3": ["CRM", "NOW", "ORCL"],
            "platform6_no_nflx": ["AAPL", "MSFT", "CRM", "ADBE", "NOW", "ORCL"],
            "platform6_no_adbe": ["AAPL", "MSFT", "NFLX", "CRM", "NOW", "ORCL"],
            "hardware7": ["NVDA", "AVGO", "AMD", "MU", "MRVL", "TSM", "MSFT"],
        }
        self.bucket = (self.get_parameter("bucket") or "growth4").strip()
        self.allowed_tickers = self.bucket_map.get(self.bucket, self.bucket_map["growth4"])

        self.event_mode = (self.get_parameter("event_mode") or "pre1").strip().lower()
        self.report_time_filter = (self.get_parameter("report_time_filter") or "any").strip().lower()
        self.estimate_mode = (self.get_parameter("estimate_mode") or "").strip().lower()
        if not self.estimate_mode:
            require_estimate = (self.get_parameter("require_estimate") or "false").strip().lower()
            self.estimate_mode = "required" if require_estimate == "true" else "any"

        self.quality_weight = float(self.get_parameter("quality_weight") or 0)
        self.quality_min_events = int(float(self.get_parameter("quality_min_events") or 1))
        self.quality_shrinkage_events = float(self.get_parameter("quality_shrinkage_events") or 2)
        self.quality_filter_min_events = int(float(self.get_parameter("quality_filter_min_events") or 0))
        self.quality_min_avg_return = float(self.get_parameter("quality_min_avg_return") or -999)

        self.lookback_days = int(float(self.get_parameter("lookback_days") or 15))
        self.min_price = float(self.get_parameter("min_price") or 20)
        self.min_avg_dollar_volume = float(
            self.get_parameter("min_avg_dollar_volume")
            or (250_000_000 if self.bucket == "growth4" else 150_000_000)
        )

        self.context_symbol_names = [
            item.strip().upper()
            for item in (self.get_parameter("context_symbols") or "").split(",")
            if item.strip()
        ]
        self.context_lookback_days = int(float(self.get_parameter("context_lookback_days") or 5))
        self.context_return_threshold = float(self.get_parameter("context_return_threshold") or 0.0)
        context_min_positive = (self.get_parameter("context_min_positive") or "").strip()
        context_max_positive = (self.get_parameter("context_max_positive") or "").strip()
        self.context_min_positive = int(float(context_min_positive)) if context_min_positive else None
        self.context_max_positive = int(float(context_max_positive)) if context_max_positive else None

        if self.strategy_style == "intraday":
            self.selection_pool_size = int(float(self.get_parameter("selection_pool_size") or 2))
            self.intraday_family = (self.get_parameter("intraday_family") or "bsl").strip().lower()
            self.weak_return_max = float(self.get_parameter("weak_return_max") or -0.03)
            self.require_recent_weakness = (
                (self.get_parameter("require_recent_weakness") or "true").strip().lower() == "true"
            )
            self.recent_return_score_mode = (
                (self.get_parameter("recent_return_score_mode") or "negative_only").strip().lower()
            )
            self.gap_min = float(self.get_parameter("gap_min") or -0.015)
            self.gap_max = float(self.get_parameter("gap_max") or 0.02)
            self.premarket_vol_ratio_min = float(self.get_parameter("premarket_vol_ratio_min") or 0.004)
            self.min_premarket_dollar_volume = float(self.get_parameter("min_premarket_dollar_volume") or 2_500_000)
            self.max_key_level_distance_pct = float(self.get_parameter("max_key_level_distance_pct") or 0.03)
            self.rank_premarket_dollar_volume_scale = float(
                self.get_parameter("rank_premarket_dollar_volume_scale") or 4_000_000
            )
            self.rank_key_level_distance_penalty = float(
                self.get_parameter("rank_key_level_distance_penalty") or 0.008
            )
            self.morning_flush_pct = float(self.get_parameter("morning_flush_pct") or 0.003)
            self.breakdown_buffer_pct = float(self.get_parameter("breakdown_buffer_pct") or 0.001)
            self.opening_range_minutes = int(float(self.get_parameter("opening_range_minutes") or 5))
            self.confirm_hold_minutes = int(float(self.get_parameter("confirm_hold_minutes") or 3))
            self.max_entry_minutes = int(float(self.get_parameter("max_entry_minutes") or 120))
            self.max_holding_minutes = int(float(self.get_parameter("max_holding_minutes") or 240))
            self.force_exit_minutes_before_close = int(
                float(self.get_parameter("force_exit_minutes_before_close") or 5)
            )
            self.risk_reward = float(self.get_parameter("risk_reward") or 2.0)
            self.stop_buffer_pct = float(self.get_parameter("stop_buffer_pct") or 0.001)
            self.context_require_above_vwap = (
                (self.get_parameter("context_require_above_vwap") or "true").strip().lower() == "true"
            )
            self.context_require_above_open = (
                (self.get_parameter("context_require_above_open") or "false").strip().lower() == "true"
            )
            self.max_daily_trades = int(float(self.get_parameter("max_daily_trades") or 1))
            self.max_daily_history = max(self.lookback_days + 10, 40)
        else:
            self.max_names = int(float(self.get_parameter("max_names") or 3))
            self.hold_days = int(float(self.get_parameter("hold_days") or 2))
            hold_days_before_open = (self.get_parameter("hold_days_before_open") or "").strip()
            hold_days_after_close = (self.get_parameter("hold_days_after_close") or "").strip()
            hold_days_unknown = (self.get_parameter("hold_days_unknown") or "").strip()
            self.hold_days_before_open = int(float(hold_days_before_open)) if hold_days_before_open else None
            self.hold_days_after_close = int(float(hold_days_after_close)) if hold_days_after_close else None
            self.hold_days_unknown = int(float(hold_days_unknown)) if hold_days_unknown else None
            recent_return_min = (self.get_parameter("recent_return_min") or "").strip()
            recent_return_max = (self.get_parameter("recent_return_max") or "").strip()
            self.recent_return_min = float(recent_return_min) if recent_return_min else None
            self.recent_return_max = float(recent_return_max) if recent_return_max else None
            self.max_daily_history = max(self.lookback_days + 10, 40)

        self.symbol_by_ticker = {}
        resolution = Resolution.MINUTE if self.strategy_style == "intraday" else Resolution.DAILY
        extended = self.strategy_style == "intraday"
        for ticker in self.allowed_tickers:
            security = self.add_equity(
                ticker,
                resolution,
                extended_market_hours=extended,
                data_normalization_mode=DataNormalizationMode.RAW,
            )
            security.set_slippage_model(ConstantSlippageModel(0.0001))
            self.symbol_by_ticker[ticker] = security.symbol

        self.context_symbol_by_ticker = {}
        for ticker in self.context_symbol_names:
            if ticker in self.symbol_by_ticker:
                self.context_symbol_by_ticker[ticker] = self.symbol_by_ticker[ticker]
                continue
            security = self.add_equity(
                ticker,
                resolution,
                extended_market_hours=extended,
                data_normalization_mode=DataNormalizationMode.RAW,
            )
            security.set_slippage_model(ConstantSlippageModel(0.0001))
            self.context_symbol_by_ticker[ticker] = security.symbol

        self.selection_count = 0
        self.rebalance_count = 0
        self.selection_by_ticker = {}
        self.known_report_dates = {}
        self.known_report_times = {}
        self.known_estimates = {}
        self.report_time_counts = {}
        self.symbol_quality_sum_return = {}
        self.symbol_quality_event_count = {}
        self.symbol_quality_win_count = {}

        all_symbols = {
            *self.symbol_by_ticker.values(),
            *self.context_symbol_by_ticker.values(),
        }
        self.daily_history = {symbol: [] for symbol in all_symbols}
        self._bootstrap_daily_history()

        if self.strategy_style == "intraday":
            self.current_day = None
            self.intraday_state = {symbol: self._new_intraday_state() for symbol in all_symbols}
            self.intraday_event_tickers = []
            self.watchlist_symbols = []
            self.watchlist_finalized = False
            self.entry_symbol = None
            self.entry_time = None
            self.entry_price = None
            self.stop_price = None
            self.target_price = None
            self.daily_trade_count = 0
            self.completed_trades = 0
            self.day_selection_log_count = 0
        else:
            self.days_remaining = {}
            self.active_event_positions = {}
            self.last_processed_date = None

        self.add_universe(EODHDUpcomingEarnings, self._select_earnings_universe)

    def _bootstrap_daily_history(self) -> None:
        for symbol in self.daily_history:
            try:
                history = list(self.history[TradeBar](symbol, self.max_daily_history, Resolution.DAILY))
            except Exception:
                history = []
            rows = []
            for bar in history:
                rows.append(
                    {
                        "date": bar.end_time.date(),
                        "open": float(bar.open),
                        "high": float(bar.high),
                        "low": float(bar.low),
                        "close": float(bar.close),
                        "volume": float(bar.volume),
                        "dollar_volume": float(bar.close * bar.volume),
                    }
                )
            self.daily_history[symbol] = rows[-self.max_daily_history:]

    def _new_intraday_state(self):
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
            "flush_seen": False,
            "confirm_start": None,
            "prev_day": None,
            "gap_pct": 0.0,
            "premarket_vol_ratio": 0.0,
            "avg_dollar_volume": 0.0,
            "premarket_dollar_volume": 0.0,
            "recent_return": 0.0,
            "key_level": None,
            "key_level_distance_pct": 0.0,
        }

    def _select_earnings_universe(self, earnings):
        symbols = []
        for datum in earnings:
            if datum.symbol.value not in self.allowed_tickers:
                continue
            if datum.report_date is None:
                continue
            self.known_report_dates[datum.symbol.value] = datum.report_date.date()
            report_time = str(datum.report_time).strip() if datum.report_time is not None else ""
            self.known_report_times[datum.symbol.value] = report_time
            self.known_estimates[datum.symbol.value] = datum.estimate
            if report_time:
                self.report_time_counts[report_time] = self.report_time_counts.get(report_time, 0) + 1
            symbols.append(datum.symbol)
        return symbols

    def on_data(self, data: Slice) -> None:
        if self.strategy_style == "master_portfolio":
            self.master_integration.on_data(data)
            return
        if self.strategy_style == "intraday":
            self._on_data_intraday(data)
        else:
            self._on_data_swing(data)

    def on_order_event(self, order_event: OrderEvent) -> None:
        if self.strategy_style == "master_portfolio":
            self.master_integration.on_order_event(order_event)

    def _on_data_swing(self, data: Slice) -> None:
        today = self.time.date()
        if self.last_processed_date == today:
            return
        self.last_processed_date = today

        for symbol in self.daily_history:
            if symbol in data.bars:
                bar = data.bars[symbol]
                history = self.daily_history[symbol]
                history.append(
                    {
                        "date": today,
                        "close": float(bar.close),
                        "dollar_volume": float(bar.close * bar.volume),
                    }
                )
                if len(history) > self.max_daily_history:
                    self.daily_history[symbol] = history[-self.max_daily_history:]

        expired = []
        for ticker in list(self.days_remaining):
            self.days_remaining[ticker] -= 1
            if self.days_remaining[ticker] <= 0:
                expired.append(ticker)

        for ticker in expired:
            symbol = self.symbol_by_ticker[ticker]
            self._record_completed_event(ticker, symbol)
            if self.portfolio[symbol].invested:
                self.liquidate(symbol, "event_hold_expired")
            self.days_remaining.pop(ticker, None)
            self.active_event_positions.pop(ticker, None)

        context_positive_count = self._context_positive_count()
        if self.context_min_positive is not None and context_positive_count is not None:
            if context_positive_count < self.context_min_positive:
                return
        if self.context_max_positive is not None and context_positive_count is not None:
            if context_positive_count > self.context_max_positive:
                return

        candidates = []
        for ticker in self.allowed_tickers:
            symbol = self.symbol_by_ticker[ticker]
            security = self.securities[symbol]
            if not security.has_data or security.price < self.min_price:
                continue

            report_date = self.known_report_dates.get(ticker)
            if report_date is None or not self._event_matches(today, report_date):
                continue
            report_time = self.known_report_times.get(ticker, "")
            if not self._report_time_matches(report_time):
                continue
            estimate = self.known_estimates.get(ticker)
            if self.estimate_mode == "required" and estimate is None:
                continue
            if self.estimate_mode == "missing" and estimate is not None:
                continue
            if self._fails_quality_floor(ticker):
                continue

            avg_dollar_volume = self._avg_dollar_volume(symbol, 20)
            if avg_dollar_volume < self.min_avg_dollar_volume:
                continue

            recent_return = self._recent_return(symbol, self.lookback_days)
            if recent_return is None:
                continue
            if self.recent_return_min is not None and recent_return < self.recent_return_min:
                continue
            if self.recent_return_max is not None and recent_return > self.recent_return_max:
                continue

            days_delta = (report_date - today).days
            score = -recent_return
            if self.event_mode == "pre1":
                score += 0.15
            elif self.event_mode == "pre2":
                score += 0.10
            elif self.event_mode == "pre3":
                score += max(0, 4 - days_delta) * 0.04
            score += self._symbol_quality_bonus(ticker)
            candidates.append((score, ticker, symbol))

        candidates.sort(key=lambda item: (-item[0], item[1]))
        selected = candidates[: self.max_names]
        if selected:
            self.selection_count += 1
            for _, ticker, _ in selected:
                self.selection_by_ticker[ticker] = self.selection_by_ticker.get(ticker, 0) + 1
                if ticker not in self.days_remaining:
                    report_time = self.known_report_times.get(ticker, "")
                    self.days_remaining[ticker] = self._effective_hold_days(report_time)
                    symbol = self.symbol_by_ticker[ticker]
                    self.active_event_positions[ticker] = {
                        "entry_price": float(self.securities[symbol].price),
                        "entry_date": str(today),
                        "report_time": report_time,
                    }

        desired_tickers = sorted(self.days_remaining.keys())
        desired_symbols = [self.symbol_by_ticker[ticker] for ticker in desired_tickers]
        invested_symbols = [
            symbol for symbol, holding in self.portfolio.items()
            if holding.invested
        ]
        for symbol in invested_symbols:
            if symbol not in desired_symbols:
                self.liquidate(symbol, "not_in_event_basket")

        if desired_symbols:
            weight = 1.0 / len(desired_symbols)
            for symbol in desired_symbols:
                self.set_holdings(symbol, weight)

        self.rebalance_count += 1
        if self.rebalance_count <= 5:
            tickers = ", ".join(ticker for _, ticker, _ in selected) or "none"
            self.log(
                f"{today} style=swing mode={self.event_mode} bucket={self.bucket} "
                f"estimate_mode={self.estimate_mode} selected={tickers} "
                f"active={','.join(desired_tickers) or 'none'}"
            )

    def _on_data_intraday(self, data: Slice) -> None:
        today = self.time.date()
        if self.current_day != today:
            self._roll_intraday_day(today)

        for symbol in self.daily_history:
            if symbol in data.bars:
                self._update_intraday_state(symbol, data.bars[symbol])

        if self.entry_symbol is not None:
            self._manage_open_intraday()

        if not self.intraday_event_tickers:
            return
        if self.daily_trade_count >= self.max_daily_trades or self.entry_symbol is not None:
            return
        if not self._in_intraday_entry_window():
            return
        if not self._context_intraday_ok():
            return

        if not self.watchlist_finalized:
            self._finalize_intraday_watchlist()
        if not self.watchlist_symbols:
            return

        for symbol in self.watchlist_symbols:
            if self.entry_symbol is not None or self.daily_trade_count >= self.max_daily_trades:
                break
            self._try_intraday_entry(symbol)

    def _roll_intraday_day(self, new_day: date) -> None:
        if self.current_day is not None:
            for symbol, state in self.intraday_state.items():
                if state["regular_open"] is None or state["regular_close"] is None:
                    continue
                history = self.daily_history[symbol]
                history.append(
                    {
                        "date": self.current_day,
                        "open": state["regular_open"],
                        "high": state["regular_high"],
                        "low": state["regular_low"],
                        "close": state["regular_close"],
                        "volume": state["regular_volume"],
                        "dollar_volume": state["regular_close"] * state["regular_volume"],
                    }
                )
                if len(history) > self.max_daily_history:
                    self.daily_history[symbol] = history[-self.max_daily_history:]

        if self.entry_symbol is not None and self.portfolio[self.entry_symbol].invested:
            self._close_intraday("day_roll_liquidate")

        self.current_day = new_day
        self.intraday_state = {symbol: self._new_intraday_state() for symbol in self.intraday_state}
        self.watchlist_symbols = []
        self.watchlist_finalized = False
        self.entry_symbol = None
        self.entry_time = None
        self.entry_price = None
        self.stop_price = None
        self.target_price = None
        self.daily_trade_count = 0
        self.intraday_event_tickers = self._eligible_intraday_event_tickers(new_day)

    def _eligible_intraday_event_tickers(self, today: date):
        tickers = []
        for ticker in self.allowed_tickers:
            report_date = self.known_report_dates.get(ticker)
            if report_date is None or not self._event_matches(today, report_date):
                continue
            report_time = self.known_report_times.get(ticker, "")
            if not self._report_time_matches(report_time):
                continue
            estimate = self.known_estimates.get(ticker)
            if self.estimate_mode == "required" and estimate is None:
                continue
            if self.estimate_mode == "missing" and estimate is not None:
                continue
            if self._fails_quality_floor(ticker):
                continue
            tickers.append(ticker)
        return tickers

    def _update_intraday_state(self, symbol: Symbol, bar: TradeBar) -> None:
        state = self.intraday_state[symbol]
        current_time = bar.end_time.time()
        market_open = time(9, 30)
        market_close = time(16, 0)

        if current_time < market_open:
            state["premarket_high"] = bar.high if state["premarket_high"] is None else max(state["premarket_high"], bar.high)
            state["premarket_low"] = bar.low if state["premarket_low"] is None else min(state["premarket_low"], bar.low)
            state["premarket_volume"] += float(bar.volume)
            return

        if current_time >= market_close:
            return

        price = float(bar.close)
        volume = float(bar.volume)
        if state["regular_open"] is None:
            state["regular_open"] = float(bar.open)
            history = self.daily_history.get(symbol, [])
            state["prev_day"] = history[-1] if history else None

        state["regular_high"] = price if state["regular_high"] is None else max(state["regular_high"], float(bar.high))
        state["regular_low"] = price if state["regular_low"] is None else min(state["regular_low"], float(bar.low))
        state["regular_close"] = price
        state["regular_volume"] += volume

        state["session_high"] = price if state["session_high"] is None else max(state["session_high"], float(bar.high))
        state["session_low"] = price if state["session_low"] is None else min(state["session_low"], float(bar.low))
        state["vwap_price_volume"] += price * volume
        state["vwap_volume"] += volume

        opening_range_end = (datetime.combine(self.current_day, market_open) + timedelta(minutes=self.opening_range_minutes)).time()
        if current_time <= opening_range_end:
            state["opening_range_high"] = (
                float(bar.high)
                if state["opening_range_high"] is None
                else max(state["opening_range_high"], float(bar.high))
            )
            state["opening_range_low"] = (
                float(bar.low)
                if state["opening_range_low"] is None
                else min(state["opening_range_low"], float(bar.low))
            )

    def _finalize_intraday_watchlist(self) -> None:
        if not self._opening_range_complete():
            return

        candidates = []
        for ticker in self.intraday_event_tickers:
            symbol = self.symbol_by_ticker[ticker]
            security = self.securities[symbol]
            if not security.has_data or security.price < self.min_price:
                continue

            state = self.intraday_state[symbol]
            prev_day = state["prev_day"]
            if prev_day is None or state["regular_open"] is None:
                continue
            avg_dollar_volume = self._avg_dollar_volume(symbol, 20)
            if avg_dollar_volume < self.min_avg_dollar_volume:
                continue
            recent_return = self._recent_return(symbol, self.lookback_days)
            if recent_return is None:
                continue
            if self.require_recent_weakness and recent_return > self.weak_return_max:
                continue

            if prev_day["close"] <= 0:
                continue
            gap_pct = (state["regular_open"] / prev_day["close"]) - 1.0
            if gap_pct < self.gap_min or gap_pct > self.gap_max:
                continue

            premarket_dollar_volume = state["premarket_volume"] * max(state["regular_open"], prev_day["close"])
            if premarket_dollar_volume < self.min_premarket_dollar_volume:
                continue

            premarket_vol_ratio = premarket_dollar_volume / avg_dollar_volume if avg_dollar_volume > 0 else 0.0
            if premarket_vol_ratio < self.premarket_vol_ratio_min:
                continue

            if self.intraday_family == "failed_breakdown":
                key_level = prev_day["low"]
                score = (
                    self._intraday_recent_return_score(recent_return)
                    * max(premarket_vol_ratio, 0.0)
                    * (1.0 + abs(min(gap_pct, 0.0)))
                )
            else:
                key_level = max(prev_day["high"], prev_day["close"])
                score = self._intraday_recent_return_score(recent_return) * max(premarket_vol_ratio, 0.0)

            key_level_distance_pct = abs((state["regular_open"] / key_level) - 1.0) if key_level > 0 else 0.0
            if self.max_key_level_distance_pct > 0 and key_level_distance_pct > self.max_key_level_distance_pct:
                continue

            if self.rank_premarket_dollar_volume_scale > 0:
                score *= 1.0 + min(premarket_dollar_volume / self.rank_premarket_dollar_volume_scale, 10.0)
            if self.rank_key_level_distance_penalty > 0:
                score /= 1.0 + (key_level_distance_pct / self.rank_key_level_distance_penalty)

            state["gap_pct"] = gap_pct
            state["premarket_vol_ratio"] = premarket_vol_ratio
            state["avg_dollar_volume"] = avg_dollar_volume
            state["premarket_dollar_volume"] = premarket_dollar_volume
            state["recent_return"] = recent_return
            state["key_level"] = key_level
            state["key_level_distance_pct"] = key_level_distance_pct

            candidates.append((score, ticker, symbol))

        candidates.sort(key=lambda item: (-item[0], item[1]))
        selected = candidates[: self.selection_pool_size]
        self.watchlist_symbols = [item[2] for item in selected]
        self.watchlist_finalized = True

        if selected:
            self.selection_count += 1
            for _, ticker, _ in selected:
                self.selection_by_ticker[ticker] = self.selection_by_ticker.get(ticker, 0) + 1

        if self.day_selection_log_count < 8:
            tickers = ",".join(item[1] for item in selected) or "none"
            self.log(
                f"{self.current_day} style=intraday family={self.intraday_family} "
                f"bucket={self.bucket} mode={self.event_mode} report_time={self.report_time_filter} "
                f"estimate_mode={self.estimate_mode} candidates={','.join(self.intraday_event_tickers) or 'none'} "
                f"selected={tickers}"
            )
            self.day_selection_log_count += 1

    def _context_intraday_ok(self) -> bool:
        if not self.context_symbol_by_ticker:
            return True

        positive = 0
        seen = 0
        for symbol in self.context_symbol_by_ticker.values():
            state = self.intraday_state.get(symbol)
            if state is None or state["regular_open"] is None:
                return False
            vwap = self._session_vwap(symbol)
            if vwap <= 0:
                return False
            price = float(self.securities[symbol].price)
            ok = True
            if self.context_require_above_vwap and price <= vwap:
                ok = False
            if self.context_require_above_open and price <= state["regular_open"]:
                ok = False
            seen += 1
            if ok:
                positive += 1

        if seen == 0:
            return False
        if self.context_min_positive is not None and positive < self.context_min_positive:
            return False
        if self.context_max_positive is not None and positive > self.context_max_positive:
            return False
        return True

    def _try_intraday_entry(self, symbol: Symbol) -> None:
        state = self.intraday_state[symbol]
        prev_day = state["prev_day"]
        if (
            prev_day is None
            or state["regular_open"] is None
            or state["opening_range_low"] is None
            or state["opening_range_high"] is None
            or state["session_low"] is None
        ):
            return

        price = float(self.securities[symbol].price)
        vwap = self._session_vwap(symbol)
        if vwap <= 0:
            return

        if self.intraday_family == "failed_breakdown":
            flush_level = min(
                state["regular_open"] * (1.0 - self.morning_flush_pct),
                prev_day["low"] * (1.0 - self.breakdown_buffer_pct),
            )
            if state["session_low"] <= flush_level:
                state["flush_seen"] = True
            if not state["flush_seen"]:
                return
            if price <= vwap or price <= prev_day["low"]:
                state["confirm_start"] = None
                return
            stop_reference = min(state["session_low"], state["opening_range_low"])
            tag = "event_failed_breakdown_entry"
        else:
            if state["session_low"] <= state["regular_open"] * (1.0 - self.morning_flush_pct):
                state["flush_seen"] = True
            if not state["flush_seen"]:
                return
            breakout_level = max(prev_day["high"], prev_day["close"], state["opening_range_high"])
            if price <= vwap or price <= breakout_level:
                state["confirm_start"] = None
                return
            stop_reference = min(state["session_low"], state["opening_range_low"], prev_day["close"])
            tag = "event_bsl_entry"

        if state["confirm_start"] is None:
            state["confirm_start"] = self.time
            return

        held_above = (self.time - state["confirm_start"]).total_seconds() / 60.0
        if held_above + 1e-9 < self.confirm_hold_minutes:
            return

        self._enter_intraday(symbol, price, stop_reference, tag)

    def _enter_intraday(self, symbol: Symbol, price: float, stop_reference: float, tag: str) -> None:
        stop_price = stop_reference * (1.0 - self.stop_buffer_pct)
        if stop_price <= 0 or stop_price >= price:
            return

        risk_per_share = price - stop_price
        if risk_per_share <= 0:
            return

        target_price = price + (self.risk_reward * risk_per_share)
        self.set_holdings(symbol, 1.0, tag=tag)
        self.entry_symbol = symbol
        self.entry_time = self.time
        self.entry_price = price
        self.stop_price = stop_price
        self.target_price = target_price
        self.daily_trade_count += 1
        self.log(
            f"{self.time} enter {symbol.value} family={self.intraday_family} "
            f"entry={price:.2f} stop={stop_price:.2f} target={target_price:.2f}"
        )

    def _manage_open_intraday(self) -> None:
        symbol = self.entry_symbol
        if symbol is None:
            return

        price = float(self.securities[symbol].price)
        current_time = self.time.time()
        force_exit_time = (
            datetime.combine(self.current_day, time(16, 0))
            - timedelta(minutes=self.force_exit_minutes_before_close)
        ).time()
        if price <= self.stop_price:
            self._close_intraday("intraday_stop")
            return
        if price >= self.target_price:
            self._close_intraday("intraday_target")
            return
        if self.entry_time is not None:
            held_minutes = (self.time - self.entry_time).total_seconds() / 60.0
            if held_minutes >= self.max_holding_minutes:
                self._close_intraday("intraday_time_exit")
                return
        if current_time >= force_exit_time:
            self._close_intraday("intraday_eod_exit")

    def _close_intraday(self, tag: str) -> None:
        if self.entry_symbol is None:
            return
        symbol = self.entry_symbol
        if self.portfolio[symbol].invested:
            self.liquidate(symbol, tag)
        self.completed_trades += 1
        self.entry_symbol = None
        self.entry_time = None
        self.entry_price = None
        self.stop_price = None
        self.target_price = None

    def _opening_range_complete(self) -> bool:
        market_open = datetime.combine(self.current_day, time(9, 30))
        return self.time >= market_open + timedelta(minutes=self.opening_range_minutes)

    def _in_intraday_entry_window(self) -> bool:
        market_open = datetime.combine(self.current_day, time(9, 30))
        entry_deadline = market_open + timedelta(minutes=self.max_entry_minutes)
        return self._opening_range_complete() and self.time <= entry_deadline

    def _event_matches(self, today: date, report_date: date) -> bool:
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

    def _avg_dollar_volume(self, symbol: Symbol, lookback_days: int) -> float:
        history = self.daily_history[symbol]
        if len(history) < lookback_days:
            return 0.0
        sample = history[-lookback_days:]
        return sum(item["dollar_volume"] for item in sample) / float(lookback_days)

    def _recent_return(self, symbol: Symbol, lookback_days: int):
        history = self.daily_history[symbol]
        if len(history) < lookback_days + 1:
            return None
        start_close = history[-(lookback_days + 1)]["close"]
        end_close = history[-1]["close"]
        if start_close <= 0:
            return None
        return (end_close / start_close) - 1.0

    def _intraday_recent_return_score(self, recent_return: float) -> float:
        if self.recent_return_score_mode == "absolute":
            return abs(recent_return)
        if self.recent_return_score_mode == "none":
            return 1.0
        return abs(min(recent_return, 0.0))

    def _session_vwap(self, symbol: Symbol) -> float:
        state = self.intraday_state.get(symbol)
        if state is None or state["vwap_volume"] <= 0:
            return 0.0
        return state["vwap_price_volume"] / state["vwap_volume"]

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

    def _effective_hold_days(self, report_time: str) -> int:
        value = (report_time or "").strip().lower()
        if ("before" in value or "bmo" in value or "open" in value) and self.hold_days_before_open is not None:
            return self.hold_days_before_open
        if ("after" in value or "amc" in value or "close" in value) and self.hold_days_after_close is not None:
            return self.hold_days_after_close
        if value == "" and self.hold_days_unknown is not None:
            return self.hold_days_unknown
        return self.hold_days

    def _context_positive_count(self):
        if not self.context_symbol_by_ticker:
            return None
        count = 0
        seen = 0
        for symbol in self.context_symbol_by_ticker.values():
            recent_return = self._recent_return(symbol, self.context_lookback_days)
            if recent_return is None:
                return None
            seen += 1
            if recent_return >= self.context_return_threshold:
                count += 1
        return count if seen > 0 else None

    def _symbol_quality_bonus(self, ticker: str) -> float:
        if self.quality_weight == 0:
            return 0.0
        count = self.symbol_quality_event_count.get(ticker, 0)
        if count < self.quality_min_events:
            return 0.0
        avg_return = self.symbol_quality_sum_return.get(ticker, 0.0) / float(count)
        shrink = count / float(count + self.quality_shrinkage_events) if self.quality_shrinkage_events > 0 else 1.0
        return avg_return * shrink * self.quality_weight

    def _fails_quality_floor(self, ticker: str) -> bool:
        if self.quality_filter_min_events <= 0:
            return False
        count = self.symbol_quality_event_count.get(ticker, 0)
        if count < self.quality_filter_min_events:
            return False
        avg_return = self.symbol_quality_sum_return.get(ticker, 0.0) / float(count)
        return avg_return < self.quality_min_avg_return

    def _record_completed_event(self, ticker: str, symbol: Symbol) -> None:
        position = self.active_event_positions.get(ticker)
        if position is None:
            return
        entry_price = float(position.get("entry_price", 0.0))
        exit_price = float(self.securities[symbol].price)
        if entry_price <= 0 or exit_price <= 0:
            return
        event_return = (exit_price / entry_price) - 1.0
        self.symbol_quality_sum_return[ticker] = self.symbol_quality_sum_return.get(ticker, 0.0) + event_return
        self.symbol_quality_event_count[ticker] = self.symbol_quality_event_count.get(ticker, 0) + 1
        if event_return > 0:
            self.symbol_quality_win_count[ticker] = self.symbol_quality_win_count.get(ticker, 0) + 1

    def on_end_of_algorithm(self) -> None:
        if self.strategy_style == "master_portfolio":
            self.master_integration.on_end_of_algorithm()
            return
        summary = ", ".join(
            f"{ticker}:{count}"
            for ticker, count in sorted(
                self.selection_by_ticker.items(),
                key=lambda item: (-item[1], item[0])
            )
        ) or "none"
        report_times = ", ".join(
            f"{label}:{count}"
            for label, count in sorted(
                self.report_time_counts.items(),
                key=lambda item: (-item[1], item[0])
            )
        ) or "none"
        quality_summary = ", ".join(
            f"{ticker}:{self.symbol_quality_sum_return.get(ticker, 0.0) / self.symbol_quality_event_count[ticker]:.3f}"
            for ticker in sorted(
                self.symbol_quality_event_count,
                key=lambda item: (
                    -(
                        self.symbol_quality_sum_return.get(item, 0.0)
                        / float(self.symbol_quality_event_count[item])
                    ),
                    item,
                )
            )
        ) or "none"
        extra = ""
        if self.strategy_style == "intraday":
            extra = (
                f" | intraday_family={self.intraday_family} | selection_pool_size={self.selection_pool_size}"
                f" | trades={self.completed_trades}"
            )
        self.log(
            f"Earnings event round complete | style={self.strategy_style} | bucket={self.bucket} "
            f"| mode={self.event_mode} | report_time_filter={self.report_time_filter} "
            f"| estimate_mode={self.estimate_mode} | selections={self.selection_count} "
            f"| rebalances={self.rebalance_count} | ticker_counts={summary} "
            f"| report_times={report_times} | quality={quality_summary}{extra}"
        )
