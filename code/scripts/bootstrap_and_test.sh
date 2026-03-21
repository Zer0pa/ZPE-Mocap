#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-}"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .

if [[ "$MODE" == "bootstrap-only" ]]; then
  exit 0
fi

python -m unittest discover -s tests -v
