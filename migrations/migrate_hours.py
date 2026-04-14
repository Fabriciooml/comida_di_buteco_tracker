#!/usr/bin/env python3
"""One-time migration: parse working_hours and populate bar_hours table."""
import argparse
import sqlite3

from pipeline.db import CREATE_BAR_HOURS_TABLE, CREATE_BAR_HOURS_INDEX, upsert_bar_hours
from pipeline.parsers.hours_parser import parse_hours


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_BAR_HOURS_TABLE)
    conn.execute(CREATE_BAR_HOURS_INDEX)
    conn.commit()


def backfill(conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT id, working_hours FROM bars").fetchall()
    populated = failed = skipped = 0
    for bar_id, raw in rows:
        hours = parse_hours(raw)
        if not hours:
            if raw:
                print(f"  [WARN] Parse failure for id={bar_id}: {raw!r}")
                failed += 1
            else:
                skipped += 1
        upsert_bar_hours(conn, bar_id, hours)
        if hours:
            populated += 1
    print(f"  Populated: {populated}  |  Parse failures: {failed}  |  NULL skipped: {skipped}")


def main() -> None:
    p = argparse.ArgumentParser(description="Populate bar_hours from working_hours")
    p.add_argument("--db", default="butecos.db")
    args = p.parse_args()

    conn = sqlite3.connect(args.db)
    print("Step 1: ensuring bar_hours table exists...")
    ensure_table(conn)
    print("Step 2: backfilling bar_hours from working_hours...")
    backfill(conn)
    conn.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
