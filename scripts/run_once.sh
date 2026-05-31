#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python -m intelligence_hub init-db
python -m intelligence_hub seed-demo
python -m intelligence_hub digest --today
