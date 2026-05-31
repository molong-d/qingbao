from urllib.error import URLError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from intelligence_hub.src.models import Item, utc_now_iso


NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch(source: dict, timeout: int = 8) -> tuple[list[Item], list[str]]:
    try:
        with urlopen(source["url"], timeout=timeout) as response:
            body = response.read()
    except (URLError, TimeoutError, OSError) as exc:
        return [], [f"arxiv:{source['name']} failed: {exc}"]

    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        return [], [f"arxiv:{source['name']} parse failed: {exc}"]

    items: list[Item] = []
    for entry in root.findall("atom:entry", NS)[:10]:
        title = " ".join((entry.findtext("atom:title", default="", namespaces=NS) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=NS) or "").split())
        url = ""
        for link in entry.findall("atom:link", NS):
            if link.attrib.get("href"):
                url = link.attrib["href"]
                break
        published = entry.findtext("atom:published", default=utc_now_iso(), namespaces=NS)
        if title and url:
            items.append(Item(title=title, url=url, source_name=source["name"], source_type="arxiv", summary=summary, published_at=published))
    return items, []
