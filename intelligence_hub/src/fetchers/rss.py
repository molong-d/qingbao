from urllib.error import URLError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from intelligence_hub.src.models import Item, utc_now_iso
from intelligence_hub.src.text import clean_text


def fetch(source: dict, timeout: int = 8) -> tuple[list[Item], list[str]]:
    warnings: list[str] = []
    try:
        with urlopen(source["url"], timeout=timeout) as response:
            body = response.read()
    except (URLError, TimeoutError, OSError) as exc:
        return [], [f"rss:{source['name']} failed: {exc}"]

    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        return [], [f"rss:{source['name']} parse failed: {exc}"]

    items: list[Item] = []
    for node in root.findall(".//item")[:10]:
        title = clean_text(node.findtext("title"))
        link = (node.findtext("link") or "").strip()
        summary = clean_text(node.findtext("description"))
        if title and link:
            items.append(Item(title=title, url=link, source_name=source["name"], source_type="rss", summary=summary, published_at=utc_now_iso()))
    return items, warnings
