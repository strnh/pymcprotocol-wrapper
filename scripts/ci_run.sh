#!/usr/bin/env bash
set -euo pipefail

# Simple local CI helper: create venv, install dev deps, run tests
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
else
  pip install pytest
fi

PYTHONPATH=src pytest -q
