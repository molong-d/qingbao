import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from intelligence_hub.src.models import Item, utc_now_iso
from intelligence_hub.src.text import clean_text


def fetch(source: dict, timeout: int = 8) -> tuple[list[Item], list[str]]:
    request = Request(source["url"], headers={"User-Agent": "qingbao-intelligence-hub"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return [], [f"github:{source['name']} failed: {exc}"]

    items: list[Item] = []
    for repo in payload.get("items", [])[:10]:
        title = clean_text(repo.get("full_name") or repo.get("name"))
        url = repo.get("html_url", "")
        summary = clean_text(repo.get("description") or "")
        published = repo.get("updated_at") or utc_now_iso()
        if title and url:
            items.append(Item(title=title, url=url, source_name=source["name"], source_type="github", summary=summary, published_at=published))
    return items, []
