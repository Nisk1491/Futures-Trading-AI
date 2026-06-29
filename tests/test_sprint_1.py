from datetime import datetime, timedelta

import pytest

from futures_trading_ai.config.loader import load_strategy_config
from futures_trading_ai.data.models import Candle
from futures_trading_ai.indicators.ma_cross import MACross, detect_ma_cross
from futures_trading_ai.indicators.moving_average import calculate_sma
from futures_trading_ai.strategy.nisk_ma_cross_strategy import generate_signal
from futures_trading_ai.strategy.signals import SignalSide, TradeSignal


def candle(close: float, index: int = 0) -> Candle:
    return Candle(
        timestamp=datetime(2026, 1, 1) + timedelta(minutes=index * 5),
        open=close,
        high=close + 1,
        low=close - 1,
        close=close,
        volume=1,
    )


def config(fast: int = 2, slow: int = 3) -> dict:
    return {
        "strategy": {
            "name": "test",
            "timeframe": "5m",
            "indicators": {
                "moving_average_cross": {
                    "ma_type": "SMA",
                    "fast_period": fast,
                    "slow_period": slow,
                }
            },
            "signal": {
                "golden_cross": "LONG",
                "death_cross": "SHORT",
                "no_cross": "WAIT",
            },
            "risk": {
                "stop_loss_source": "signal_candle_extreme",
                "risk_reward_ratio": 2.0,
            },
        }
    }


def test_candle_validates_high_and_low():
    with pytest.raises(ValueError):
        Candle(datetime(2026, 1, 1), open=10, high=9, low=11, close=10, volume=1)


def test_trade_signal_requires_reason_and_risk_fields_for_trade():
    wait = TradeSignal(SignalSide.WAIT, None, None, None, "waiting")
    assert wait.side is SignalSide.WAIT

    with pytest.raises(ValueError):
        TradeSignal(SignalSide.LONG, 100, 99, None, "missing take profit")


def test_calculate_sma_returns_none_for_unavailable_values():
    assert calculate_sma([1, 2, 3, 4], 3) == [None, None, 2, 3]


def test_calculate_sma_validates_period():
    with pytest.raises(ValueError):
        calculate_sma([1, 2, 3], 0)


def test_detect_ma_cross_states():
    assert detect_ma_cross(1, 2, 3, 2) is MACross.GOLDEN_CROSS
    assert detect_ma_cross(3, 2, 1, 2) is MACross.DEATH_CROSS
    assert detect_ma_cross(1, 2, 1, 2) is MACross.NO_CROSS
    assert detect_ma_cross(None, 2, 3, 2) is MACross.NO_CROSS


def test_strategy_config_loading():
    loaded = load_strategy_config("config/strategy.yaml")
    ma_config = loaded["strategy"]["indicators"]["moving_average_cross"]
    assert loaded["strategy"]["name"] == "nisk_ma_cross_v0_1"
    assert ma_config["fast_period"] == 20
    assert ma_config["slow_period"] == 60


def test_strategy_returns_wait_when_not_enough_candles():
    signal = generate_signal([candle(10), candle(11), candle(12)], config())
    assert signal.side is SignalSide.WAIT
    assert "Need at least" in signal.reason


def test_strategy_outputs_long_on_golden_cross():
    candles = [candle(value, index) for index, value in enumerate([10, 10, 10, 20])]
    signal = generate_signal(candles, config())
    assert signal.side is SignalSide.LONG
    assert signal.entry_price == 20
    assert signal.stop_loss == 19
    assert signal.take_profit == 22
    assert signal.risk_reward_ratio == 2


def test_strategy_outputs_short_on_death_cross():
    candles = [candle(value, index) for index, value in enumerate([20, 20, 20, 10])]
    signal = generate_signal(candles, config())
    assert signal.side is SignalSide.SHORT
    assert signal.entry_price == 10
    assert signal.stop_loss == 11
    assert signal.take_profit == 8
    assert signal.risk_reward_ratio == 2


def test_strategy_outputs_wait_when_no_cross():
    candles = [candle(value, index) for index, value in enumerate([10, 10, 10, 10])]
    signal = generate_signal(candles, config())
    assert signal.side is SignalSide.WAIT
    assert signal.reason == "No MA cross detected"
