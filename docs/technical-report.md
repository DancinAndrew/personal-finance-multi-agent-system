# Technical Report

## Problem

個人投資研究常遇到資料分散、來源可信度不明、新聞與券商摘要容易被過度解讀的問題。本系統以群聯電子（8299）為範例，建立可展示的多代理研究流程。

## System Design

- Frontend：Vue research workbench。
- Backend：Flask API。
- Agents：deterministic MVP agents。
- Data：local Markdown / JSON fixtures。
- Knowledge：Evidence Pack with provenance and contradiction log。
- Evaluation：5-point rubric plus hallucination guardrails。

## Agent Design

1. Intent Router：確認是否為台股研究任務。
2. Source Retrieval：讀取 source catalog、evidence pages、provenance。
3. News / Sector Agent：整理 AI SSD 與 NAND 敘事。
4. Fundamental Agent：整理營收、獲利能力、安全性、成長力與現金流品質。
5. Valuation Agent：用非即時示範股價、EPS 假設、公開券商摘要與缺口資料建立估值拆解。
6. Health Check Agent：將七種股票健診轉成保守狀態、理由與資料缺口。
7. Risk Agent：產生反方風險。
8. Report Generator：產生研究輔助報告。
9. Evaluation Agent：依 rubric 與 guardrails 評分。

## Data Sources

第一版使用本機整理的公開來源，包括群聯官方營收、鉅亨、經濟日報、CMoney、FTNN，以及 proxy golden sample。CMoney 與新聞摘要明確標記為非完整券商研報。

## Evaluation

Rubric 包含：

- 來源 grounding。
- 財務與估值嚴謹度。
- 基本面覆蓋與缺口誠實度。
- 健診與資料缺口誠實度。
- 產業敘事品質。
- 風險與反方觀點。
- 使用者可用性。

通過門檻為 4.0 / 5。

## Limitations

- 不提供買賣建議。
- 不接即時行情。
- 估值股價 fixture 不是即時行情，目標價與 Forward P/E 只作情境敏感度。
- 不接真實 LLM。
- 不接 Supabase。
- 尚未納入正式券商研報全文。
- Q1 財報新聞仍需正式財報補驗。

## Future Work

- 接入真實 LLM provider。
- 接 Supabase Cloud 保存研究歷史。
- 加入 Exa API 或 crawler。
- 接行情資料。
- 擴充為完整 knowledge graph 或 hybrid search。
