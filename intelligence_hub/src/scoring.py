from datetime import datetime, timezone

from intelligence_hub.src.classify import classify_item
from intelligence_hub.src.config import load_config
from intelligence_hub.src.models import Item, Score


def _parse_dt(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc)


def _recency_multiplier(published_at: str, scoring_cfg: dict) -> float:
    now = datetime.now(timezone.utc)
    published = _parse_dt(published_at)
    if published.tzinfo is None:
        published = published.replace(tzinfo=timezone.utc)
    days = max((now - published).days, 0)
    decay = scoring_cfg["recency_decay"]
    if days == 0:
        return decay["same_day"]
    if days <= 7:
        return decay["week"]
    if days <= 30:
        return decay["month"]
    return decay["older"]


def _matches(needles: list[str], text: str) -> list[str]:
    text_lower = text.lower()
    return sorted({needle for needle in needles if needle.lower() in text_lower})


def suggest_action(action_score: float, scoring_cfg: dict) -> str:
    for row in scoring_cfg["action_thresholds"]:
        if action_score >= row["min"]:
            return row["action"]
    return "A0 忽略"


def score_item(item: Item) -> Score:
    scoring_cfg = load_config("scoring.yaml")
    watchlist = load_config("watchlist.yaml")
    topic = classify_item(item)
    text = f"{item.title} {item.summary} {topic}"
    matched_keywords = _matches(watchlist["keywords"], text)
    matched_entities = _matches(watchlist["entities"], text)
    matched_opportunities = _matches(scoring_cfg["opportunity_keywords"], text)

    source_weight = scoring_cfg["source_weight"].get(item.source_type, 0.7)
    credibility_score = round(min(100, source_weight * 100), 1)
    topic_score = scoring_cfg["topic_weight"] if topic else 0
    keyword_score = len(matched_keywords) * scoring_cfg["keyword_weight"]
    entity_score = len(matched_entities) * scoring_cfg["entity_weight"]
    recency = _recency_multiplier(item.published_at, scoring_cfg)
    baselines = scoring_cfg["score_baselines"]
    opportunity_weights = scoring_cfg["opportunity_signal_weights"]
    action_weights = scoring_cfg["action_score_weights"]

    importance_score = round(min(100, (baselines["importance"] + topic_score + keyword_score + entity_score) * recency), 1)
    relevance_score = round(min(100, baselines["relevance"] + keyword_score + entity_score + topic_score), 1)
    opportunity_score = round(
        min(
            100,
            baselines["opportunity"]
            + len(matched_opportunities) * opportunity_weights["keyword"]
            + len(matched_entities) * opportunity_weights["entity"]
            + len(matched_keywords) * opportunity_weights["watchlist_keyword"],
        ),
        1,
    )
    action_score = round(
        (importance_score * action_weights["importance"])
        + (credibility_score * action_weights["credibility"])
        + (relevance_score * action_weights["relevance"])
        + (opportunity_score * action_weights["opportunity"]),
        1,
    )
    reason = (
        f"命中领域“{topic}”，关键词 {len(matched_keywords)} 个、实体 {len(matched_entities)} 个；"
        f"来源可信度 {credibility_score}，机会信号 {len(matched_opportunities)} 个。"
    )
    return Score(
        importance_score=importance_score,
        credibility_score=credibility_score,
        relevance_score=relevance_score,
        opportunity_score=opportunity_score,
        action_score=action_score,
        matched_keywords=matched_keywords,
        matched_entities=matched_entities,
        score_reason=reason,
        suggested_action=suggest_action(action_score, scoring_cfg),
    )
