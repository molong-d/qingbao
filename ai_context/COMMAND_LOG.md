# Command Log

## 2026-05-31

- `pwd` - confirmed repository path `/home/long/project/qingbao`.
- `ls -la` - inspected top-level repository contents.
- `find . -maxdepth 3 -type f | sort | head -200` - inspected existing files.
- `git status --short` - confirmed no tracked/untracked application files before this work.
- `mkdir -p ai_context intelligence_hub/config intelligence_hub/src/fetchers intelligence_hub/data intelligence_hub/reports/daily tests scripts notes` - created required project directories.
- `chmod +x scripts/run_once.sh scripts/inspect.sh` - made helper scripts executable.
- `python -m intelligence_hub status` - checked app status before and after initialization.
- `python -m intelligence_hub init-db` - created/updated SQLite schema and sources.
- `python -m intelligence_hub seed-demo` - inserted/scored demo items idempotently.
- `python -m intelligence_hub digest --today` - generated the daily Markdown report.
- `python -m unittest discover -s tests` - ran unit tests.
- `bash scripts/run_once.sh` - verified one-shot local run.
- `bash scripts/inspect.sh` - verified inspection script and opportunity listing.
- `python -m intelligence_hub fetch-once` - ran enabled public fetchers with graceful degradation.
- `git diff --stat` - checked tracked diff stat; output was empty because this repository had no tracked application files and all new files are currently untracked.
- `git status --short` - checked working tree state.
- `git ls-files --others --exclude-standard | sort` - listed new untracked project files.
- `printf '核心 MVP: 完成...'` - printed required final terminal summary.

## 2026-05-31 Stability Review

- `sed -n '1,240p' intelligence_hub/src/cli.py` - reviewed CLI behavior.
- `sed -n '1,260p' intelligence_hub/src/scoring.py` - reviewed scoring constants and configuration use.
- `sed -n '1,260p' intelligence_hub/src/db.py` - reviewed SQLite schema and idempotent insert behavior.
- `sed -n '1,220p' .gitignore` - reviewed ignored runtime artifacts.
- `sed -n '1,220p' README.md` - reviewed zero-start instructions.
- `sed -n '1,220p' intelligence_hub/src/digest.py` - reviewed report overwrite behavior.
- `find tests -maxdepth 2 -type f -name '*.py' -print -exec sed -n '1,220p' {} \\;` - reviewed test coverage.
- `rg -n "api[_-]?key|secret|password|cookie|BEGIN (RSA|OPENSSH|PRIVATE)|ghp_|github_pat|sk-[A-Za-z0-9]" -S .` - scanned for common secret patterns.
- `python -m unittest discover -s tests` - ran updated unit tests.
- `git status --ignored --short intelligence_hub/data intelligence_hub/reports/daily` - confirmed database and daily reports are ignored.
- `python -c "from intelligence_hub.src.db import db_counts; print(db_counts())"` - checked database counts after repeated seed and fetch validation.

## 2026-05-31 V0.2.1 Quality Fix

- `sed -n '1,260p' intelligence_hub/src/digest.py` - reviewed digest rendering and demo handling.
- `sed -n '1,260p' intelligence_hub/src/scoring.py` - reviewed entity matching and suggested action logic.
- `sed -n '1,260p' intelligence_hub/src/cli.py` - reviewed CLI support for digest flags and fetch output.
- `sed -n '1,260p' intelligence_hub/config/scoring.yaml` - reviewed scoring policy config.
- `sed -n '1,220p' intelligence_hub/src/fetchers/rss.py` - reviewed RSS timeout and text handling.
- `sed -n '1,220p' intelligence_hub/src/fetchers/arxiv.py` - reviewed arXiv timeout and text handling.
- `sed -n '1,220p' intelligence_hub/src/fetchers/hn.py` - reviewed HN timeout and text handling.
- `sed -n '1,200p' intelligence_hub/src/fetchers/runner.py` - reviewed single-source failure behavior.
- `python -m unittest discover -s tests` - ran unit tests after V0.2.1 fixes.
- `python -m intelligence_hub status` - verified CLI status on V0.2.1.
- `python -m intelligence_hub init-db` - verified idempotent DB initialization.
- `python -m intelligence_hub seed-demo` - verified demo seeding remains idempotent.
- `python -m intelligence_hub digest --today` - generated default digest with demo labels.
- `python -m intelligence_hub digest --today --exclude-demo` - verified demo exclusion flag.
- `rg -n "Demo 条目|demo 验证数据" intelligence_hub/reports/daily/2026-05-31.md` - checked digest demo labeling/exclusion.
- `python -m intelligence_hub fetch-once` - verified per-source status/count output and single-source failure degradation.
- `bash scripts/run_once.sh` - verified one-shot core chain.
- `bash scripts/inspect.sh` - verified status/opportunity inspection.
- `git diff --stat` - reviewed tracked diff stat.
- `git status --short` - reviewed working tree state.
- `git ls-files --others --exclude-standard | sort` - listed new untracked V0.2.1 files.
