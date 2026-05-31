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

## 2026-05-31 V0.2.1 Quality Fix Validation

### Fixes Verified

- Demo and real data separation:
  - Default `digest --today` keeps demo rows and labels them as `demo 验证数据`.
  - `digest --today --exclude-demo` generated a report with `Demo 条目: 已排除`.
  - `sources.yaml` now includes `exclude_demo_in_digest`.

- Entity matching:
  - Added tests confirming `Meta` does not match `metal`, `metadata`, or `metamaterial`.
  - Added test confirming `Meta` still matches as a standalone English entity.

- HTML text cleanup:
  - Added `clean_text` helper using standard-library `html.unescape` and simple tag stripping.
  - Added test for `&nbsp;`, `&#160;`, `&#8230;`, `&amp;`, and simple HTML tags.

- Suggested action:
  - Added configurable `opportunity_action_thresholds`.
  - Added test confirming a high-opportunity personal item with `opportunity_score >= 80` gets A5/A6/A7, not only A3.
  - `scripts/inspect.sh` now shows demo item `AI workflow 开源项目招募贡献者` as `A6 做工具/工作流原型`.

- Fetcher stability:
  - RSS/HN/arXiv already use timeout; text cleanup now applies to RSS/arXiv/HN/GitHub.
  - Fetch runner now returns per-source status and count.
  - Added deterministic test proving one failed source does not block a successful source.

- Digest readability:
  - Rows include `数据类型`.
  - `demo://` rows are labeled `demo 验证数据`.
  - Empty summaries render as `暂无摘要，不建议直接采用该条判断`.
  - `为什么重要` includes score reason plus cleaned summary/fallback.

### Required Commands

- `python -m intelligence_hub status`
  - Result: PASS
  - Output version: `Qingbao Intelligence Hub v0.2.1`
  - Counts before final fetch validation: `{'sources': 5, 'items': 44, 'scores': 44, 'actions': 0}`

- `python -m intelligence_hub init-db`
  - Result: PASS

- `python -m intelligence_hub seed-demo`
  - Result: PASS
  - Output: `seeded/scored demo items: 15`

- `python -m intelligence_hub digest --today`
  - Result: PASS
  - Output: generated `intelligence_hub/reports/daily/2026-05-31.md`

- `python -m intelligence_hub fetch-once`
  - Result: PASS with source degradation
  - Output:
    - `source: arxiv_ai status: failed items: 0`
    - `source: hn_frontpage status: success items: 5`
    - `source: mit_ai status: success items: 10`
    - warning: `arxiv:arxiv_ai failed: HTTP Error 429: Unknown Error`
    - total: `fetched/scored items: 15`
  - Note: live public results are not guaranteed to be reproducible across days or network environments.

- `python -m unittest discover -s tests`
  - Result: PASS
  - Output: `Ran 11 tests ... OK`

- `bash scripts/run_once.sh`
  - Result: PASS

- `bash scripts/inspect.sh`
  - Result: PASS
  - Output version: `v0.2.1`
  - Counts: `{'sources': 5, 'items': 44, 'scores': 44, 'actions': 0}`

- `git diff --stat`
  - Result: PASS
  - Output: 14 tracked files changed, `119 insertions(+), 22 deletions(-)`.
  - Note: new untracked files are not included in `git diff --stat`: `intelligence_hub/src/text.py`, `tests/test_fetchers.py`, `tests/test_text.py`.

### Additional Checks

- `python -m intelligence_hub digest --today --exclude-demo`
  - Result: PASS
  - `rg -n "Demo 条目|demo 验证数据" intelligence_hub/reports/daily/2026-05-31.md` showed `Demo 条目: 已排除`.

- Final default report was regenerated with `python -m intelligence_hub digest --today`.

### Failed Validation

None. The arXiv 429 during `fetch-once` was a source-level public endpoint failure and was handled as a warning without failing the command.
