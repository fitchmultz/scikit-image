# Acme SDK Accelerator

Portable Cursor plugin for governed SDK changes: request → plan → build → review → test → deploy (CI handoff).

## Contents

- `rules/` — persistent repo conventions and approval boundaries
- `skills/` — scoped change workflow for Cursor Agent
- `agents/` — verifier Agent for readiness review
- `hooks/` — approved-root guard for agent-loop boundaries
- `skills/scikit-image-change-workflow/scripts/` — change-brief renderer for PM/QA/DevOps/CI handoff
- `.cursor-plugin/plugin.json` — plugin manifest

## Install (bundled in this repository)

This plugin is committed at `.cursor/plugins/acme-sdk-accelerator/` and loads
automatically for everyone who opens this repository in a trusted Cursor
workspace. Loading is wired through the project-level `workspaceOpen` hook in
`.cursor/hooks.json`, which returns this plugin's absolute path via `pluginPaths`
(see https://cursor.com/docs/hooks). No per-user copy or manual setup is needed;
restart Cursor if it was open before the plugin was added.

All internal paths are portable: `hooks/hooks.json` resolves the guard script via
the always-present `$CURSOR_PROJECT_DIR` environment variable, so the plugin works
from any checkout location without rewriting placeholders.

> Note: `workspaceOpen` is an IDE lifecycle hook and does not apply to cloud
> agents, so cloud-agent runs will not auto-load the plugin via this mechanism.

## Customer ownership

| Owner | Role |
| --- | --- |
| Maya Chen | Technical champion / plugin owner |
| David Park | Primary champion candidate / operational sponsor |
| Nina Alvarez | QA gates |
| Marcus Webb | CI/CD guardrails |
| Priya Nair | Executive renewal target |

## Interaction model

The intended user surface is plain English. The Agent Skill decides when to run for scoped SDK changes, then applies the request → plan → build → review → test → deploy (CI handoff) workflow. The verifier Agent and change-brief renderer are internal controls, not commands a customer has to memorize.

## References

- https://cursor.com/docs/plugins
- https://cursor.com/docs/reference/plugins
