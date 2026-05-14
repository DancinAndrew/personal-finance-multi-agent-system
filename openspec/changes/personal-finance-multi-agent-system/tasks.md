# Tasks：多代理個人投資 / 理財系統 MVP

狀態：草稿 v0.1  
對應設計：`openspec/changes/personal-finance-multi-agent-system/design.md`  
第一版範圍：本機 fixture、mock / deterministic agents、手動股價、群聯 7 頁 LLMWiki-lite  

> 這份任務清單是實作前的工作拆解。每個階段都應能獨立驗收，避免一開始就接 Supabase、即時行情 API、爬蟲或真實 LLM。

## 0. Implementation 前提

- [x] 第一版先不接 Supabase，只用本機 Markdown / JSON fixture。
- [x] 第一版先不用真實 LLM，採 mock / deterministic agents。
- [x] 第一版股價用手動 fixture 或使用者輸入，不接即時行情 API。
- [x] LLMWiki-lite 第一版只做群聯 7 個 wiki pages + provenance + contradiction log。

## 1. 專案骨架

- [x] 建立 monorepo 目錄：`backend/`、`frontend/`、`data/`、`knowledge/`。
- [x] 建立交付物目錄：`docs/`、`slides/`。
- [x] 建立後端 Flask 專案骨架，但先不安裝或新增未確認依賴。
- [x] 建立前端 Vue 專案骨架，但先不接外部 UI framework，除非後續確認需要。
- [x] 建立共用文件：`README.md`、本機啟動方式、資料 fixture 說明。
- [x] 建立 `.env.example`，不得包含真實 secrets。
- [x] 確認 `.gitignore` 覆蓋 Python、Node、env、cache、local secrets。

驗收標準：

- 目錄結構清楚，能看出 backend / frontend / data / knowledge 的責任邊界。
- 尚未引入 Supabase、LLM provider、行情 API 或 crawler。

## 2. 本機資料 Fixture

- [x] 建立 `data/phison/source_catalog.json`，收錄 golden sample 中的來源 ID、標題、日期、URL、來源類型與可信度限制。
- [x] 建立 `data/phison/sources/*.md`，保存 5 到 10 則可展示的 source excerpt。
- [x] 建立 `data/phison/price_fixture.json`，包含示範股價、日期與「不可視為最新行情」標記。
- [x] 建立 `data/evaluation/rubric.json`，對應 5 分制 rubric 與 4.0 / 5 通過門檻。
- [x] 建立 `data/phison/demo_run.json`，作為 deterministic demo 的完整輸入。

驗收標準：

- 每筆 source 都有 `id`、`title`、`source`、`source_type`、`date`、`url_or_path`、`reliability_note`。
- price fixture 有明確日期，UI 與報告不得把它當成即時股價。
- rubric 能覆蓋 source grounding、valuation rigor、industry narrative、risk coverage、user usefulness。

## 3. LLMWiki-lite 知識層

- [x] 建立 `knowledge/FINANCE_WIKI.md`，定義 wiki page 格式、citation、claim provenance、stale claim、contradiction log 與 review gate。
- [x] 建立 `knowledge/phison/pages/Company_Phison_8299.md`。
- [x] 建立 `knowledge/phison/pages/Theme_AI_SSD.md`。
- [x] 建立 `knowledge/phison/pages/Cycle_NAND.md`。
- [x] 建立 `knowledge/phison/pages/Valuation_EPS_Assumptions.md`。
- [x] 建立 `knowledge/phison/pages/Risk_Register.md`。
- [x] 建立 `knowledge/phison/pages/Brokerage_View_Summary.md`。
- [x] 建立 `knowledge/phison/Contradiction_Log.md`。
- [x] 建立 `knowledge/phison/provenance.json`，記錄重要 claim 與 source IDs。

驗收標準：

- 7 個 wiki pages 都能被人類直接閱讀，不只是資料 dump。
- 每個重要財務數字、EPS 假設、目標價、券商觀點都能追溯到 source ID。
- `Contradiction_Log.md` 至少記錄目前已知限制，例如 CMoney 03/09 有 10 家券商但未揭露完整名單。

