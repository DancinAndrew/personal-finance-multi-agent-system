## ADDED Requirements

### Requirement: 系統將 MVP 研究範圍限定在台股
系統 MUST 把台股視為 MVP 的投資研究 universe。

#### Scenario: 使用者詢問台股
- **WHEN** 使用者用股票代號或公司名稱詢問上市 / 上櫃台灣公司
- **THEN** 系統必須將該 request 視為 in scope，並啟動台股研究 workflow。

#### Scenario: 使用者詢問非台股資產
- **WHEN** 使用者詢問美股、crypto、海外 ETF、基金、債券或保險商品
- **THEN** MVP 必須說明第一版範圍限定在台股，並拒絕、要求切換成台股標的，或標記為 future scope。

#### Scenario: 使用者詢問完整資產配置
- **WHEN** 使用者詢問跨資產類別的完整 portfolio allocation
- **THEN** MVP 必須將任務縮小到單一個股研究，或把 portfolio analysis 記錄為 future capability。

### Requirement: 系統使用群聯作為第一個 MVP seed target
系統 MUST 使用群聯電子（8299）作為第一個 end-to-end 台股研究標的。

#### Scenario: 系統需要第一個 MVP 公司
- **WHEN** 系統需要 prototype data collection、report generation 或 evaluation 的 default company
- **THEN** 系統必須選擇群聯電子（8299）作為 default target。

#### Scenario: 既有 Obsidian 研究筆記可用
- **WHEN** 系統建立第一版群聯 research corpus
- **THEN** 系統必須納入使用者既有 Obsidian note 作為 initial reference document，並記錄 note path。

#### Scenario: 生成報告被評估
- **WHEN** 系統評估生成的群聯報告
- **THEN** 系統必須用使用者既有群聯研究筆記的結構與期待作為比較基準，但不得把該筆記視為自動最新或必然正確。

### Requirement: 系統提供可展示的網頁應用
系統 MUST 透過適合 demo 的 web application 暴露 MVP。

#### Scenario: 使用者開啟網頁應用
- **WHEN** 使用者開啟 local 或 deployed web application
- **THEN** 系統必須提供可輸入研究問題、查看 agent workflow、查看 sources、閱讀 generated report 的介面。

#### Scenario: 使用者執行預設群聯研究任務
- **WHEN** 使用者選擇 default Phison research task
- **THEN** 系統必須展示「AI SSD 成長故事是否足以支撐群聯目前估值」這個問題的 end-to-end workflow。

#### Scenario: 研究結果被顯示
- **WHEN** web application 顯示研究結果
- **THEN** 介面必須明確標示 output 是 research support，而不是 buy/sell advice。

#### Scenario: 課程評審在本機啟動專案
- **WHEN** 課程評審依 README 在 local environment 啟動專案
- **THEN** default demo 必須不需要 Supabase、真實 LLM key、即時行情 API 或外部 crawler 也能跑。

### Requirement: 系統顯示可觀察的 agent execution traces
系統 MUST 透過 agent execution traces 讓研究過程可被觀察。

#### Scenario: 使用者啟動 default Phison research task
- **WHEN** 使用者啟動 default Phison research task
- **THEN** web application 必須顯示 execution timeline，包含 intent routing、retrieval、fundamental analysis、risk / opposing view analysis、report generation 與 evaluation。

#### Scenario: 使用者檢查單一 agent step
- **WHEN** 使用者開啟某個 agent step
- **THEN** 系統必須顯示該 step 的 input summary、output summary、used sources、confidence 或 evaluation metadata，以及可用的 latency / cost metadata。

#### Scenario: 完整 intermediate output 存在
- **WHEN** 系統記錄第一版 agent traces
- **THEN** 系統預設只儲存 summaries 與 sources，不持久化完整 intermediate outputs，除非未來先設計 privacy、storage 與 debugging policy。

#### Scenario: 使用者追溯報告 claim
- **WHEN** 使用者檢查研究報告中的重要 claim
- **THEN** 系統必須能將該 claim 連回 responsible agent step 與 source materials。

### Requirement: 系統第一版主要使用新聞與財報 / 財務資料
系統第一版群聯研究資料集 MUST 優先使用新聞與財報 / 財務資訊。

