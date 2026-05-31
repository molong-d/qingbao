# Validation Log

## 2026-05-31

### Required Validation

- `python -m intelligence_hub status`
  - Result: PASS
  - Initial output showed missing database and zero counts.
  - Final output showed database exists with `sources=5`, `items=35`, `scores=35`, `actions=0`.

- `python -m intelligence_hub init-db`
  - Result: PASS
  - Output: initialized database at `intelligence_hub/data/intelligence.db`.

- `python -m intelligence_hub seed-demo`
  - Result: PASS
  - Output: `seeded/scored demo items: 15`.
  - Re-run through `scripts/run_once.sh` did not duplicate demo rows because URL fingerprints are unique.

- `python -m intelligence_hub digest --today`
  - Result: PASS
  - Output: generated `intelligence_hub/reports/daily/2026-05-31.md`.

- `python -m unittest discover -s tests`
  - Result: PASS
  - Output: `Ran 3 tests ... OK`.

- `bash scripts/run_once.sh`
  - Result: PASS
  - Output: initialized DB, seeded demo, generated daily report.

- `bash scripts/inspect.sh`
  - Result: PASS
  - Output: status succeeded, listed 4 high-opportunity demo items, printed latest report path.

- `python -m intelligence_hub fetch-once`
  - Result: PASS
  - Output: `fetched/scored items: 20`.
  - No warnings were emitted in this run. Fetchers still return warnings rather than raising on network failure.

- `git diff --stat`
  - Result: PASS
  - Output: empty because all application files are newly untracked in this initially empty repository.

- `git status --short`
  - Result: PASS
  - Output shows new untracked directories/files: `README.md`, `ai_context/`, `intelligence_hub/`, `notes/`, `scripts/`, `tests/`.

### Core Chain

`init-db -> seed-demo -> digest --today` works and generated the Markdown daily report.

### Failed Validation

None.

## 2026-05-31 Stability Review Validation

### Review Findings

- `fetch-once` 20 条来源是真实公网源抓取，本轮验证输出为:
  - `arxiv_ai`: 5
  - `hn_frontpage`: 5
  - `mit_ai`: 10
  - total processed/scored: 20
- 该 20 条不是严格可复现数据集，因为 RSS、HN 和 arXiv 都会随时间、网络状态和源内容变化。已在 README 明确说明，并让 `fetch-once` 输出 per-source counts 便于复盘。
- 重复 `seed-demo` 不会重复插入 demo 数据。验证后数据库 counts 为 `{'sources': 5, 'items': 40, 'scores': 40, 'actions': 0}`；其中 item 总数包含此前 live fetch 条目，重复 seed 没有新增 demo 重复项。
- `digest --today` 多次运行覆盖同一天同一路径文件，不追加。验证 `find intelligence_hub/reports/daily -maxdepth 1 -type f -name '*.md' | sort` 只显示 `2026-05-31.md`，并新增单元测试锁定覆盖行为。
- `.gitignore` 已排除 SQLite 数据库和日报运行产物。`git status --ignored --short intelligence_hub/data intelligence_hub/reports/daily` 输出:
  - `!! intelligence_hub/data/`
  - `!! intelligence_hub/reports/daily/`
- README 已补充从 clean clone 到生成日报的最小命令，并说明无需安装依赖。
- `scoring.py` 原先有硬编码 baseline 和权重；已将 baseline、机会信号权重、action score blend weights 移入 `scoring.yaml`。
- tests 已从 3 个增加到 5 个，覆盖 scoring、DB 幂等、digest 生成、digest 覆盖、CLI 核心链路幂等。
- 敏感信息扫描命令只命中 AGENTS/TASK_STATE 中的规则描述，没有发现 API key、token、cookie、私钥或常见 secret pattern。

### Commands And Results

- `python -m intelligence_hub status`
  - Result: PASS
  - Output counts: `{'sources': 5, 'items': 40, 'scores': 40, 'actions': 0}`

- `python -m intelligence_hub init-db`
  - Result: PASS

- `python -m intelligence_hub seed-demo`
  - Result: PASS
  - Repeated run result: PASS

- `python -c "from intelligence_hub.src.db import db_counts; print(db_counts())"`
  - Result: PASS
  - Output after repeated seed: `{'sources': 5, 'items': 40, 'scores': 40, 'actions': 0}`

- `python -m intelligence_hub digest --today`
  - Result: PASS
  - Repeated run result: PASS; same path overwritten.

- `find intelligence_hub/reports/daily -maxdepth 1 -type f -name '*.md' | sort`
  - Result: PASS
  - Output: `intelligence_hub/reports/daily/2026-05-31.md`

- `python -m intelligence_hub fetch-once`
  - Result: PASS
  - Output: `arxiv_ai=5`, `hn_frontpage=5`, `mit_ai=10`, `fetched/scored items: 20`
  - Note: live count is not guaranteed across future runs.

- `python -m unittest discover -s tests`
  - Result: PASS
  - Output: `Ran 5 tests ... OK`

- `bash scripts/run_once.sh`
  - Result: PASS

- `bash scripts/inspect.sh`
  - Result: PASS

- `git status --ignored --short intelligence_hub/data intelligence_hub/reports/daily`
  - Result: PASS
  - Confirmed database and report directories are ignored.

- `rg -n "api[_-]?key|secret|password|cookie|BEGIN (RSA|OPENSSH|PRIVATE)|ghp_|github_pat|sk-[A-Za-z0-9]" -S .`
  - Result: PASS
  - Only matched policy text, no secret values.

- `git diff --stat`
  - Result: PASS
  - Output: `.gitignore | 1 +` because most project files are still untracked in this initial repository state.
