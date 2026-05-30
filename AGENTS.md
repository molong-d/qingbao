# Qingbao Intelligence Hub - AGENTS.md

你正在开发“个人战略情报与机会感知系统”。

系统定位：
- 不是普通新闻聚合器。
- 是个人战略情报与机会感知系统。
- 目标是长期跟踪 AI、机器人与具身智能、Web3、金融宏观、产业公司、政策监管、个人机会信号。
- 第一版目标是本地可运行、可验证、可回滚的 MVP。

技术路线：
- Ubuntu 22.04
- Python
- SQLite
- Markdown
- YAML 配置
- 后续可扩展 Streamlit，但当前阶段不要优先做前端。
- 先规则打分，后 LLM/RAG。
- 不要上云。
- 不要写死 API Key。

Harness 工程原则：
1. 最小变更。
2. 分阶段推进。
3. 每阶段必须有验收标准。
4. 每阶段必须有验证命令。
5. 失败先记录、定位、降级，不要盲目大改。
6. 不允许无说明地删除已有文件。
7. 不允许大规模重构，除非先说明理由并记录。
8. 不允许引入重依赖，除非有必要且记录理由。
9. 不允许把密钥、token、cookie 写入代码或日志。
10. 所有操作必须可复盘。

必须维护这些文件：
- ai_context/COMMAND_LOG.md：记录执行过的重要命令。
- ai_context/DECISION_LOG.md：记录关键设计决策。
- ai_context/VALIDATION_LOG.md：记录验证命令、结果、失败原因。
- ai_context/TASK_STATE.md：记录当前阶段、完成项、未完成项、阻塞项。
- ai_context/HANDOFF_REPORT.md：最终交接报告。

工作方式：
- 先侦察项目结构，再修改。
- 先写计划，再执行。
- 每完成一个阶段，立刻运行验证。
- 验证失败时，最多尝试两轮小修。
- 两轮仍失败，记录失败原因和保守降级方案，然后继续其他不受影响任务。
- 最后必须输出完整交接报告。

当前优先级：
P0：项目骨架、配置、SQLite、demo 数据、评分、Markdown 日报、测试。
P1：RSS/arXiv/GitHub/HN fetcher。
P2：人工反馈、机会库、历史查询。
P3：Streamlit dashboard。
P4：LLM 摘要、RAG、Agent 化，当前不要做。

禁止：
- 不要一上来做复杂 Agent。
- 不要一上来做向量数据库。
- 不要一上来做 LLM 总结。
- 不要为了看起来高级而牺牲可运行性。
- 不要自动 git commit，除非用户明确要求。
