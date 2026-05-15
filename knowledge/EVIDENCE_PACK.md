# Finance Evidence Pack Schema

狀態：v0.1
用途：規範研究 evidence pages 的格式、引用、矛盾與人工 review。

## 原則

- Raw sources 不可直接修改，只能引用。
- Evidence pages 可以更新，但高風險更新必須人工 review。
- 每個重要 claim 必須能追溯到 `source_id`、日期、資料類型與可信度限制。
- CMoney、新聞、FactSet 共識、官方資料必須分層，不得混成同一可信度。
- Evidence Pack 不是最終投資建議，而是 agent 分析前的可讀證據層。

## Evidence Page Format

每個 page 應包含：

```markdown
# Page Title

狀態：
最後更新：
主要來源：

## 核心結論

## 重要 Claims

| Claim ID | Claim | Sources | 狀態 |

## 對研究問題的意義

## 風險 / 限制
```

## Claim Status

| Status | 意義 |
|---|---|
| `active` | 目前可用的 claim |
| `needs_review` | 需要人工確認後才能正式使用 |
| `stale` | 來源過期或 source hash 改變，需要更新 |
| `contradicted` | 已被新來源或其他來源明確衝突 |

## Contradiction Rules

以下情況必須寫入 `knowledge/phison/Contradiction_Log.md`：

- 同一年度 EPS 假設差異大到足以改變估值結論。
- 目標價或券商名單的來源沒有揭露細節，但 agent 嘗試補齊。
- 新財報數字推翻舊新聞摘要。
- 來源類型被誤用，例如把 CMoney 摘要當完整券商研報。
- 股價資料沒有日期或被誤稱為即時行情。

## Review Gate

以下更新不得自動採納：

- 改變偏多 / 中性 / 偏空結論。
- 改變 evaluation rubric 或 golden sample 標準。
- 新增未經來源確認的券商名單。
- 將新聞摘要升級成正式財報或完整研報。
- 將示範股價升級為即時行情。