#### Scenario: 建立第一版資料集
- **WHEN** 系統建立第一版群聯資料集
- **THEN** 系統必須包含使用者既有 Obsidian 群聯 note、5 到 10 篇相關新聞，以及 1 到 2 份官方 financial documents。

#### Scenario: 資料來源超出第一版範圍
- **WHEN** earnings-call transcripts、annual report deep dives 或其他來源尚未準備
- **THEN** 系統必須標記為 future data sources，不得假裝已完整納入。

### Requirement: 系統從手動 curated source data 開始
第一版系統 MUST 使用手動 curated Phison dataset。

#### Scenario: 手動整理新聞與財務資料
- **WHEN** 第一版 Phison dataset 被建立
- **THEN** 每個 item 必須記錄 title、source、date、URL 或 local path，以及和研究問題的 relevance。

#### Scenario: 之後加入自動蒐集
- **WHEN** 後續版本加入 crawlers 或 Exa API
- **THEN** automated sources 必須保留和 manually curated data 相同的 source metadata 與 quality checks。

### Requirement: 系統提供 Evidence Pack 研究知識層
系統 MUST 將 raw sources 整理成 human-readable、linkable、auditable 的 research evidence pack layer，放在 retrieval 與 agent analysis 中間。

#### Scenario: Raw source 被讀取
- **WHEN** 系統讀取新聞、財報、CMoney summaries、FactSet consensus estimates、公司官方資料或使用者 notes
- **THEN** 系統必須保留 raw source record，不得覆寫原文，也不得把摘要當成 primary source data。

#### Scenario: Research evidence page 被產生
- **WHEN** 系統從 sources 抽取 company、industry、product、valuation、risk 或 brokerage-view knowledge
- **THEN** 系統必須把 knowledge 寫入 human-readable evidence page，並為每個重要 claim 記錄 source、date 與 reliability limitation。

#### Scenario: 新資料和既有 evidence claim 衝突
- **WHEN** 新 source 和既有 evidence claim 在 EPS、target price、risk、industry narrative 或 data recency 上衝突
- **THEN** 系統必須把 conflict 記錄到 contradiction log，而不是默默覆蓋舊 claim。

#### Scenario: Source 更新或變 stale
- **WHEN** source document 改變、content hash 改變，或 key data 超過可接受 freshness window
- **THEN** 系統必須將 derived claims 標為 stale，並在 report 與 evaluation 中降低 confidence 或要求 update。

#### Scenario: High-risk evidence update 被提出
- **WHEN** evidence update 會改變 valuation conclusions、risk level、investment thesis 或 golden-sample evaluation criteria
- **THEN** MVP 必須要求 human review，才能把該 update 當成 accepted knowledge。

### Requirement: 系統使用外部券商報告或公開來源 proxy 作為 golden sample
系統第一版 SHOULD 優先使用外部券商研究報告作為 golden sample；若沒有正式券商報告，則 MUST 使用清楚標示的 public-source proxy golden sample。

#### Scenario: 外部券商報告可用
- **WHEN** 外部券商報告可作為 reference
- **THEN** 系統必須用它評估 generated output 是否具備 individual-stock research depth、valuation assumptions、risk disclosure 與 investment thesis structure。

#### Scenario: 外部券商報告不可用
- **WHEN** 沒有可用的外部券商報告
- **THEN** 系統必須使用 public-source proxy golden sample 作為暫時 evaluation 基準，並標示它是 proxy 而非正式 brokerage report。

#### Scenario: 使用 public-source proxy golden sample
- **WHEN** 系統從 CMoney summaries、news articles、FactSet consensus estimates 或 official company financial data 建立 golden sample
- **THEN** 每個重要數字都必須記錄 source、date、source type 與 reliability limitation。
- **AND** 系統不得捏造未揭露的券商名稱、valuation models 或 report details。

### Requirement: 系統回答第一個群聯估值研究問題
系統 MUST 針對「AI SSD 成長故事是否足以支撐群聯目前估值」產出研究結果。

#### Scenario: 使用者啟動 default research question
- **WHEN** 使用者啟動 default Phison research task
- **THEN** 系統必須分析 AI SSD growth narrative、financial data、valuation assumptions、risks 與 opposing views。

#### Scenario: 成長故事和估值證據衝突
- **WHEN** fundamental agent 和 risk agent 對 valuation support 有不同判斷
- **THEN** 系統必須揭露 disagreement，並指出哪些 assumptions 最影響結論。

