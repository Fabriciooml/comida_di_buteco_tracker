from pipeline.parsers.hours_parser import parse_hours


def test_none_returns_empty():
    assert parse_hours(None) == []


def test_empty_string_returns_empty():
    assert parse_hours("") == []


def test_single_day_single_session():
    r = parse_hours("Sábado: 13h – 0h")
    assert len(r) == 1
    assert r[0] == {"day_of_week": 6, "session": 1, "open_time": "13:00", "close_time": "00:00"}


def test_multiple_days():
    raw = (
        "Terça-feira: 18h – 23h30 | Quarta-feira: 18h – 23h30 | "
        "Quinta-feira: 18h – 23h30 | Sexta-feira: 18h – 23h30 | "
        "Sábado: 18h – 23h30 | Domingo: 18h – 23h30"
    )
    r = parse_hours(raw)
    assert len(r) == 6
    days = [h["day_of_week"] for h in r]
    assert days == [2, 3, 4, 5, 6, 7]
    assert all(h["open_time"] == "18:00" for h in r)
    assert all(h["close_time"] == "23:30" for h in r)


def test_split_session():
    r = parse_hours("Terça-feira: 11h – 15h e 17h30 – 23h")
    assert len(r) == 2
    assert r[0] == {"day_of_week": 2, "session": 1, "open_time": "11:00", "close_time": "15:00"}
    assert r[1] == {"day_of_week": 2, "session": 2, "open_time": "17:30", "close_time": "23:00"}


def test_time_with_minutes():
    r = parse_hours("Quinta-feira: 18h – 23h30")
    assert r[0]["open_time"] == "18:00"
    assert r[0]["close_time"] == "23:30"


def test_midnight_close():
    r = parse_hours("Segunda-feira: 17h – 0h")
    assert r[0]["close_time"] == "00:00"


def test_post_midnight_close():
    r = parse_hours("Terça-feira: 17h – 1h")
    assert r[0]["close_time"] == "01:00"


def test_post_midnight_with_minutes():
    r = parse_hours("Domingo: 18h – 1h30")
    assert r[0]["close_time"] == "01:30"


def test_colon_time_form():
    # One real row mixes "22:20" colon notation
    r = parse_hours("Sábado: 11h – 22:20")
    assert len(r) == 1
    assert r[0]["close_time"] == "22:20"


def test_trailing_pipe_stripped():
    r = parse_hours("Sexta-feira: 18h – 22h30 |")
    assert len(r) == 1
    assert r[0]["open_time"] == "18:00"


def test_trailing_double_pipe_stripped():
    r = parse_hours("Quarta-feira: 18h – 23h | Quinta-feira: 18h – 23h ||")
    assert len(r) == 2


def test_free_form_returns_empty():
    assert parse_hours("Terça a sexta de 17:00 às 23:00 e sábado de 15:00 às 21:00") == []


def test_pipe_l_separator_returns_empty():
    assert parse_hours(
        "Terça à quinta de 17h às 00h l Sexta e sábado de 11h às 00 horas"
    ) == []


def test_comma_day_format_returns_empty():
    assert parse_hours("Terça, das 16h às 23h | Quarta, das 16h às 23h") == []


def test_day_of_week_mapping():
    days = [
        ("Segunda-feira", 1),
        ("Terça-feira", 2),
        ("Quarta-feira", 3),
        ("Quinta-feira", 4),
        ("Sexta-feira", 5),
        ("Sábado", 6),
        ("Domingo", 7),
    ]
    for name, expected in days:
        r = parse_hours(f"{name}: 17h – 23h")
        assert len(r) == 1, f"failed for {name}"
        assert r[0]["day_of_week"] == expected, f"wrong day for {name}"


def test_split_session_session_numbers():
    r = parse_hours("Segunda-feira: 11h – 14h e 17h30 – 23h | Terça-feira: 11h – 14h e 17h30 – 23h")
    assert len(r) == 4
    sessions = [(h["day_of_week"], h["session"]) for h in r]
    assert sessions == [(1, 1), (1, 2), (2, 1), (2, 2)]