## 4. 後端 Deterministic Pipeline

- [x] 實作 Flask app factory 與 `/api/health`。
- [x] 實作 file store，讀取 source catalog、wiki pages、provenance、rubric、demo run。
- [x] 實作 `IntentRouter` mock：辨識群聯台股研究任務。
- [x] 實作 `SourceRetrieval` deterministic agent：回傳 curated source bundle 與 wiki context。
- [x] 實作 `NewsSectorAgent` deterministic agent：產出 AI SSD / NAND 敘事摘要。
- [x] 實作 `FundamentalAgent` deterministic agent：產出 EPS 情境、Forward P/E 計算與估值敏感度。
- [x] 實作 `RiskAgent` deterministic agent：產出 NAND 週期、庫存、現金流、資料限制等風險。
- [x] 實作 `ReportGenerator` deterministic agent：產生 source-backed research report。
- [x] 實作 `EvaluationAgent` deterministic agent：依 rubric 評分並檢查反幻覺清單。
- [x] 實作 `ResearchOrchestrator`：串起 agents，產生 run、steps、sources、report、evaluation。

驗收標準：

- 呼叫預設 run 時，後端能回傳完整 trace、source list、wiki context、report、evaluation。
- 每個 agent step 都包含 `input_summary`、`output_summary`、`source_ids`、`confidence`、`latency_ms`。
- 報告不得輸出買賣指令，且必須標示研究輔助與資料限制。

## 5. 後端 API

- [x] `GET /api/health`
- [x] `GET /api/demo/default-run`
- [x] `POST /api/research-runs`
- [x] `GET /api/research-runs/{run_id}`
- [x] `GET /api/research-runs/{run_id}/steps`
- [x] `GET /api/research-runs/{run_id}/sources`
- [x] `GET /api/research-runs/{run_id}/evaluation`
- [x] `GET /api/research-runs/{run_id}/wiki`

驗收標準：

- 所有 API 回傳穩定 JSON schema。
- 錯誤輸入會回傳清楚錯誤訊息，而不是 server error。
- API 不需要 Supabase、LLM key 或外部網路即可跑通。

## 6. 後端測試

- [x] 測試 file store 能讀取所有 fixture。
- [x] 測試 orchestrator 能產生完整 research run。
- [x] 測試 evaluation 分數低於 4.0 時會標示低信心或需要補資料。
- [x] 測試反幻覺規則：不得宣稱讀過完整券商研報、不得補齊未揭露券商名單。
- [x] 測試 API schema 與錯誤處理。

驗收標準：

- 測試可在本機重現。
- 核心 pipeline 不依賴外部服務。

## 7. Vue 前端

- [x] 建立 `ResearchRunView` 主頁。
- [x] 建立 `ResearchQuestionBar`，預設群聯與研究問題，支援手動示範股價輸入。
- [x] 建立 `AgentTimeline`，顯示 agent steps 狀態與摘要。
- [x] 建立 `AgentStepDrawer`，顯示單步來源、信心、耗時與輸入 / 輸出摘要。
- [x] 建立 `SourceList`，顯示 source type 與 reliability note。
- [x] 建立 `WikiPageViewer`，顯示 LLMWiki-lite pages 與 provenance。
- [x] 建立 `ContradictionLog`，顯示矛盾、過期 claim 與待 review 項目。
- [x] 建立 `ReportViewer`，顯示研究報告與來源連結。
- [x] 建立 `EvaluationPanel`，顯示總分、rubric scores 與修正建議。

驗收標準：

- 第一畫面就是可操作的研究工作台，不是 landing page。
- 使用者能看見 agent trace、source、wiki、report、evaluation 五件事。
- 所有文字在桌面與手機寬度下不重疊、不溢出。

## 8. 前後端整合

