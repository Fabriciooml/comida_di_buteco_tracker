import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
RATE_LIMIT_SECONDS = 1.0
USER_AGENT = "comida-di-buteco-tracker/1.0"


def build_query(row: tuple) -> str:
    street, street_number, neighborhood, city, state = row
    street_part = f"{street or ''} {street_number or ''}".strip() or None
    parts = [p for p in [street_part, neighborhood, city, state] if p]
    return ", ".join(parts)


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
    cur = conn.execute(
        "SELECT id, street, street_number, neighborhood, city, state "
        "FROM bars WHERE latitude IS NULL"
    )
    rows = cur.fetchall()
    print(f"Geocoding {len(rows)} bars...")

    for bar_id, *addr_fields in rows:
        query = build_query(tuple(addr_fields))
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
            else:
                print(f"[FAIL] bar_id={bar_id}: no results for '{query}'")
        except Exception as e:
            print(f"[ERROR] bar_id={bar_id}: {e}")
        time.sleep(RATE_LIMIT_SECONDS)

    conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "butecos.db"
    run(db_path)
