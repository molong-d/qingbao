# Task State

## Current Project State

- Repository: `/home/long/project/qingbao`
- Git remote: `git@github.com:molong-d/qingbao.git` according to user context.
- Initial codebase was nearly empty: `.gitignore`, `AGENTS.md`, and Git metadata.
- No application package, database schema, tests, scripts, or reports existed before this run.

## Current Objective

Build "个人战略情报与机会感知系统 V0.1 -> V0.2" as a local, verifiable MVP that can answer daily:

1. 今天最值得关注的 5 条信息是什么？
2. 为什么重要？
3. 和用户有什么关系？
4. 建议用户采取什么动作？
5. 哪些方向值得持续跟踪？

## Phase Plan

- Phase 0: Initialize logs and task state.
- Phase 1: Create minimal Python package and CLI.
- Phase 2: Add topic, watchlist, scoring, and source config files.
- Phase 3: Add idempotent SQLite schema and persistence helpers.
- Phase 4: Add demo data, classification, scoring, dedupe, and suggested actions.
- Phase 5: Generate Markdown daily digest.
- Phase 6: Add best-effort RSS, arXiv, GitHub, and Hacker News fetchers with graceful degradation.
- Phase 7: Add feedback and opportunities commands.
- Phase 8: Add scripts and README.
- Phase 9: Run required validation commands and fix small failures.
- Phase 10: Update final handoff report.

## Acceptance Criteria

- `python -m intelligence_hub status` works.
- `python -m intelligence_hub init-db` can run repeatedly without destroying data.
- `python -m intelligence_hub seed-demo` can run repeatedly without duplicate demo items.
- `python -m intelligence_hub digest --today` generates `intelligence_hub/reports/daily/YYYY-MM-DD.md`.
- Core chain works: `init-db -> seed-demo -> digest --today`.
- `python -m unittest discover -s tests` passes.
- `scripts/run_once.sh` and `scripts/inspect.sh` run from the repository root.
- Network fetch failures are logged or returned as warnings without crashing core workflow.

## Risk Controls

- Keep implementation standard-library-first and local-only.
- Do not write API keys, tokens, or cookies into code or logs.
- Keep schema and files small and additive.
- Do not delete existing files without explicit reason.
- Limit failed validation fixes to two small repair rounds.
- Record important commands, decisions, validation results, and handoff details in `ai_context`.

## Status

- Phase 0: Complete.
- Phase 1: Complete.
- Phase 2: Complete.
- Phase 3: Complete.
- Phase 4: Complete.
- Phase 5: Complete.
- Phase 6: Complete with best-effort network fetchers.
- Phase 7: Complete with simple feedback and opportunity listing.
- Phase 8: Complete.
- Phase 9: Complete; all required validation passed.
- Phase 10: Complete after `HANDOFF_REPORT.md` update.
- Blockers: none.

## Completed Items

- Local Python package and CLI.
- JSON-compatible YAML config files for topics, watchlist, scoring, and sources.
- Idempotent SQLite schema for sources, items, item scores, tags, and actions.
- Demo source with 15 items across all required domains.
- Rule-based classification, scoring, dedupe, suggested action, and score reasons.
- Markdown daily digest generator.
- RSS, arXiv, GitHub, and Hacker News best-effort fetchers.
- Feedback and opportunities commands.
- README and shell scripts.
- Unit tests for scoring, digest, and database idempotency.

## Unfinished Items

- No frontend, LLM summary, RAG, vector DB, or cloud integration by design.
- Fetcher coverage is minimal and should be expanded only after observing source quality.
