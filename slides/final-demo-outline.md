# Final Demo Outline

## 1. Problem

個人投資者研究台股時，很容易被新聞、券商目標價和單一敘事帶走，缺少可追溯、可反駁的研究流程。

## 2. User

想學習台股個股研究、但需要 AI 幫忙整理資料、拆解假設與檢查風險的個人投資者。

## 3. Core Idea

不是單純 RAG，而是：

```text
Raw sources -> LLMWiki-lite -> Multi-agent workflow -> Report -> Evaluation
```

## 4. Architecture

- Vue frontend。
- Flask backend。
- Local fixtures。
- Deterministic agents。
- LLMWiki-lite provenance。

## 5. Demo Path

1. 開啟研究工作台。
2. 使用群聯 8299 預設研究問題。
3. 調整示範股價。
4. 啟動研究。
5. 展示 agent trace。
6. 展示 source map。
7. 展示 wiki provenance 與 contradiction log。
8. 展示 report。
9. 展示 evaluation score。

## 6. Safety and Audit

- 明確標示不是買賣建議。
- CMoney / 新聞摘要不是完整券商研報。
- 未揭露券商名單不得自行補齊。
- 示範股價不是即時行情。

## 7. Next Steps

- 接真實 LLM。
- 接 Supabase。
- 加入 Exa / crawler。
- 補正式財報與券商研報。
- 擴充到更多台股標的。
