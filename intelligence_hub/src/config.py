import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = ROOT / "intelligence_hub"
CONFIG_DIR = PACKAGE_DIR / "config"
DATA_DIR = PACKAGE_DIR / "data"
REPORT_DIR = PACKAGE_DIR / "reports" / "daily"
DB_PATH = DATA_DIR / "intelligence.db"


def load_config(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
