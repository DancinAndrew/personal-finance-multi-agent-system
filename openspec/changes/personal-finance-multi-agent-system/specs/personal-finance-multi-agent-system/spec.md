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

### Requirement: System provides an LLMWiki-lite research knowledge layer
The system SHALL organize raw sources into a human-readable, linkable, and auditable research wiki layer between retrieval and agent analysis.

#### Scenario: Raw source is read
- **WHEN** the system reads news, financial reports, CMoney summaries, FactSet consensus estimates, official company data, or user notes
- **THEN** it preserves the raw source record and must not overwrite the original text or treat summaries as primary source data.

#### Scenario: Research wiki page is produced
- **WHEN** the system extracts company, industry, product, valuation, risk, or brokerage-view knowledge from sources
- **THEN** it writes the knowledge into a human-readable wiki page and records the source, date, and reliability limitation for each important claim.

#### Scenario: New data conflicts with an existing wiki claim
- **WHEN** a new source conflicts with an existing wiki claim about EPS, target price, risk, industry narrative, or data recency
- **THEN** the system records the conflict in a contradiction log instead of silently overwriting the previous claim.

#### Scenario: Source is updated or stale
- **WHEN** a source document changes, its content hash changes, or key data exceeds the acceptable freshness window
- **THEN** the system marks derived claims as stale and lowers confidence or asks for an update in reports and evaluation.

#### Scenario: High-risk wiki update is proposed
- **WHEN** a wiki update changes valuation conclusions, risk level, investment thesis, or golden-sample evaluation criteria
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
- **THEN** the project includes a system architecture diagram, service flow diagram, and agent workflow diagram showing frontend, backend, data layer, research wiki, agents, and evaluation.

#### Scenario: Demo slides are prepared
- **WHEN** demo presentation slides are produced
- **THEN** they explain the problem, user, core AI workflow, LLMWiki-lite knowledge layer, agent trace, demo path, risks, limitations, and next steps.

#### Scenario: External services are unavailable
- **WHEN** external APIs, model services, or network access are unavailable during evaluation
- **THEN** the project can still demonstrate the main happy path using local fixtures and deterministic agents.
