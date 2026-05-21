# Tasks：多代理個人投資 / 理財系統 MVP

狀態：草稿 v0.1
對應設計：`openspec/changes/personal-finance-multi-agent-system/design.md`
第一版範圍：本機 fixture、mock / deterministic agents、手動股價、群聯 7 頁 Evidence Pack

> 這份任務清單是實作前的工作拆解。每個階段都應能獨立驗收，避免一開始就接 Supabase、即時行情 API、爬蟲或真實 LLM。

## 0. Implementation 前提

- [x] 第一版先不接 Supabase，只用本機 Markdown / JSON fixture。
- [x] 第一版先不用真實 LLM，採 mock / deterministic agents。
- [x] 第一版股價用手動 fixture 或使用者輸入，不接即時行情 API。
- [x] Evidence Pack 第一版只做群聯 7 個 evidence pages + provenance + contradiction log。

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

## 3. Evidence Pack 知識層

- [x] 建立 `knowledge/EVIDENCE_PACK.md`，定義 evidence page 格式、citation、claim provenance、stale claim、contradiction log 與 review gate。
- [x] 建立 `knowledge/phison/pages/Company_Phison_8299.md`。
- [x] 建立 `knowledge/phison/pages/Theme_AI_SSD.md`。
- [x] 建立 `knowledge/phison/pages/Cycle_NAND.md`。
- [x] 建立 `knowledge/phison/pages/Valuation_EPS_Assumptions.md`。
- [x] 建立 `knowledge/phison/pages/Risk_Register.md`。
- [x] 建立 `knowledge/phison/pages/Brokerage_View_Summary.md`。
- [x] 建立 `knowledge/phison/Contradiction_Log.md`。
- [x] 建立 `knowledge/phison/provenance.json`，記錄重要 claim 與 source IDs。

驗收標準：

- 7 個 evidence pages 都能被人類直接閱讀，不只是資料 dump。
- 每個重要財務數字、EPS 假設、目標價、券商觀點都能追溯到 source ID。
- `Contradiction_Log.md` 至少記錄目前已知限制，例如 CMoney 03/09 有 10 家券商但未揭露完整名單。

## 4. 後端 Deterministic Pipeline

- [x] 實作 Flask app factory 與 `/api/health`。
- [x] 實作 file store，讀取 source catalog、evidence pages、provenance、rubric、demo run。
- [x] 實作 `IntentRouter` mock：辨識群聯台股研究任務。
- [x] 實作 `SourceRetrieval` deterministic agent：回傳 curated source bundle 與 evidence context。
- [x] 實作 `NewsSectorAgent` deterministic agent：產出 AI SSD / NAND 敘事摘要。
- [x] 實作 `FundamentalAgent` deterministic agent：產出 EPS 情境、Forward P/E 計算與估值敏感度。
- [x] 實作 `RiskAgent` deterministic agent：產出 NAND 週期、庫存、現金流、資料限制等風險。
- [x] 實作 `ReportGenerator` deterministic agent：產生 source-backed research report。
- [x] 實作 `EvaluationAgent` deterministic agent：依 rubric 評分並檢查反幻覺清單。
- [x] 實作 `ResearchOrchestrator`：串起 agents，產生 run、steps、sources、report、evaluation。

驗收標準：

- 呼叫預設 run 時，後端能回傳完整 trace、source list、evidence context、report、evaluation。
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
- [x] `GET /api/research-runs/{run_id}/evidence`

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
- [x] 建立 `EvidencePageViewer`，顯示 Evidence Pack pages 與 provenance。
- [x] 建立 `ContradictionLog`，顯示矛盾、過期 claim 與待 review 項目。
- [x] 建立 `ReportViewer`，顯示研究報告與來源連結。
- [x] 建立 `EvaluationPanel`，顯示總分、rubric scores 與修正建議。

驗收標準：

- 第一畫面就是可操作的研究工作台，不是 landing page。
- 使用者能看見 agent trace、source、evidence、report、evaluation 五件事。
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
- UI 上所有重要 claim 都能追到 source 或 evidence provenance。

## 9. 展示與文件

