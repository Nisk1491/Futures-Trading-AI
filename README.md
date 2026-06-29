# Futures-Trading-AI

AI期貨交易系統，包含策略、回測、風控、交易日誌與AI分析。

## Project Mission

這個專案的第一目標不是一開始就全自動下單，而是先把「Nisk 的交易判斷流程」數位化，建立一套可以被回測、驗證、優化的交易決策系統。

## First Milestone: Signal Bot

第一版先完成「訊號提醒版」，包含：

- 讀取 5 分鐘 K 線資料
- 計算支撐、壓力、突破與回踩
- 產生做多、做空、觀望訊號
- 計算停損、停利與風報比
- 輸出交易日誌，方便後續檢討

## Project Structure

```text
Futures-Trading-AI/
├── docs/
│   ├── PROJECT.md
│   ├── ROADMAP.md
│   ├── STRATEGY.md
│   ├── RISK.md
│   └── CODEX_TASKS.md
├── src/
│   └── futures_trading_ai/
│       ├── data/
│       ├── indicators/
│       ├── strategy/
│       ├── backtest/
│       ├── risk/
│       ├── broker/
│       └── journal/
├── tests/
├── examples/
└── data/
```

## Safety First

本專案初期只做訊號與回測，不直接連接實盤自動下單。任何自動下單功能都必須經過：

1. 歷史資料回測
2. 模擬交易
3. 小口數測試
4. 明確風控限制

## Strategy Direction

初始策略方向：

- 5 分鐘 K 線
- 支撐壓力區間
- 突破確認
- 回踩不破
- 風報比至少 1:2
- 單筆風險固定
- 每日最大虧損限制

## Development Status

目前狀態：專案初始化。

下一步：建立文件、策略規格、資料格式與第一版 Codex 任務。