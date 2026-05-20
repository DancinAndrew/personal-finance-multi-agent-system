# Documentation Map

本 repo 的文件整理原則是：**不要把所有 Markdown 合成一個大檔案，而是讓每個資料夾只承擔一種責任，並把入口集中在 README / AGENTS / OpenSpec context。**

## 合併與重新定位結果

| 原本狀態 | 現在位置 / 決策 | 原因 |
|---|---|---|
| `TAICA_AIASE2026-main/final_project_資訊整理.md` 放在外部課程資料夾內 | `docs/course-final-project.md` | 這是本專案會用到的課程要求摘要，應放進 `docs/`；外部課程 dump 不作為 canonical project docs |
| `docs/proposal.md` 容易和 OpenSpec proposal 混淆 | `docs/project-proposal.md` | 課程 / 展示 proposal 和 OpenSpec change proposal 是不同用途 |
| `SPEC.md`、`openspec/`、`docs/` 同時存在 | 保留，但定義優先順序 | `SPEC.md` 管產品方向，OpenSpec 管變更與驗收，`docs/` 管穩定交付文件 |
| `data/` 看起來像文件 | 保留為 runtime fixtures/source excerpts | 這些是 deterministic pipeline 的輸入資料，不是文件草稿 |
| `knowledge/` 看起來像文件 | 保留為 Evidence Pack | 這是投資 claim 的可審計證據層，和一般 docs 不同 |

## Ground Truth 順序

1. `AGENTS.md`：代理與開發流程規則。
2. `README.md`：專案入口、啟動、驗證、文件總覽。
3. `SPEC.md`：產品定位、MVP 範圍、使用者價值、重要決策。
4. `openspec/changes/personal-finance-multi-agent-system/`：目前這個 change 的 proposal、design、tasks、requirement scenarios。
5. `docs/architecture.md`、`docs/api.md`、`docs/technical-report.md`：穩定工程文件與課程交付物。
6. `data/`：demo run、source catalog、source excerpts、price / evaluation / health-check fixtures。
7. `knowledge/`：Evidence Pack schema、research evidence pages、provenance、contradiction log。

如果上述文件衝突：

- 產品方向以 `SPEC.md` 為準。
- 實作中的驗收條件以 OpenSpec `spec.md` 和 `tasks.md` 為準。
- 來源、claim、投資研究內容以 `data/` 和 `knowledge/` 的 source / provenance 為準。
- 發現衝突時不要只改程式；要同步更新 `SPEC.md`、OpenSpec 或 `docs/` 的對應文件。

## 文件職責

| 路徑 | 職責 | 更新時機 |
|---|---|---|
| `SPEC.md` | 中文產品規格與 MVP 決策 | 需求、範圍、產品定位改變 |
| `openspec/config.yaml` | OpenSpec 專案 context | 文件結構、開發規則或 artifact 規則改變 |
| `openspec/changes/personal-finance-multi-agent-system/proposal.md` | Change intent | OpenSpec change 的目標或 impact 改變 |
| `openspec/changes/personal-finance-multi-agent-system/design.md` | Feature design | 架構、資料契約、agent workflow 改變 |
| `openspec/changes/personal-finance-multi-agent-system/tasks.md` | 實作任務與驗收 | 任務完成狀態或下一步切片改變 |
| `openspec/changes/personal-finance-multi-agent-system/specs/personal-finance-multi-agent-system/spec.md` | Testable requirements | 新增或修改可驗收行為 |
| `docs/project-proposal.md` | 課程 / 展示 proposal | 對外提案敘事改變 |
| `docs/course-final-project.md` | AIASE final project 要求整理 | 課程要求有新資訊 |
| `docs/architecture.md` | 系統架構圖與 agent workflow | 元件或資料流改變 |
| `docs/api.md` | API contract | endpoint、payload、錯誤處理改變 |
| `docs/technical-report.md` | Technical report 草稿 | 課程報告內容更新 |
| `docs/statementdog-feature-benchmark.md` | 財報狗 benchmark | 股票健診或財務分析 benchmark 改變 |
| `slides/final-demo-outline.md` | Demo slides outline | 展示流程或說法改變 |
| `.agents/` | Project-local ECC skills / rules | 需要 Everything Claude Code 的開發規則或 workflow skill |

## 不再新增的文件型態

- 不在 root 新增臨時規劃文件；root 只保留 `README.md`、`SPEC.md`、`AGENTS.md` 這類入口文件。
- 不在 `TAICA_AIASE2026-main/` 新增本專案文件；課程要求摘要統一放 `docs/course-final-project.md`。
- 不把 runtime source excerpts 複製到 `docs/`；它們應留在 `data/phison/sources/`。
- 不把 Evidence Pack pages 當成課程報告；它們應留在 `knowledge/phison/pages/`，並維持 provenance。
