# Acme SDK Accelerator

Portable Cursor plugin for governed SDK changes: request → plan → build → review → test → deploy (CI handoff).

## Contents

- `rules/` — persistent repo conventions and approval boundaries
- `skills/` — scoped change workflow for Cursor Agent
- `agents/` — verifier Agent for readiness review
- `hooks/` — approved-root guard for agent-loop boundaries
- `skills/scikit-image-change-workflow/scripts/` — change-brief renderer for PM/QA/DevOps/CI handoff
- `.cursor-plugin/plugin.json` — plugin manifest

## Install (local pilot)

```bash
cp -R /path/to/acme-sdk-accelerator ~/.cursor/plugins/local/acme-sdk-accelerator
```

Replace `__ACME_PLUGIN_ROOT__` in `hooks/hooks.json` and the renderer example in `skills/scikit-image-change-workflow/SKILL.md` with the installed plugin path, then restart Cursor.

This repository's `tools/install-local-plugin.sh` performs the copy and rewrite automatically.

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
