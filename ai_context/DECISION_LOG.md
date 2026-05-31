# Decision Log

## 2026-05-31

- Build V0.2 as a local Python standard-library-first MVP: SQLite, YAML-like config files, Markdown reports, and `unittest`.
- Avoid API keys, cloud services, vector databases, LLM summarization, and frontend work in this phase.
- Use idempotent database initialization and URL-based item deduplication so `init-db` and `seed-demo` can be re-run safely.
- Implement network fetchers as best-effort adapters that never break the demo and digest workflow when a source fails.
- Keep generated SQLite database and Python cache files ignored by `.gitignore`; deliver source, config, tests, notes, scripts, and generated Markdown report as visible project artifacts.
- Add feedback as a simple append-only action table plus opportunity log append, avoiding any complex preference model in V0.2.
- Treat live `fetch-once` output as best-effort and environment-dependent. The reproducible baseline is the demo dataset and core chain tests; fetchers now print per-source counts to make live runs auditable.
- Treat daily Markdown reports as runtime artifacts and ignore `intelligence_hub/reports/daily/*.md` in Git.
- Move scoring baselines and blend weights into `scoring.yaml` to reduce hardcoded scoring policy in Python while keeping the algorithm simple.