- [x] 更新 README，說明專案目的、架構、啟動方式、資料限制。
- [x] 建立 `docs/project-proposal.md`，說明題目、使用者場景、quality-of-life 價值、outcome 與 scope。
- [x] 建立 `docs/architecture.md`，放入系統架構圖、服務流程圖、agent workflow 與 Evidence Pack 知識層。
- [x] 建立 `docs/api.md`，記錄 API endpoint、request / response、錯誤處理與資料限制。
- [x] 建立 `docs/technical-report.md`，整理系統設計、資料來源、模型 / agent 設計、evaluation、風險與未來工作。
- [x] 補上 demo script：展示時應依序介紹資料來源、Evidence Pack、agent trace、report、evaluation。
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
- [x] 驗證 default run 完整呈現 trace、sources、evidence、report、evaluation。
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

- [x] 在 OpenSpec proposal 補上 Fundamental Agent 擴充方向：從 EPS / P/E 情境擴成五大基本面品質 snapshot。
- [x] 在 OpenSpec design 補上 Fundamental Agent 擴充的資料策略、coverage status、fixture schema、五大面向、response contract、report、frontend 與 evaluation 設計。
- [x] 在 OpenSpec spec 補上 Fundamental Agent 擴充的 `SHALL` requirements 與 scenarios。
- [x] 在 OpenSpec tasks 補上 Fundamental Agent 擴充的可執行任務拆解。
- [x] 執行 `openspec validate personal-finance-multi-agent-system --strict --no-interactive`，確認 OpenSpec 仍有效。

### 12. Fundamental Agent 擴充

> 本節已完成本機 deterministic 實作；後續仍保留 12.12 的延伸代理作為下一階段。

### 12.1 Fundamental Agent 實作前提

- [x] 確認本切片只使用本機 public fixture，不接 MOPS crawler、財報狗登入 / 付費資料、Supabase、Exa、真實 LLM 或即時行情。
- [x] 確認既有 `valuation_scenarios` 必須保留，避免破壞既有 report、UI 與測試。
- [x] 確認 Fundamental Agent 的新目標是五大基本面面向，不再只輸出 EPS / Forward P/E。
- [x] 確認 coverage status 固定為 `available`、`partial`、`missing`、`not_available`。
- [x] 確認 partial / missing 不能被 report 寫成已完整驗證。

驗收標準：

- 實作者不需要再決定 Fundamental Agent 的資料策略、category set 或 status enum。
- EPS / P/E 情境與基本面品質分析在資料契約中清楚分離。

### 12.2 Fundamental Metrics Fixture

- [x] 建立 `data/phison/fundamental_metrics_fixture.json`。
- [x] fixture 必須包含 `as_of_date`、`data_policy`、`categories`。
- [x] `categories` 必須剛好包含五大面向：
  - `revenue`
  - `profitability`
  - `safety`
  - `growth`
  - `cash_flow_quality`
- [x] 每個 category 必須包含 `id`、`name`、`coverage_status`、`category_takeaway`、`metrics`、`missing_data`。
- [x] 每個 metric 必須包含 `id`、`label`、`period`、`value`、`unit`、`coverage_status`、`source_ids`、`interpretation`、`missing_data`。
- [x] 若 `value` 為 `null`，則 `coverage_status` 不得為 `available`，且 `missing_data` 不得為空。
- [x] `source_ids` 必須引用已存在 source catalog ID。
- [x] `unit` 必須使用穩定值，例如 `TWD_BN`、`TWD`、`percent`、`days`、`ratio`、`text`、`not_applicable`。

驗收標準：

- fixture 能清楚區分已取得數字、部分線索與缺資料。
- fixture 不包含虛構 margin、cash flow、balance sheet 或同業排名。

### 12.3 第一版資料覆蓋策略

- [x] `revenue` 第一版標 `partial`，可引用 S1 / S2 呈現 2026-04 月營收與新聞線索。
- [x] `revenue` 必須列出缺口：近 12 個月營收序列、累計營收 YoY、產品別營收。
- [x] `profitability` 第一版標 `partial`，可引用 S3 呈現 Q1 EPS。
- [x] `profitability` 必須列出缺口：毛利率、營業利益率、淨利率、ROE / ROA。
- [x] `safety` 第一版標 `missing`，列出負債比、流動比、速動比、利息保障倍數與金融借款缺口。
- [x] `growth` 第一版標 `partial`，可引用 S1 / S2 / S3 作營收與 EPS 成長線索。
- [x] `growth` 必須列出缺口：完整月營收 YoY 序列、毛利 / 營業利益 / 淨利成長率。
- [x] `cash_flow_quality` 第一版標 `missing`，列出 OCF、FCF、OCF / net income、存貨與應收帳款週轉缺口。

