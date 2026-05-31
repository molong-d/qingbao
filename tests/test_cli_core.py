import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from intelligence_hub.src.cli import main
from intelligence_hub.src.db import db_counts


class CliCoreTest(unittest.TestCase):
    def test_core_chain_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "test.db"
            report_dir = Path(tmp) / "reports"
            with patch("intelligence_hub.src.db.DB_PATH", db_path), patch("intelligence_hub.src.digest.REPORT_DIR", report_dir):
                with redirect_stdout(StringIO()):
                    self.assertEqual(main(["init-db"]), 0)
                    self.assertEqual(main(["seed-demo"]), 0)
                    self.assertEqual(main(["seed-demo"]), 0)
                self.assertEqual(db_counts()["items"], 15)
                with redirect_stdout(StringIO()):
                    self.assertEqual(main(["digest", "--today"]), 0)
                self.assertEqual(len(list(report_dir.glob("*.md"))), 1)


if __name__ == "__main__":
    unittest.main()
