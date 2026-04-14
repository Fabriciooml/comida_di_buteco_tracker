#!/usr/bin/env python3
"""One-time migration: add food_category, is_vegan, is_vegetarian columns and backfill via LLM."""
import argparse
import sqlite3

from pipeline.parsers.food_classifier import classify_food

NEW_COLUMNS = [
    ("food_category", "TEXT"),
    ("is_vegan", "INTEGER"),
    ("is_vegetarian", "INTEGER"),
]


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def add_columns(conn: sqlite3.Connection) -> None:
    for col, col_type in NEW_COLUMNS:
        if not _column_exists(conn, "bars", col):
            conn.execute(f"ALTER TABLE bars ADD COLUMN {col} {col_type}")
            print(f"  Added column: {col}")
        else:
            print(f"  Column already exists (skipped): {col}")
    conn.commit()


def backfill(conn: sqlite3.Connection) -> None:
    rows = conn.execute(
        "SELECT id, food_name, food_description FROM bars"
    ).fetchall()
    updated = 0
    skipped = 0
    for row_id, food_name, food_description in rows:
        if not food_name and not food_description:
            print(f"  [WARN] No food data for id={row_id}, skipping.")
            skipped += 1
            continue
        result = classify_food(food_name, food_description)
        conn.execute(
            "UPDATE bars SET food_category=?, is_vegan=?, is_vegetarian=? WHERE id=?",
            (result["category"], int(result["is_vegan"]), int(result["is_vegetarian"]), row_id),
        )
        print(
            f"  [{row_id}] {food_name!r} → category={result['category']!r}"
            f" vegan={result['is_vegan']} vegetarian={result['is_vegetarian']}"
        )
        updated += 1
    conn.commit()
    print(f"  Classified {updated} rows. Skipped: {skipped}.")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Migrate bars table to add food category and dietary attributes"
    )
    p.add_argument("--db", default="butecos.db")
    args = p.parse_args()

    conn = sqlite3.connect(args.db)
    print("Step 1: adding columns...")
    add_columns(conn)
    print("Step 2: classifying food attributes...")
    backfill(conn)
    conn.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
