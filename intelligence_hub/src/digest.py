import json
from collections import defaultdict
from datetime import datetime

from intelligence_hub.src.config import REPORT_DIR, load_config
from intelligence_hub.src.db import list_ranked_items
from intelligence_hub.src.text import clean_text


TOPICS = [
    "AI 与前沿科技",
    "机器人与具身智能",
    "Web3 与数字资产",
    "金融与宏观",
    "产业与公司",
    "政策与监管",
    "个人机会",
]


def _item_block(row) -> str:
    keywords = ", ".join(json.loads(row["matched_keywords"] or "[]")) or "无"
    entities = ", ".join(json.loads(row["matched_entities"] or "[]")) or "无"
    is_demo = row["source_type"] == "demo" or row["url"].startswith("demo://")
    source_note = "demo 验证数据" if is_demo else "真实/公共来源"
    summary = clean_text(row["summary"])
    if not summary:
        summary = "暂无摘要，不建议直接采用该条判断"
    importance = f"{row['score_reason']} 摘要要点: {summary}"
    return "\n".join(
        [
            f"### {row['title']}",
            f"- 来源: {row['source_name']}",
            f"- 数据类型: {source_note}",
            f"- 链接: {row['url']}",
            f"- 领域: {row['topic']}",
            f"- 重要性分: {row['importance_score']}",
            f"- 可信度分: {row['credibility_score']}",
            f"- 相关性分: {row['relevance_score']}",
            f"- 机会分: {row['opportunity_score']}",
            f"- 行动分: {row['action_score']}",
            f"- 命中关键词: {keywords}",
            f"- 命中实体: {entities}",
            f"- 为什么重要: {importance}",
            f"- 建议动作: {row['suggested_action']}",
            "",
        ]
    )


def generate_daily(today: bool = False, exclude_demo: bool | None = None) -> str:
    report_date = datetime.now().date().isoformat()
    rows = list_ranked_items()
    if exclude_demo is None:
        exclude_demo = bool(load_config("sources.yaml").get("exclude_demo_in_digest", False))
    if exclude_demo:
        rows = [row for row in rows if row["source_type"] != "demo" and not row["url"].startswith("demo://")]
    by_topic = defaultdict(list)
    for row in rows:
        by_topic[row["topic"]].append(row)

    lines = [
        "# 每日个人战略情报简报",
        "",
        f"- 日期: {report_date}",
        f"- 条目数: {len(rows)}",
        f"- Demo 条目: {'已排除' if exclude_demo else '保留，标注为 demo 验证数据'}",
        "",
        "## 今日最重要的 5 条",
        "",
    ]
    for row in rows[:5]:
        lines.append(_item_block(row))

    for topic in TOPICS:
        lines.extend([f"## {topic}", ""])
        topic_rows = by_topic.get(topic, [])
        if not topic_rows:
            lines.extend(["暂无条目。", ""])
            continue
        for row in topic_rows[:5]:
            lines.append(_item_block(row))

    lines.extend(["## 今日行动建议", ""])
    for row in rows[:5]:
        lines.append(f"- {row['suggested_action']}: {row['title']}")
    lines.append("")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"{report_date}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
