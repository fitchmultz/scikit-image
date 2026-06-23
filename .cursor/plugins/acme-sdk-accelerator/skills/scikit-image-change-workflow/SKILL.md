---
name: scikit-image-change-workflow
description: Use this skill when a user asks Cursor Agent to make, fix, test, document, or prepare a PR-ready scoped change in the scikit-image repository from a plain-English request or issue link. Guides Agent through scope, code/test edits, strict gates, explicit commit/PR choice, and change brief for engineering, PM, QA, and DevOps. Use only for scikit-image scoped change work.
---

# scikit-image change workflow

## Goal

Make it easy, fast, and safe for a new engineer or adjacent partner to get a real scikit-image change through the governed SDLC path — request, plan, build, review, test, deploy (CI handoff) — with commit and PR creation controlled by explicit user choice.

## Workflow

1. **Request:** Confirm you are in a real `scikit-image` checkout. Treat the user prompt as product intent.
2. Read `README.md`, `CONTRIBUTING.rst`, and the nearest source/test files for the requested area.
3. Treat `CONTRIBUTING.rst` as the source of truth. Follow its development process, AI policy, style, testing, documentation, branch, and PR guidance.
4. Convert the user request into a small implementation target. Avoid broad refactors.
5. **Plan:** Write a short change plan before editing: target files, tests to add or update, risks, and acceptance criteria. Present it in the response before making edits.
6. Create or reuse a local branch named like `cursor/<short-change-name>`.
7. **Build:** Edit code and tests end-to-end. Use gates, tests, verifier output, and handoff evidence as the safety mechanism.
8. **Review:** Before local commit, run the strict code-quality gate: inspect the diff for deprecated APIs, scikit-image anti-patterns, missing/weak tests, docstring drift, unclear user-facing behavior, and unresolved risks.
9. **Test:** Before local commit, run the focused `spin test` command for touched behavior first. Configure the project development environment when needed and keep it for later Cursor runs. Use the sibling demo environment at `../.venv-skimage` so Meson does not treat dependency headers as source-tree paths. Activate an existing `../.venv-skimage`; create one with Python 3.13 via uv when setup is needed; read `pyproject.toml` and `CONTRIBUTING.rst`; install the needed pyproject extras with uv; then prepare the build/test setup. For this checkout, the expected setup path is:
   ```bash
   uv venv --python 3.13 ../.venv-skimage
   source ../.venv-skimage/bin/activate
   python --version
   uv pip install -e '.[build,test,developer,data]'
   spin install -v
   ```
   Use direct imports or ad hoc pytest runs as diagnostics, then run focused `spin test` as the acceptance gate.
10. Before local commit, run `pre-commit run --files <changed files>` for suitable changed files from `../.venv-skimage`. When `pre-commit` needs setup, prepare it using the repo guidance.
11. Before local commit, run `spin test --test-modified --base-ref upstream/main` when practical after the focused gate passes; otherwise record why focused `spin test` is the live local gate and full modified-test coverage remains the CI gate.
12. Keep the configured `../.venv-skimage` and clean generated setup artifacts beyond the intended repo changes, such as a new `uv.lock`, build/cache output, and ad hoc logs.
13. When focused `spin test` or suitable `pre-commit` remains unavailable after following `CONTRIBUTING.rst`, stop as `BLOCKED`: report the exact setup blocker and next fix step before any commit/PR choice.
14. Before asking about commit or PR creation, run the verifier Agent (`scikit-image-verifier`) when available and read its verdict.
15. Treat verifier `PASS` as the prerequisite for final readiness and the commit/PR choice. Treat verifier `FAIL` or `BLOCKED` as the final status for the turn: report the verdict, blocker, and next fix/setup step.
16. Fix flagged residual risks that fit the original request scope, rerun the affected gates and verifier, and keep iterating until those in-scope risks are resolved. Report residual risks only when they require a user/product choice or belong to a separate change.
17. Before asking about commit or PR creation, complete the final readiness check: strict gate evidence is recorded, focused `spin test` passed, suitable `pre-commit` passed, verifier returned `PASS`, only intentional files remain changed, AI disclosure is ready, and readiness risks are clear.
18. **Deploy (CI handoff):** After commit approval, generate change briefs with DevOps/CI notes for Marcus's pipeline gates.
19. Ask: “Anything else you want included, or are we done? If done, do you want leave uncommitted, local commit, or local commit plus PR?”
20. Wait for the user's explicit choice before commit, push, or PR creation.
21. If the user chooses commit, create the local commit, then generate both handoff files:
   - `.cursor/acme-sdk-accelerator/change-brief.md`
   - `.cursor/acme-sdk-accelerator/change-brief.html`
22. If the user chooses PR too, open/push only after the local commit exists, the change brief is clean, and the user explicitly approved PR creation.

Use the bundled renderer when useful:

```bash
python .cursor/plugins/acme-sdk-accelerator/skills/scikit-image-change-workflow/scripts/render_change_brief.py \
  --request "<user request>" \
  --plan "<change plan: files, tests, acceptance criteria>" \
  --summary "<what changed>" \
  --test "<command>: <result>" \
  --qa-note "<what QA should verify>" \
  --devops-note "<CI/deploy note>"
```

## scikit-image rules to honor

- Use the user's fork as `origin` and the project repo as `upstream`.
- Keep changes on a feature branch.
- Add tests for changed behavior and require behavior assertions beyond execution-only checks.
- Check for deprecated APIs and scikit-image anti-patterns before commit.
- Use `np.random.RandomState(seed)` in tests that need deterministic random data.
- Use scikit-image import conventions from `CONTRIBUTING.rst`.
- Use NumPy dtype objects such as `np.uint8`.
- Follow numpydoc when changing docs/docstrings.
- Add gallery examples for new functionality.
- Disclose Cursor/AI assistance in the PR-ready text.
- Complete the final readiness check first, with focused `spin test`, suitable `pre-commit`, and verifier `PASS`, then ask whether the user wants leave uncommitted, local commit, or local commit plus PR.

## Available scripts

- `scripts/render_change_brief.py` renders `.cursor/acme-sdk-accelerator/change-brief.md` and `.cursor/acme-sdk-accelerator/change-brief.html` from supplied summary, validation, QA, DevOps, and risk notes.

## Output quality

The final response should give the user only:

- branch name;
- commit status or commit hash if the user approved commit;
- tests run and results;
- paths to the markdown and HTML change brief if generated;
- residual risk or setup blocker.

## Constraints

- Cursor settings own approvals and auto-run. Leave them unchanged.
- Keep context inside approved workspace roots.
- Commit, push, publish, or open a PR only after a completed final readiness check and explicit user approval.
- Environment setup configures and preserves the sibling demo environment `../.venv-skimage` using `pyproject.toml` and `CONTRIBUTING.rst` before marking the change ready.
- In-scope residual risks are fixed and re-verified before the final handoff.
