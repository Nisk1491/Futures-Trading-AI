"""Moving-average cross detection."""

from __future__ import annotations

from enum import StrEnum


class MACross(StrEnum):
    """Possible moving-average cross states."""

    GOLDEN_CROSS = "GOLDEN_CROSS"
    DEATH_CROSS = "DEATH_CROSS"
    NO_CROSS = "NO_CROSS"


def detect_ma_cross(
    previous_fast: float | None,
    previous_slow: float | None,
    current_fast: float | None,
    current_slow: float | None,
) -> MACross:
    """Detect whether fast and slow moving averages crossed on the current bar."""
    if None in (previous_fast, previous_slow, current_fast, current_slow):
        return MACross.NO_CROSS

    if previous_fast <= previous_slow and current_fast > current_slow:
        return MACross.GOLDEN_CROSS
    if previous_fast >= previous_slow and current_fast < current_slow:
        return MACross.DEATH_CROSS
    return MACross.NO_CROSS