- [x] 前端串接 Flask API，載入 default run。
- [x] 支援啟動研究任務並刷新 trace / report / evaluation。
- [x] 支援手動展示股價傳入後端，重新計算 Forward P/E。
- [x] 在 UI 顯示資料日期與「非即時行情」提醒。
- [x] 在 UI 顯示「研究輔助，不是買賣建議」。

驗收標準：

- 不需要外部 API key 即可完整 demo。
- 更改示範股價後，估值情境能更新。
- UI 上所有重要 claim 都能追到 source 或 wiki provenance。

## 9. 展示與文件

- [x] 更新 README，說明專案目的、架構、啟動方式、資料限制。
- [x] 建立 `docs/proposal.md`，說明題目、使用者場景、quality-of-life 價值、outcome 與 scope。
- [x] 建立 `docs/architecture.md`，放入系統架構圖、服務流程圖、agent workflow 與 LLMWiki-lite 知識層。
- [x] 建立 `docs/api.md`，記錄 API endpoint、request / response、錯誤處理與資料限制。
- [x] 建立 `docs/technical-report.md`，整理系統設計、資料來源、模型 / agent 設計、evaluation、風險與未來工作。
- [x] 補上 demo script：展示時應依序介紹資料來源、LLMWiki-lite、agent trace、report、evaluation。
- [x] 建立 `slides/final-demo-outline.md` 或簡報草稿，覆蓋問題、使用者、AI workflow、demo、限制、下一步。
- [x] 補上「未來工作」：Supabase、真實 LLM、Exa / crawler、即時行情、正式券商研報、完整 knowledge graph。
- [x] 補上資料來源與免責聲明。

驗收標準：

- 旁人只讀 README 就知道怎麼跑 demo。
- 課程展示能清楚說明這不是單純 RAG，而是有可審計知識層與 agent trace。
- technical report 與 slides 覆蓋 AIASE final project 要求的架構、流程、API、Demo 與 GitHub source 說明。

## 10. 最終驗證

- [x] 執行 OpenSpec validation。
- [x] 執行後端測試。
- [x] 啟動 Flask dev server。
- [x] 啟動 Vue dev server。
- [x] 用瀏覽器檢查桌面與手機 viewport。
- [x] 驗證 default run 完整呈現 trace、sources、wiki、report、evaluation。
- [x] 檢查沒有硬編即時股價、沒有真實 LLM key、沒有 Supabase 依賴。
- [x] 依 README 從乾淨環境重跑一次本機 demo 流程。
- [x] 檢查 docs 與 slides 草稿是否覆蓋 final project 四項評分面向。

驗收標準：

- MVP 可在本機穩定展示。
- 報告分數達到或超過 4.0 / 5。
- 若分數未達 4.0 / 5，系統能說明缺口與需要補的資料。

## 11. 後續：財報狗 benchmark 與 AI 統整報告升級

- [x] 建立 `docs/statementdog-feature-benchmark.md`，拆解財報狗個股頁與股票健診功能。
- [x] 在 OpenSpec proposal 補上第二階段最小切片：Health Check Agent。
- [x] 在 OpenSpec design 補上 Health Check Agent 的資料策略、狀態語意、fixture schema、pipeline 位置、response contract、報告、前端與 evaluation 設計。
- [x] 在 OpenSpec spec 補上 Health Check Agent 的 `SHALL` requirements 與 scenarios。
- [x] 在 OpenSpec tasks 補上 Health Check Agent 的可執行任務拆解。
- [x] 執行 `openspec validate personal-finance-multi-agent-system --strict --no-interactive`，確認 OpenSpec 仍有效。

### 11.1 Health Check Agent 實作前提

- [x] 確認本切片只使用本機公開 fixture，不新增 mock pass / fail 數字。
- [x] 確認本切片不接 Supabase、Exa、crawler、真實 LLM、即時行情、財報狗登入或付費資料。
- [x] 確認 health-check 狀態 wire values 固定為 `pass`、`fail`、`unknown`、`not_available`。
- [x] 確認 `unknown` 與 `not_available` 的差異會在文件、API、report、UI 中一致呈現。

