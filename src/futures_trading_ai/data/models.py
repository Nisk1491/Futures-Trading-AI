"""Data models for market data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Candle:
    """OHLCV candle used by indicators and strategies."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self) -> None:
        if self.high < self.low:
            raise ValueError("candle high must be greater than or equal to low")

        prices = {
            "open": self.open,
            "close": self.close,
        }
        for field_name, price in prices.items():
            if price > self.high or price < self.low:
                raise ValueError(f"candle {field_name} must be between low and high")

        if self.volume < 0:
            raise ValueError("candle volume must be non-negative")
