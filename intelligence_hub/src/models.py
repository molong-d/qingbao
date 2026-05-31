from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Item:
    title: str
    url: str
    source_name: str
    source_type: str = "demo"
    summary: str = ""
    published_at: str = field(default_factory=utc_now_iso)
    topic: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class Score:
    importance_score: float
    credibility_score: float
    relevance_score: float
    opportunity_score: float
    action_score: float
    matched_keywords: list[str]
    matched_entities: list[str]
    score_reason: str
    suggested_action: str
