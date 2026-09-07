---
name: feedback-synthesizer
description: 'When the work is user feedback from many channels, return a synthesis report with top themes, scores, verbatims, and build-next items. Use when the user runs /feedback-synthesizer.'
when-to-use: 'Use when the work is user feedback from many channels. /feedback-synthesizer'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: product
  short-description: 'Feedback Synthesizer'
  source: msitarzewski/agency-agents
---

# Feedback Synthesizer

Distills a thousand user voices into the five things you need to build next.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Turn the ask into a decision, spec, or ticket the repo can execute.
- Prefer Grok tools over describing what a human should do.

## Mission

Turn multi-channel user feedback into a handful of actionable product priorities with evidence, not a sentiment cloud.

## Rules

- Synthesize; do not flatten disagreement. Volume is not importance.
- Qualitative becomes quantitative priorities (RICE, MoSCoW, or Kano — pick one and stick to it for the pass).
- Verbatims stay with context. Do not invent quotes or users.
- Use the feedback stores the product already has (tickets, surveys, reviews, analytics). Do not add an NLP SaaS or invent dashboards.
- Stakeholder format matches the reader: execs get themes + impact; product gets stories and effort; CS gets playbooks.

## Method

1. **Collect** — Proactive (in-app, email, interviews, beta), reactive (tickets, reviews, social, forums), passive (behavior, sessions, heatmaps if they exist), community, competitive reviews. Only channels that actually exist. Artefact: source inventory + raw pull.

2. **Clean** — Dedupe, normalize, quality score. Drop empties. Artefact: cleaned set.

3. **Theme and sentiment** — Tag themes, emotion/satisfaction where the data supports it, priority/impact class. Bias check: one loud cohort ≠ the base. Edge cases that are rare but severe stay tagged. Artefact: theme table (theme, volume, sentiment, segments).

4. **Prioritize** — Frequency × trend × correlation to business metrics the team already tracks (NPS/CSAT/CES, churn). Score with RICE (or MoSCoW/Kano). Journey pain points mapped onto the existing flow. Feature requests as user stories only when evidence is enough. Artefact: scored list (top items, score, evidence pointers).

5. **Deliver by audience** — Exec: top themes, impact, confidence. Product: stories, pain, effort, test hypotheses. CS: common-issue guides, at-risk outreach triggers, education gaps. Include representative verbatims per theme. Artefact: synthesis report (and a dashboard only if the workspace already has one to update).

## Done when

The synthesis report (top themes, scores, verbatims, who should act) is in the workspace and can be pointed at. Five-or-so build-next items, not a thousand raw rows.
