import sqlite3
from pipeline.models import Bar
from pipeline.db import init_db, upsert_bar, upsert_bar_hours, get_bar_id


def test_init_db_creates_table(mem_db):
    init_db(mem_db)
    cur = mem_db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bars'"
    )
    assert cur.fetchone() is not None


def test_upsert_inserts_bar(mem_db):
    init_db(mem_db)
    bar = Bar(
        name="Bar Teste",
        address="Rua A, 1 | Centro, Belo Horizonte – MG",
        street="Rua A",
        street_number="1",
        neighborhood="Centro",
        city="Belo Horizonte",
        state="MG",
        food_name="Petisco",
        food_image_url="https://img.com/pic.jpg",
        food_description="Delicioso.",
        working_hours="Seg–Sex 18h–23h",
        detail_url="https://comidadibuteco.com.br/butecos/bar-teste/",
    )
    upsert_bar(mem_db, bar)
    cur = mem_db.execute(
        "SELECT name, food_name, street, street_number, neighborhood, city, state"
        " FROM bars WHERE detail_url=?",
        (bar.detail_url,),
    )
    row = cur.fetchone()
    assert row[0] == "Bar Teste"
    assert row[1] == "Petisco"
    assert row[2] == "Rua A"
    assert row[3] == "1"
    assert row[4] == "Centro"
    assert row[5] == "Belo Horizonte"
    assert row[6] == "MG"


def test_upsert_is_idempotent(mem_db):
    init_db(mem_db)
    bar = Bar(name="Bar Idem", detail_url="https://comidadibuteco.com.br/butecos/bar-idem/")
    upsert_bar(mem_db, bar)
    upsert_bar(mem_db, bar)
    cur = mem_db.execute("SELECT count(*) FROM bars")
    assert cur.fetchone()[0] == 1


def test_upsert_updates_existing_record(mem_db):
    init_db(mem_db)
    url = "https://comidadibuteco.com.br/butecos/bar-update/"
    bar_v1 = Bar(name="Bar V1", food_name="Antigo", detail_url=url)
    bar_v2 = Bar(name="Bar V1", food_name="Novo", detail_url=url)
    upsert_bar(mem_db, bar_v1)
    upsert_bar(mem_db, bar_v2)
    cur = mem_db.execute("SELECT food_name FROM bars WHERE detail_url=?", (url,))
    assert cur.fetchone()[0] == "Novo"


def test_init_db_creates_bar_hours_table(mem_db):
    init_db(mem_db)
    cur = mem_db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bar_hours'"
    )
    assert cur.fetchone() is not None


def _insert_bar(conn, url="https://comidadibuteco.com.br/butecos/bar-h/"):
    init_db(conn)
    bar = Bar(name="Bar H", detail_url=url)
    upsert_bar(conn, bar)
    return get_bar_id(conn, url)


def test_get_bar_id_returns_correct_id(mem_db):
    bar_id = _insert_bar(mem_db)
    assert isinstance(bar_id, int)


def test_get_bar_id_returns_none_for_unknown(mem_db):
    init_db(mem_db)
    assert get_bar_id(mem_db, "https://not-here.com/") is None


_SAMPLE_HOURS = [
    {"day_of_week": 5, "session": 1, "open_time": "17:00", "close_time": "23:00"},
    {"day_of_week": 6, "session": 1, "open_time": "12:00", "close_time": "23:00"},
]


def test_upsert_bar_hours_inserts_rows(mem_db):
    bar_id = _insert_bar(mem_db)
    upsert_bar_hours(mem_db, bar_id, _SAMPLE_HOURS)
    cur = mem_db.execute(
        "SELECT day_of_week, open_time, close_time FROM bar_hours WHERE bar_id=? ORDER BY day_of_week",
        (bar_id,),
    )
    rows = cur.fetchall()
    assert len(rows) == 2
    assert rows[0] == (5, "17:00", "23:00")
    assert rows[1] == (6, "12:00", "23:00")


def test_upsert_bar_hours_is_idempotent(mem_db):
    bar_id = _insert_bar(mem_db)
    upsert_bar_hours(mem_db, bar_id, _SAMPLE_HOURS)
    upsert_bar_hours(mem_db, bar_id, _SAMPLE_HOURS)
    cur = mem_db.execute("SELECT count(*) FROM bar_hours WHERE bar_id=?", (bar_id,))
    assert cur.fetchone()[0] == 2


def test_upsert_bar_hours_replaces_on_rescrape(mem_db):
    bar_id = _insert_bar(mem_db)
    upsert_bar_hours(mem_db, bar_id, _SAMPLE_HOURS)
    new_hours = [{"day_of_week": 7, "session": 1, "open_time": "11:00", "close_time": "18:00"}]
    upsert_bar_hours(mem_db, bar_id, new_hours)
    cur = mem_db.execute(
        "SELECT day_of_week FROM bar_hours WHERE bar_id=?", (bar_id,)
    )
    rows = cur.fetchall()
    assert len(rows) == 1
    assert rows[0][0] == 7


def test_upsert_bar_hours_empty_list_clears_rows(mem_db):
    bar_id = _insert_bar(mem_db)
    upsert_bar_hours(mem_db, bar_id, _SAMPLE_HOURS)
    upsert_bar_hours(mem_db, bar_id, [])
    cur = mem_db.execute("SELECT count(*) FROM bar_hours WHERE bar_id=?", (bar_id,))
    assert cur.fetchone()[0] == 0


def test_schema_has_food_attribute_columns(mem_db):
    init_db(mem_db)
    cur = mem_db.execute("PRAGMA table_info(bars)")
    columns = {row[1] for row in cur.fetchall()}
    assert "food_category" in columns
    assert "is_vegan" in columns
    assert "is_vegetarian" in columns


def test_upsert_persists_food_attributes(mem_db):
    init_db(mem_db)
    bar = Bar(
        name="Bar Vegano",
        detail_url="https://comidadibuteco.com.br/butecos/bar-vegano/",
        food_name="Bolinho de cenoura",
        food_description="Bolinho crocante de cenoura e tofu.",
        food_category="bolinhos",
        is_vegan=True,
        is_vegetarian=True,
    )
    upsert_bar(mem_db, bar)
    cur = mem_db.execute(
        "SELECT food_category, is_vegan, is_vegetarian FROM bars WHERE detail_url=?",
        (bar.detail_url,),
    )
    row = cur.fetchone()
    assert row[0] == "bolinhos"
    assert bool(row[1]) is True
    assert bool(row[2]) is True
