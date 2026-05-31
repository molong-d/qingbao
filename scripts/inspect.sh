#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python -m intelligence_hub status
python -m intelligence_hub opportunities --top 10
latest_report="$(find intelligence_hub/reports/daily -maxdepth 1 -type f -name '*.md' | sort | tail -1 || true)"
if [[ -n "${latest_report}" ]]; then
  echo "latest_report: ${latest_report}"
else
  echo "latest_report: none"
fi
