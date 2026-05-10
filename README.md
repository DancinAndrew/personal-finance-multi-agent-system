# Personal Finance Multi-Agent System

多代理個人投資 / 理財研究系統，第一版聚焦台股個股研究，預設標的為群聯電子（8299）。

目前 repo 已進入第一版 MVP 實作。核心文件：

- `SPEC.md`：中文產品規格與 AIASE final project 對齊。
- `openspec/changes/personal-finance-multi-agent-system/`：OpenSpec proposal、design、tasks 與需求規格。
- `golden_samples/`：群聯公開來源 proxy golden sample。
- `TAICA_AIASE2026-main/final_project_資訊整理.md`：課程 final project 要求整理。
- `backend/`：Flask API 與 deterministic multi-agent pipeline。
- `frontend/`：Vue 研究工作台。
- `data/`：本機 source / price / evaluation fixtures。
- `knowledge/`：LLMWiki-lite 研究頁、provenance 與 contradiction log。

第一版實作邊界：

- Flask 後端 + Vue 前端。
- 本機 Markdown / JSON fixture。
- mock / deterministic agents。
- 手動股價或使用者輸入，不接即時行情 API。
- LLMWiki-lite：群聯 7 個 wiki pages + provenance + contradiction log。
- 不先接 Supabase、真實 LLM、爬蟲或外部行情 API。

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
npm audit --audit-level=moderate
```

## Demo Path

1. 開啟 Vue 工作台。
2. 使用預設標的「群聯電子 8299」與研究問題。
3. 調整示範股價，啟動研究。
4. 依序展示 Agent Trace、Sources、LLMWiki-lite、Research Report、Evaluation。
5. 強調輸出是研究輔助，不是買賣建議。