驗收標準：

- 開始 coding 前，實作者不需要再決定資料策略或狀態 enum。
- 若資料不足，預設行為是標缺口，不是猜測結論。

### 11.2 Health Check Fixture

- [x] 建立 `data/phison/health_check_fixture.json`。
- [x] fixture 必須剛好包含 7 種 health checks：
  - `landmine_risk`
  - `dividend_income`
  - `growth_stock`
  - `value_stock`
  - `chip_signal`
  - `quality_stock`
  - `turnaround_stock`
- [x] 每筆 check 必須包含 `id`、`name`、`status`、`status_reason`、`criteria`、`source_ids`、`missing_data`、`report_takeaway`、`data_policy`。
- [x] `growth_stock` 可引用營收與 Q1 EPS 相關來源作 partial evidence，但第一版仍標 `unknown`，不得標 `pass`。
- [x] `chip_signal` 第一版標 `not_available`，原因必須說明籌碼資料需要額外資料源或登入 / 付費資料。
- [x] 其他資料不足項目標 `unknown`，並列出缺少的財務或歷史資料。

驗收標準：

- fixture 可讓人一眼看出每項健診缺什麼資料。
- fixture 不包含任何虛構財務數字、虛構 pass / fail 結論或未授權資料。

### 11.3 Store 與資料驗證

- [x] 在 file store 新增 health check fixture loader。
- [x] loader 必須驗證 fixture 是 list 或有明確 top-level checks array。
- [x] loader 或 agent 必須驗證每筆 check 的 status 在合法 enum 內。
- [x] loader 或 agent 必須驗證 `source_ids` 引用的 ID 存在於 source catalog。
- [x] 當 fixture 缺少必填欄位時，測試應失敗並回傳清楚錯誤。

驗收標準：

- 壞資料不會默默進入 report。
- source ID 拼錯時會被測試抓到。

### 11.4 Health Check Agent

- [x] 新增 deterministic `HealthCheckAgent`。
- [x] Agent input：`run_id`、health check fixture、source catalog、可選的 fundamentals payload。
- [x] Agent output payload 必須包含 `summary` 與 `checks`。
- [x] `summary` 必須包含 `total`、`pass`、`fail`、`unknown`、`not_available`、`data_policy`、`major_gaps`。
- [x] Agent step 必須包含 `input_summary`、`output_summary`、`source_ids`、`confidence`、`latency_ms`、`cost_usd`。
- [x] `output_summary` 必須說明 7 項檢核、各狀態數量與主要缺口。

驗收標準：

- 預設 run 中可以看見 `health_check_agent` step。
- Health Check Agent 的輸出可以獨立被 UI、report、evaluation 使用。

### 11.5 Orchestrator / API Contract

- [x] 將 Health Check Agent 串在 Fundamental Agent 之後、Risk Agent 之前。
- [x] default run 的 steps 數量由 7 變成 8。
- [x] 完整 run response 新增 `analysis.health_checks.summary`。
- [x] 完整 run response 新增 `analysis.health_checks.checks`。
- [x] 不新增新的 API endpoint；沿用既有 `/api/demo/default-run` 與 `/api/research-runs` response。
- [x] 更新 `docs/api.md`，記錄 `analysis.health_checks` 的 response shape 與資料限制。

驗收標準：

- 前端只需讀取現有 run payload 就能顯示 Health tab。
- API 文件明確寫出 health check 不是財報狗付費資料結果。

### 11.6 Report Generator

- [x] 報告新增「股票健診摘要」段落。
- [x] 段落必須列出七種健診、狀態、保守 takeaway、主要缺口。
- [x] 報告必須註記 health check 來自本機公開 fixture，不是財報狗登入 / 付費資料。
- [x] 報告不得把 `unknown` 或 `not_available` 改寫成通過、偏多、買進理由或完整驗證。
- [x] 若 health check 資料不足，報告仍必須顯示缺口，而不是省略該段。

