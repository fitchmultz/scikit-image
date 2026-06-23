# AGENTS.md

scikit-image is a scientific Python library (imported as `skimage`) built with
Meson + Cython + Pythran. Standard contributor workflow (build, test, docs,
benchmarks) is documented in `CONTRIBUTING.rst` and driven by the `spin` CLI
(configured in `pyproject.toml` / `.spin/cmds.py`).

## Cursor Cloud specific instructions

- A development virtualenv is provisioned at `~/.venvs/skimage-dev` (created by
  the startup update script). Activate it before running anything:
  `source ~/.venvs/skimage-dev/bin/activate`. All `spin`, `pytest`, and
  `pre-commit` commands assume this venv is active.
- IMPORTANT build gotcha: on this image the default `cc`/`c++` resolve to
  `clang`, and `clang++` fails to link C++ (`/usr/bin/ld: cannot find -lstdc++`).
  You MUST build with the GNU toolchain by prefixing build/install commands with
  `CC=gcc CXX=g++` (e.g. `CC=gcc CXX=g++ spin install`). The update script
  already does this; if you ever wipe `build/` and rebuild manually, remember the
  prefix. Meson caches the compiler in the build dir, so once configured with
  gcc/g++, `spin test`/import-time rebuilds reuse it without the prefix.
- The package is installed editable via meson-python, so `spin install` rebuilds
  changed extensions automatically on the next `import skimage`. After editing
  Cython/C/C++/Pythran sources just re-run/re-import; a full `spin build --clean`
  is only needed if incremental builds misbehave.
- Tests: `spin test` (full) or scope it, e.g. `spin test -- tests/skimage/filters`
  or `spin test -- -k threshold`. Add `--doctest` to mirror CI. The suite lives
  under `tests/` (testpaths in `pyproject.toml`).
- `matplotlib` is intentionally not installed (it is an optional dependency), so
  a few tests that need it are skipped — this is expected, not a failure. Install
  `requirements/optional.txt` if you need that coverage.
- Lint/format is run through pre-commit: `pre-commit run ruff --all-files` and
  `pre-commit run ruff-format --all-files` (ruff is not installed standalone in
  the venv).
