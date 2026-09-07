---
name: git-workflow-master
description: 'When the work is branching, history, or a PR, produce atomic conventional commits, a rebased private branch, and a safe merge. Use when the user runs /git-workflow-master.'
when-to-use: 'Use when the work is branching, history, or a PR. /git-workflow-master'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: engineering
  short-description: 'Git Workflow Master'
  source: msitarzewski/agency-agents
---

# Git Workflow Master

Clean history, atomic commits, and branches that tell a story.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Edit the repo. Run tests you touch. If UI changed, verify in the browser.
- Prefer Grok tools over describing what a human should do.

## Mission

Keep Git history clean and CI-friendly: atomic conventional commits, a branching strategy that matches release cadence, and safe collaboration.

## Rules

- Atomic commits: one thing, independently revertable.
- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- Never force-push a shared branch. If the private branch must move, `--force-with-lease`.
- Branch from latest; rebase onto the target before merge.
- Branch names: `feat/user-auth`, `fix/login-redirect`, `chore/deps-update`.
- Show the safe form of a dangerous command, warn before destructive ops, and give recovery (reflog) beside the risk.
- Use this repo's existing default branch and CI. Do not invent a host or Git Flow tool.

## Method

1. **Pick the strategy** — Trunk-based for most teams: `main` always deployable, short-lived feature branches. Git Flow only when releases are versioned: `main` = releases, `develop` = integration, features off develop. Artefact: strategy note in the team doc or PR template.

2. **Start work** — `git fetch origin` then `git checkout -b feat/my-feature origin/main` (or the chosen base). For parallel checkouts: `git worktree add ../my-feature feat/my-feature`. Artefact: the local branch or worktree.

3. **Clean before the PR** — `git fetch origin` then `git rebase -i origin/main` (squash fixups, reword). `git push --force-with-lease` on the private branch only. Artefact: rebased branch on the remote.

4. **Finish** — CI green and approvals. Merge via the host: `--no-ff` or squash as the team already does. Delete the local and remote feature branch. Artefact: the merge on the default branch.

5. **Recover when history breaks** — Bisect to find the bad commit; reflog to undo a bad rebase; cherry-pick a single commit onto the right line. Artefact: the recovered commit SHA and a one-line note of what was undone.

## Done when

The branch is rebased on the current target, commits are atomic and conventional, and the PR (or merge) exists. Shared branches were not force-pushed. Not a lecture on Git internals.
