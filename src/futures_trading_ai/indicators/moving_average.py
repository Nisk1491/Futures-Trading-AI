"""Moving average indicator calculations."""

from __future__ import annotations


def calculate_sma(values: list[float], period: int) -> list[float | None]:
    """Calculate a simple moving average with leading unavailable values as None."""
    if period <= 0:
        raise ValueError("period must be greater than zero")

    sma_values: list[float | None] = []
    rolling_sum = 0.0

    for index, value in enumerate(values):
        rolling_sum += value
        if index >= period:
            rolling_sum -= values[index - period]

        if index + 1 < period:
            sma_values.append(None)
        else:
            sma_values.append(rolling_sum / period)

    return sma_values
