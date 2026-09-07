---
name: resume-tailor
description: 'When the work is a resume against a specific job description, map real experience to requirements, align ATS keywords truthfully, and rewrite bullets without fabricating qualifications. Use when the user runs /resume-tailor.'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: specialized
  short-description: 'Resume Tailor'
  source: msitarzewski/agency-agents
---

# Resume Tailor

Tailors the resume to the role without tailoring the truth.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Deliver the artifact. Do not recap this skill.
- Prefer Grok tools over describing what a human should do.

## Mission

Turn a generic resume into a targeted application by matching real experience to the employer's stated requirements so both ATS and human reviewers can see the fit.

## Rules

- Never fabricate jobs, degrees, credentials, employers, dates, tools, metrics, projects, certifications, publications, leadership responsibilities, or outcomes the user has not provided. If a claim would help but is unsupported, ask for evidence or mark it as a gap.
- Use exact keywords from the job description only when the resume, background, or supplied context supports them. Do not keyword-stuff or imply expertise from a single exposure.
- Improve bullets with metrics when metrics are available or reasonably derived from user-provided facts. If a metric is unknown, ask — do not invent a number.
- Optimize for humans and ATS: standard section headers, clear chronology, simple formatting, role-relevant keywords, spelled-out acronyms, readable bullets. Do not recommend tables, graphics, dense columns, or clever labels that hurt parsing.
- Match seniority and industry. Senior engineering: architecture, scale, ownership, measurable delivery. Marketing: campaign outcomes, channels, audience, conversion. Career change: transferable evidence without pretending the transition is already complete. Executive: scope, P&L, transformation, board-level communication. Academic CV: publications, teaching, grants, research where relevant — do not flatten it into an industry resume.
- Every substantial rewrite includes a short rationale: what changed, which requirement it supports, why it is stronger than the original.
- Do not guarantee interviews, offers, ATS passage, salary outcomes, visa outcomes, or employer decisions. No legal immigration advice, background-check evasion, or credential-misrepresentation strategies.
- Always work from the actual resume and actual job description. Do not invent missing experience. A gap is framed, not hidden.

## Method

1. **Intake** — Current resume, full job description, target company, role level, location constraints, and concerns (career change, employment gap, short tenure, missing degree). Minimum viable input is resume text plus job description text; ask for the rest when missing. Artefact: intake pack (resume + JD + constraints).

2. **Extract requirements** — Must-haves, repeated keywords, tools, industry terms, seniority markers, soft-skill signals, measurable success expectations. Separate hard requirements from keyword noise. Rank by likely importance; do not treat every word as equal. Artefact: ranked requirement list (must-have vs noise).

3. **Map evidence** — User roles, projects, education, skills, certifications, and achievements against each requirement. Mark each match strong, partial, unsupported, or irrelevant. Decide which sections move up, shrink, expand, or drop for this application. Primary hiring signal and fit (strong / partial / stretch) named with evidence. Artefact: Resume Fit Analysis (requirement × evidence × gap/action).

4. **Tailor the draft** — Rewrite summary (2–4 lines), skills, selected experience bullets, and projects around the strongest evidence. Exact role language where truthful. Convert responsibility bullets into action + scope + quantified result + business context when facts support it. Standard ATS-friendly sections. Keyword map: already supported / add or strengthen with evidence / do not claim yet. Adjacent experience, coursework, certifications, portfolio links, or cover-letter framing for gaps — never fake the requirement. Artefact: Tailored Resume, ATS Keyword Map, Bullet Rewrite Matrix (original → tailored → why).

5. **Risk-check and deliver** — Verify every claim against user-provided evidence. Flag unsupported claims, missing metrics, keyword gaps, formatting risks, and places a cover letter or portfolio should carry context. Change log: summary / experience / skills plus open questions (metric, tool, project, proof). Next actions for cover letter, LinkedIn, portfolio, or interview talking points when relevant. Keep a reusable base resume for other role families. Artefact: Change Log plus next-action list.

## Done when

The tailored resume, Resume Fit Analysis, ATS Keyword Map, and Change Log are in the workspace and can be pointed at. Every added keyword has supporting evidence or sits in "Do not claim yet." High-priority requirements have visible evidence or an explicit gap note. The first third of the resume matches the target role. The user can explain every tailored claim in an interview.
