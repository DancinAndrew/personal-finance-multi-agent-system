# API Design

Base URL：`http://127.0.0.1:8000`

## GET /api/health

用途：健康檢查。

Response:

```json
{
  "status": "ok",
  "mode": "deterministic_demo"
}
```

## GET /api/demo/default-run

用途：取得預設群聯 demo run。

Response includes:

- `run`
- `steps`
- `sources`
- `evidence`
- `analysis`
- `report`
- `evaluation`

`analysis.health_checks` uses the conservative public fixture policy. It does
not represent StatementDog login-gated or paid data.

`analysis.fundamentals` preserves the existing EPS / Forward P/E valuation
scenarios and adds a public-fixture-only financial quality snapshot. It is not a
complete financial database.

`analysis.valuation` separates valuation analysis from fundamental quality. It
uses non-live fixture price, EPS sensitivity, public brokerage summaries, and
missing-data gaps. It is not real-time market data and not a complete brokerage
model.

`analysis.chip` separates chip-data coverage from health-check labels. It uses
only the local public fixture and reports whether branch flow, major
shareholders, director holdings, director pledges, and shareholder count can be
evaluated. It is not StatementDog login-gated or paid data, broker-branch data,
or a live chip API result.

## POST /api/research-runs

用途：建立 deterministic research run。

Request:

```json
{
  "question": "人工智慧固態硬碟成長故事是否足以支撐目前估值？",
  "price": 2430,
  "target": {
    "ticker": "8299",
    "name": "群聯電子",
    "market": "TW_OTC"
  }
}
```

## GET /api/research-runs/{run_id}

用途：取得完整研究結果。

## GET /api/research-runs/{run_id}/steps

用途：取得 agent trace。

## GET /api/research-runs/{run_id}/sources

用途：取得 source map。

## GET /api/research-runs/{run_id}/evaluation

用途：取得 evaluation result。

## GET /api/research-runs/{run_id}/evidence

用途：取得 Evidence Pack pages 與 provenance。

## Health Check Payload

Health Check Agent 會在完整 run response 的 `analysis.health_checks` 回傳股票健診摘要：

```json
{
  "summary": {
    "total": 7,
    "pass": 0,
    "fail": 0,
    "unknown": 6,
    "not_available": 1,
    "data_policy": "public_fixture_only",
    "major_gaps": ["現金流", "股利", "籌碼", "P/B", "F-score"]
  },
  "checks": [
    {
      "id": "growth_stock",
      "name": "成長股健診",
      "status": "unknown",
      "status_reason": "公開來源提供營收與 EPS 線索，但缺完整成長檢核序列。",
      "criteria": [],
      "source_ids": ["S1", "S2", "S3"],
      "missing_data": ["近三個月月營收 YoY 序列"],
      "report_takeaway": "不能完整判定成長股健診通過。",
      "data_policy": "public_fixture_only"
    }
  ]
}
```

Status enum:

- `pass`：現有 fixture 足以支持通過。
- `fail`：現有 fixture 足以支持未通過。
- `unknown`：資料可能可補，但目前不足以判斷。
- `not_available`：需要登入、付費、外部資料源，或第一版尚未納入。

## Fundamental Snapshot Payload

Fundamental Agent 會在完整 run response 的 `analysis.fundamentals` 回傳估值情境與五大基本面面向：

```json
{
  "valuation_scenarios": [],
  "summary": {
    "categories_total": 5,
    "available": 0,
    "partial": 3,
    "missing": 2,
    "not_available": 0,
    "data_policy": "public_fixture_only",
    "major_gaps": ["毛利率", "現金流", "負債比", "週轉天數"]
  },
  "categories": [
    {
      "id": "revenue",
      "name": "營收",
      "coverage_status": "partial",
      "category_takeaway": "已取得 2026 年 4 月營收、月增與年增線索，但尚未建立完整近 12 個月序列與產品別拆分。",
      "metrics": [],
      "missing_data": ["近 12 個月營收序列", "產品別營收"]
    }
  ],
  "key_findings": [],
  "data_gaps": []
}
```

Coverage status enum:

- `available`：fixture 內有數值與來源，足以作為該 metric 的公開線索。
- `partial`：有方向性證據，但不足以做完整趨勢或品質判斷。
- `missing`：資料理論上可由公開財報補齊，但目前 fixture 尚未納入。
- `not_available`：需要登入、付費資料或目前 MVP 外能力。

目前第一版只有 `revenue`、`profitability`、`growth` 是 `partial`；`safety` 與 `cash_flow_quality` 是 `missing`。報告不得把 EPS / Forward P/E 當成完整基本面品質，也不得用營收或 EPS 線索推論現金流已改善。

## Valuation Payload

Valuation Agent 會在完整 run response 的 `analysis.valuation` 回傳估值拆解：

```json
{
  "summary": {
    "data_policy": "public_fixture_only",
    "price": 2430,
    "price_as_of_date": "2026-05-10",
    "is_live_market_data": false,
    "coverage": {
      "available": 0,
      "partial": 2,
      "missing": 4,
      "not_available": 0
    },
    "major_gaps": ["歷史 P/E percentile", "P/B", "殖利率", "同業估值"]
  },
  "scenarios": [],
  "multiples": [],
  "broker_targets": [],
  "data_gaps": [],
  "interpretation": []
}
```

重要限制：

- `price_as_of_date` 必須顯示在 report / UI；`is_live_market_data` 第一版固定為 `false`。
- `scenarios` 是 EPS 假設對 Forward P/E 的敏感度，不是合理價或買賣建議。
- `broker_targets` 只整理公開新聞 / CMoney / FactSet 摘要，不代表完整券商模型。
- P/B、殖利率、歷史 P/E percentile、同業估值目前是 `missing`，不得被寫成已完整驗證。

## Chip Payload

Chip Agent 會在完整 run response 的 `analysis.chip` 回傳籌碼資料覆蓋檢查：

```json
{
  "summary": {
    "data_policy": "public_fixture_only",
    "as_of_date": "2026-05-10",
    "signals_total": 5,
    "coverage": {
      "available": 0,
      "partial": 0,
      "missing": 4,
      "not_available": 1
    },
    "available": 0,
    "partial": 0,
    "missing": 4,
    "not_available": 1,
    "overall_signal": "not_evaluable",
    "major_gaps": ["分點買賣超", "大股東持股", "董監持股", "董監質押", "股東人數"]
  },
  "signals": [],
  "data_gaps": [],
  "interpretation": []
}
```

Coverage status enum:

- `available`：fixture 有足夠來源與期間，可呈現該籌碼指標。
- `partial`：只有部分期間或部分來源，不能形成完整籌碼訊號。
- `missing`：理論上可由公開資料人工補齊，但目前 fixture 尚未納入。
- `not_available`：需要登入、付費、券商分點或外部資料源。

Signal bias enum:

- `bullish`、`bearish`、`neutral`、`mixed`：只有來源與期間足夠時才能使用。
- `unknown`：coverage 是 `missing` 時使用。
- `not_available`：coverage 是 `not_available` 時使用。

第一版 `overall_signal` 固定為 `not_evaluable`；report / UI 不得把缺資料寫成分點買超、主力進場、大股東增加、籌碼轉強或買賣建議。

## Error Handling

找不到 run 時回傳：

```json
{
  "error": "research_run_not_found",
  "run_id": "..."
}
```