### Requirement: 系統釐清投資研究意圖
系統 MUST 在啟動 retrieval 或 specialist agents 前，先 classify 每個 user request。

#### Scenario: 使用者詢問簡單概念
- **WHEN** 使用者詢問一般投資概念，例如「什麼是 DCA？」
- **THEN** 系統必須直接給出簡潔解釋，不啟動完整 multi-agent pipeline。

#### Scenario: 使用者要求跨來源投資分析
- **WHEN** 使用者要求 company、ETF、fund、sector 或 portfolio analysis
- **THEN** 系統必須將 request route 到相關 specialist agents，並記錄 selected route。

#### Scenario: 使用者要求不安全或過度具體的建議
- **WHEN** 使用者要求保證報酬、精確買賣指令或 legally sensitive advice
- **THEN** 系統必須拒絕或重新框定為 research support，並附上 risk disclosure。

### Requirement: 系統將不同投資學派拆成 specialist agents
系統 MUST 將不同 investment perspectives 建模成 separate agents，讓它們的 assumptions 可以互相比較。

#### Scenario: 需要基本面分析
- **WHEN** query 需要 company quality、earnings、valuation、PE ratio 或 business model analysis
- **THEN** Fundamental Agent 必須產出有來源支持的觀點，並列出 assumptions 與 uncertainties。

#### Scenario: 需要技術分析
- **WHEN** query 需要 price trend、volume、momentum 或 technical indicators
- **THEN** Technical Agent 必須基於 quantitative market signals 產出 view，且不得假裝在評估 business quality。

#### Scenario: 需要 macro 或 sector context
- **WHEN** query 取決於 interest rates、inflation、industry cycle、supply chain 或 policy context
- **THEN** Macro / Sector Agent 必須產出 contextual view，並標示哪些 claims 有資料支持、哪些是 inferred。

#### Scenario: Agents 觀點衝突
- **WHEN** agents disagree
- **THEN** 系統必須揭露 disagreement，而不是強迫輸出單一 confident answer。

### Requirement: 系統將 dashboard-style indicators 合成 AI 研究報告
系統 MUST 把 dashboard-style financial metrics 視為 inputs 與 benchmarks，而不是最終 user experience。

#### Scenario: 使用者要求完整單一個股分析
- **WHEN** 使用者要求分析一檔台股
- **THEN** 系統必須整合 news、fundamentals、growth、profitability、safety、valuation、technical、chip 與 risk perspectives。
- **AND** output 必須是 research report，而不是一堆需要使用者自行解讀的 scattered metrics。

#### Scenario: Dashboard indicators 衝突
- **WHEN** 不同 perspectives 衝突，例如營收成長但估值昂貴、籌碼改善但 earnings 未確認，或低估值但現金流惡化
- **THEN** 系統必須明確列出 conflict、possible explanations、missing sources，以及最影響結論的 assumptions。

#### Scenario: Stock health-check data 不可用
- **WHEN** 某個 health-check item 需要 unavailable、paywalled、login-gated 或未經 public sources 驗證的 data
- **THEN** 系統必須將該 item 標為 `unknown`、`not available` 或 `needs source`，不得假裝已完成檢核。

#### Scenario: Report completeness 被評估
- **WHEN** report generator 完成 single-stock research report
- **THEN** evaluation agent 必須檢查報告是否涵蓋 thesis、latest changes、stock health-check summary、fundamentals、growth quality、valuation、technical and chip signals、opposing views、data gaps、tracking indicators、sources 與 confidence。

### Requirement: 系統產生保守股票健診摘要
系統 MUST 在 current deterministic MVP 可用來源範圍內，把七種 StatementDog-style 股票健診 perspectives 轉成 auditable health-check outputs。

#### Scenario: Health-check output 被產生
- **WHEN** default Phison research run 被產生
- **THEN** run 必須包含 `health_check_agent` trace step。
- **AND** `analysis.health_checks.checks` 必須剛好包含七種 checks：landmine risk、dividend income、growth stock、value stock、chip signal、quality stock、turnaround stock。
- **AND** 每個 check 必須包含 stable ID、display name、status、status reason、criteria、source IDs、missing data、report takeaway 與 data policy。

