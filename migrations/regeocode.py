#!/usr/bin/env python3
"""Re-geocode bars that already have coordinates using the improved structured query.

Only updates when a match is found up to fallback 2 (free-text with neighborhood).
The coarse city-only fallback is intentionally skipped to avoid downgrading precision.
"""
import argparse
import sqlite3
import time

from pipeline.geocode import (
    RATE_LIMIT_SECONDS,
    build_params,
    geocode_address,
    _fallback_params,
)

# Stop before the last (coarse) fallback when re-geocoding existing rows.
_MAX_FALLBACKS = 2


def run(db_path: str = "butecos.db") -> None:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "SELECT id, street, street_number, neighborhood, city, state "
            "FROM bars WHERE latitude IS NOT NULL"
        )
        rows = cur.fetchall()
        print(f"Re-geocoding {len(rows)} bars with existing coordinates...")

        updated = skipped = failed = 0
        for i, (bar_id, street, street_number, neighborhood, city, state) in enumerate(rows):
            if i > 0:
                time.sleep(RATE_LIMIT_SECONDS)

            params = build_params(street, street_number, city, state)
            if not params:
                print(f"[SKIP] bar_id={bar_id}: no address fields")
                skipped += 1
                continue

            try:
                result = geocode_address(params)
                if result:
                    lat, lon = result
                    conn.execute(
                        "UPDATE bars SET latitude=?, longitude=? WHERE id=?",
                        (lat, lon, bar_id),
                    )
                    conn.commit()
                    print(f"[OK] bar_id={bar_id}: {lat:.7f}, {lon:.7f}")
                    updated += 1
                    continue

                fallbacks = _fallback_params(street, street_number, neighborhood, city, state)
                resolved = False
                for label, fallback_params in fallbacks[:_MAX_FALLBACKS]:
                    time.sleep(RATE_LIMIT_SECONDS)
                    result = geocode_address(fallback_params)
                    if result:
                        lat, lon = result
                        conn.execute(
                            "UPDATE bars SET latitude=?, longitude=? WHERE id=?",
                            (lat, lon, bar_id),
                        )
                        conn.commit()
                        print(f"[OK-FALLBACK({label})] bar_id={bar_id}: {lat:.7f}, {lon:.7f}")
                        updated += 1
                        resolved = True
                        break

                if not resolved:
                    print(f"[NO-MATCH] bar_id={bar_id}: keeping existing coordinates")
                    failed += 1

            except Exception as e:
                print(f"[ERROR] bar_id={bar_id}: {e}")
                failed += 1

        print(f"\nDone. Updated: {updated}  |  No match: {failed}  |  Skipped: {skipped}")
    finally:
        conn.close()


def main() -> None:
    p = argparse.ArgumentParser(description="Re-geocode bars with improved structured query")
    p.add_argument("--db", default="butecos.db")
    args = p.parse_args()
    run(args.db)


if __name__ == "__main__":
    main()
