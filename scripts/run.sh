#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export PYTHONPATH="$ROOT_DIR/src"

USE_LIVE_API=${USE_LIVE_API:-0}
EXTRA_ARGS=()
if [[ "$USE_LIVE_API" == "1" ]]; then
  EXTRA_ARGS+=("--use-live-api")
fi

python -m automated_leetcode_prep.cli run "${EXTRA_ARGS[@]}" "$@"
