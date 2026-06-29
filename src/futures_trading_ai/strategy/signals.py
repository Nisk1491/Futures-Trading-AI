"""Trading signal models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SignalSide(StrEnum):
    """Supported strategy signal sides."""

    LONG = "LONG"
    SHORT = "SHORT"
    WAIT = "WAIT"


@dataclass(frozen=True, slots=True)
class TradeSignal:
    """Strategy output containing signal direction and risk details."""

    side: SignalSide
    entry_price: float | None
    stop_loss: float | None
    take_profit: float | None
    reason: str
    risk_points: float | None = None
    reward_points: float | None = None
    risk_reward_ratio: float | None = None

    def __post_init__(self) -> None:
        if not self.reason:
            raise ValueError("trade signal reason must not be empty")
        if self.side is SignalSide.WAIT:
            return
        required = {
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "risk_points": self.risk_points,
            "reward_points": self.reward_points,
            "risk_reward_ratio": self.risk_reward_ratio,
        }
        missing = [name for name, value in required.items() if value is None]
        if missing:
            raise ValueError(f"non-WAIT signal requires risk fields: {', '.join(missing)}")
