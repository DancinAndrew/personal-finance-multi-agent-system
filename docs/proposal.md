# Proposal：多代理個人投資 / 理財研究系統

## 一句話定位

建立一個可展示的生成式 AI Web service，幫使用者把台股個股研究拆成可追溯、可審計、可評估的多代理流程。

## 使用者與場景

使用者是想學習台股個股研究、但還不熟悉如何整合新聞、財報、券商摘要與產業敘事的個人投資者。第一版以群聯電子（8299）為研究標的，回答「AI SSD 成長故事是否足以支撐目前估值」。

## Quality-of-Life 價值

- 降低個股研究起步成本。
- 把資料來源、代理推理、風險與評估放在同一個工作台。
- 讓使用者學會判斷資料可信度，而不是只看單一新聞或目標價。

## Outcome

使用者得到一份帶來源、估值情境、風險與評估分數的研究輔助報告，並能追溯每個重要主張來自哪些來源與哪個 agent step。

## MVP Scope

- Flask API。
- Vue Web 工作台。
- 本機 fixtures。
- Deterministic agents。
- LLMWiki-lite 研究知識層。
- 群聯 proxy golden sample。

## Out of Scope

- 自動下單。
- 即時行情。
- Supabase 持久化。
- 真實 LLM provider。
- 自動爬蟲。
- 完整 knowledge graph。