驗收標準：

- 使用者不需要打開財報狗多個頁面，也能看到系統知道哪些健診還不能判斷。
- 報告的 health check 段落能支援後續補資料與再評估。

### 11.7 Evaluation Agent

- [x] rubric 新增或擴充 health-check completeness / data-gap honesty 的評分面向。
- [x] 若報告缺少「股票健診摘要」，evaluation 應降分或標示 `needs_revision`。
- [x] 若七種健診沒有全部出現，evaluation 應降分。
- [x] 若報告宣稱已使用財報狗付費 / 登入資料，但 fixture 沒有該資料，evaluation 應 hard fail。
- [x] 若報告把 `unknown` 或 `not_available` 說成已通過、已失敗或完整驗證，evaluation 應 hard fail。
- [x] Evaluation notes 應說明目前主要缺口，例如現金流、股利、籌碼、P/B、F-score、歷史估值區間。

驗收標準：

- evaluation 不只評報告好不好看，也評它有沒有誠實承認資料不足。
- 反幻覺規則能涵蓋 health check 的高風險錯誤。

### 11.8 Frontend

- [x] detail panel 新增 `Health` tab。
- [x] Health tab 顯示七種健診的 status chip、reason、missing data、source IDs。
- [x] `unknown` 與 `not_available` 的樣式必須和 `pass` / `fail` 明顯不同。
- [x] summary band 可顯示 health gaps，例如 `6 unknown / 1 N/A`。
- [x] desktop 與 mobile viewport 下，長文字不得溢出、重疊或擠壓主要操作。

驗收標準：

- demo 時可以直接點 Health tab 解釋「資料不足也是系統輸出」。
- UI 不會讓使用者誤會 unknown 是通過。

### 11.9 TDD 與驗證

- [x] 先寫 RED tests，再實作 production code。
- [x] 後端測試：file store 能讀取 health check fixture。
- [x] 後端測試：fixture 剛好有 7 項，且 status enum 合法。
- [x] 後端測試：source IDs 都存在於 source catalog。
- [x] 後端測試：default run 包含 `health_check_agent`，steps 數量為 8。
- [x] 後端測試：`analysis.health_checks.checks` 有 7 項。
- [x] 後端測試：report 包含「股票健診摘要」與資料限制。
- [x] 後端測試：report 不得宣稱使用財報狗付費 / 登入資料。
- [x] 後端測試：evaluation 能抓出缺少 health check summary 的報告。
- [x] Flask API 測試：default run endpoint 回傳 `analysis.health_checks`。
- [x] 前端驗證：`npm run build` 成功。
- [x] 瀏覽器驗證：desktop / mobile Health tab 可讀、可操作、不溢出。

驗收標準：

- 實作完成前，不把 tasks 勾選為完成。
- 測試能保護 health check 的反幻覺邊界。

### 11.10 第二階段後續，但不在本切片

- [ ] 擴充 Fundamental Agent，覆蓋營收、獲利能力、安全性、成長力與現金流品質。
- [ ] 新增 Valuation Agent，覆蓋 P/E、P/B、殖利率與情境估值。
- [ ] 新增 Chip Agent，覆蓋分點、董監持股、董監質押、大股東持股與股東人數。
- [ ] 新增 Technical Agent，補足財報狗較少覆蓋的價格、量能、動能與技術面。
- [ ] 新增 Synthesis Agent，將消息面、基本面、技術面、籌碼面、估值面與風險面合成完整研究報告。
- [ ] 擴充 Evaluation Agent，檢查報告是否涵蓋 thesis、最新變化、健診摘要、反方觀點、資料缺口、追蹤指標、來源與信心。

驗收標準：

- 使用者不需要逐頁閱讀財報儀表板，就能得到一份完整、有來源、有矛盾標記、有追蹤指標的研究報告。
- 若某個健診或籌碼資料需要登入、付費或外部資料來源，系統必須標示資料缺口，不得假裝已完成檢核。
