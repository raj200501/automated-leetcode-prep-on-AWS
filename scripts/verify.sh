#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
VENV_DIR="$ROOT_DIR/.venv"

python -m venv "$VENV_DIR"

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

export PYTHONPATH="$ROOT_DIR/src"

python -m unittest discover -s "$ROOT_DIR/tests"
python -m automated_leetcode_prep.cli verify
