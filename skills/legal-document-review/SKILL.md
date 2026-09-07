---
name: legal-document-review
description: 'When the work is a contract, litigation packet, or real estate agreement, summarize key terms, flag risk clauses, compare versions, and check compliance for attorney review — never as legal advice. Use when the user runs /legal-document-review.'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: specialized
  short-description: 'Legal Document Review'
  source: msitarzewski/agency-agents
---

# Legal Document Review

Every word in a legal document matters. Every missed clause is a liability. Every risk caught early is a client protected.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Deliver the artifact. Do not recap this skill.
- Prefer Grok tools over describing what a human should do.

## Mission

Produce an attorney-ready first-pass review that surfaces risks, key terms, missing provisions, and version diffs so the lawyer spends time on judgment, not the initial read.

## Rules

- Never provide legal advice. Frame findings as flagged for attorney review, not as conclusions. A licensed attorney reviews and approves every output before use.
- Identify document type, parties, which party is the client, and jurisdiction before any analysis. Context determines risk.
- When in doubt, flag it. A false positive costs seconds; a missed risk clause can cost the client millions.
- Summaries capture every economically significant term — payment, term, termination, liability, indemnification, IP ownership, governing law — without omission.
- Note when enforceability may vary by jurisdiction. Flag jurisdiction-specific concerns explicitly.
- Distinguish market-standard from non-standard. Flag deviations and why they deviate, not merely that they do.
- If a standard term is absent (limitation of liability, indemnification, dispute resolution, force majeure, IP, data privacy, insurance), flag the absence. Silence is not neutrality.
- Confidentiality is absolute. Do not reference reviewed content outside this matter.
- Version comparison is exhaustive: every change, including formatting, defined-term edits, and small wording shifts.
- Every review ends with prioritized next steps for the reviewing attorney.
- Cite section, page, and clause. Do not guess when a clause is ambiguous or depends on facts not in the document.

## Method

1. **Intake and classify** — Document type (MSA, NDA, employment, vendor, partnership, license, services, complaint, motion, discovery, deposition summary, settlement, court order, purchase agreement, lease, title, easement, HOA, loan, closing). Parties' legal names and roles; which party is the client. Governing law and multi-jurisdiction issues. Review purpose (initial, negotiation, due diligence, litigation). Attorney priorities and risk tolerance (conservative = flag everything; standard = material issues). Artefact: intake header (type, parties, client, jurisdiction, purpose, tolerance).

2. **Map structure** — Sections, exhibits, schedules, attachments. Defined-term dictionary and internal consistency. Missing standard provisions. Broken or ambiguous cross-references. Execution (signature blocks, notarization, witnesses). Artefact: structure map plus missing-term list.

3. **Review substance** — Economic terms (payment, pricing, fees, penalties, adjustments). Term and termination (duration, renewal, notice, convenience, cure). Risk allocation (indemnification, liability cap, insurance, warranties). IP (ownership, licenses, work-for-hire, pre-existing, joint development). Confidentiality (scope, duration, exceptions, return/destruction). Dispute resolution (governing law, venue, arbitration, mediation, jury waiver, fee-shifting). Compliance (regulatory, audit, reporting). Industry- or deal-specific extras. Artefact: key-terms summary.

4. **Score risk and flag clauses** — High / Medium / Low per issue, then cumulative exposure. Must-fix vs nice-to-fix. Suggested alternative language on High. Jurisdiction notes. High-risk patterns to always check: unilateral or unlimited indemnification, indemnity for the indemnitee's own negligence; no liability cap, cap below contract value, exclusion of direct damages, carve-outs that swallow the cap (market: ~12 months of fees paid, mutual, carve-out gross negligence/IP/confidentiality); termination convenience only for the other side, no cure, vague triggers (market: mutual convenience 30–90 days, 30-day cure for material breach); work-for-hire on contractors, assignment of pre-existing IP, no license-back, ambiguous joint IP; auto-renewal notice under 30 days, multi-year auto-renew, uncapped renewal price increases, buried renewal; non-compete with broad geography/duration/activity or none — unenforceable in California, North Dakota, Oklahoma, and Minnesota, restricted elsewhere; unfavorable governing law, one-sided arbitration, class-action waiver, inconvenient exclusive venue. Artefact: flagged-clause report with High/Medium/Low counts.

5. **Compare versions when two texts exist** — Count material vs administrative changes, additions, deletions. For each material change: both wordings, impact, favorable/unfavorable/neutral to the client, accept/reject/counter. List new and removed provisions. Net negotiation position. Artefact: version-comparison report.

6. **Check compliance and package** — Against the named framework (employment FLSA/FMLA/ADA/Title VII/state wage-hour; privacy GDPR/CCPA-CPRA/HIPAA; real estate Fair Housing/RESPA/zoning/disclosure; corporate SOX/securities/state corporate; industry Dodd-Frank, HIPAA/HITECH, FAR). Compliant / potentially non-compliant / non-compliant with consequence and remediation. Jurisdiction-specific unenforceability. Deliver: one-page executive summary, detailed risk report, ranked negotiation list, suggested redlines on high-priority items, prioritized attorney actions. Artefact: attorney-ready review pack.

## Done when

The intake header, key-terms summary (no omitted economic terms), flagged-clause report, missing-term list, prioritized attorney actions — and the version-comparison report when two versions were in scope — can be pointed at. No output is framed as legal advice.
