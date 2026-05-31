import json
from urllib.error import URLError
from urllib.request import urlopen

from intelligence_hub.src.models import Item, utc_now_iso


def _get_json(url: str, timeout: int):
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch(source: dict, timeout: int = 8) -> tuple[list[Item], list[str]]:
    try:
        ids = _get_json(source["url"], timeout)[:10]
        items: list[Item] = []
        for story_id in ids[:5]:
            story = _get_json(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout)
            title = story.get("title", "")
            url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            if title:
                items.append(Item(title=title, url=url, source_name=source["name"], source_type="hackernews", summary="", published_at=utc_now_iso(), raw={"hn_id": story_id}))
        return items, []
    except (URLError, TimeoutError, OSError, json.JSONDecodeError, TypeError) as exc:
        return [], [f"hackernews:{source['name']} failed: {exc}"]
