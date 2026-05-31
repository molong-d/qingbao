import unittest
from unittest.mock import patch

from intelligence_hub.src.fetchers.runner import fetch_enabled_sources
from intelligence_hub.src.models import Item


class FetcherRunnerTest(unittest.TestCase):
    def test_single_source_failure_keeps_other_sources(self):
        sources = {
            "sources": [
                {"name": "bad", "type": "rss", "enabled": True, "url": "bad://source"},
                {"name": "good", "type": "arxiv", "enabled": True, "url": "good://source"},
            ]
        }

        def fake_load_config(name):
            return sources

        def bad_fetch(source):
            return [], ["rss:bad failed: test"]

        def good_fetch(source):
            return [Item(title="Good item", url="test://good", source_name=source["name"], source_type="arxiv")], []

        with patch("intelligence_hub.src.fetchers.runner.load_config", fake_load_config):
            with patch.dict("intelligence_hub.src.fetchers.runner.FETCHERS", {"rss": bad_fetch, "arxiv": good_fetch}, clear=True):
                items, warnings, counts = fetch_enabled_sources()

        self.assertEqual(len(items), 1)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(counts["bad"]["status"], "failed")
        self.assertEqual(counts["bad"]["count"], 0)
        self.assertEqual(counts["good"]["status"], "success")
        self.assertEqual(counts["good"]["count"], 1)


if __name__ == "__main__":
    unittest.main()