#### Scenario: Health-check status 被序列化
- **WHEN** health-check item 透過 API 回傳或在 report 中使用
- **THEN** status 必須是 `pass`、`fail`、`unknown` 或 `not_available` 其中之一。
- **AND** 系統只能在資料可能補齊但目前不足時使用 `unknown`。
- **AND** 系統只能在資料需要登入、付費、外部資料源或超出 MVP capability 時使用 `not_available`。

#### Scenario: Current public fixtures 不足以判斷 check
- **WHEN** available public fixture 不包含足夠資料判斷 health check pass / fail
- **THEN** 系統必須將 check 標為 `unknown`。
- **AND** 系統必須列出做出判斷所需的 missing data。
- **AND** 系統不得從 incomplete data 推論 bullish、bearish、pass 或 fail conclusion。

#### Scenario: Chip data 需要 unavailable sources
- **WHEN** chip-related checks 需要 broker trading、major shareholder、director holding、pledged share 或 shareholder-count data，而 local fixture 沒有
- **THEN** 系統必須將 chip signal check 標為 `not_available`。
- **AND** 系統必須說明 current MVP 沒有 required source 或 permission。

#### Scenario: 有 partial growth evidence
- **WHEN** fixture 包含和 growth 有關的 revenue 或 EPS evidence，但缺完整 StatementDog-style growth-check criteria
- **THEN** 系統可以把 relevant source IDs attach 到 growth stock check。
- **AND** 除非所有 required criteria 都可被評估，否則系統仍必須將 check 標為 `unknown`。

#### Scenario: Health-check summary 被加入報告
- **WHEN** report generator 建立 research report
- **THEN** report 必須包含 stock health-check summary，列出所有七種 check names、statuses、conservative takeaways 與 key missing data。
- **AND** report 必須明確說明 health-check section 基於 local public fixtures，而不是 StatementDog login-gated 或 paid data。

#### Scenario: Health-check output 被顯示在 web app
- **WHEN** web application 顯示 completed run
- **THEN** 它必須提供 Health view，顯示每個 health-check status、reason、missing data 與 source IDs。
- **AND** `unknown` 與 `not_available` 必須在視覺上和 `pass` / `fail` 可區分。

#### Scenario: Health-check claims 被評估
- **WHEN** evaluation agent review 含 health-check content 的 report
- **THEN** 它必須檢查七種 checks 是否全部出現，以及 missing data 是否被明確呈現。
- **AND** 當 health-check summary 缺失或不完整時，系統必須降分或標示 report needs revision。

#### Scenario: Health-check hallucination 被偵測
- **WHEN** report 宣稱 `unknown` 或 `not_available` checks 已通過、已失敗或已完整驗證
- **THEN** evaluation agent 必須將其視為 hard failure。
- **AND** 若 report 宣稱使用 fixture 沒有的 StatementDog paid、login-gated 或 unavailable data，evaluation agent 也必須將其視為 hard failure。

### Requirement: 系統將 fundamental analysis 擴充成 financial quality snapshot
系統 MUST 將 Fundamental Agent 從 EPS 與 Forward P/E 情境，擴充成覆蓋營收、獲利能力、安全性、成長力與現金流品質的 structured financial quality snapshot。

#### Scenario: Fundamental snapshot 被產生
- **WHEN** default Phison research run 被產生
- **THEN** `analysis.fundamentals` 必須保留既有 `valuation_scenarios`。
- **AND** `analysis.fundamentals` 也必須包含 `summary`、`categories`、`key_findings` 與 `data_gaps`。
- **AND** `analysis.fundamentals.categories` 必須剛好包含五個 categories：revenue、profitability、safety、growth、cash-flow quality。

#### Scenario: Fundamental metric coverage 被序列化
- **WHEN** fundamental category 或 metric 透過 API 回傳或在 report 中使用
- **THEN** 它的 coverage status 必須是 `available`、`partial`、`missing` 或 `not_available` 其中之一。
- **AND** 系統只有在 fixture 有足夠資料與 source IDs 支持該 metric 時，才能使用 `available`。
- **AND** 當只有 directional evidence、但不足以做 full trend 或 quality judgment 時，系統必須使用 `partial`。
- **AND** 當資料理論上可由 public financial sources 取得、但目前 fixture 尚未納入時，系統必須使用 `missing`。
- **AND** 當資料需要 unavailable external permissions、paid data 或超出 current MVP boundary 的 capability 時，系統才可使用 `not_available`。

