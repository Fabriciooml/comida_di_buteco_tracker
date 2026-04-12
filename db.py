import sqlite3
from models import Bar
from hours_parser import ParsedHours

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS bars (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT NOT NULL,
    address          TEXT,
    street           TEXT,
    street_number    TEXT,
    complement       TEXT,
    neighborhood     TEXT,
    city             TEXT,
    state            TEXT,
    food_name        TEXT,
    food_image_url   TEXT,
    food_description TEXT,
    food_category    TEXT,
    is_vegan         INTEGER,
    is_vegetarian    INTEGER,
    working_hours    TEXT,
    detail_url       TEXT UNIQUE,
    updated_at       TEXT DEFAULT (datetime('now'))
);
"""

UPSERT = """
INSERT INTO bars (name, address, street, street_number, complement, neighborhood, city, state,
                  food_name, food_image_url, food_description, food_category, is_vegan, is_vegetarian,
                  working_hours, detail_url, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
ON CONFLICT(detail_url) DO UPDATE SET
    name             = excluded.name,
    address          = excluded.address,
    street           = excluded.street,
    street_number    = excluded.street_number,
    complement       = excluded.complement,
    neighborhood     = excluded.neighborhood,
    city             = excluded.city,
    state            = excluded.state,
    food_name        = excluded.food_name,
    food_image_url   = excluded.food_image_url,
    food_description = excluded.food_description,
    food_category    = excluded.food_category,
    is_vegan         = excluded.is_vegan,
    is_vegetarian    = excluded.is_vegetarian,
    working_hours    = excluded.working_hours,
    updated_at       = datetime('now');
"""


CREATE_BAR_HOURS_TABLE = """
CREATE TABLE IF NOT EXISTS bar_hours (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    bar_id      INTEGER NOT NULL REFERENCES bars(id),
    day_of_week INTEGER NOT NULL,
    session     INTEGER NOT NULL DEFAULT 1,
    open_time   TEXT NOT NULL,
    close_time  TEXT NOT NULL
);
"""

CREATE_BAR_HOURS_INDEX = """
CREATE INDEX IF NOT EXISTS idx_bar_hours_day ON bar_hours(day_of_week, open_time, close_time);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_TABLE)
    conn.execute(CREATE_BAR_HOURS_TABLE)
    conn.execute(CREATE_BAR_HOURS_INDEX)
    conn.commit()


def upsert_bar(conn: sqlite3.Connection, bar: Bar) -> None:
    conn.execute(UPSERT, (
        bar.name,
        bar.address,
        bar.street,
        bar.street_number,
        bar.complement,
        bar.neighborhood,
        bar.city,
        bar.state,
        bar.food_name,
        bar.food_image_url,
        bar.food_description,
        bar.food_category,
        bar.is_vegan,
        bar.is_vegetarian,
        bar.working_hours,
        bar.detail_url,
    ))
    conn.commit()


def get_bar_id(conn: sqlite3.Connection, detail_url: str) -> int | None:
    cur = conn.execute("SELECT id FROM bars WHERE detail_url = ?", (detail_url,))
    row = cur.fetchone()
    return row[0] if row else None


def upsert_bar_hours(
    conn: sqlite3.Connection, bar_id: int, hours: list[ParsedHours]
) -> None:
    conn.execute("DELETE FROM bar_hours WHERE bar_id = ?", (bar_id,))
    conn.executemany(
        "INSERT INTO bar_hours (bar_id, day_of_week, session, open_time, close_time) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            (bar_id, h["day_of_week"], h["session"], h["open_time"], h["close_time"])
            for h in hours
        ],
    )
    conn.commit()
