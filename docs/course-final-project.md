# AIASE 2026 Final Project 資訊整理

整理日期：2026-05-09
來源範圍：`TAICA_AIASE2026-main` 目前 repo 內的 Markdown 檔案，並輔以關鍵字掃描 Notebook。Notebook 命中多為教學範例與圖片資料，沒有發現比 `syllabus.md`、`README.md`、`W1.md`、`W3.md` 更明確的 final project 規定。

## 一句話結論

Final Project 佔總成績 **40%**，目標是做出一個可展示、最好可上線的「生成式 AI 應用系統 / Web 服務」。題目方向是 **Build Services for Better Quality-of-Life**，可個人或兩人組隊；提案草稿要求在 **2026 年 5 月前**提出，但 repo 沒寫精確日期與時間。最後評分重點集中在系統架構、服務流程與 API 設計、Demo 簡報、GitHub 原始碼與技術報告；抽查不能執行則 0 分。

## 已明確寫在課程文件中的規定

| 項目 | 文件中的資訊 | 來源 |
|---|---|---|
| 成績比重 | Final Project 佔 **40%**；6 次 HW 合計 60%。 | `README.md:44-55`, `syllabus.md:84-94`, `W1.md:720-726` |
| 專題定位 | 完成一項可展示的生成式 AI 應用系統；W1 也寫成「可上線的生成式 AI 應用系統期末專題」。 | `syllabus.md:17-30`, `W1.md:97-107` |
| 主題方向 | **Final Project - Build Services for Better Quality-of-Life**。 | `W1.md:732-739` |
| 團隊人數 | 1 人或 2 人一組。 | `W1.md:725`, `W1.md:736` |
| 提案截止 | `Draft proposals before May`。依 2026 課程脈絡，意思是 2026-05-01 前，但 repo 沒有精確到日期或時間。 | `W1.md:737` |
| Demo 時段 | 第 16-18 週為 `Online/Onsite Demo`，共 9 小時，內容為 `Project Demo`。 | `syllabus.md:76-80`, `W1.md:319-323` |
| Live Demo | 不是每組都要 Live Demo；AI 會先挑選可 Live Demo 的組別，也可自告奮勇。Live Demo 有機會 Final Project **90 分以上**。 | `W1.md:738` |
| 一般評分區間 | W1 寫「其他一律 60-90 分」，由 Instructor and AI review。 | `W1.md:739` |
| 不能執行 | 抽查不能執行，一律 0 分。 | `W1.md:739` |
| 遲交政策 | 遲交 0 分。 | `W1.md:728` |
| 繳交平台 | 所有 HW 和 Project 都以 **GitHub Classroom** 上傳。 | `W1.md:135-137` |
| 評分前公開性 | 評分前請 keep private；評分後可以放到自己的 GitHub repo。 | `W1.md:136-137` |
| 課程資源限制 | 不提供 Public Service budget；課程後續會提供成大架設的 LLM API Key 作為相關作業基礎需求。 | `W1.md:139` |

## 評分面向與應交付物

`syllabus.md` 明確列出 Final Project 的評分面向：

1. **系統架構圖**：要包含微服務拆分、Agent workflow。
2. **服務流程圖與 API 設計**：不只是畫 UI，還要說清楚服務如何流動、API 如何被呼叫。
3. **Demo Presentation and Slides**：需要能展示專題價值與系統運作。
4. **GitHub Source and Technical Report**：需要原始碼與技術報告。

來源：`syllabus.md:96-101`

## 專題應該長什麼樣子

課程整體目標不是做一個單純聊天介面，而是「生成式 AI 應用系統工程」。從課程大綱看，final project 很可能會期待你把以下能力放進一個可執行系統裡：

| 面向 | 應該在專題中看得到的證據 | 來源 |
|---|---|---|
| Full-stack 應用 | 前端、後端、LLM 層、Agent workflow、資料流，而不是只有 prompt。 | `README.md:10-13`, `syllabus.md:17`, `W1.md:43-50` |
| SDLC / Spec-driven | 需求分析、Use Case、系統需求、高階架構、服務邊界與模組切分。 | `syllabus.md:23-24`, `syllabus.md:40-41`, `W2.md:649-655` |
| 架構圖與流程圖 | Mermaid/UML 可用來表達元件關係、資料流、流程分支；課程特別強調「先畫圖，再實作」。 | `W2.md:668-688`, `W2.md:921-933` |
| API / Tool contract | API 設計本身是評分面向；Agent 課程也強調 Tool Schema 可視為 API Contract。 | `syllabus.md:98-101`, `W3.md:1200-1207` |
| Agent / RAG 能力 | 課程涵蓋 Agent workflow、MCP、ADK、agent-to-agent、RAG pipeline、向量資料庫。若專題跟這些完全無關，要小心課程契合度。 | `syllabus.md:65-72` |
| 安全與審計 | Prompt injection 防禦、response auditing、最小權限、HITL、guardrails 是課程目標之一。 | `syllabus.md:27-30`, `W3.md:1195-1207` |
| 可觀測性 | Logs、metrics、distributed tracing、token 成本、延遲與錯誤復原，是第 13 週主題。 | `syllabus.md:69-70` |
| 可重現執行 | Final project 明確有「不能執行 0 分」；因此 README、環境變數、啟動指令、測試或 demo script 都很重要。 | `W1.md:739` |

## 題目選擇線索

W3 提供了三個思考 final project 的問題：

1. 你未來想深耕哪個垂直領域？
2. 你能設計一個 outcome-based 的 AI 服務嗎？如何定義「成果」並設計計費機制？
3. 你的「選擇品味」是什麼？在 AI 大量生成內容與程式碼的時代，你憑什麼判斷好壞？

