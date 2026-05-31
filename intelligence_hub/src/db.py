import json
import sqlite3
from pathlib import Path

from intelligence_hub.src.config import DB_PATH
from intelligence_hub.src.dedupe import item_fingerprint
from intelligence_hub.src.models import Item, Score, utc_now_iso


SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    url TEXT,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    summary TEXT,
    published_at TEXT NOT NULL,
    topic TEXT,
    raw_json TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_scores (
    item_id INTEGER PRIMARY KEY,
    importance_score REAL NOT NULL,
    credibility_score REAL NOT NULL,
    relevance_score REAL NOT NULL,
    opportunity_score REAL NOT NULL,
    action_score REAL NOT NULL,
    matched_keywords TEXT NOT NULL,
    matched_entities TEXT NOT NULL,
    score_reason TEXT NOT NULL,
    suggested_action TEXT NOT NULL,
    scored_at TEXT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(item_id, tag),
    FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES items(id)
);
"""


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    if db_path is None:
        db_path = DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path | None = None) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)


def upsert_source(name: str, source_type: str, url: str = "", enabled: bool = True) -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO sources(name, type, url, enabled, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET type=excluded.type, url=excluded.url, enabled=excluded.enabled
            """,
            (name, source_type, url, int(enabled), utc_now_iso()),
        )


def upsert_item(item: Item) -> int:
    fingerprint = item_fingerprint(item)
    now = utc_now_iso()
    with connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO items(
                fingerprint, title, url, source_name, source_type, summary, published_at, topic, raw_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fingerprint,
                item.title,
                item.url,
                item.source_name,
                item.source_type,
                item.summary,
                item.published_at,
                item.topic,
                json.dumps(item.raw, ensure_ascii=False),
                now,
            ),
        )
        row = conn.execute("SELECT id FROM items WHERE fingerprint = ?", (fingerprint,)).fetchone()
        return int(row["id"])


def upsert_score(item_id: int, score: Score) -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO item_scores(
                item_id, importance_score, credibility_score, relevance_score, opportunity_score, action_score,
                matched_keywords, matched_entities, score_reason, suggested_action, scored_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(item_id) DO UPDATE SET
                importance_score=excluded.importance_score,
                credibility_score=excluded.credibility_score,
                relevance_score=excluded.relevance_score,
                opportunity_score=excluded.opportunity_score,
                action_score=excluded.action_score,
                matched_keywords=excluded.matched_keywords,
                matched_entities=excluded.matched_entities,
                score_reason=excluded.score_reason,
                suggested_action=excluded.suggested_action,
                scored_at=excluded.scored_at
            """,
            (
                item_id,
                score.importance_score,
                score.credibility_score,
                score.relevance_score,
                score.opportunity_score,
                score.action_score,
                json.dumps(score.matched_keywords, ensure_ascii=False),
                json.dumps(score.matched_entities, ensure_ascii=False),
                score.score_reason,
                score.suggested_action,
                utc_now_iso(),
            ),
        )


def list_ranked_items(limit: int | None = None) -> list[sqlite3.Row]:
    sql = """
        SELECT i.*, s.importance_score, s.credibility_score, s.relevance_score, s.opportunity_score,
               s.action_score, s.matched_keywords, s.matched_entities, s.score_reason, s.suggested_action
        FROM items i
        JOIN item_scores s ON s.item_id = i.id
        ORDER BY s.action_score DESC, s.importance_score DESC, i.published_at DESC
    """
    params: tuple = ()
    if limit:
        sql += " LIMIT ?"
        params = (limit,)
    with connect() as conn:
        return list(conn.execute(sql, params).fetchall())


def db_counts() -> dict[str, int]:
    with connect() as conn:
        return {
            "sources": conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0],
            "items": conn.execute("SELECT COUNT(*) FROM items").fetchone()[0],
            "scores": conn.execute("SELECT COUNT(*) FROM item_scores").fetchone()[0],
            "actions": conn.execute("SELECT COUNT(*) FROM actions").fetchone()[0],
        }


def add_action(item_id: int, label: str, note: str = "") -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO actions(item_id, label, note, created_at) VALUES (?, ?, ?, ?)",
            (item_id, label, note, utc_now_iso()),
        )
