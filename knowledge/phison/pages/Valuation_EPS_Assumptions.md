# Valuation EPS Assumptions

狀態：active  
最後更新：2026-05-10  
主要來源：S3、S4、S5、S7、S8、S9  

## 核心結論

群聯估值是否被 AI SSD 成長故事支撐，關鍵取決於 2026 EPS 假設。公開來源顯示 2026 EPS 從較保守的 FactSet 低標 134.78 元，到群益摘要 307.99 元，差距足以改變 Forward P/E 與投資結論。

## 重要 Claims

| Claim ID | Claim | Sources | 狀態 |
|---|---|---|---|
| claim_eps_factset_low | FactSet 2026 EPS 低標為 134.78 元。 | S5 | active |
| claim_eps_factset_median | FactSet 2026 EPS 中位數為 184.73 元。 | S5 | active |
| claim_eps_factset_avg | FactSet 2026 EPS 平均為 192.4 元。 | S5 | active |
| claim_eps_factset_high | FactSet 2026 EPS 高標為 276.05 元。 | S5 | active |
| claim_eps_capital_20260507 | 群益 2026-05-07 摘要預估 2026 EPS 約 307.99 元。 | S4 | active |
| claim_eps_q1_annualized | Q1 EPS 68.8 元乘以 4 約為 275.2 元，但只能作粗略 sanity check。 | S3 | needs_review |

## 對研究問題的意義

同一個股價 `P` 下，Forward P/E 對 EPS 假設非常敏感：

- FactSet 低標：`P / 134.78`
- FactSet 中位數：`P / 184.73`
- FactSet 平均：`P / 192.4`
- FactSet 高標：`P / 276.05`
- 群益高標摘要：`P / 307.99`

若採保守共識，市場已反映很多期待；若採高標 EPS，估值看起來合理許多。系統必須同時呈現這兩種視角。

## 風險 / 限制

- S4、S7、S8 是券商摘要，不是完整券商研報。
- S3 Q1 EPS 需正式財報補驗。
- 系統不得把最高 EPS 當作唯一 base case。
