# Personal Finance Multi-Agent System

多代理個人投資 / 理財研究系統，第一版聚焦台股個股研究，預設標的為群聯電子（8299）。

目前 repo 仍在 OpenSpec 規格與設計階段，尚未開始產品實作。核心文件：

- `SPEC.md`：中文產品規格與 AIASE final project 對齊。
- `openspec/changes/personal-finance-multi-agent-system/`：OpenSpec proposal、design、tasks 與需求規格。
- `golden_samples/`：群聯公開來源 proxy golden sample。
- `TAICA_AIASE2026-main/final_project_資訊整理.md`：課程 final project 要求整理。

第一版實作邊界：

- Flask 後端 + Vue 前端。
- 本機 Markdown / JSON fixture。
- mock / deterministic agents。
- 手動股價或使用者輸入，不接即時行情 API。
- LLMWiki-lite：群聯 7 個 wiki pages + provenance + contradiction log。
- 不先接 Supabase、真實 LLM、爬蟲或外部行情 API。
