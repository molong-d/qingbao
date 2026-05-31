import unittest

from intelligence_hub.src.fetchers.demo import demo_items
from intelligence_hub.src.models import Item
from intelligence_hub.src.scoring import score_item


class ScoringTest(unittest.TestCase):
    def test_score_contains_required_fields(self):
        score = score_item(demo_items()[0])
        self.assertGreater(score.importance_score, 0)
        self.assertGreater(score.credibility_score, 0)
        self.assertTrue(score.suggested_action.startswith("A"))
        self.assertIsInstance(score.matched_keywords, list)

    def test_english_entity_uses_word_boundary(self):
        item = Item(
            title="metadata and metamaterial analysis for metal parts",
            url="test://meta-boundary",
            source_name="test",
            source_type="demo",
            summary="No company names are present.",
            topic="AI 与前沿科技",
        )
        score = score_item(item)
        self.assertNotIn("Meta", score.matched_entities)

    def test_english_entity_matches_token(self):
        item = Item(
            title="Meta releases open model workflow",
            url="test://meta-token",
            source_name="test",
            source_type="demo",
            summary="Meta and open source AI workflow update.",
            topic="产业与公司",
        )
        score = score_item(item)
        self.assertIn("Meta", score.matched_entities)

    def test_high_opportunity_personal_item_gets_stronger_action(self):
        item = Item(
            title="AI workflow 开源项目招聘贡献者并提供 grant",
            url="test://high-opportunity",
            source_name="test",
            source_type="demo",
            summary="招聘 开源 黑客松 资助 API 工具 原型 合作 beta grant workflow",
            topic="个人机会",
        )
        score = score_item(item)
        self.assertGreaterEqual(score.opportunity_score, 80)
        self.assertIn(score.suggested_action[:2], {"A5", "A6", "A7"})


if __name__ == "__main__":
    unittest.main()