#### Scenario: Revenue evidence 存在
- **WHEN** fixture 包含 official 或 news-based monthly revenue evidence
- **THEN** revenue category 可依 required sequence 是否完整，標為 `partial` 或 `available`。
- **AND** 系統必須記錄 source IDs、period、unit、interpretation 與 missing trend data。

#### Scenario: Profitability evidence 不完整
- **WHEN** fixture 包含 EPS evidence，但缺 gross margin、operating margin、net margin、ROE 或 ROA
- **THEN** profitability category 必須標為 `partial`。
- **AND** 系統不得只靠 EPS 宣稱 broad profitability improvement。

#### Scenario: Safety 與 cash-flow data 缺失
- **WHEN** fixture 缺 balance-sheet ratios、debt metrics、operating cash flow、free cash flow、OCF-to-net-income、inventory turnover 或 receivable turnover
- **THEN** safety 與 cash-flow quality categories 必須標為 `missing`。
- **AND** 系統必須列出 future evaluation 需要補的 missing data。

#### Scenario: Growth evidence 是 partial
- **WHEN** fixture 包含 revenue 或 EPS growth clues，但缺 full monthly revenue YoY sequence 與 profit-growth metrics
- **THEN** growth category 必須標為 `partial`。
- **AND** 系統必須說明哪些 growth claims 有 source-backed，哪些仍未驗證。

#### Scenario: Fundamental report section 被產生
- **WHEN** report generator 建立 research report
- **THEN** report 必須包含 fundamental breakdown，覆蓋五個 categories、coverage statuses、source-backed takeaways 與 data gaps。
- **AND** report 必須將 EPS / Forward P/E valuation sensitivity 和 broader business quality 分開。

#### Scenario: Fundamental overclaim 被偵測
- **WHEN** report 宣稱 missing 或 partial metrics 已完整驗證
- **THEN** evaluation agent 必須將其視為 hard failure 或標記 report needs revision。
- **AND** evaluation agent 也必須懲罰沒有警語就把 Q1 EPS 年化成 full-year forecast 的 report。

### Requirement: 系統將 valuation analysis 從 fundamental quality 中分離
系統 MUST 新增 Valuation Agent，產生 structured valuation snapshot，且不得把 valuation multiples、target prices 或 broker summaries 當成 business quality 或 buy-worthiness 的證明。

#### Scenario: Valuation snapshot 被產生
- **WHEN** default Phison research run 被產生
- **THEN** `analysis.valuation` 必須包含 `summary`、`scenarios`、`multiples`、`broker_targets`、`data_gaps` 與 `interpretation`。
- **AND** 既有 `analysis.fundamentals.valuation_scenarios` 必須保留 backward compatibility，直到 UI 與 report 完成遷移。
- **AND** Valuation Agent 必須記錄 price date，以及 price 是 fixture-based 還是 live market data。

#### Scenario: Valuation coverage 明確化
- **WHEN** valuation metric 透過 API 回傳或在 report 中使用
- **THEN** 它的 coverage status 必須是 `available`、`partial`、`missing` 或 `not_available` 其中之一。
- **AND** 當 Forward P/E 來自 EPS assumptions，但缺 historical P/E distribution、peer comparison 或 multi-year earnings validation 時，可標為 `partial`。
- **AND** 除非 fixture 包含 source-backed values，否則 P/B 與 dividend-yield checks 必須標為 `missing`。

#### Scenario: Broker targets 是 source-backed assumptions
- **WHEN** 系統顯示 broker target prices 或 target-price ranges
- **THEN** 系統必須記錄 source IDs、publication dates、target price、broker 或 source label，以及 reliability notes。
- **AND** CMoney 或 news summaries 必須被標示為 summaries，而不是 full brokerage reports。
- **AND** 系統不得捏造未揭露 broker names 或 model details。

#### Scenario: Scenario sensitivity 被報告
- **WHEN** EPS、price 或 target-price assumptions 在不同 sources 間不同
- **THEN** Valuation Agent 必須報告 scenario matrix，並分開 conservative、base 與 optimistic assumptions。
- **AND** 它必須說明 AI SSD growth story 要支撐 current valuation，需要哪些 assumptions 成立。

