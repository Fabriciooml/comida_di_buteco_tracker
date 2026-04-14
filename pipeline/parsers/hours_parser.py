import re
from typing import TypedDict


_DAY_MAP = {
    "segunda-feira": 1,
    "terça-feira":   2,
    "quarta-feira":  3,
    "quinta-feira":  4,
    "sexta-feira":   5,
    "sábado":        6,
    "domingo":       7,
}

_TIME_RE = re.compile(r'^(\d{1,2})(?:h(\d{2})?|:(\d{2}))$')


class ParsedHours(TypedDict):
    day_of_week: int
    session:     int
    open_time:   str
    close_time:  str


def _parse_time(token: str) -> str:
    m = _TIME_RE.match(token.strip())
    if not m:
        raise ValueError(f"unrecognised time token: {token!r}")
    hour = int(m.group(1))
    minutes = m.group(2) or m.group(3) or "00"
    return f"{hour:02d}:{minutes}"


def _parse_segment(seg: str) -> list[ParsedHours]:
    day_raw, _, time_expr = seg.partition(":")
    day_key = day_raw.strip().lower()
    if day_key not in _DAY_MAP:
        raise KeyError(day_key)
    day_of_week = _DAY_MAP[day_key]

    sessions_raw = time_expr.strip().split(" e ")
    result: list[ParsedHours] = []
    for session_idx, range_str in enumerate(sessions_raw, start=1):
        parts = range_str.split("\u2013")  # en-dash
        if len(parts) != 2:
            raise ValueError(f"expected 'open – close', got: {range_str!r}")
        open_time = _parse_time(parts[0])
        close_time = _parse_time(parts[1])
        result.append({
            "day_of_week": day_of_week,
            "session":     session_idx,
            "open_time":   open_time,
            "close_time":  close_time,
        })
    return result


def parse_hours(raw: str | None) -> list[ParsedHours]:
    if not raw:
        return []
    cleaned = raw.strip().rstrip("|").rstrip()
    segments = [s.strip() for s in cleaned.split(" | ") if s.strip()]
    result: list[ParsedHours] = []
    for seg in segments:
        try:
            result.extend(_parse_segment(seg))
        except (ValueError, KeyError):
            return []
    return result
