# AGENTS.md

本 repo 是台股個股研究用的 personal finance multi-agent system。所有代理在修改程式或文件前，先用這份檔案確認專案 ground truth、文件邊界與驗證方式。

## 先讀順序

1. `README.md`：專案入口、啟動方式、文件總覽。
2. `docs/README.md`：文件整理規則與 ground truth 順序。
3. `SPEC.md`：產品定位、MVP 範圍、台股 / 群聯 / Evidence Pack / AIASE 對齊。
4. `openspec/changes/personal-finance-multi-agent-system/`：目前 change 的 proposal、design、tasks、requirement scenarios。
5. `docs/architecture.md`、`docs/api.md`、`docs/technical-report.md`：穩定工程文件與課程交付物。
6. `data/` 與 `knowledge/`：runtime fixtures、source excerpts、Evidence Pack、provenance 與 contradiction log。

## 文件邊界

- `SPEC.md` 是產品與 MVP 行為的主要規格。
- `openspec/` 是變更控制與可驗收需求，不是一般文件倉庫。
- OpenSpec 文件預設使用繁體中文撰寫；只有 `MUST`、`SHALL`、`Requirement`、`Scenario`、`WHEN`、`THEN`、API 欄位名稱、enum 值等 parser 或 wire contract 必要 token 保留英文。
- `docs/` 放穩定工程文件、課程交付文件與 benchmark。
- `data/` 是 deterministic pipeline 的機器可讀輸入，包含 source catalog、source excerpts、price fixture、evaluation rubric、demo run。
- `knowledge/` 是 Evidence Pack，不是普通筆記；投資 claim 必須能追溯 source ID、provenance 與 contradiction log。
- `golden_samples/` 是 evaluation reference，不可宣稱等同正式券商研報。
- `TAICA_AIASE2026-main/` 若存在，視為外部課程材料 dump；canonical 課程要求摘要是 `docs/course-final-project.md`。

## 開發規則

- 保持 Python-first；後端是 Flask，前端是 Vue，除非現有專案文件明確改變。
- 不要安裝依賴、啟用 MCP、接外部服務、加入 Supabase、LLM provider、crawler、行情 API，除非使用者明確同意。
- 修改功能前先檢查 OpenSpec requirement 和 tasks；需求改變時同步更新 `SPEC.md`、OpenSpec 和相關 `docs/`。
- 修改 API 時同步更新 `docs/api.md`；修改 agent workflow 或資料流時同步更新 `docs/architecture.md`。
- 修改投資研究資料時，不要直接覆蓋 raw sources；更新 Evidence Pack 時要保留 provenance，重大結論變更要寫入 contradiction log 或 review gate。
- 不輸出買賣指令、保證報酬或未經來源確認的券商 / 財務數字。
- 保留使用者既有變更；不要 revert unrelated files。

## Everything Claude Code / ECC

這個 repo 使用 project-local ECC assets：

- Skills：`.agents/skills/`
- Rules：`.agents/rules/ecc/common/`、`.agents/rules/ecc/python/`

建議使用情境：

- `coding-standards`：一般程式碼品質與可讀性。
- `python-patterns`：後端 Python / Flask /資料處理變更。
- `python-testing` 或 `tdd-workflow`：新增功能、修 bug、擴充 agent behavior。
- `api-design`：新增或改 API endpoint / payload。
- `backend-patterns`：後端架構、store、orchestrator、agent pipeline。
- `security-review`：處理使用者輸入、金融風險、secrets、外部 API 或權限。
- `search-first`：引入新工具或框架前先調研，不要自己硬寫。
- `verification-loop`：收尾驗證與 diff review。
- `git-workflow`：需要整理 commit、branch、push 或 PR 時。

若 ECC skill/rule 與使用者指令、系統指令或本 `AGENTS.md` 衝突，優先順序為：使用者 / 系統指令 > 本 `AGENTS.md` > ECC skill/rule。

## 驗證指令

優先使用 repo 既有指令，不新增工具：

```bash
python3 -m unittest discover backend/tests
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall backend
openspec validate personal-finance-multi-agent-system --strict --no-interactive
cd frontend
npm run build
```

如果改到文件結構，也要跑：

```bash
rg -n "docs/proposal.md|TAICA_AIASE2026-main/final_project_資訊整理.md|/Users/andrew-ideaslab/Documents/New project/SPEC.md" SPEC.md openspec slides
git diff --check
```

## 新文件放置規則

- 新的長期工程文件放 `docs/`。
- 新的產品規格或範圍決策先更新 `SPEC.md`。
- 新的可驗收功能需求放 OpenSpec `spec.md`，任務放 `tasks.md`。
- 新的 raw/demo source 放 `data/phison/sources/` 並更新 `data/phison/source_catalog.json`。
- 新的研究 evidence 放 `knowledge/phison/pages/` 並更新 `knowledge/phison/provenance.json`。
- 不在 root 新增臨時 Markdown 文件。
