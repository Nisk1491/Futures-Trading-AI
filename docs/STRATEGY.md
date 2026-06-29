# Strategy Specification

## 策略名稱

Nisk MA Cross Strategy v0.1

## 使用週期

- 主要週期：5 分鐘 K 線
- 初期商品：期貨商品，先以微型台指或台指期為主要觀察對象

## 第一版核心策略

第一版先使用 20MA 與 60MA 判斷多空方向。

這一版的重點不是追求複雜，而是先建立可以設定、可以回測、可以解釋的策略架構。

## 均線定義

- fast_ma: 20
- slow_ma: 60
- ma_type: SMA

未來可改為 EMA 或其他均線，但第一版先使用簡單移動平均線 SMA。

## 金叉定義

當 20MA 從下方穿越 60MA 到上方，定義為金叉。

條件：

```text
previous_20ma <= previous_60ma
current_20ma > current_60ma
```

金叉後，策略狀態偏多。

## 死叉定義

當 20MA 從上方穿越 60MA 到下方，定義為死叉。

條件：

```text
previous_20ma >= previous_60ma
current_20ma < current_60ma
```

死叉後，策略狀態偏空。

## 訊號輸出

策略引擎只輸出三種狀態：

- LONG：20MA 金叉 60MA
- SHORT：20MA 死叉 60MA
- WAIT：沒有交叉訊號

每一個訊號都必須包含：

- signal
- entry_price
- stop_loss
- take_profit
- risk_points
- reward_points
- risk_reward_ratio
- reason

## 策略設定檔方向

策略不要寫死在 Python 裡，未來要透過設定檔控制，例如：

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

這樣未來要測試 5/20、10/60、20/120 或 EMA，只需要改設定檔，不需要重寫策略程式。

## 暫不處理

第一版先不處理：

- 實盤自動下單
- AI 自動決定買賣
- 複雜技術指標堆疊
- 高頻交易
- 無停損策略

## 下一步

Codex 優先實作：

1. Moving average calculator
2. MA cross detector
3. Strategy config loader
4. Signal model
5. Unit tests
