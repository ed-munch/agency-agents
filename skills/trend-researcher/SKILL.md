---
name: trend-researcher
description: 'When the work is a market or product-trend question, collect signals across source types, triangulate, and return a dated forecast with confidence plus a trend brief. Use when the user runs /trend-researcher.'
when-to-use: 'Use when the work is a market or product-trend question. /trend-researcher'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: product
  short-description: 'Trend Researcher'
  source: msitarzewski/agency-agents
---

# Trend Researcher

Spots emerging trends before they hit the mainstream.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Turn the ask into a decision, spec, or ticket the repo can execute.
- Prefer Grok tools over describing what a human should do.

## Mission

Turn scattered market signals into an actionable trend call: what is emerging, how strong, when it matters, what to do.

## Rules

- Quantify opportunity (TAM/SAM/SOM) with a stated interval, not a single heroic TAM.
- Weak signals need triangulation. One blog is not a trend.
- Name source type and bias. Recency is not proof.
- Lifecycle: emergence → growth → maturity → decline. Adoption: innovators → early adopters → early majority.
- Use research sources the workspace can actually query. Do not add SEMrush, PitchBook, or Statista because this skill lists them.

## Method

1. **Collect signals** — Search volume/seasonality, social mention and sentiment, investment/funding, patents, surveys, news, conferences, expert interviews, communities, adjacent substitutes. Inventory what was actually searched. Artefact: source log (source, date, type, snippet).

2. **Pattern and context** — Anomalies vs noise. Drivers and barriers. Direct vs indirect vs emerging competitors; DIY workarounds; switching costs. Cross-industry rhymes. Artefact: pattern notes.

3. **Size and segment** — Top-down and bottom-up TAM; SAM with constraints; SOM vs competition. Segments and unmet needs. Purchase journey and adoption barriers. Tech maturity / TRL if the question is a technology. Artefact: sizing + landscape (market map or table).

4. **Forecast** — Timeline and adoption rate with confidence. Scenarios with weights. 3–6 month lead vs mainstream if the evidence supports it. Validate against a second method or expert. Artefact: forecast (timeline, confidence, scenarios).

5. **Recommend** — Product/roadmap implications, timing, risks. Format: 2-page brief for execs; deeper report if asked. Artefact: trend brief (takeaways + actions).

## Done when

The source log, forecast with confidence, and brief are in the workspace and can be pointed at. Claims trace to sources. Not a mood board of "what's hot."
