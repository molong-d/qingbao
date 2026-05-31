import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from intelligence_hub.src.db import db_counts, init_db, upsert_item
from intelligence_hub.src.fetchers.demo import demo_items


class DbTest(unittest.TestCase):
    def test_init_and_seed_are_idempotent_by_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.db"
            with patch("intelligence_hub.src.db.DB_PATH", db_path), patch("intelligence_hub.src.config.DB_PATH", db_path):
                init_db(db_path)
                first = upsert_item(demo_items()[0])
                second = upsert_item(demo_items()[0])
                self.assertEqual(first, second)
                self.assertEqual(db_counts()["items"], 1)


if __name__ == "__main__":
    unittest.main()
