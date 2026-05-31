from intelligence_hub.src.config import load_config
from intelligence_hub.src.models import Item


def classify_item(item: Item) -> str:
    topics = load_config("topics.yaml")["topics"]
    text = f"{item.title} {item.summary}".lower()
    best_topic = topics[0]["name"]
    best_hits = -1
    for topic in topics:
        hits = sum(1 for kw in topic["keywords"] if kw.lower() in text)
        if hits > best_hits:
            best_hits = hits
            best_topic = topic["name"]
    return item.topic or best_topic
