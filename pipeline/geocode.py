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


def build_params(street: str | None, street_number: str | None,
                 city: str | None, state: str | None) -> dict:
    street_val = f"{street or ''} {street_number or ''}".strip() or None
    return {k: v for k, v in {
        "street": street_val,
        "city": city,
        "state": state,
    }.items() if v}


def _fallback_params(street: str | None, street_number: str | None,
                     neighborhood: str | None, city: str | None,
                     state: str | None) -> list[tuple[str, dict]]:
    """Return (label, params) pairs to try when the primary query fails."""
    fallbacks = []

    # 1. Structured — drop street type prefix (first word)
    if street:
        words = street.split(None, 1)
        if len(words) == 2:
            street_name_only = f"{words[1]} {street_number or ''}".strip()
            fallbacks.append(("without street prefix", {
                k: v for k, v in {
                    "street": street_name_only,
                    "city": city,
                    "state": state,
                }.items() if v
            }))

    # 2. Free-text with neighborhood (the original approach)
    street_part = f"{street or ''} {street_number or ''}".strip() or None
    parts = [p for p in [street_part, neighborhood, city, state] if p]
    if parts:
        fallbacks.append(("free-text with neighborhood", {"q": ", ".join(parts)}))

    # 3. Free-text neighborhood-only — coarse fallback
    parts3 = [p for p in [neighborhood, city, state] if p]
    if parts3:
        fallbacks.append(("neighborhood only", {"q": ", ".join(parts3)}))

    return fallbacks


def geocode_address(params: dict) -> tuple[float, float] | None:
    base: dict = {"format": "json", "limit": 1}
    if "q" not in params:
        base["countrycodes"] = "br"
    url = f"{NOMINATIM_URL}?{urllib.parse.urlencode({**base, **params})}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        results = json.loads(resp.read())
    if results:
        return round(float(results[0]["lat"]), 7), round(float(results[0]["lon"]), 7)
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

            params = build_params(street, street_number, city, state)
            if not params:
                print(f"[SKIP] bar_id={bar_id}: no address fields")
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
                    continue

                # Primary query failed — try fallbacks.
                resolved = False
                for label, fallback_params in _fallback_params(
                    street, street_number, neighborhood, city, state
                ):
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
                        resolved = True
                        break

                if not resolved:
                    print(f"[FAIL] bar_id={bar_id}: no results (all fallbacks tried)")

            except Exception as e:
                print(f"[ERROR] bar_id={bar_id}: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "butecos.db"
    run(db_path)
