"""Nisk moving-average cross strategy engine."""

from __future__ import annotations

from typing import Any

from futures_trading_ai.data.models import Candle
from futures_trading_ai.indicators.ma_cross import MACross, detect_ma_cross
from futures_trading_ai.indicators.moving_average import calculate_sma
from futures_trading_ai.strategy.signals import SignalSide, TradeSignal


def generate_signal(candles: list[Candle], strategy_config: dict[str, Any]) -> TradeSignal:
    """Generate one signal for the latest candle from configured MA-cross rules."""
    strategy = _strategy_section(strategy_config)
    ma_config = strategy["indicators"]["moving_average_cross"]
    fast_period = int(ma_config["fast_period"])
    slow_period = int(ma_config["slow_period"])
    ma_type = str(ma_config["ma_type"]).upper()

    if ma_type != "SMA":
        return _wait(f"MA type {ma_type} is not supported yet")
    if len(candles) < slow_period + 1:
        return _wait(f"Need at least {slow_period + 1} candles to detect a cross")

    closes = [candle.close for candle in candles]
    fast_ma = calculate_sma(closes, fast_period)
    slow_ma = calculate_sma(closes, slow_period)
    cross = detect_ma_cross(fast_ma[-2], slow_ma[-2], fast_ma[-1], slow_ma[-1])

    signal_config = strategy["signal"]
    if cross is MACross.GOLDEN_CROSS:
        side = SignalSide(signal_config["golden_cross"])
        return _trade_signal(side, candles[-1], strategy, "Golden cross detected")
    if cross is MACross.DEATH_CROSS:
        side = SignalSide(signal_config["death_cross"])
        return _trade_signal(side, candles[-1], strategy, "Death cross detected")

    return TradeSignal(
        side=SignalSide(signal_config["no_cross"]),
        entry_price=None,
        stop_loss=None,
        take_profit=None,
        reason="No MA cross detected",
    )


class NiskMACrossStrategy:
    """Small strategy wrapper that keeps configuration separate from execution."""

    def __init__(self, strategy_config: dict[str, Any]) -> None:
        self.strategy_config = strategy_config

    def generate_signal(self, candles: list[Candle]) -> TradeSignal:
        """Generate one signal for the latest candle."""
        return generate_signal(candles, self.strategy_config)


def _strategy_section(strategy_config: dict[str, Any]) -> dict[str, Any]:
    strategy = strategy_config.get("strategy", strategy_config)
    if not isinstance(strategy, dict):
        raise ValueError("strategy config must be a dictionary")
    return strategy


def _wait(reason: str) -> TradeSignal:
    return TradeSignal(
        side=SignalSide.WAIT,
        entry_price=None,
        stop_loss=None,
        take_profit=None,
        reason=reason,
    )


def _trade_signal(side: SignalSide, candle: Candle, strategy: dict[str, Any], reason: str) -> TradeSignal:
    if side is SignalSide.WAIT:
        return _wait(reason)

    risk_config = strategy["risk"]
    risk_reward_ratio = float(risk_config["risk_reward_ratio"])
    entry_price = candle.close
    stop_loss = _stop_loss_for(side, candle, risk_config)

    if side is SignalSide.LONG:
        risk_points = entry_price - stop_loss
        take_profit = entry_price + (risk_points * risk_reward_ratio)
    elif side is SignalSide.SHORT:
        risk_points = stop_loss - entry_price
        take_profit = entry_price - (risk_points * risk_reward_ratio)
    else:
        return _wait(reason)

    if risk_points <= 0:
        raise ValueError("risk points must be greater than zero")

    reward_points = abs(take_profit - entry_price)
    return TradeSignal(
        side=side,
        entry_price=entry_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
        reason=reason,
        risk_points=risk_points,
        reward_points=reward_points,
        risk_reward_ratio=reward_points / risk_points,
    )


def _stop_loss_for(side: SignalSide, candle: Candle, risk_config: dict[str, Any]) -> float:
    source = risk_config["stop_loss_source"]
    if source != "signal_candle_extreme":
        raise ValueError(f"unsupported stop_loss_source: {source}")
    if side is SignalSide.LONG:
        return candle.low
    if side is SignalSide.SHORT:
        return candle.high
    raise ValueError("WAIT signals do not have stop loss values")
