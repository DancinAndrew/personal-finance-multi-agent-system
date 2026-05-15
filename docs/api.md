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

## Error Handling

找不到 run 時回傳：

```json
{
  "error": "research_run_not_found",
  "run_id": "..."
}
```
