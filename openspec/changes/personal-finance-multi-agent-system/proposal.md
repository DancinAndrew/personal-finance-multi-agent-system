## 為什麼

這個專案需要用 spec-first 的方式，先把「multi-agent 個人投資 / 理財研究系統」的行為定義清楚，再決定技術細節、資料庫、UI 或部署方式。第一版需求來自 Chris 諮詢筆記與使用者想學台股投資的目標，因此重點不是做通用投資聊天機器人，而是做一個可展示、可驗證、對使用者真實研究群聯有幫助的台股研究工作台。

OpenSpec 文件預設使用繁體中文撰寫。若因 OpenSpec 格式需要保留 `Requirement`、`Scenario`、`WHEN`、`THEN`、`AND` 等英文結構標記，標記可保留英文，但標題內容、說明與驗收語意都應使用中文。

## 變更內容

- 新增一個 multi-agent 投資研究系統能力。
- 定義 MVP 的行為：意圖路由、專家代理、可追溯資料檢索、成本 / 延遲控制、評估流程與人類決策邊界。
- 將第一版 MVP 範圍限定在台股，而不是全球投資、完整資產配置或泛用理財。
- 使用群聯電子（8299）作為第一個 seed target，並連接使用者既有的 Obsidian 研究筆記。
- 將 MVP 做成可展示的網頁應用。
- 在網頁應用中展示可觀察的代理執行軌跡。
- 第一版 agent trace 只儲存摘要與來源，不儲存完整 intermediate outputs。
- 第一版主要資料來源以新聞與財報 / 財務資訊為主。
- 第一版先使用手動 curated dataset，crawler 或 Exa API 留到後續延伸。
- 新增 Evidence Pack 研究證據層，讓 raw sources 先整理成人可讀、可連結、可稽核、有 provenance 的 evidence pages，再交給 agents 使用。
- 設定第一版 evaluation 通過門檻為 4.0 / 5。
- 優先以外部券商研究報告作為 golden sample；若使用者沒有券商報告，先使用清楚標示為 proxy 的公開來源 golden sample。
- 將第一個研究問題設定為：「AI SSD 成長故事是否足以支撐群聯目前估值」。
- 將財報狗 / StatementDog 式 dashboard 與股票健診作為產品 benchmark，但系統目標是合成 AI 研究報告，而不是讓使用者自己逐頁看 dashboard。
- 新增第二階段最小切片：保守 Health Check Agent，將七種 StatementDog-style 股票健診角度轉成可稽核的 `pass`、`fail`、`unknown`、`not_available` 輸出。
- 要求 Health Check Agent 遇到缺資料、付費資料、登入資料或不可驗證資料時，必須標示資料缺口，不得假裝已完成檢核。
- 第二階段切片維持本機 deterministic：不依賴 Supabase、真實 LLM、crawler、Exa API、即時行情、StatementDog 登入或付費資料。
- 新增下一個第二階段切片：Fundamental Agent 擴充，將營收、獲利能力、安全性、成長力、現金流品質整理成 structured financial snapshot，並清楚標示來源覆蓋與 missing-data gaps。
- 保留既有 EPS / Forward P/E 情境，但將它和完整基本面品質分析分開，避免估值敏感度被誤解成完整基本面研究。
- 新增下一個 docs-first 切片：Valuation Agent，將估值分析從基本面品質中分離，覆蓋 earnings multiples、券商目標價區間、情境敏感度，以及 P/B、殖利率、歷史估值資料缺口。
- 要求 Valuation Agent 將目標價與 Forward P/E 視為假設與情境敏感度，而不是合理價證明、買進建議或股票便宜的證據。
- 新增下一個 docs-first 切片：Chip Agent，將分點籌碼、大股東持股、董監持股、董監質押與股東人數整理成保守籌碼面 snapshot。
- 要求 Chip Agent 在第一版維持本機 deterministic，遇到登入、付費、未納入 fixture 或不可驗證資料時標示 `missing` 或 `not_available`，不得把籌碼缺口包裝成主力進出、買賣訊號或健診通過。

## 能力範圍

### 新增能力

- `personal-finance-multi-agent-system`：定義台股投資研究輔助系統的行為，包括路由、專家 agents、來源 grounding、evaluation 與安全邊界。
- `stock-health-check-agent`：定義七種投資視角的保守股票健診行為，包括資料缺口處理，以及如何整合到報告、trace 與 evaluation。
- `fundamental-analysis-agent`：定義 deterministic 基本面分析行為，覆蓋營收、獲利能力、安全性、成長力與現金流品質，並包含 metric coverage status 與報告整合方式。
- `valuation-analysis-agent`：定義 deterministic 估值分析行為，使用 public fixtures、明確 valuation coverage status、情境敏感度、source-backed broker target ranges 與 overclaim guardrails。
- `chip-analysis-agent`：定義 deterministic 籌碼面分析行為，覆蓋分點、法人 / 主力線索、大股東、董監、質押與股東人數資料缺口，並約束不可把 unavailable chip data 寫成交易訊號。

### 修改能力

目前沒有修改既有能力，而是在同一個 active change 中逐步擴充 MVP 能力。

## 影響

- OpenSpec active change：`personal-finance-multi-agent-system`
- 主要討論與規格 artifact：`SPEC.md`
- 第一版仍不新增 runtime dependency、外部資料源、API key 或部署要求。
- 後續所有 OpenSpec proposal、spec、design、tasks 預設使用繁體中文撰寫；必要的 wire values、API field names、enum values 與 OpenSpec 結構標記可保留英文。
