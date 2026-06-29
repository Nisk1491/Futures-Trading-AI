# Roadmap

## Phase 0: 專案初始化

- [x] 建立 GitHub repository
- [x] 建立 README
- [x] 建立專案文件
- [ ] 建立 Python 專案骨架
- [ ] 建立測試架構

## Phase 1: Signal Bot

目標：先做出訊號提醒，不做實盤自動下單。

- [ ] 定義 K 線資料格式
- [ ] 建立 Candle 資料模型
- [ ] 建立支撐壓力偵測
- [ ] 建立突破判斷
- [ ] 建立回踩判斷
- [ ] 建立多空訊號輸出
- [ ] 建立風報比計算

## Phase 2: Backtest

- [ ] 匯入歷史 K 線 CSV
- [ ] 回放每一根 K 線
- [ ] 記錄每一次交易訊號
- [ ] 統計勝率
- [ ] 統計平均賺賠比
- [ ] 統計最大連虧
- [ ] 統計最大回撤

## Phase 3: Trade Journal

- [ ] 建立交易日誌格式
- [ ] 記錄進場理由
- [ ] 記錄停損停利
- [ ] 記錄實際結果
- [ ] 產生每日檢討報告

## Phase 4: Broker Integration

- [ ] 研究券商 API
- [ ] 建立 broker adapter interface
- [ ] 模擬下單
- [ ] 紙上交易
- [ ] 小口數實測

## Phase 5: AI Reviewer

- [ ] 讀取交易日誌
- [ ] 分析常見錯誤
- [ ] 統計哪些條件最有效
- [ ] 產生每日改進建議
