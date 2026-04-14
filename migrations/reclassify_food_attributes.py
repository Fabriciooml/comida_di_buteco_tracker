#!/usr/bin/env python3
"""Re-run classifier on all rows to pick up updated keyword lists."""
import argparse
import sqlite3

from pipeline.parsers.food_classifier import classify_food


def reclassify(conn: sqlite3.Connection) -> None:
    rows = conn.execute(
        "SELECT id, food_name, food_description FROM bars"
    ).fetchall()
    updated = skipped = 0
    for row_id, food_name, food_description in rows:
        if not food_name and not food_description:
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
    print(f"Reclassified {updated} rows. Skipped {skipped} (no food data).")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Reclassify all bars using the updated keyword lists"
    )
    p.add_argument("--db", default="butecos.db")
    args = p.parse_args()

    conn = sqlite3.connect(args.db)
    reclassify(conn)
    conn.close()


if __name__ == "__main__":
    main()
