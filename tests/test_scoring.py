import unittest

from intelligence_hub.src.fetchers.demo import demo_items
from intelligence_hub.src.scoring import score_item


class ScoringTest(unittest.TestCase):
    def test_score_contains_required_fields(self):
        score = score_item(demo_items()[0])
        self.assertGreater(score.importance_score, 0)
        self.assertGreater(score.credibility_score, 0)
        self.assertTrue(score.suggested_action.startswith("A"))
        self.assertIsInstance(score.matched_keywords, list)


if __name__ == "__main__":
    unittest.main()
