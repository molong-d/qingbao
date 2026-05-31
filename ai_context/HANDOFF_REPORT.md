# Handoff Report

## 1. 本轮完成了什么

- 构建了本地可运行的 Qingbao Intelligence Hub V0.2 MVP。
- 完成核心链路：`init-db -> seed-demo -> digest --today`。
- 实现 SQLite 存储、demo 数据、规则评分、Markdown 日报、真实 fetcher 降级接口、人工反馈、机会列表、脚本和测试。
- 未引入云服务、LLM/RAG、向量数据库或 API Key。

## 2. 修改/新增文件列表

- `README.md`
- `ai_context/COMMAND_LOG.md`
- `ai_context/DECISION_LOG.md`
- `ai_context/VALIDATION_LOG.md`
- `ai_context/TASK_STATE.md`
- `ai_context/HANDOFF_REPORT.md`
- `intelligence_hub/__init__.py`
- `intelligence_hub/__main__.py`
- `intelligence_hub/config/topics.yaml`
- `intelligence_hub/config/watchlist.yaml`
- `intelligence_hub/config/scoring.yaml`
- `intelligence_hub/config/sources.yaml`
- `intelligence_hub/src/cli.py`
- `intelligence_hub/src/config.py`
- `intelligence_hub/src/db.py`
- `intelligence_hub/src/models.py`
- `intelligence_hub/src/scoring.py`
- `intelligence_hub/src/classify.py`
- `intelligence_hub/src/dedupe.py`
- `intelligence_hub/src/digest.py`
- `intelligence_hub/src/fetchers/demo.py`
- `intelligence_hub/src/fetchers/rss.py`
- `intelligence_hub/src/fetchers/arxiv.py`
- `intelligence_hub/src/fetchers/github.py`
- `intelligence_hub/src/fetchers/hn.py`
- `intelligence_hub/src/fetchers/runner.py`
- `tests/test_scoring.py`
- `tests/test_digest.py`
- `tests/test_db.py`
- `scripts/run_once.sh`
- `scripts/inspect.sh`
- `notes/opportunity_log.md`
- `notes/trend_journal.md`
- `notes/company_watch.md`
- `intelligence_hub/reports/daily/2026-05-31.md`

Generated but ignored runtime artifact:

- `intelligence_hub/data/intelligence.db`

## 3. 核心功能说明

- `python -m intelligence_hub status`: 查看版本、数据库路径、报表路径、表计数。
- `python -m intelligence_hub init-db`: 幂等创建 SQLite schema，并写入 sources 配置。
- `python -m intelligence_hub seed-demo`: 幂等写入 15 条 demo 数据并评分。
- `python -m intelligence_hub digest --today`: 生成 Markdown 日报。
- `python -m intelligence_hub fetch-once`: 按 `sources.yaml` 启用状态抓取 RSS、arXiv、GitHub、HN，失败时返回 warning，不中断核心链路。
- `python -m intelligence_hub feedback --item-id <id> --label <label>`: 记录人工反馈到 `actions`。
- `python -m intelligence_hub opportunities --top 10`: 输出高机会分条目。

## 4. 实际验证命令与结果

- `python -m intelligence_hub status`: PASS。
- `python -m intelligence_hub init-db`: PASS。
- `python -m intelligence_hub seed-demo`: PASS，输出 `seeded/scored demo items: 15`。
- `python -m intelligence_hub digest --today`: PASS，生成日报。
- `python -m intelligence_hub fetch-once`: PASS，输出 `fetched/scored items: 20`。
- `python -m unittest discover -s tests`: PASS，`Ran 3 tests ... OK`。
- `bash scripts/run_once.sh`: PASS。
- `bash scripts/inspect.sh`: PASS。
- `git diff --stat`: PASS，输出为空，因为本仓库初始无已跟踪应用文件，新增文件当前均为 untracked。

## 5. 生成的日报路径

- `intelligence_hub/reports/daily/2026-05-31.md`

## 6. 数据库路径

- `intelligence_hub/data/intelligence.db`

## 7. 已知问题

