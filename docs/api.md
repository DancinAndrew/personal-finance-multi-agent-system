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
- `wiki`
- `analysis`
- `report`
- `evaluation`

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

## GET /api/research-runs/{run_id}/wiki

用途：取得 LLMWiki-lite pages 與 provenance。

## Error Handling

找不到 run 時回傳：

```json
{
  "error": "research_run_not_found",
  "run_id": "..."
}
```
