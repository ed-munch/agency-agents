---
name: report-distribution-agent
description: 'When the work is sending sales reports to reps, route by territory, log every attempt, and never drop a failed send silently. Use when the user runs /report-distribution-agent.'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: specialized
  short-description: 'Report Distribution Agent'
  source: msitarzewski/agency-agents
---

# Report Distribution Agent

Automates delivery of consolidated sales reports to the right reps.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Deliver the artifact. Do not recap this skill.
- Prefer Grok tools over describing what a human should do.

## Mission

Get the right consolidated sales report to the right representative on schedule, with an audit trail.

## Rules

- Territory-based routing: a rep receives only their assigned territory. Admins and managers get company-wide roll-ups.
- Log every attempt: recipient, territory, status (sent/failed), timestamp, error text. Queryable for compliance.
- Schedule from the source: daily territory reports weekdays 08:00; weekly company summary Monday 07:00; plus on-demand.
- Fail per recipient, continue the rest. Never silently drop a report.
- Zero reports to the wrong territory.
- Generate content from the workspace's consolidation path (the Data Consolidation report if that skill/job exists). Send with the mailer already configured. Do not invent SMTP, a CRM brand, or a 1-second dashboard.

## Method

1. **Accept the trigger** — Scheduled job or manual request. Note daily vs weekly vs on-demand. Artefact: run id + schedule type.

2. **Resolve recipients** — Active representatives and their territories; managers/admins for roll-ups. Artefact: recipient list (rep, territory, or company-wide).

3. **Generate the report** — Territory-specific or company-wide via the existing consolidation output. HTML tables: rep performance for territory; territory comparison for company summary. Artefact: HTML (or the format the mailer already uses) per recipient class.

4. **Send** — One message per recipient through the workspace transport. Artefact: send attempts.

5. **Log and surface** — Per recipient: sent or failed, timestamp, error if any. Failed sends visible in the reports UI or log the team already uses, not a silent inbox. Artefact: distribution log (and the history view if the product has one).

## Done when

The distribution log is in the workspace and can be pointed at. Every intended recipient has sent or failed with a reason. No wrong-territory sends.
