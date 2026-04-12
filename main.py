import argparse
import asyncio
import sqlite3
from db import init_db, upsert_bar, upsert_bar_hours, get_bar_id
from hours_parser import parse_hours
from scraper import scrape_all


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scrape Comida di Buteco BH bars")
    p.add_argument("--db", default="butecos.db", help="SQLite file path (default: butecos.db)")
    p.add_argument("--dry-run", action="store_true", help="Print bars to stdout, no DB writes")
    return p.parse_args()


async def run(args: argparse.Namespace) -> None:
    conn = None
    if not args.dry_run:
        conn = sqlite3.connect(args.db)
        init_db(conn)

    count = 0
    async for bar in scrape_all():
        count += 1
        if args.dry_run:
            print(bar)
        else:
            upsert_bar(conn, bar)
            bar_id = get_bar_id(conn, bar.detail_url)
            if bar_id is not None:
                upsert_bar_hours(conn, bar_id, parse_hours(bar.working_hours))
            print(f"[{count}] {bar.name}")

    if conn is not None:
        conn.close()
        print(f"\nDone. {count} bars written to {args.db}")
    else:
        print(f"\nDry run complete. {count} bars found.")


def main() -> None:
    args = parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
