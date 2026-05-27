# Personal Finance Multi-Agent System

多代理個人投資 / 理財研究系統，第一版聚焦台股個股研究，預設標的為群聯電子（8299）。

目前 repo 已進入第一版 MVP 實作。這個 repo 採「文件入口集中、執行資料分層」的整理方式：產品規格、OpenSpec 變更、課程交付文件、runtime fixtures、Evidence Pack 各自保留責任邊界，但都可以從本 README 和 `docs/README.md` 找到。

## 文件與 Ground Truth

| 路徑 | 角色 | 什麼時候讀 |
|---|---|---|
| `docs/README.md` | 文件地圖與整理規則 | 不確定文件該放哪裡、或要找 ground truth 時先讀 |
| `SPEC.md` | 產品範圍、使用者價值、MVP 行為的主要規格 | 判斷需求是否符合台股 / 群聯 / Evidence Pack / AIASE 方向 |
| `openspec/changes/personal-finance-multi-agent-system/` | OpenSpec 變更提案、設計、任務與可測需求 | 實作或修改功能前讀，並在需求變更時同步更新 |
| `docs/project-proposal.md` | 課程 / 展示用 proposal | 對外說明題目、使用者、outcome、scope |
| `docs/course-final-project.md` | AIASE final project 要求整理 | 檢查課程交付物、評分面向、可執行 demo 風險 |
| `docs/architecture.md` | 穩定架構與 agent workflow 圖 | 說明系統如何運作或更新架構圖時讀 |
| `docs/api.md` | API endpoint、payload、錯誤與限制 | 修改 Flask API 或前端串接時讀 |
| `docs/technical-report.md` | 技術報告草稿 | 課程 technical report 與系統設計說明 |
| `docs/statementdog-feature-benchmark.md` | 財報狗 benchmark 拆解 | 擴充股票健診、財務分析、AI 統整報告時讀 |
| `data/` | 本機 JSON / Markdown fixtures 與 source excerpts | deterministic pipeline 的輸入資料，不是一般說明文件 |
| `knowledge/` | Evidence Pack 研究頁、provenance、contradiction log | 投資研究 claim 的可審計證據層 |
| `golden_samples/` | 群聯公開來源 proxy golden sample | 評估報告結構、來源引用與反幻覺能力 |
| `slides/` | Demo presentation outline | 準備展示與口頭 demo |
| `AGENTS.md` | Codex / agent 開發規則 | 任何代理開始改 repo 前都應先讀 |
| `.agents/` | Project-local Everything Claude Code / ECC skills 與 rules | 需要 coding、testing、API、security、verification 等開發規則時讀 |

原本的課程整理已從 `TAICA_AIASE2026-main/final_project_資訊整理.md` 合併到 `docs/course-final-project.md`；`docs/proposal.md` 也改名為 `docs/project-proposal.md`，避免和 OpenSpec 的 `proposal.md` 混淆。`TAICA_AIASE2026-main/` 若仍存在，視為外部課程材料 dump，不是本 repo 的 canonical project docs。

第一版實作邊界：

- Flask 後端 + Vue 前端。
- 本機 Markdown / JSON fixture。
- mock / deterministic agents。
- 手動股價或使用者輸入，不接即時行情 API。
- Evidence Pack：群聯 7 個 evidence pages + provenance + contradiction log。
- 不先接 Supabase、真實 LLM、爬蟲或外部行情 API。

開發時的 ground truth 順序：

1. 先讀 `AGENTS.md` 和 `docs/README.md` 確認文件邊界。
2. 用 `SPEC.md` 判斷產品和課程方向。
3. 用 `openspec/changes/personal-finance-multi-agent-system/` 判斷當前實作需求與驗收條件。
4. 修改 API、架構、報告或展示時，同步更新 `docs/` 對應文件。
5. 修改研究資料或投資 claim 時，以 `data/` 與 `knowledge/` 的 source / Evidence Pack / provenance 為準。

## 本機啟動

後端需要 Flask。若尚未安裝依賴，請先建立虛擬環境後安裝：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

啟動後端：

```bash
python3 -m backend.app
```

前端需要 Node.js 與 npm。安裝並啟動：

```bash
cd frontend
npm install
npm run dev
```

預設前端網址為 `http://127.0.0.1:5173`，後端 API 為 `http://127.0.0.1:8000`。

## 驗證

不需要外部 API key 即可跑核心測試：

```bash
python3 -m unittest discover backend/tests
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall backend
openspec validate personal-finance-multi-agent-system --strict --no-interactive
cd frontend
npm run build
npx playwright install chromium
npm run verify:technical-tab
npm audit --audit-level=moderate
```

`npm run verify:technical-tab` 會自動啟動本機 Flask API 與 Vue dev server，使用 Playwright 在 desktop / mobile viewport 打開 `Technical` tab，檢查五個技術面向、`not_evaluable` 狀態、資料政策與水平溢出。截圖輸出在 `frontend/test-results/technical-tab/`，該資料夾不進 git。

## Demo Path

1. 開啟 Vue 工作台。
2. 使用預設標的「群聯電子 8299」與研究問題。
3. 調整示範股價，啟動研究。
4. 依序展示 Agent Trace、Sources、Evidence Pack、Research Report、Evaluation。
5. 強調輸出是研究輔助，不是買賣建議。
