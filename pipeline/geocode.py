import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
RATE_LIMIT_SECONDS = 1.0
USER_AGENT = "comida-di-buteco-tracker/1.0"

# Neighborhood name corrections to apply to existing DB rows before geocoding.
_NEIGHBORHOOD_CORRECTIONS = {
    "Santa Teresa": "Santa Tereza",
}


def build_query(row: tuple) -> str:
    street, street_number, neighborhood, city, state = row
    street_part = f"{street or ''} {street_number or ''}".strip() or None
    parts = [p for p in [street_part, neighborhood, city, state] if p]
    return ", ".join(parts)


def _fallback_queries(street: str | None, street_number: str | None,
                      neighborhood: str | None, city: str | None,
                      state: str | None) -> list[tuple[str, str]]:
    """Return (label, query) pairs to try when the primary query fails."""
    fallbacks = []

    # 1. Drop neighborhood
    street_part = f"{street or ''} {street_number or ''}".strip() or None
    parts = [p for p in [street_part, city, state] if p]
    if parts and parts != [p for p in [street_part, neighborhood, city, state] if p]:
        fallbacks.append(("without neighborhood", ", ".join(parts)))

    # 2. Drop street type prefix (first word), keep street name + number + neighborhood
    if street:
        words = street.split(None, 1)
        if len(words) == 2:
            street_name_only = f"{words[1]} {street_number or ''}".strip()
            parts2 = [p for p in [street_name_only, neighborhood, city, state] if p]
            fallbacks.append(("without street prefix", ", ".join(parts2)))

    # 3. Drop street entirely — coarse neighborhood-level fallback
    parts3 = [p for p in [neighborhood, city, state] if p]
    if parts3:
        fallbacks.append(("neighborhood only", ", ".join(parts3)))

    return fallbacks


def geocode_address(query: str) -> tuple[float, float] | None:
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": 1})
    url = f"{NOMINATIM_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        results = json.loads(resp.read())
    if results:
        return float(results[0]["lat"]), float(results[0]["lon"])
    return None


def run(db_path: str = "butecos.db") -> None:
    conn = sqlite3.connect(db_path)
    try:
        # Fix neighborhood typos in already-scraped rows.
        for wrong, correct in _NEIGHBORHOOD_CORRECTIONS.items():
            conn.execute(
                "UPDATE bars SET neighborhood=? WHERE neighborhood=?",
                (correct, wrong),
            )
        conn.commit()

        cur = conn.execute(
            "SELECT id, street, street_number, neighborhood, city, state "
            "FROM bars WHERE latitude IS NULL"
        )
        rows = cur.fetchall()
        print(f"Geocoding {len(rows)} bars...")

        for i, (bar_id, street, street_number, neighborhood, city, state) in enumerate(rows):
            if i > 0:
                time.sleep(RATE_LIMIT_SECONDS)

            addr = (street, street_number, neighborhood, city, state)
            query = build_query(addr)
            if not query:
                print(f"[SKIP] bar_id={bar_id}: no address fields")
                continue

            try:
                result = geocode_address(query)
                if result:
                    lat, lon = result
                    conn.execute(
                        "UPDATE bars SET latitude=?, longitude=? WHERE id=?",
                        (lat, lon, bar_id),
                    )
                    conn.commit()
                    print(f"[OK] bar_id={bar_id}: {lat:.6f}, {lon:.6f}")
                    continue

                # Primary query failed — try fallbacks.
                resolved = False
                for label, fallback_query in _fallback_queries(street, street_number, neighborhood, city, state):
                    time.sleep(RATE_LIMIT_SECONDS)
                    result = geocode_address(fallback_query)
                    if result:
                        lat, lon = result
                        conn.execute(
                            "UPDATE bars SET latitude=?, longitude=? WHERE id=?",
                            (lat, lon, bar_id),
                        )
                        conn.commit()
                        print(f"[OK-FALLBACK({label})] bar_id={bar_id}: {lat:.6f}, {lon:.6f}")
                        resolved = True
                        break

                if not resolved:
                    print(f"[FAIL] bar_id={bar_id}: no results for '{query}' (all fallbacks tried)")

            except Exception as e:
                print(f"[ERROR] bar_id={bar_id}: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "butecos.db"
    run(db_path)
