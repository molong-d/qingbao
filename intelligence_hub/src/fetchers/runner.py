from intelligence_hub.src.config import load_config
from intelligence_hub.src.fetchers import arxiv, github, hn, rss


FETCHERS = {
    "rss": rss.fetch,
    "arxiv": arxiv.fetch,
    "github": github.fetch,
    "hackernews": hn.fetch,
}


def fetch_enabled_sources() -> tuple[list, list[str], dict[str, int]]:
    items = []
    counts: dict[str, int] = {}
    warnings: list[str] = []
    for source in load_config("sources.yaml")["sources"]:
        if not source.get("enabled", False) or source["type"] == "demo":
            continue
        fetcher = FETCHERS.get(source["type"])
        if not fetcher:
            warnings.append(f"no fetcher for source type {source['type']}")
            counts[source["name"]] = 0
            continue
        fetched, source_warnings = fetcher(source)
        counts[source["name"]] = len(fetched)
        items.extend(fetched)
        warnings.extend(source_warnings)
    return items, warnings, counts
