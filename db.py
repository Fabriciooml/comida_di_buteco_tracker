import sqlite3
from models import Bar

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS bars (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT NOT NULL,
    address          TEXT,
    food_name        TEXT,
    food_image_url   TEXT,
    food_description TEXT,
    working_hours    TEXT,
    detail_url       TEXT UNIQUE,
    updated_at       TEXT DEFAULT (datetime('now'))
);
"""

UPSERT = """
INSERT INTO bars (name, address, food_name, food_image_url, food_description, working_hours, detail_url, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
ON CONFLICT(detail_url) DO UPDATE SET
    name             = excluded.name,
    address          = excluded.address,
    food_name        = excluded.food_name,
    food_image_url   = excluded.food_image_url,
    food_description = excluded.food_description,
    working_hours    = excluded.working_hours,
    updated_at       = datetime('now');
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_TABLE)
    conn.commit()


def upsert_bar(conn: sqlite3.Connection, bar: Bar) -> None:
    conn.execute(UPSERT, (
        bar.name,
        bar.address,
        bar.food_name,
        bar.food_image_url,
        bar.food_description,
        bar.working_hours,
        bar.detail_url,
    ))
    conn.commit()
