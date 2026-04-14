import re
from typing import TypedDict


_NEIGHBORHOOD_CORRECTIONS: dict[str, str] = {
    "Santa Teresa": "Santa Tereza",
}

_PATTERN = re.compile(
    r'^(?P<street>.+?),\s*(?P<number>\d+[A-Za-z]?)\s*'
    r'(?:[–\u2013\u2014-]\s*(?P<complement>[^|]+?))?\s*\|\s*'
    r'(?P<neighborhood>[^,]+),\s*(?P<city>[^–\u2013]+?)\s*[–\u2013]\s*(?P<state>[A-Z]{2})\s*$'
)


class ParsedAddress(TypedDict):
    street: str | None
    street_number: str | None
    complement: str | None
    neighborhood: str | None
    city: str | None
    state: str | None


def parse_address(raw: str | None) -> ParsedAddress:
    empty: ParsedAddress = {
        "street": None,
        "street_number": None,
        "complement": None,
        "neighborhood": None,
        "city": None,
        "state": None,
    }
    if not raw:
        return empty
    m = _PATTERN.match(raw.strip())
    if not m:
        return empty
    neighborhood_raw = m.group("neighborhood").strip()
    return {
        "street": m.group("street").strip(),
        "street_number": m.group("number").strip(),
        "complement": (m.group("complement") or "").strip() or None,
        "neighborhood": _NEIGHBORHOOD_CORRECTIONS.get(neighborhood_raw, neighborhood_raw),
        "city": m.group("city").strip(),
        "state": m.group("state").strip(),
    }
