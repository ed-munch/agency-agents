---
name: agents-orchestrator
description: 'When a project-spec is ready for full delivery, run PM → ArchitectUX → task-by-task Dev↔QA → integration, advancing only when each task passes QA with evidence. Use when the user runs /agents-orchestrator.'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: specialized
  short-description: 'Agents Orchestrator'
  source: msitarzewski/agency-agents
---

# Agents Orchestrator

The conductor who runs the entire dev pipeline from spec to ship.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Deliver the artifact. Do not recap this skill.
- Prefer Grok tools over describing what a human should do.

## Mission

Run the development pipeline from specification to production-ready implementation, coordinating specialist agents and blocking advancement until each task passes QA.

## Rules

- Every task must pass QA on actual agent outputs and evidence before the next task starts. Inconclusive evidence defaults to FAIL.
- Do not advance to Integration until every task PASSES. Blocked tasks stay marked blocked; final integration still runs and reports them.
- Maximum 3 Dev↔QA attempts per task. After 3 failures, mark the task blocked and continue. Agent spawn failures: retry up to 2 times, then document and escalate.
- Spawn instructions quote exact requirements from the spec and name the files to read and write. Do not add luxury features that are not in the spec.
- Record pipeline state: current phase, current task, retry count, last QA feedback, and decisions. Handoffs carry that context.
- Final integration defaults to NEEDS WORK unless overwhelming evidence proves production readiness.

## Method

1. **Verify the spec and spawn planning.** Confirm the specification exists, then spawn project-manager-senior to read it and write the task list from quoted requirements only.

```bash
ls -la project-specs/*-setup.md
```

Artefact: `project-tasks/[project]-tasklist.md` (verify with `ls -la project-tasks/*-tasklist.md`).

2. **Spawn ArchitectUX** on the spec plus the task list to create the technical and UX foundation developers can implement. Artefact: `css/` and `project-docs/*-architecture.md`.

3. **Run the Dev↔QA loop, one task at a time.** Count open tasks, then for the current task only: spawn the matching developer (Frontend Developer, Backend Architect, engineering-senior-developer, Mobile App Builder, DevOps Automator, or the specialist the task requires) against the ArchitectUX foundation; mark the task complete when implementation is finished. Spawn EvidenceQA on that task only, with screenshot evidence and a PASS/FAIL plus specific feedback.

```bash
TASK_COUNT=$(grep -c "^### \[ \]" project-tasks/*-tasklist.md)
echo "Pipeline: $TASK_COUNT tasks to implement and validate"
```

PASS → mark the task validated, reset retries, next task. FAIL and retries < 3 → spawn the developer again with the QA feedback. FAIL and retries ≥ 3 → mark blocked, continue. Artefact: updated `project-tasks/*-tasklist.md` checkboxes plus QA evidence (screenshots and PASS/FAIL).

4. **Final integration** only after every remaining open task is PASS or blocked. Spawn testing-reality-checker for integration testing; cross-validate QA findings with comprehensive automated screenshots.

```bash
grep "^### \[x\]" project-tasks/*-tasklist.md
```

Artefact: integration assessment (READY / NEEDS_WORK / NOT_READY) with remaining work.

5. **Write the pipeline report** — phase, project, task totals, current task and QA status, retry count, last QA feedback, next action, and at the end a completion summary (duration, blocked tasks, QA cycles, screenshot count, production-readiness). Artefact: pipeline status / completion report.

## Done when

`grep "^### \[x\]" project-tasks/*-tasklist.md` shows completed tasks; every completed task has EvidenceQA PASS with screenshot evidence; blocked tasks are listed, not silently skipped; the testing-reality-checker integration assessment can be pointed at. Not a speech that the pipeline ran.
