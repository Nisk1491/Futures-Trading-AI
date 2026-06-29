# Codex Task Plan

## Task 1: Create Python project skeleton

Create the following folders and placeholder files:

```text
src/futures_trading_ai/
src/futures_trading_ai/data/
src/futures_trading_ai/indicators/
src/futures_trading_ai/strategy/
src/futures_trading_ai/backtest/
src/futures_trading_ai/broker/
src/futures_trading_ai/journal/
tests/
examples/
```

Add `__init__.py` files where needed.

## Task 2: Define Candle model

Create `src/futures_trading_ai/data/models.py` with:

- Candle dataclass
- fields: timestamp, open, high, low, close, volume
- validation for high and low

## Task 3: Define Signal model

Create `src/futures_trading_ai/strategy/signals.py` with:

- SignalSide enum: LONG, SHORT, WAIT
- TradeSignal dataclass
- fields: side, entry_price, stop_loss, take_profit, reason

## Task 4: Support and resistance module

Create `src/futures_trading_ai/indicators/support_resistance.py`.

Start with a simple swing high and swing low detector.

## Task 5: Basic strategy engine

Create `src/futures_trading_ai/strategy/nisk_strategy.py`.

First version can return WAIT most of the time, but must include clear structure for future strategy logic.

## Task 6: Tests

Create tests for:

- Candle model
- Signal model
- Support and resistance detection
- Strategy output format

## Development Rules

- Keep code simple.
- Add type hints.
- Avoid real broker API in the first version.
- Do not add live order execution yet.
- Every strategy output must include a reason string.
