# AGENTS.md

scikit-image is a pure Python image-processing **library** (import name `skimage`),
built from C/C++/Cython/Pythran sources via the Meson build system (`meson-python`)
and driven by the [`spin`](https://github.com/scientific-python/spin) developer CLI.
There is no server, web app, or database — "running the app" means building the
compiled extensions and importing/using `skimage` (or running its tests).

## Cursor Cloud specific instructions

### Environment layout

- A Python 3.12 virtualenv lives **outside the repo** at `~/skimage-venv`. It must
  live outside the source tree: Meson rejects numpy/pythran include paths that
  resolve inside `/workspace` (e.g. a repo-local `.venv`), so do **not** create a
  venv inside the repository.
- The startup update script keeps this venv's dependencies in sync. Activate it
  before doing anything: `source ~/skimage-venv/bin/activate`. Activation is what
  puts `meson`/`ninja`/`spin` on `PATH` (required by `spin build`).
- System build tools (`gcc`, `g++`, `libstdc++-*-dev`, `python3-dev`,
  `python3.12-venv`) are baked into the VM snapshot, not the update script.

### Build / run / test (all via `spin`, with the venv activated)

- Build the compiled extensions (out-of-tree into `build/`): `spin build`.
  Use the GNU toolchain — `export CC=gcc CXX=g++` — when (re)configuring the build.
  The default `c++` resolves to clang, which previously failed to link `libstdc++`.
  This only matters for the initial `meson setup` / `spin build --clean`; the
  configured `build/` dir persists in the snapshot and incremental rebuilds reuse it.
- Run code against the freshly built package: `spin run python <script.py>`
  (note: `spin python` does not accept `-c`; use `spin run python -c '...'`).
- Run tests: `spin test` (full suite, doctests on). Unit tests live in
  `tests/` (e.g. `tests/skimage/color/`), not under `src/`. Run a subset by
  passing a tests path, e.g. `spin test --no-doctest -- tests/skimage/color`.
  Passing a module name like `skimage.color` only collects that module's doctests.
- Lint: `pre-commit run --all-files` (ruff, ruff-format, prettier, cython-lint).
  First run downloads hook environments (needs network).

### Notes

- `src/` contains two parallel APIs: the stable `skimage` and the experimental
  `skimage2` (re-exported from the installed `_skimage2`).
- pytest runs with `filterwarnings=error` — warnings are treated as failures.
- Some `skimage.data` sample images download on first access via `pooch`
  (needs network); most do not.