來源：`W3.md:260-264`

W1 也用「Agent 可以部署在哪些領域」提示題目方向：

| 領域 | 佔比 |
|---|---:|
| Software engineering | 49.7% |
| Back-office automation | 9.1% |
| Other | 7.1% |
| Marketing and copywriting | 4.4% |
| Sales and CRM | 4.3% |
| Finance and accounting | 4.0% |
| Data analysis and BI | 3.5% |
| Academic research | 2.8% |
| Cybersecurity | 2.4% |
| Customer service | 2.2% |
| Gaming and interactive media | 2.1% |
| Document and presentation creation | 1.9% |
| Education and tutoring | 1.8% |
| E-commerce operations | 1.3% |
| Medicine and healthcare | 1.0% |
| Legal | 0.9% |
| Travel and logistics | 0.8% |

來源：`W1.md:749-772`

## 建議的提案內容

repo 沒有提供正式 proposal template，但根據評分面向與課程主軸，一份安全的提案草稿應至少包含：

- 專題名稱與一句話定位：要解決哪個 quality-of-life 問題。
- 使用者與場景：誰會用、什麼時候用、現有流程痛點是什麼。
- Outcome 定義：使用者得到的具體成果是什麼；如何判斷有效。
- AI / Agent / RAG 角色：AI 是核心功能，不只是開發輔助；列出 perception、memory、reasoning、action 或 retrieval 流程。
- 系統架構圖：前端、後端、LLM gateway、資料庫、向量資料庫、外部 API、背景任務、observability。
- 服務流程圖：使用者操作到 API、Agent、資料讀寫、回傳結果的完整路徑。
- API 設計草案：主要 endpoint、request/response、錯誤處理、權限與成本控制。
- Demo scope：期末 demo 時一定能跑的 happy path，以及備援 demo 資料。
- 風險與限制：金鑰、費用、外部 API、資料品質、模型幻覺、安全審核。
- 交付物計畫：GitHub repo、README、technical report、slides、測試或驗證方式。

## 期末前自查清單

- [ ] 專題明確是一個生成式 AI 應用系統或 Web 服務。
- [ ] 有清楚的 quality-of-life 問題與使用者場景。
- [ ] 有實作層級的 AI / Agent / RAG 功能，而不是只在文件中提到 AI。
- [ ] 有系統架構圖，並標出微服務拆分與 Agent workflow。
- [ ] 有服務流程圖，能看出使用者請求如何經過前端、後端、模型、資料層。
- [ ] 有 API 設計文件或 technical report 中的 API section。
- [ ] GitHub repo 乾淨、可 clone、可依 README 在新環境跑起來。
- [ ] `.env.example` 存在，真實 API key 沒有 commit。
- [ ] 有固定 demo script，可以在網路或模型不穩時用備援資料展示。
- [ ] Slides 能說清楚：問題、使用者、架構、核心 AI 流程、demo、限制、下一步。
- [ ] Technical report 能說清楚：系統設計、資料來源、模型/工具選擇、API、評估、風險。
- [ ] 若想衝 90 分以上，準備主動 Live Demo，且 demo 必須穩。

## 文件中沒有明講、需要再確認的資訊

以下在目前 repo 沒有找到明確答案：

- Final project 最終程式碼 / 報告 / slides 的精確截止日期與時間。
- Final project GitHub Classroom 邀請連結。
- Proposal 的正式格式、檔名、提交位置、是否需要老師先核准。
- 評分 rubrics 的細項百分比；目前只看到四個評分面向，沒有每項配分。
- Technical report 的格式與長度要求。
- Slides 的格式、頁數、是否要繳 PDF 或原始檔。
- 是否一定要部署成公開 URL；課程只說完成 Web service / 可展示 / 可上線，沒有寫硬性部署平台。
- Live Demo 的 AI 挑選標準。
- 兩人組隊的登記方式與成員貢獻認定方式。

## 最小可行交付組合

若要保守準備，至少做出以下內容：

```text
project-repo/
├── README.md                 # 安裝、環境變數、啟動、demo script
├── docs/
│   ├── proposal.md            # 題目、場景、outcome、scope
│   ├── architecture.md        # 系統架構圖、服務邊界、Agent workflow
│   ├── api.md                 # API 設計與錯誤處理
│   └── technical-report.md    # 技術報告
├── slides/                    # demo presentation
├── frontend/                  # Web UI
├── backend/                   # API server / LLM gateway
├── agent_or_rag/              # Agent workflow、RAG、tools、evals
├── tests/                     # 至少涵蓋核心流程
└── .env.example               # 不含真實 secrets
```

## 來源索引

- `README.md:10-13`：課程核心是完成生成式 AI Web service。
- `README.md:44-55`：評量方式，Final Project 40%。
- `syllabus.md:17-30`：課程目標與 final project 定位。
- `syllabus.md:65-80`：Agent、安全、可觀測性、分散式 AI 與 Demo weeks。
- `syllabus.md:84-101`：Final Project 40% 與四個評分面向。
- `W1.md:130-139`：GitHub Classroom、private policy、預算與 LLM API key 說明。
- `W1.md:720-739`：Final Project 比重、團隊人數、提案、Live Demo、評分與不能執行 0 分。
- `W1.md:749-772`：Final Project opportunity areas。
- `W2.md:649-688`：Spec-driven development 與架構圖。
- `W2.md:921-933`：先調研、先寫 spec、先畫圖、逐步驗證。
- `W3.md:260-264`：Thinking your Final Project 三個問題。
- `W3.md:1195-1207`：Agent 安全、guardrails、observability、spec-driven 回顧。