#### Scenario: Valuation overclaim 被偵測
- **WHEN** report 把單一 target price、Forward P/E 或 upside percentage 當成 fair-value proof、buy recommendation 或股票便宜的證明
- **THEN** evaluation agent 必須將其視為 hard failure 或標記 report needs revision。
- **AND** 若 price data 是 fixture-based 或 stale，report 必須寫出 price date，並避免 live-price language。

### Requirement: 系統使用可追溯資料來源
系統 MUST 將 retrieved documents 或 external data 產生的 claims 附上 source references。

#### Scenario: 使用新聞資料
- **WHEN** 系統摘要 news
- **THEN** 它必須包含 publication source、date、title 與短 relevance explanation。

#### Scenario: 使用財報 / 財務資料
- **WHEN** 系統使用 financial metrics
- **THEN** 它必須記錄 metric name、period、source document，以及該 value 是 raw data 還是 model-derived。

#### Scenario: Source quality 不足
- **WHEN** available sources stale、thin、contradictory 或 low quality
- **THEN** 系統必須降低 confidence，並要求 additional data 或縮小 conclusion。

### Requirement: 系統控制成本與延遲
當 cheaper path 足夠時，系統 MUST 避免執行昂貴 retrieval 與 agent pipelines。

#### Scenario: 類似問題已存在
- **WHEN** new request 和 prior evaluated request 語意相似
- **THEN** 系統必須先 reuse 或 adapt cached answer path，再決定是否啟動 full pipeline。

#### Scenario: 需要 full pipeline
- **WHEN** request 需要 fresh multi-source analysis
- **THEN** 系統必須記錄哪些 agents 有執行、approximate token usage、latency 與 cache hits。

### Requirement: 系統評估每個 research output
系統 MUST 在把 generated reports 當成 final 前進行 evaluation。

#### Scenario: Report 被產生
- **WHEN** Report Generator 產生 investment research summary
- **THEN** Evaluation Agent 必須依照 rubric 評分，rubric 覆蓋 source grounding、logical consistency、risk coverage、uncertainty 與 user usefulness。

#### Scenario: Evaluation score 太低
- **WHEN** evaluation score 低於 4.0 / 5
- **THEN** 系統必須 revise report、要求更多 data，或明確標示 output 是 low confidence。

#### Scenario: Golden set 可用
- **WHEN** benchmark report 或 manually curated answer 存在
- **THEN** 系統必須將 generated output 和 golden set 比較，並記錄 score differences。

### Requirement: 系統保留人類決策責任
系統 MUST 明確說明 outputs 是 decision-support research，不是 autonomous financial advice。

#### Scenario: Final answer 包含投資觀點
- **WHEN** 系統輸出 bullish、bearish 或 neutral view
- **THEN** 它必須包含 assumptions、risks、confidence level，並提醒 user 仍需對決策負責。

#### Scenario: 使用者要求執行交易
- **WHEN** 使用者要求系統下單或 rebalance assets
- **THEN** MVP 必須拒絕，並說明 execution 不在 scope。

### Requirement: 專案提供 AIASE final-project deliverables
除了 runnable product，專案也 MUST 準備 AIASE final-project grading 需要的 documentation 與 presentation artifacts。

#### Scenario: GitHub source 被提交
- **WHEN** 專案準備提交到 GitHub Classroom 或課程 submission platform
- **THEN** repository 必須包含 reproducible README、environment variable example、frontend and backend source、local fixtures 與 verification commands。

#### Scenario: Technical report 被撰寫
- **WHEN** technical report 被產生
- **THEN** 它必須說明 user problem、quality-of-life value、system architecture、agent workflow、data sources、API design、evaluation、limitations 與 future work。

#### Scenario: Architecture 與 flow diagrams 被準備
- **WHEN** 準備 course demo 或 technical report materials
- **THEN** project 必須包含 system architecture diagram、service flow diagram 與 agent workflow diagram，顯示 frontend、backend、data layer、research evidence pack、agents 與 evaluation。

#### Scenario: Demo slides 被準備
- **WHEN** demo presentation slides 被產生
- **THEN** slides 必須說明 problem、user、core AI workflow、Evidence Pack knowledge layer、agent trace、demo path、risks、limitations 與 next steps。

#### Scenario: External services 不可用
- **WHEN** evaluation 期間 external APIs、model services 或 network access 不可用
- **THEN** project 仍必須能用 local fixtures 與 deterministic agents 展示 main happy path。
