# Project Overview

## 核心定位

Futures-Trading-AI 是一套期貨交易決策系統。它的核心不是預測未來，而是把交易規則標準化，讓每一次進場、停損、停利都有明確依據。

## 第一階段目標

建立一個可以穩定運作的 Signal Bot：

- 接收或讀取 5 分鐘 K 線資料
- 判斷目前市場狀態
- 輸出交易訊號
- 計算風險與報酬
- 記錄每一次訊號原因

## 長期願景

未來系統會逐步擴展為 Nisk Trading OS：

- Strategy Engine：策略引擎
- Decision Engine：決策引擎
- Backtest Engine：回測引擎
- Risk Manager：風控模組
- Trade Journal：交易日誌
- AI Reviewer：AI 交易檢討助手
- Broker Adapter：券商 API 串接層

## 開發原則

1. 先規則化，再自動化。
2. 先回測，再模擬，再實盤。
3. 任何交易訊號都必須能說明原因。
4. 任何策略都必須有停損。
5. 不做沒有風控的自動下單。
