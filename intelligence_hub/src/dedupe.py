import hashlib

from intelligence_hub.src.models import Item


def item_fingerprint(item: Item) -> str:
    key = item.url.strip() or f"{item.source_name}:{item.title.strip().lower()}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()