- `*.yaml` 配置目前使用 JSON-compatible YAML 子集，由 Python 标准库 `json` 解析；这是为避免引入 PyYAML 依赖的保守选择。
- `git diff --stat` 对 untracked 新文件不显示统计，需要结合 `git status --short` 或 `git ls-files --others --exclude-standard` 查看新增文件。
- 真实 fetcher 仍是最小实现，未做复杂去噪、分页、限速队列或源质量评估。
- `fetch-once` 的条目数量和内容依赖实时公网源，本轮为 20 条，但不能作为离线可复现断言。当前可复现基线是 demo 数据和单元测试。

## 8. 未完成项

- Streamlit dashboard 未做，符合当前 P3 非优先级。
- LLM 摘要、RAG、Agent 化未做，符合当前 P4 禁止项。
- 未实现复杂反馈学习，仅记录人工动作和机会日志。

## 9. 下一步建议

- 观察 3-7 天日报质量，调整 `watchlist.yaml` 与 `scoring.yaml` 权重。
- 为 RSS fetcher 增加本地 fixture 测试和更多稳定源。
- 增加 `items.published_at` 的按日期过滤，使日报默认只聚焦当天和近几天。
- 增加 `notes/trend_journal.md` 的半自动趋势复盘命令。

## 10. 如何回滚

建议先保存当前改动快照：

```bash
git status
git diff --stat
git diff > backup.patch
git ls-files --others --exclude-standard | sort
```

由于本轮主要是新增未跟踪文件，若确认不要这些变更，可删除新增路径：

```bash
rm -rf README.md ai_context intelligence_hub notes scripts tests
```

如果后续已 `git add` 但未提交，可先取消暂存：

```bash
git restore --staged .
```

如果只想恢复到修改前状态且没有需要保留的新增文件，删除上述新增路径即可。不要使用 `git reset --hard`，除非已经确认没有任何需要保留的本地改动。

## 11. 稳定性审查补充

本轮按用户要求做了代码审查和最小稳定性增强，没有新增 dashboard、LLM、RAG 或大功能。

### 修正内容

- `fetch-once` 现在输出每个启用源的抓取数量，便于确认 live run 的来源分布。
- README 增加从零运行步骤，并明确 `fetch-once` 是实时公网源，数量和标题不保证跨天复现。
- `.gitignore` 增加 `intelligence_hub/reports/daily/*.md`，将日报视为运行产物。
- `scoring.py` 中 baseline、机会信号权重、action score 权重移入 `scoring.yaml`。
- 新增 `tests/test_cli_core.py`，覆盖 `init-db -> seed-demo -> seed-demo -> digest` 的核心链路幂等。
- `tests/test_digest.py` 增加同日日报覆盖写入测试。

### 审查结论

- 重复 `seed-demo` 不会重复插入，依赖 item fingerprint 唯一约束。
- `digest --today` 是覆盖写入同一天文件，不追加；当前行为合理，避免同日日报重复膨胀。
- 数据库、日报和 Python cache 均不会作为普通 untracked 产物暴露。
- 敏感信息扫描未发现密钥、token、cookie 或私钥。
- 当前测试覆盖核心链路，但真实 fetcher 仍应继续用 live smoke test 验证，不应写成依赖公网稳定性的单元测试。

### 最新验证

- `python -m intelligence_hub status`: PASS，counts `{'sources': 5, 'items': 40, 'scores': 40, 'actions': 0}`。
- `python -m intelligence_hub init-db`: PASS。
- `python -m intelligence_hub seed-demo`: PASS，重复执行 PASS。
- `python -m intelligence_hub digest --today`: PASS，重复执行覆盖同一路径。
- `python -m intelligence_hub fetch-once`: PASS，`arxiv_ai=5`、`hn_frontpage=5`、`mit_ai=10`、total `20`。
- `python -m unittest discover -s tests`: PASS，`Ran 5 tests ... OK`。
- `bash scripts/run_once.sh`: PASS。
- `bash scripts/inspect.sh`: PASS。
- secret pattern scan: PASS，仅命中规则文本。
