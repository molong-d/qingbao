import json
from collections import defaultdict
from datetime import datetime

from intelligence_hub.src.config import REPORT_DIR
from intelligence_hub.src.db import list_ranked_items


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
    return "\n".join(
        [
            f"### {row['title']}",
            f"- 来源: {row['source_name']}",
            f"- 链接: {row['url']}",
            f"- 领域: {row['topic']}",
            f"- 重要性分: {row['importance_score']}",
            f"- 可信度分: {row['credibility_score']}",
            f"- 相关性分: {row['relevance_score']}",
            f"- 机会分: {row['opportunity_score']}",
            f"- 行动分: {row['action_score']}",
            f"- 命中关键词: {keywords}",
            f"- 命中实体: {entities}",
            f"- 为什么重要: {row['score_reason']} {row['summary']}",
            f"- 建议动作: {row['suggested_action']}",
            "",
        ]
    )


def generate_daily(today: bool = False) -> str:
    report_date = datetime.now().date().isoformat()
    rows = list_ranked_items()
    by_topic = defaultdict(list)
    for row in rows:
        by_topic[row["topic"]].append(row)

    lines = [
        "# 每日个人战略情报简报",
        "",
        f"- 日期: {report_date}",
        f"- 条目数: {len(rows)}",
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