驗收標準：

- 財務面向不會因為有 EPS 或營收新聞就被誤判為完整。
- 報告可以誠實回答「我們知道什麼、還不知道什麼」。

### 12.4 Store 與資料驗證

- [x] 在 file store 新增 fundamental metrics fixture loader。
- [x] loader 必須驗證 top-level schema 與五大 category 數量。
- [x] loader 或 agent 必須驗證 category / metric coverage status 合法。
- [x] loader 或 agent 必須驗證 `source_ids` 存在於 source catalog。
- [x] loader 或 agent 必須驗證 `value = null` 時不得標 `available`。
- [x] 當 category 缺少 required metrics 或 required fields 時，測試應失敗並回傳清楚錯誤。

驗收標準：

- 壞的 financial fixture 不會進入 report。
- source 或 status 拼錯會被測試抓到。

### 12.5 Fundamental Agent Output

- [x] 擴充 deterministic `FundamentalAgent`，保留既有 EPS / Forward P/E `valuation_scenarios`。
- [x] Agent input：`run_id`、price、price_date、fundamental metrics fixture、source catalog。
- [x] Agent output 必須包含 `valuation_scenarios`、`summary`、`categories`、`key_findings`、`data_gaps`。
- [x] `summary` 必須包含 `categories_total`、`available`、`partial`、`missing`、`not_available`、`data_policy`、`major_gaps`。
- [x] `key_findings` 必須用保守語氣說明營收 / EPS 線索與資料缺口。
- [x] `data_gaps` 必須彙整五大面向中最重要的缺口。
- [x] Agent step 的 `output_summary` 必須同時提到 EPS/P/E 情境與五大基本面 coverage。

驗收標準：

- `analysis.fundamentals.valuation_scenarios` 與既有前端 / report 相容。
- 新增 fundamentals categories 後，Health Check Agent 可以消費這些資料缺口。

### 12.6 Orchestrator / API Contract

- [x] Orchestrator 讀取 fundamental metrics fixture 並傳入 Fundamental Agent。
- [x] 完整 run response 的 `analysis.fundamentals` 新增 `summary`。
- [x] 完整 run response 的 `analysis.fundamentals` 新增 `categories`。
- [x] 完整 run response 的 `analysis.fundamentals` 新增 `key_findings`。
- [x] 完整 run response 的 `analysis.fundamentals` 新增 `data_gaps`。
- [x] 不新增新的 API endpoint；沿用既有 run response。
- [x] 更新 `docs/api.md`，記錄 fundamentals expanded payload 與資料限制。

驗收標準：

- 前端可以只靠現有 run payload 顯示 Fundamental tab。
- API 文件明確寫出這不是完整財報資料庫，而是 public fixture financial snapshot。

### 12.7 Report Generator

- [x] 報告新增或擴充「基本面拆解」段落。
- [x] 段落必須列出五大面向、coverage status、takeaway、主要 metrics、主要缺口。
- [x] 報告必須把 EPS / Forward P/E 情境標示為估值敏感度，不等同完整基本面品質。
- [x] 報告不得因 Q1 EPS 強就宣稱獲利能力全面改善。
- [x] 報告不得因營收強就宣稱現金流品質改善。
- [x] 報告不得因 Forward P/E 看起來較低就宣稱公司便宜。
- [x] `safety` 與 `cash_flow_quality` 若為 `missing`，必須在報告中保留缺口。

驗收標準：

- 使用者能看到「營收 / EPS 已有線索，但安全性與現金流仍缺資料」。
- 報告不再把估值情境誤包裝成完整基本面研究。

### 12.8 Health Check Agent Integration

- [x] Health Check Agent 可讀取擴充後的 fundamentals payload。
- [x] `growth_stock` 可引用 `fundamentals.categories.growth` 的 partial evidence。
- [x] `landmine_risk` 可引用 `cash_flow_quality` 的 missing gaps。
- [x] `value_stock` 不得把 Forward P/E 情境當成完整便宜股判定。
- [x] Health Check Agent 不重新計算 fundamental metrics，只消費 Fundamental Agent output 與 health check fixture。

驗收標準：

- Health Check 與 Fundamental Agent 的責任不重疊。
- 股票健診的缺口和基本面資料缺口一致，不互相矛盾。

### 12.9 Evaluation Agent

