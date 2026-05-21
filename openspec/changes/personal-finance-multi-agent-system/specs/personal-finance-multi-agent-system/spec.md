## ADDED Requirements

### Requirement: System scopes MVP research to Taiwan equities
The system SHALL treat Taiwan equities as the MVP investment universe.

#### Scenario: User asks about a Taiwan stock
- **WHEN** the user asks about a listed or OTC Taiwan company by stock code or company name
- **THEN** the system treats the request as in scope and starts the Taiwan equity research workflow.

#### Scenario: User asks about non-Taiwan assets
- **WHEN** the user asks about US stocks, crypto, overseas ETFs, funds, bonds, or insurance products
- **THEN** the MVP explains that the first version is scoped to Taiwan equities and either refuses, asks to switch to a Taiwan stock, or marks the request as future scope.

#### Scenario: User asks for portfolio allocation
- **WHEN** the user asks for full portfolio allocation across asset classes
- **THEN** the MVP narrows the task to single-stock research or records portfolio analysis as a future capability.

### Requirement: System uses Phison as the first MVP seed target
The system SHALL use Phison Electronics (8299) as the first end-to-end Taiwan equity research target.

#### Scenario: User asks for the first MVP company
- **WHEN** the system needs a default company for prototype data collection, report generation, or evaluation
- **THEN** it selects Phison Electronics (8299) as the default target.

#### Scenario: Existing Obsidian research note is available
- **WHEN** the system builds the first Phison research corpus
- **THEN** it includes the user's Obsidian note as an initial reference document and records the note path.

#### Scenario: Generated report is evaluated
- **WHEN** the system evaluates a generated Phison report
- **THEN** it compares the output against the structure and expectations of the user's existing Phison research note without treating the note as automatically current or infallible.

### Requirement: System provides a demoable web application
The system SHALL expose the MVP through a web application suitable for demonstration.

#### Scenario: User opens the web application
- **WHEN** the user opens the local or deployed web application
- **THEN** the system provides an interface for entering a research question, viewing agent workflow, viewing sources, and reading the generated report.

#### Scenario: User runs the default Phison research task
- **WHEN** the user selects the default Phison research task
- **THEN** the system demonstrates the end-to-end workflow for the question "whether the AI SSD growth story supports Phison's current valuation."

#### Scenario: Research result is displayed
- **WHEN** the web application displays a research result
- **THEN** the interface clearly labels the output as research support rather than buy/sell advice.

#### Scenario: Course evaluator runs the project locally
- **WHEN** a course evaluator starts the project from the README in a local environment
- **THEN** the default demo runs without requiring Supabase, a real LLM key, live market data API, or external crawler.

### Requirement: System shows observable agent execution traces
The system SHALL make the research process observable through agent execution traces.

#### Scenario: User starts the default Phison research task
- **WHEN** the user starts the default Phison research task
- **THEN** the web application displays an execution timeline including intent routing, retrieval, fundamental analysis, risk or opposing view analysis, report generation, and evaluation.

#### Scenario: User inspects a single agent step
- **WHEN** the user opens an agent step
- **THEN** the system shows that step's input summary, output summary, used sources, confidence or evaluation metadata, and available latency or cost metadata.

#### Scenario: Full intermediate output exists
- **WHEN** the system records first-version agent traces
- **THEN** it stores summaries and sources by default and does not persist full intermediate outputs unless a future privacy, storage, and debugging policy is designed.

#### Scenario: User traces a report claim
- **WHEN** the user inspects an important claim in the research report
- **THEN** the system links the claim back to the responsible agent step and source materials.

### Requirement: System uses news and financial reports as first primary data sources
The system SHALL prioritize news and financial reports for the first Phison research dataset.

#### Scenario: First dataset is built
- **WHEN** the system builds the first Phison dataset
- **THEN** it includes the user's existing Obsidian Phison note, 5 to 10 relevant news items, and 1 to 2 official financial documents.

#### Scenario: Data source is beyond first version scope
- **WHEN** earnings-call transcripts, annual report deep dives, or other sources are not yet prepared
- **THEN** the system marks them as future data sources and does not pretend they were fully included.

### Requirement: System starts with manually curated source data
The system SHALL use a manually curated Phison dataset for the first version.

#### Scenario: Manual news and financial data are curated
- **WHEN** the first Phison dataset is created
- **THEN** each item records title, source, date, URL or local path, and relevance to the research question.

#### Scenario: Automated collection is added later
- **WHEN** a later version adds crawlers or Exa API
- **THEN** automated sources preserve the same source metadata and quality checks as manually curated data.

