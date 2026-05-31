import argparse
from pathlib import Path

from intelligence_hub import __version__
from intelligence_hub.src.classify import classify_item
from intelligence_hub.src.config import DB_PATH, REPORT_DIR, load_config
from intelligence_hub.src.db import add_action, db_counts, init_db, list_ranked_items, upsert_item, upsert_score, upsert_source
from intelligence_hub.src.digest import generate_daily
from intelligence_hub.src.fetchers.demo import demo_items
from intelligence_hub.src.fetchers.runner import fetch_enabled_sources
from intelligence_hub.src.scoring import score_item


VALID_LABELS = {"useful", "useless", "track", "write", "research", "prototype", "ignore"}


def _ensure_sources() -> None:
    for source in load_config("sources.yaml")["sources"]:
        upsert_source(source["name"], source["type"], source.get("url", ""), bool(source.get("enabled", True)))


def _store_scored(items) -> int:
    count = 0
    for item in items:
        item.topic = classify_item(item)
        item_id = upsert_item(item)
        upsert_score(item_id, score_item(item))
        count += 1
    return count


def cmd_status(_: argparse.Namespace) -> int:
    exists = DB_PATH.exists()
    counts = db_counts() if exists else {"sources": 0, "items": 0, "scores": 0, "actions": 0}
    print(f"Qingbao Intelligence Hub v{__version__}")
    print(f"database: {DB_PATH} ({'exists' if exists else 'missing'})")
    print(f"reports: {REPORT_DIR}")
    print(f"counts: {counts}")
    return 0


def cmd_init_db(_: argparse.Namespace) -> int:
    init_db()
    _ensure_sources()
    print(f"initialized database: {DB_PATH}")
    return 0


def cmd_seed_demo(_: argparse.Namespace) -> int:
    init_db()
    _ensure_sources()
    count = _store_scored(demo_items())
    print(f"seeded/scored demo items: {count}")
    return 0


def cmd_digest(args: argparse.Namespace) -> int:
    init_db()
    path = generate_daily(today=args.today, exclude_demo=args.exclude_demo)
    print(f"generated digest: {path}")
    return 0


def cmd_fetch_once(_: argparse.Namespace) -> int:
    init_db()
    _ensure_sources()
    items, warnings, counts = fetch_enabled_sources()
    count = _store_scored(items)
    for source_name, result in counts.items():
        print(f"source: {source_name}\tstatus: {result['status']}\titems: {result['count']}")
    for warning in warnings:
        print(f"warning: {warning}")
    print(f"fetched/scored items: {count}")
    return 0


def _append_opportunity(row) -> None:
    path = Path("notes/opportunity_log.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# Opportunity Log\n\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"- item_id={row['id']} | score={row['opportunity_score']} | {row['title']} | {row['url']}\n")


def cmd_feedback(args: argparse.Namespace) -> int:
    if args.label not in VALID_LABELS:
        raise SystemExit(f"invalid label: {args.label}; valid labels: {', '.join(sorted(VALID_LABELS))}")
    init_db()
    add_action(args.item_id, args.label)
    if args.label in {"track", "write", "research", "prototype", "useful"}:
        row = next((row for row in list_ranked_items() if row["id"] == args.item_id), None)
        if row and row["opportunity_score"] >= 50:
            _append_opportunity(row)
    print(f"recorded feedback: item_id={args.item_id}, label={args.label}")
    return 0


def cmd_opportunities(args: argparse.Namespace) -> int:
    init_db()
    rows = [row for row in list_ranked_items() if row["opportunity_score"] >= 50][: args.top]
    for row in rows:
        print(f"{row['id']}\t{row['opportunity_score']}\t{row['suggested_action']}\t{row['title']}")
    print(f"opportunities: {len(rows)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m intelligence_hub")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("init-db").set_defaults(func=cmd_init_db)
    sub.add_parser("seed-demo").set_defaults(func=cmd_seed_demo)
    digest = sub.add_parser("digest")
    digest.add_argument("--today", action="store_true")
    digest.add_argument("--exclude-demo", action="store_true", default=None)
    digest.set_defaults(func=cmd_digest)
    sub.add_parser("fetch-once").set_defaults(func=cmd_fetch_once)
    feedback = sub.add_parser("feedback")
    feedback.add_argument("--item-id", type=int, required=True)
    feedback.add_argument("--label", required=True)
    feedback.set_defaults(func=cmd_feedback)
    opportunities = sub.add_parser("opportunities")
    opportunities.add_argument("--top", type=int, default=10)
    opportunities.set_defaults(func=cmd_opportunities)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
