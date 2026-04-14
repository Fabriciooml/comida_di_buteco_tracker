#!/usr/bin/env python3
"""One-time migration: add structured address columns and backfill from address."""
import argparse
import sqlite3

from pipeline.parsers.address_parser import parse_address

NEW_COLUMNS = ["street", "street_number", "complement", "neighborhood", "city", "state"]


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def add_columns(conn: sqlite3.Connection) -> None:
    for col in NEW_COLUMNS:
        if not _column_exists(conn, "bars", col):
            conn.execute(f"ALTER TABLE bars ADD COLUMN {col} TEXT")
            print(f"  Added column: {col}")
        else:
            print(f"  Column already exists (skipped): {col}")
    conn.commit()


def backfill(conn: sqlite3.Connection) -> None:
    rows = conn.execute(
        "SELECT id, address FROM bars WHERE address IS NOT NULL"
    ).fetchall()
    updated = 0
    failed = 0
    for row_id, raw in rows:
        parsed = parse_address(raw)
        if parsed["street"] is None:
            print(f"  [WARN] Could not parse address for id={row_id}: {raw!r}")
            failed += 1
            continue
        conn.execute(
            """UPDATE bars SET
                   street=?, street_number=?, complement=?,
                   neighborhood=?, city=?, state=?
               WHERE id=?""",
            (
                parsed["street"],
                parsed["street_number"],
                parsed["complement"],
                parsed["neighborhood"],
                parsed["city"],
                parsed["state"],
                row_id,
            ),
        )
        updated += 1
    conn.commit()
    print(f"  Backfilled {updated} rows. Parse failures: {failed}.")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Migrate bars table to structured address columns"
    )
    p.add_argument("--db", default="butecos.db")
    args = p.parse_args()

    conn = sqlite3.connect(args.db)
    print("Step 1: adding columns...")
    add_columns(conn)
    print("Step 2: backfilling from address...")
    backfill(conn)
    conn.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
