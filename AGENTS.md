# AGENTS.md

scikit-image is a scientific Python library (imported as `skimage`) built with
Meson + Cython + Pythran. Standard contributor workflow (build, test, docs,
benchmarks) is documented in `CONTRIBUTING.rst` and driven by the `spin` CLI
(configured in `pyproject.toml` / `.spin/cmds.py`).

## Bundled Cursor plugin

This repo ships a Cursor plugin at `.cursor/plugins/acme-sdk-accelerator/`
(the "Acme SDK Accelerator" governed-change workflow). It is committed to the
repo so every contributor gets it automatically: the project-level
`workspaceOpen` hook in `.cursor/hooks.json` returns the plugin's absolute path
via `pluginPaths`, which is the documented way to auto-load a repo-bundled plugin
(see https://cursor.com/docs/hooks). Internal plugin paths are portable — they
resolve through the always-present `$CURSOR_PROJECT_DIR`, so no per-checkout
rewriting is needed. Caveat: `workspaceOpen` is an IDE lifecycle hook and does
**not** apply to cloud agents, so cloud-agent runs do not auto-load the plugin.

## Cursor Cloud specific instructions

- Cloud agents use `.cursor/environment.json`, which runs
  `.cursor/scripts/setup-cloud-env.sh` on startup. That script creates
  `~/.venvs/skimage-dev`, installs `requirements.txt`, and runs
  `CC=gcc CXX=g++ spin install`. Re-run it manually after dependency changes:
  `bash .cursor/scripts/setup-cloud-env.sh`.
- IMPORTANT build gotcha: on the cloud image the default `cc`/`c++` resolve to
  `clang`, and `clang++` fails to link C++ (`/usr/bin/ld: cannot find -lstdc++`).
  Build with the GNU toolchain by prefixing build/install commands with
  `CC=gcc CXX=g++` (e.g. `CC=gcc CXX=g++ spin install`). Meson caches the
  compiler in the build dir, so once configured with gcc/g++, `spin test` and
  import-time rebuilds reuse it without the prefix.
- IMPORTANT PATH gotcha: `spin install` invokes meson-python, which must find the
  `meson` executable on `PATH`. Activate the venv (or put its `bin` directory on
  `PATH`) before running `spin install`; calling `~/.venvs/skimage-dev/bin/spin`
  directly without activation can fail with `meson executable "meson" not found`
  even when meson is installed in the venv.
- The package is installed editable via meson-python, so `spin install` rebuilds
  changed extensions automatically on the next `import skimage`. A full
  `spin build --clean` is only needed if incremental builds misbehave.
- Tests: `spin test` (full) or scope it, e.g. `spin test -- tests/skimage/filters`
  or `spin test -- -k threshold`. Add `--doctest` to mirror CI. Tests live under
  `tests/` (testpaths in `pyproject.toml`).
- `matplotlib` is intentionally not installed (optional dependency), so a few
  tests that need it are skipped — this is expected, not a failure. Install
  `requirements/optional.txt` for that coverage.
- Lint/format runs through pre-commit: `pre-commit run ruff --all-files` and
  `pre-commit run ruff-format --all-files` (ruff is not installed standalone).
