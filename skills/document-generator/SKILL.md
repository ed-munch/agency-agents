---
name: document-generator
description: 'When a professional PDF, PPTX, DOCX, or XLSX needs to be generated from data, pick the format, write a reusable generation script, and produce the file. Use when the user runs /document-generator.'
when-to-use: 'Use when the user needs a professional PDF, PPTX, DOCX, or XLSX generated from data. /document-generator'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: specialized
  short-description: 'Document Generator'
  source: msitarzewski/agency-agents
---

# Document Generator

Professional documents from code — PDFs, slides, spreadsheets, and reports.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Deliver the artifact. Do not recap this skill.
- Prefer Grok tools over describing what a human should do.

## Mission

Generate professional documents programmatically — PDFs, presentations, spreadsheets, and Word documents — using the right code-based tool for each format.

## Rules

- Use document styles and themes, never hardcoded fonts/sizes.
- Branding matches the guidelines in the workspace if they exist.
- Data-driven: data in, file out. Reusable template functions, not a one-off script.
- Accessible: alt text, heading hierarchy, tagged PDF when the format is PDF.
- Provide the generation script AND the output file.
- Use a generator **already installed** in the workspace (Python or Node library already in the lockfile). If none can produce the chosen format, STOP. Do not add reportlab, puppeteer, python-pptx, or docx because this skill names them.

## Method

1. **Lock audience, purpose, and format** — PDF, PPTX, XLSX, or DOCX. Artefact: audience + purpose + format choice.

2. **Pick the installed generator** — From the lockfile / imports already in the repo, the library that can emit that format. Artefact: tool + approach notes.

3. **Build reusable templates** — Functions, styles/themes, brand tokens if present. Artefact: template functions.

4. **Generate from data** — Input data → output file. Artefact: output file.

5. **Deliver script and file** — Generation script plus the file, plus how to customize. Artefact: generation script + output file + formatting notes.

## Done when

The format choice, templates, script, and output file can be pointed at. Not a one-off script with hardcoded fonts, and not a new PDF stack added to a repo that had none.
