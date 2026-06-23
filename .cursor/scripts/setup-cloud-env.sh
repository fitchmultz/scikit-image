#!/usr/bin/env bash
# Idempotent cloud-agent setup for scikit-image.
#
# Cloud images default to clang, which fails to link C++ extensions here.
# meson-python also requires the venv bin directory on PATH so `meson` is
# discoverable when `spin install` invokes pip.

set -euo pipefail

VENV_DIR="${SKIMAGE_DEV_VENV:-$HOME/.venvs/skimage-dev}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found on PATH" >&2
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "$REPO_ROOT/requirements.txt"

if ! command -v meson >/dev/null 2>&1; then
  echo "meson is not on PATH after installing build requirements" >&2
  echo "PATH=$PATH" >&2
  exit 1
fi

cd "$REPO_ROOT"
CC=gcc CXX=g++ spin install

python -c "import skimage; print('skimage', skimage.__version__)"