- [x] rubric 新增或擴充 fundamental coverage / overclaim guardrail。
- [x] 若 report 缺少五大面向基本面拆解，evaluation 應降分或標 `needs_revision`。
- [x] 若 report 把 partial / missing metric 寫成已完整驗證，evaluation 應 hard fail。
- [x] 若 report 將 Q1 EPS 無警語年化成全年正式預估，evaluation 應 hard fail 或重大扣分。
- [x] 若 report 清楚列出營收、獲利、安全性、成長力、現金流品質與缺口，evaluation 應提高 valuation rigor / risk coverage / user usefulness 的評分理由。

驗收標準：

- evaluation 能抓出「用 EPS 代替完整基本面」的錯誤。
- evaluation 能獎勵誠實列缺口的報告。

### 12.10 Frontend

- [x] detail panel 新增 `Fundamentals` tab，或在既有 detail panel 中新增 fundamentals view。
- [x] Fundamentals view 顯示五大 categories、coverage status、category takeaway、主要 metrics、source IDs、missing data。
- [x] `available`、`partial`、`missing`、`not_available` 的樣式必須可區分。
- [x] Valuation scenarios 與 fundamentals categories 可放在同一 tab，但必須分區，不得混成同一張表。
- [x] desktop 與 mobile viewport 下，長 metric 名稱、missing data 與 source IDs 不得溢出。

驗收標準：

- demo 時可以清楚解釋「基本面目前覆蓋了哪些資料、還缺哪些資料」。
- UI 不會讓使用者誤會 partial / missing 是已完成分析。

### 12.11 TDD 與驗證

- [x] 先寫 RED tests，再實作 production code。
- [x] 後端測試：file store 能讀取 fundamental metrics fixture。
- [x] 後端測試：fixture 剛好有五大 categories，且 coverage status 合法。
- [x] 後端測試：source IDs 都存在於 source catalog。
- [x] 後端測試：`value = null` 時不得標 `available`。
- [x] 後端測試：default run 保留 `valuation_scenarios`。
- [x] 後端測試：default run 包含 `analysis.fundamentals.summary`、`categories`、`key_findings`、`data_gaps`。
- [x] 後端測試：report 包含「基本面拆解」與五大面向。
- [x] 後端測試：report 不得把 Q1 EPS 年化成正式全年預估。
- [x] 後端測試：evaluation 能抓出缺少 fundamental breakdown 的報告。
- [x] Flask API 測試：default run endpoint 回傳 expanded `analysis.fundamentals`。
- [x] 前端驗證：`npm run build` 成功。
- [x] 瀏覽器驗證：desktop / mobile Fundamentals tab 可讀、可操作、不溢出。

驗收標準：

- 實作完成前，不把 Fundamental Agent 實作項目勾選為完成。
- 測試能保護 fundamental overclaim 與資料缺口誠實度。

### 12.12 第二階段後續，但不在本切片

- [x] 將 Valuation Agent 提升為下一個 OpenSpec docs-first 切片，覆蓋 P/E、P/B、殖利率與情境估值。
- [ ] 新增 Chip Agent，覆蓋分點、董監持股、董監質押、大股東持股與股東人數。
- [ ] 新增 Technical Agent，補足財報狗較少覆蓋的價格、量能、動能與技術面。
- [ ] 新增 Synthesis Agent，將消息面、基本面、技術面、籌碼面、估值面與風險面合成完整研究報告。
- [ ] 擴充 Evaluation Agent，檢查報告是否涵蓋 thesis、最新變化、健診摘要、反方觀點、資料缺口、追蹤指標、來源與信心。

驗收標準：

- 使用者不需要逐頁閱讀財報儀表板，就能得到一份完整、有來源、有矛盾標記、有追蹤指標的研究報告。
- 若某個健診或籌碼資料需要登入、付費或外部資料來源，系統必須標示資料缺口，不得假裝已完成檢核。

## 13. Valuation Agent 規劃

> 本節是下一個 docs-first 實作切片；目前只定義 OpenSpec，不代表已實作。

### 13.1 Valuation Agent 實作前提

