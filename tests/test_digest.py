import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from intelligence_hub.src.db import init_db, upsert_item, upsert_score
from intelligence_hub.src.digest import generate_daily
from intelligence_hub.src.fetchers.demo import demo_items
from intelligence_hub.src.scoring import score_item


class DigestTest(unittest.TestCase):
    def test_generate_daily_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.db"
            report_dir = Path(tmp) / "reports"
            with patch("intelligence_hub.src.db.DB_PATH", db_path), patch("intelligence_hub.src.config.DB_PATH", db_path), patch("intelligence_hub.src.digest.REPORT_DIR", report_dir):
                init_db(db_path)
                item = demo_items()[0]
                item_id = upsert_item(item)
                upsert_score(item_id, score_item(item))
                path = Path(generate_daily(today=True))
                self.assertTrue(path.exists())
                self.assertIn("每日个人战略情报简报", path.read_text(encoding="utf-8"))

    def test_generate_daily_overwrites_same_day_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.db"
            report_dir = Path(tmp) / "reports"
            with patch("intelligence_hub.src.db.DB_PATH", db_path), patch("intelligence_hub.src.digest.REPORT_DIR", report_dir):
                init_db(db_path)
                item = demo_items()[0]
                item_id = upsert_item(item)
                upsert_score(item_id, score_item(item))
                path = Path(generate_daily(today=True))
                first_size = path.stat().st_size
                second_path = Path(generate_daily(today=True))
                self.assertEqual(path, second_path)
                self.assertEqual(first_size, second_path.stat().st_size)
                self.assertEqual(second_path.read_text(encoding="utf-8").count(item.title), 3)


if __name__ == "__main__":
    unittest.main()
