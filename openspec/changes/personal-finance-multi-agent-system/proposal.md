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
- Defer implementation design and task breakdown until the SPEC is reviewed.

## Capabilities

### New Capabilities

- `personal-finance-multi-agent-system`: Defines the behavior of a decision-support research system for Taiwan equity investing, including routing, specialist agents, source grounding, evaluation, and safety boundaries.

### Modified Capabilities

None.

## Impact

- New OpenSpec change: `personal-finance-multi-agent-system`
- New discussion artifact: `SPEC.md`
- No runtime dependency, data source, API, or framework decision is made in this proposal.