### Requirement: System provides an Evidence Pack research knowledge layer
The system SHALL organize raw sources into a human-readable, linkable, and auditable research evidence pack layer between retrieval and agent analysis.

#### Scenario: Raw source is read
- **WHEN** the system reads news, financial reports, CMoney summaries, FactSet consensus estimates, official company data, or user notes
- **THEN** it preserves the raw source record and must not overwrite the original text or treat summaries as primary source data.

#### Scenario: Research evidence page is produced
- **WHEN** the system extracts company, industry, product, valuation, risk, or brokerage-view knowledge from sources
- **THEN** it writes the knowledge into a human-readable evidence page and records the source, date, and reliability limitation for each important claim.

#### Scenario: New data conflicts with an existing evidence claim
- **WHEN** a new source conflicts with an existing evidence claim about EPS, target price, risk, industry narrative, or data recency
- **THEN** the system records the conflict in a contradiction log instead of silently overwriting the previous claim.

#### Scenario: Source is updated or stale
- **WHEN** a source document changes, its content hash changes, or key data exceeds the acceptable freshness window
- **THEN** the system marks derived claims as stale and lowers confidence or asks for an update in reports and evaluation.

#### Scenario: High-risk evidence update is proposed
- **WHEN** an evidence update changes valuation conclusions, risk level, investment thesis, or golden-sample evaluation criteria
- **THEN** the MVP requires human review before treating the update as accepted knowledge.

### Requirement: System uses an external brokerage report or public-source proxy as the golden sample
The system SHALL prefer an external brokerage research report as the first-version golden sample, but SHALL use a clearly labeled public-source proxy golden sample when no formal brokerage report is available.

#### Scenario: External brokerage report is available
- **WHEN** an external brokerage report is available as a reference
- **THEN** the system uses it to evaluate whether generated output has individual-stock research depth, valuation assumptions, risk disclosure, and investment thesis structure.

#### Scenario: External brokerage report is not available
- **WHEN** no usable external brokerage report is available
- **THEN** the system uses a public-source proxy golden sample for temporary evaluation and labels it as a proxy rather than a formal brokerage report.

#### Scenario: Public-source proxy golden sample is used
- **WHEN** the system builds a golden sample from CMoney summaries, news articles, FactSet consensus estimates, or official company financial data
- **THEN** each important number records the source, date, source type, and reliability limitation.
- **AND** the system must not invent undisclosed brokerage names, valuation models, or report details.

### Requirement: System answers the first Phison valuation research question
The system SHALL generate research output for whether the AI SSD growth story supports Phison's current valuation.

#### Scenario: User starts the default research question
- **WHEN** the user starts the default Phison research task
- **THEN** the system analyzes the AI SSD growth narrative, financial data, valuation assumptions, risks, and opposing views.

#### Scenario: Growth story and valuation evidence conflict
- **WHEN** the fundamental agent and risk agent disagree about valuation support
- **THEN** the system surfaces the disagreement and identifies which assumptions most affect the conclusion.

### Requirement: System clarifies investment research intent
The system SHALL classify each user request before invoking retrieval or specialist agents.

#### Scenario: User asks a simple concept question
- **WHEN** the user asks a general investing concept question such as "什麼是 DCA?"
- **THEN** the system answers directly with a concise explanation and does not run the full multi-agent pipeline.

#### Scenario: User asks for cross-source investment analysis
- **WHEN** the user asks for a company, ETF, fund, sector, or portfolio analysis
- **THEN** the system routes the request to relevant specialist agents and records the selected route.

#### Scenario: User asks for unsafe or over-specific advice
- **WHEN** the user asks for a guaranteed return, exact buy/sell instruction, or legally sensitive advice
- **THEN** the system refuses or reframes the request as research support with risk disclosure.

### Requirement: System separates investment schools into specialist agents
The system SHALL model different investment perspectives as separate agents so their assumptions can be compared.

#### Scenario: Fundamental analysis is needed
- **WHEN** the query requires company quality, earnings, valuation, PE ratio, or business model analysis
- **THEN** the Fundamental Agent produces a source-backed view with assumptions and uncertainties.

#### Scenario: Technical analysis is needed
- **WHEN** the query requires price trend, volume, momentum, or technical indicators
- **THEN** the Technical Agent produces a view based on quantitative market signals and does not pretend to evaluate business quality.

#### Scenario: Macro or sector context is needed
- **WHEN** the query depends on interest rates, inflation, industry cycle, supply chain, or policy context
- **THEN** the Macro / Sector Agent produces a contextual view and marks which claims are data-backed versus inferred.

