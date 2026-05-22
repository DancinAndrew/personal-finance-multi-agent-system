# Architecture

## System Context

```mermaid
flowchart LR
  User["使用者"] --> Vue["Vue Web App"]
  Vue --> Flask["Flask API"]
  Flask --> Orchestrator["Research Orchestrator"]
  Orchestrator --> Agents["Deterministic Agents"]
  Orchestrator --> Evidence["Evidence Pack"]
  Orchestrator --> Fixtures["Local JSON / Markdown Fixtures"]
  Agents --> Report["Research Report"]
  Agents --> Eval["Evaluation"]
```

## Agent Workflow

```mermaid
sequenceDiagram
  participant U as User
  participant API as Flask API
  participant O as Orchestrator
  participant R as Intent Router
  participant S as Source Retrieval
  participant N as News / Sector Agent
  participant F as Fundamental Agent
  participant V as Valuation Agent
  participant C as Chip Agent
  participant H as Health Check Agent
  participant K as Risk Agent
  participant G as Report Generator
  participant E as Evaluation Agent

  U->>API: Start Phison research
  API->>O: Create research run
  O->>R: Classify intent
  O->>S: Load sources and evidence
  O->>N: Build AI SSD / NAND narrative
  O->>F: Build five-area fundamental snapshot
  O->>V: Build valuation scenarios and target range
  O->>C: Build chip-data coverage snapshot
  O->>H: Run conservative health checks with valuation and chip context
  O->>K: Generate opposing risks with chip gaps
  O->>G: Generate source-backed report
  O->>E: Score report
  API-->>U: Return trace, sources, evidence, report, evaluation
```

Chip Agent 第一版只讀 `data/phison/chip_fixture.json`，不登入財報狗、不接券商分點或即時籌碼 API。它輸出 `analysis.chip`，讓 UI、報告、Health Check Agent 與 Evaluation Agent 都能看到籌碼資料缺口；Health Check Agent 只消費這個 output，不重新計算籌碼 metrics。

## Evidence Pack

```mermaid
flowchart TB
  Sources["Raw Sources"] --> EvidencePages["Research Evidence Pack Pages"]
  Sources --> Provenance["Claim Provenance"]
  EvidencePages --> Agents["Agents"]
  Provenance --> Agents
  EvidencePages --> Audit["Contradiction Log"]
  Audit --> Evaluation["Evaluation"]
```

## Local-First Boundary

第一版不依賴 Supabase、真實 LLM、即時行情 API 或 crawler。這讓課程抽查時即使外部服務不可用，也能展示主要 happy path。