- [x] 確認 Valuation Agent 的目標是估值分析，不再把 EPS / Forward P/E 藏在 Fundamental Agent 裡當作完整估值。
- [x] 確認本切片第一版仍只使用本機 public fixture，不接即時行情、不接完整券商研報、不接付費資料。
- [x] 確認既有 `analysis.fundamentals.valuation_scenarios` 需要保留相容性，直到 UI / report 遷移完成。
- [x] 確認新的主要 output 應是 `analysis.valuation`。
- [x] 確認目標價、Forward P/E、upside / downside 都只能作情境分析，不得輸出買賣建議。

驗收標準：

- 實作者能清楚知道 Valuation Agent 和 Fundamental Agent 的責任差異。
- 下個 implementation slice 不需要重新決定資料契約或 guardrails。

### 13.2 Valuation Fixture

- [ ] 建立 `data/phison/valuation_fixture.json`。
- [ ] fixture 必須包含 `as_of_date`、`data_policy`、`price`、`multiples`、`broker_targets`、`missing_data`。
- [ ] `price` 必須包含 `value`、`unit`、`as_of_date`、`is_live_market_data`、`source_ids`。
- [ ] 第一版 `price.is_live_market_data` 必須是 `false`。
- [ ] `multiples` 必須至少覆蓋 Forward P/E 情境，並預留 P/B、殖利率、歷史 P/E percentile。
- [ ] `broker_targets` 必須保留 target price、source label、date、source IDs 與 reliability note。
- [ ] `source_ids` 必須引用已存在 source catalog ID。

驗收標準：

- fixture 能清楚區分可計算的 Forward P/E、公開券商摘要與缺資料項目。
- fixture 不包含虛構券商模型、未揭露券商名單或即時股價。

### 13.3 第一版資料覆蓋策略

- [ ] Forward P/E scenarios 第一版標 `partial`，使用既有 EPS assumptions 與示範股價。
- [ ] Broker target range 第一版標 `partial`，可引用 CMoney / 新聞公開摘要，但不得宣稱完整研報。
- [ ] Historical P/E percentile 第一版標 `missing`。
- [ ] P/B 第一版標 `missing`。
- [ ] Dividend yield 第一版標 `missing`。
- [ ] Peer valuation 第一版標 `missing`。
- [ ] Upside / downside framing 第一版只能用 fixture price 和 target / scenario 做敏感度，不得作交易指令。

驗收標準：

- 估值輸出能回答「目前估值是否被支撐」而不是只列一串目標價。
- 使用者能看到需要補哪些資料才能更有信心判斷估值。

### 13.4 Store 與資料驗證

- [ ] 在 file store 新增 valuation fixture loader。
- [ ] loader 必須驗證 top-level schema、price schema、multiples schema、broker targets schema。
- [ ] loader 或 agent 必須驗證 valuation coverage status 合法：`available`、`partial`、`missing`、`not_available`。
- [ ] loader 或 agent 必須驗證 `source_ids` 存在於 source catalog。
- [ ] loader 或 agent 必須驗證 `is_live_market_data = false` 時 report / UI 不能使用即時行情語言。

驗收標準：

- 壞的 valuation fixture 不會進入 report。
- target price、source id、coverage status 或 price date 拼錯會被測試抓到。

### 13.5 Valuation Agent Output

- [ ] 新增 deterministic `ValuationAgent`。
- [ ] Agent input：`run_id`、price fixture、valuation fixture、EPS assumptions / fundamentals payload、source catalog。
- [ ] Agent output 必須包含 `summary`、`scenarios`、`multiples`、`broker_targets`、`data_gaps`、`interpretation`。
- [ ] `summary` 必須包含 `data_policy`、`price_as_of_date`、`is_live_market_data`、coverage counts、`major_gaps`。
- [ ] `scenarios` 必須清楚分 conservative / base / optimistic assumptions。
- [ ] `interpretation` 必須用保守語氣說明 AI SSD story 要支撐目前估值，需要哪些 EPS / margin / NAND cycle 條件。
- [ ] Agent step 的 `output_summary` 必須同時提到 Forward P/E、broker target range、coverage 與主要缺口。

驗收標準：

- `analysis.valuation` 能獨立被 UI、report、health check、evaluation 使用。
- 既有 `analysis.fundamentals.valuation_scenarios` 不被移除。

### 13.6 Orchestrator / API Contract

- [ ] Orchestrator 讀取 valuation fixture 並傳入 Valuation Agent。
- [ ] Valuation Agent 建議放在 Fundamental Agent 之後、Health Check Agent 之前。
- [ ] 完整 run response 新增 `analysis.valuation`。
- [ ] 不新增新的 API endpoint；沿用既有 run response。
- [ ] 更新 `docs/api.md`，記錄 valuation payload 與資料限制。