#### Scenario: Conflicting views exist
- **WHEN** agents disagree
- **THEN** the system surfaces the disagreement instead of forcing a single confident answer.

### Requirement: System transforms dashboard-style indicators into synthesized AI research reports
The system SHALL treat dashboard-style financial metrics as inputs and benchmarks, not as the final user experience.

#### Scenario: User requests complete single-stock analysis
- **WHEN** the user asks for an analysis of a Taiwan stock
- **THEN** the system integrates news, fundamentals, growth, profitability, safety, valuation, technical, chip, and risk perspectives.
- **AND** the output is a research report rather than scattered metrics that the user must interpret manually.

#### Scenario: Dashboard indicators conflict
- **WHEN** different perspectives conflict, such as revenue growth with expensive valuation, improving chip signals without confirmed earnings, or low valuation with deteriorating cash flow
- **THEN** the system explicitly lists the conflict, possible explanations, missing sources, and the assumptions that most affect the conclusion.

#### Scenario: Stock health-check data is unavailable
- **WHEN** a health-check item requires data that is unavailable, paywalled, login-gated, or not verified from public sources
- **THEN** the system marks the item as `unknown`, `not available`, or `needs source` instead of pretending the check was completed.

#### Scenario: Report completeness is evaluated
- **WHEN** the report generator completes a single-stock research report
- **THEN** the evaluation agent checks whether it covers thesis, latest changes, stock health-check summary, fundamentals, growth quality, valuation, technical and chip signals, opposing views, data gaps, tracking indicators, sources, and confidence.

### Requirement: System produces conservative stock health-check summaries
The system SHALL convert the seven StatementDog-style stock health-check perspectives into auditable health-check outputs using only sources available to the current deterministic MVP.

#### Scenario: Health-check output is produced
- **WHEN** the default Phison research run is generated
- **THEN** the run includes a `health_check_agent` trace step.
- **AND** `analysis.health_checks.checks` contains exactly seven checks: landmine risk, dividend income, growth stock, value stock, chip signal, quality stock, and turnaround stock.
- **AND** each check includes a stable ID, display name, status, status reason, criteria, source IDs, missing data, report takeaway, and data policy.

#### Scenario: Health-check status is serialized
- **WHEN** a health-check item is returned through the API or used in the report
- **THEN** its status is one of `pass`, `fail`, `unknown`, or `not_available`.
- **AND** the system uses `unknown` only when the data may be obtainable but is currently insufficient.
- **AND** the system uses `not_available` only when the data requires login, paid access, an external data source, or a capability outside the current MVP boundary.

#### Scenario: Current public fixtures are insufficient for a check
- **WHEN** the available public fixture does not contain enough data to determine whether a health check passes or fails
- **THEN** the system marks the check as `unknown`.
- **AND** the system lists the missing data needed to make the check decision.
- **AND** the system does not infer a bullish, bearish, pass, or fail conclusion from incomplete data.

#### Scenario: Chip data requires unavailable sources
- **WHEN** chip-related checks require broker trading, major shareholder, director holding, pledged share, or shareholder-count data that is not present in the local fixture
- **THEN** the system marks the chip signal check as `not_available`.
- **AND** the system explains that the current MVP does not include the required source or permission.

#### Scenario: Partial growth evidence exists
- **WHEN** the fixture contains revenue or EPS evidence related to growth but lacks the full StatementDog-style growth-check criteria
- **THEN** the system may attach the relevant source IDs to the growth stock check.
- **AND** the system still marks the check as `unknown` unless all required criteria can be evaluated.

#### Scenario: Health-check summary is added to the report
- **WHEN** the report generator creates the research report
- **THEN** the report includes a stock health-check summary with all seven check names, statuses, conservative takeaways, and key missing data.
- **AND** the report clearly states that the health-check section is based on local public fixtures, not StatementDog login-gated or paid data.

#### Scenario: Health-check output is shown in the web app
- **WHEN** the web application displays a completed run
- **THEN** it provides a Health view that shows each health-check status, reason, missing data, and source IDs.
- **AND** `unknown` and `not_available` are visually distinguishable from `pass` and `fail`.

#### Scenario: Health-check claims are evaluated
- **WHEN** the evaluation agent reviews a report that includes health-check content
- **THEN** it checks whether all seven checks are present and whether missing data is explicitly represented.
- **AND** it lowers the score or marks the report as needing revision when the health-check summary is missing or incomplete.

