# Codex Task Plan

## Current Strategy

Implement the first formal strategy:

- Strategy name: Nisk MA Cross Strategy v0.1
- Timeframe: 5m
- Fast MA: 20
- Slow MA: 60
- MA type: SMA
- Golden cross: LONG
- Death cross: SHORT
- No cross: WAIT

The strategy must be configurable. Do not hard-code 20 and 60 inside business logic. Put them in a config file.

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
config/
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

## Task 4: Moving average calculator

Create `src/futures_trading_ai/indicators/moving_average.py` with:

- calculate_sma(values, period)
- return a list where unavailable early values are None
- validate period > 0

## Task 5: MA cross detector

Create `src/futures_trading_ai/indicators/ma_cross.py` with:

- detect_ma_cross(previous_fast, previous_slow, current_fast, current_slow)
- return GOLDEN_CROSS, DEATH_CROSS, or NO_CROSS

Rules:

```text
previous_fast <= previous_slow and current_fast > current_slow => GOLDEN_CROSS
previous_fast >= previous_slow and current_fast < current_slow => DEATH_CROSS
otherwise => NO_CROSS
```

## Task 6: Strategy config

Create `config/strategy.yaml`:

```yaml
strategy:
  name: nisk_ma_cross_v0_1
  timeframe: 5m
  indicators:
    moving_average_cross:
      ma_type: SMA
      fast_period: 20
      slow_period: 60
  signal:
    golden_cross: LONG
    death_cross: SHORT
    no_cross: WAIT
```

Create a config loader module if needed.

## Task 7: Basic strategy engine

Create `src/futures_trading_ai/strategy/nisk_ma_cross_strategy.py`.

Input:

- list of Candle
- strategy config

Output:

- TradeSignal

Behavior:

- If candles are fewer than slow_period + 1, return WAIT.
- Calculate SMA using candle close prices.
- Detect 20/60 cross from previous candle to current candle.
- Golden cross returns LONG.
- Death cross returns SHORT.
- No cross returns WAIT.
- Every output must include a reason string.

## Task 8: Tests

Create tests for:

- Candle model
- Signal model
- SMA calculation
- MA cross detection
- Strategy config loading
- Strategy output LONG, SHORT, WAIT

## Development Rules

- Keep code simple.
- Add type hints.
- Avoid real broker API in the first version.
- Do not add live order execution yet.
- Every strategy output must include a reason string.