驗收標準：

- 前端可以只靠現有 run payload 顯示 Valuation tab。
- API 文件明確寫出 valuation 第一版不是即時行情，也不是完整券商模型。

### 13.7 Health Check Agent Integration

- [ ] `value_stock` 可讀取 `analysis.valuation`。
- [ ] `value_stock` 不得因 Forward P/E 或 target upside 看起來好，就標為 `pass`。
- [ ] 若 P/B、殖利率、歷史 P/E percentile 缺資料，`value_stock` 仍應維持 `unknown`。
- [ ] Health Check Agent 不重新計算 valuation，只消費 Valuation Agent output 與 health check fixture。

驗收標準：

- 便宜股健診和 Valuation Agent 責任不重疊。
- 健診結果不會把情境估值誤寫成已通過。

### 13.8 Report Generator

- [ ] 報告新增或擴充「估值拆解」段落。
- [ ] 段落必須列出示範股價日期、Forward P/E scenarios、broker target range、missing valuation data。
- [ ] 報告必須標示 EPS / target price / upside 是情境敏感度，不等同合理價或買賣建議。
- [ ] 報告不得把單一目標價寫成合理價。
- [ ] 報告不得把 Forward P/E 寫成股票便宜的完整證明。
- [ ] 報告不得把 CMoney / 新聞摘要寫成完整券商研報。

驗收標準：

- 使用者能看到「如果採不同 EPS 假設，估值支撐程度會如何改變」。
- 報告能清楚列出 P/B、殖利率、歷史估值與同業估值缺口。

### 13.9 Evaluation Agent

- [ ] rubric 新增或擴充 valuation overclaim guardrail。
- [ ] 若 report 缺少「估值拆解」，evaluation 應降分或標 `needs_revision`。
- [ ] 若 report 把單一目標價當合理價或買進建議，evaluation 應 hard fail。
- [ ] 若 report 使用 fixture price 但沒有日期或非即時行情提醒，evaluation 應 hard fail 或重大扣分。
- [ ] 若 report 把 Forward P/E 情境寫成股票便宜的完整證明，evaluation 應 hard fail。
- [ ] 若 report 清楚列出 target range、EPS sensitivity、price date 與缺口，evaluation 應提高 valuation rigor / user usefulness。

驗收標準：

- evaluation 能抓出「用目標價或 Forward P/E 代替完整估值」的錯誤。
- evaluation 能獎勵誠實列出估值缺口的報告。

### 13.10 Frontend

- [ ] detail panel 新增 `Valuation` tab，或在既有 detail panel 中新增 valuation view。
- [ ] Valuation view 顯示 price fixture date、scenario table、broker target table、coverage status、source IDs、data gaps。
- [ ] `available`、`partial`、`missing`、`not_available` 的樣式必須可區分。
- [ ] Valuation view 應和 Fundamentals view 分區，避免混淆估值與基本面品質。
- [ ] desktop 與 mobile viewport 下，target price、source IDs、missing data 不得溢出。

驗收標準：

- demo 時可以清楚解釋「估值目前能算什麼、不能算什麼」。
- UI 不會讓使用者誤會 target upside 是買進訊號。

### 13.11 TDD 與驗證

- [ ] 先寫 RED tests，再實作 production code。
- [ ] 後端測試：file store 能讀取 valuation fixture。
- [ ] 後端測試：fixture schema、source IDs、coverage status、price date 合法。
- [ ] 後端測試：default run 包含 `analysis.valuation.summary`、`scenarios`、`multiples`、`broker_targets`、`data_gaps`、`interpretation`。
- [ ] 後端測試：default run 保留 `analysis.fundamentals.valuation_scenarios`。
- [ ] 後端測試：report 包含「估值拆解」。
- [ ] 後端測試：evaluation 能抓出 target price / Forward P/E overclaim。
- [ ] Flask API 測試：default run endpoint 回傳 `analysis.valuation`。
- [ ] 前端驗證：`npm run build` 成功。
- [ ] 瀏覽器驗證：desktop / mobile Valuation tab 可讀、可操作、不溢出。

驗收標準：

- 實作完成前，不把 Valuation Agent 實作項目勾選為完成。
- 測試能保護 valuation overclaim 與 price fixture 誠實度。