#### Scenario: Health-check hallucination is detected
- **WHEN** the report claims that `unknown` or `not_available` checks passed, failed, or were fully verified
- **THEN** the evaluation agent treats that as a hard failure.
- **AND** the evaluation agent also treats it as a hard failure when the report claims to use StatementDog paid, login-gated, or unavailable data that is not present in the fixture.

### Requirement: System expands fundamental analysis into a financial quality snapshot
The system SHALL expand the Fundamental Agent beyond EPS and Forward P/E scenarios into a structured financial quality snapshot covering revenue, profitability, safety, growth, and cash-flow quality.

#### Scenario: Fundamental snapshot is produced
- **WHEN** the default Phison research run is generated
- **THEN** `analysis.fundamentals` preserves the existing `valuation_scenarios`.
- **AND** `analysis.fundamentals` also includes `summary`, `categories`, `key_findings`, and `data_gaps`.
- **AND** `analysis.fundamentals.categories` contains exactly five categories: revenue, profitability, safety, growth, and cash-flow quality.

#### Scenario: Fundamental metric coverage is serialized
- **WHEN** a fundamental category or metric is returned through the API or used in the report
- **THEN** its coverage status is one of `available`, `partial`, `missing`, or `not_available`.
- **AND** the system uses `available` only when the fixture contains enough data and source IDs for that metric.
- **AND** the system uses `partial` when there is directional evidence but not enough data for full trend or quality judgment.
- **AND** the system uses `missing` when the data should be obtainable from public financial sources but is not yet in the fixture.
- **AND** the system uses `not_available` only when the data requires unavailable external permissions, paid data, or a capability outside the current MVP boundary.

#### Scenario: Revenue evidence exists
- **WHEN** the fixture contains official or news-based monthly revenue evidence
- **THEN** the revenue category may be marked `partial` or `available` depending on whether the required sequence is complete.
- **AND** the system records source IDs, period, unit, interpretation, and missing trend data.

#### Scenario: Profitability evidence is incomplete
- **WHEN** the fixture contains EPS evidence but lacks gross margin, operating margin, net margin, ROE, or ROA
- **THEN** the profitability category is marked `partial`.
- **AND** the system does not claim broad profitability improvement from EPS alone.

#### Scenario: Safety and cash-flow data are missing
- **WHEN** the fixture lacks balance-sheet ratios, debt metrics, operating cash flow, free cash flow, OCF-to-net-income, inventory turnover, or receivable turnover
- **THEN** the safety and cash-flow quality categories are marked `missing`.
- **AND** the system lists the missing data needed for future evaluation.

#### Scenario: Growth evidence is partial
- **WHEN** the fixture contains revenue or EPS growth clues but lacks full monthly revenue YoY sequence and profit-growth metrics
- **THEN** the growth category is marked `partial`.
- **AND** the system explains which growth claims are source-backed and which remain unverified.

#### Scenario: Fundamental report section is generated
- **WHEN** the report generator creates the research report
- **THEN** it includes a fundamental breakdown covering all five categories, their coverage statuses, source-backed takeaways, and data gaps.
- **AND** it separates EPS / Forward P/E valuation sensitivity from broader business quality.

#### Scenario: Fundamental overclaim is detected
- **WHEN** the report claims that missing or partial metrics are fully verified
- **THEN** the evaluation agent treats that as a hard failure or marks the report as needing revision.
- **AND** the evaluation agent also penalizes reports that annualize Q1 EPS as a full-year forecast without warning.

### Requirement: System separates valuation analysis from fundamental quality
The system SHALL add a Valuation Agent that produces a structured valuation snapshot without treating valuation multiples, target prices, or broker summaries as proof of business quality or buy-worthiness.

#### Scenario: Valuation snapshot is produced
- **WHEN** the default Phison research run is generated
- **THEN** `analysis.valuation` includes `summary`, `scenarios`, `multiples`, `broker_targets`, `data_gaps`, and `interpretation`.
- **AND** existing `analysis.fundamentals.valuation_scenarios` remains available for backward compatibility until the UI and report are migrated.
- **AND** the Valuation Agent records the price date and whether the price is fixture-based or live market data.

#### Scenario: Valuation coverage is explicit
- **WHEN** a valuation metric is returned through the API or used in the report
- **THEN** its coverage status is one of `available`, `partial`, `missing`, or `not_available`.
- **AND** Forward P/E from EPS assumptions may be marked `partial` when it lacks historical P/E distribution, peer comparison, or multi-year earnings validation.
- **AND** P/B and dividend-yield checks are marked `missing` unless the fixture contains source-backed values.

