# Qingbao Intelligence Hub

个人战略情报与机会感知系统，本地运行，使用 Python、SQLite、Markdown 和配置文件完成 V0.2 MVP。

## Core Commands

From a clean clone on Ubuntu with Python 3.10+:

```bash
cd ~/project/qingbao
python -m intelligence_hub status
python -m intelligence_hub init-db
python -m intelligence_hub seed-demo
python -m intelligence_hub digest --today
```

No Python package install is required for the MVP because it uses the standard library only.

```bash
python -m intelligence_hub status
python -m intelligence_hub init-db
python -m intelligence_hub seed-demo
python -m intelligence_hub digest --today
python -m intelligence_hub fetch-once
python -m intelligence_hub opportunities --top 10
python -m intelligence_hub feedback --item-id 1 --label track
```

## One-shot Run

```bash
bash scripts/run_once.sh
bash scripts/inspect.sh
```

## Paths

- Database: `intelligence_hub/data/intelligence.db`
- Daily reports: `intelligence_hub/reports/daily/YYYY-MM-DD.md`
- Config: `intelligence_hub/config/*.yaml`
- Notes: `notes/*.md`

## Design Constraints

- Local-only; no cloud services.
- No hardcoded API keys.
- No vector database or LLM/RAG in this phase.
- Fetchers degrade gracefully when network sources fail.
- `fetch-once` uses live public sources, so the exact number and titles are not guaranteed to be reproducible across days or network environments. The demo chain is the reproducible baseline.
