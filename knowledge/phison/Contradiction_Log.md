# Contradiction Log

狀態：active  
最後更新：2026-05-10  

## Open Items

| ID | 類型 | 描述 | Sources | 狀態 | 處理方式 |
|---|---|---|---|---|---|
| C1 | EPS dispersion | 2026 EPS 假設從 FactSet 低標 134.78 元到群益摘要 307.99 元，差距足以改變估值結論。 | S4、S5 | active | 報告必須呈現情境分析，不得只採最高值。 |
| C2 | Missing broker names | CMoney 03/09 指出 10 家券商看多，但未揭露完整名單。 | S8 | active | 系統不得自行補齊名單。 |
| C3 | Source hierarchy | CMoney 與新聞摘要容易被誤當完整券商研報。 | S4、S6、S7、S8 | active | UI、報告與 evaluation 必須標示 proxy。 |
| C4 | Q1 financial verification | 新聞轉述 Q1 EPS、毛利率與淨利，但尚未在本資料集中納入正式財報。 | S3 | needs_review | 後續應用 MOPS 或公司正式財報補驗。 |
| C5 | Demo price freshness | `price_fixture.json` 的 2,430 元只作展示，不是即時行情。 | price_fixture | active | UI 與報告必須顯示非即時行情提醒。 |
