## Why

The project needs a clear spec-first path for a multi-agent personal investment and finance research system, grounded in the Chris mentorship note. The first goal is to define testable behavior before choosing frameworks, data stores, UI, or deployment.

## What Changes

- Add a new capability for a multi-agent investment research system.
- Define the MVP behavior for intent routing, specialist agents, traceable retrieval, cost / latency control, evaluation, and human decision boundaries.
- Scope the first MVP to Taiwan equities instead of broad global investing or portfolio management.
- Use Phison Electronics (8299) as the first seed target, grounded in the user's existing Obsidian research note.
- Make the MVP a demoable web application.
- Show an observable agent execution trace in the web application.
- Store only summaries and sources for first-version agent traces, not full intermediate outputs.
- Use news and financial reports as the first primary data sources.
- Start with a manually curated dataset, with crawlers or Exa API as future extensions.
- Add an LLMWiki-lite research knowledge layer so raw sources can be compiled into human-readable, linkable, provenance-backed wiki pages before agent analysis.
- Set the initial evaluation pass threshold to 4.0 / 5.
- Prefer an external brokerage research report as the primary golden sample, but start with a clearly labeled public-source proxy golden sample when the user does not have broker access.
- Use "whether the AI SSD growth story supports Phison's current valuation" as the first research question.
- Add StatementDog-style dashboard and stock health-check benchmarking as a product reference, while requiring the system to synthesize scattered indicators into an AI research report instead of leaving users to inspect dashboards manually.
- Add a second-phase minimum slice for a conservative Health Check Agent that converts the seven StatementDog-style stock health-check perspectives into auditable `pass`, `fail`, `unknown`, or `not_available` outputs.
- Require the Health Check Agent to mark missing, paywalled, login-gated, or unverified data as gaps instead of fabricating completed checks.
- Keep the second-phase slice local and deterministic: no Supabase, real LLM, crawler, Exa API, live market data, StatementDog login, or paid data dependency.
- Add the next second-phase slice for a deeper Fundamental Agent that turns revenue, profitability, safety, growth, and cash-flow quality metrics into a structured financial snapshot with explicit source coverage and missing-data gaps.
- Preserve the existing EPS / Forward P/E scenarios while separating them from broader fundamental quality analysis so valuation sensitivity does not pretend to cover full business quality.

## Capabilities

### New Capabilities

- `personal-finance-multi-agent-system`: Defines the behavior of a decision-support research system for Taiwan equity investing, including routing, specialist agents, source grounding, evaluation, and safety boundaries.
- `stock-health-check-agent`: Defines conservative stock health-check behavior for seven investment lenses, including explicit data-gap handling and integration into the report, trace, and evaluation workflow.
- `fundamental-analysis-agent`: Defines deterministic fundamental-analysis behavior for revenue, profitability, safety, growth, and cash-flow quality, including metric coverage status and report integration.

### Modified Capabilities

None.

## Impact

- New OpenSpec change: `personal-finance-multi-agent-system`
- New discussion artifact: `SPEC.md`
- No runtime dependency, data source, API, or framework decision is made in this proposal.