#### Scenario: Broker targets are source-backed assumptions
- **WHEN** broker target prices or target-price ranges are shown
- **THEN** the system records source IDs, publication dates, target price, broker or source label when available, and reliability notes.
- **AND** CMoney or news summaries are labeled as summaries rather than full brokerage reports.
- **AND** the system does not invent undisclosed broker names or model details.

#### Scenario: Scenario sensitivity is reported
- **WHEN** EPS, price, or target-price assumptions differ across sources
- **THEN** the Valuation Agent reports a scenario matrix that separates conservative, base, and optimistic assumptions.
- **AND** it explains which assumptions would need to be true for the AI SSD growth story to support the current valuation.

#### Scenario: Valuation overclaim is detected
- **WHEN** the report treats a single target price, Forward P/E, or upside percentage as fair-value proof, a buy recommendation, or proof that the stock is cheap
- **THEN** the evaluation agent treats that as a hard failure or marks the report as needing revision.
- **AND** if price data is fixture-based or stale, the report must state the price date and avoid live-price language.

### Requirement: System uses traceable data sources
The system SHALL attach source references to claims that come from retrieved documents or external data.

#### Scenario: News data is used
- **WHEN** the system summarizes news
- **THEN** it includes publication source, date, title, and a short explanation of relevance.

#### Scenario: Financial statement data is used
- **WHEN** the system uses financial metrics
- **THEN** it records the metric name, period, source document, and whether the value is raw data or model-derived.

#### Scenario: Source quality is insufficient
- **WHEN** available sources are stale, thin, contradictory, or low quality
- **THEN** the system lowers confidence and asks for additional data or narrows the conclusion.

### Requirement: System controls cost and latency
The system SHALL avoid running expensive retrieval and agent pipelines when a cheaper path is sufficient.

#### Scenario: Similar question exists
- **WHEN** a new request is semantically similar to a prior evaluated request
- **THEN** the system reuses or adapts the cached answer path before launching a full pipeline.

#### Scenario: Full pipeline is required
- **WHEN** the request requires fresh multi-source analysis
- **THEN** the system records which agents ran, approximate token usage, latency, and cache hits.

### Requirement: System evaluates every research output
The system SHALL evaluate generated reports before presenting them as final.

#### Scenario: Report is generated
- **WHEN** the Report Generator produces an investment research summary
- **THEN** the Evaluation Agent scores it against a rubric covering source grounding, logical consistency, risk coverage, uncertainty, and user usefulness.

#### Scenario: Evaluation score is too low
- **WHEN** the evaluation score is below 4.0 out of 5
- **THEN** the system must revise the report, ask for more data, or explicitly label the output as low confidence.

#### Scenario: Golden set is available
- **WHEN** a benchmark report or manually curated answer exists
- **THEN** the system compares the generated output against the golden set and records score differences.

### Requirement: System preserves human decision responsibility
The system SHALL make clear that outputs are decision-support research, not autonomous financial advice.

#### Scenario: Final answer includes an investment view
- **WHEN** the system outputs a bullish, bearish, or neutral view
- **THEN** it includes assumptions, risks, confidence level, and a reminder that the user remains responsible for decisions.

#### Scenario: User requests action execution
- **WHEN** the user asks the system to place trades or rebalance assets
- **THEN** the MVP refuses and explains that execution is out of scope.

### Requirement: Project provides AIASE final-project deliverables
The project SHALL prepare the documentation and presentation artifacts needed for AIASE final-project grading in addition to the runnable product.

#### Scenario: GitHub source is submitted
- **WHEN** the project is prepared for GitHub Classroom or the course submission platform
- **THEN** the repository includes a reproducible README, environment variable example, frontend and backend source, local fixtures, and verification commands.

#### Scenario: Technical report is written
- **WHEN** the technical report is produced
- **THEN** it explains the user problem, quality-of-life value, system architecture, agent workflow, data sources, API design, evaluation, limitations, and future work.

#### Scenario: Architecture and flow diagrams are prepared
- **WHEN** course demo or technical report materials are prepared
- **THEN** the project includes a system architecture diagram, service flow diagram, and agent workflow diagram showing frontend, backend, data layer, research evidence pack, agents, and evaluation.

#### Scenario: Demo slides are prepared
- **WHEN** demo presentation slides are produced
- **THEN** they explain the problem, user, core AI workflow, Evidence Pack knowledge layer, agent trace, demo path, risks, limitations, and next steps.

#### Scenario: External services are unavailable
- **WHEN** external APIs, model services, or network access are unavailable during evaluation
- **THEN** the project can still demonstrate the main happy path using local fixtures and deterministic agents.
