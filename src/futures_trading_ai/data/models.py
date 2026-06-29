from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Candle:
    """Single OHLCV candle."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self) -> None:
        if self.high < self.low:
            raise ValueError("high must be greater than or equal to low")
        if self.high < self.open or self.high < self.close:
            raise ValueError("high must be greater than or equal to open and close")
        if self.low > self.open or self.low > self.close:
            raise ValueError("low must be less than or equal to open and close")
        if self.volume < 0:
            raise ValueError("volume must be non-negative")
