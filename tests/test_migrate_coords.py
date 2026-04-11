import os
import sqlite3
import tempfile
import pytest
from db import init_db


@pytest.fixture
def file_db():
    """Temp-file SQLite DB with bars table initialised."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    conn = sqlite3.connect(db_path)
    init_db(conn)
    conn.close()
    yield db_path
    os.unlink(db_path)


def test_migrate_adds_latitude_column(file_db):
    from migrate_coords import migrate
    migrate(file_db)
    conn = sqlite3.connect(file_db)
    cur = conn.execute("PRAGMA table_info(bars)")
    columns = {row[1] for row in cur.fetchall()}
    conn.close()
    assert "latitude" in columns


def test_migrate_adds_longitude_column(file_db):
    from migrate_coords import migrate
    migrate(file_db)
    conn = sqlite3.connect(file_db)
    cur = conn.execute("PRAGMA table_info(bars)")
    columns = {row[1] for row in cur.fetchall()}
    conn.close()
    assert "longitude" in columns


def test_migrate_is_idempotent(file_db):
    from migrate_coords import migrate
    migrate(file_db)
    migrate(file_db)  # must not raise
    conn = sqlite3.connect(file_db)
    cur = conn.execute("PRAGMA table_info(bars)")
    columns = [row[1] for row in cur.fetchall()]
    conn.close()
    assert columns.count("latitude") == 1
    assert columns.count("longitude") == 1
