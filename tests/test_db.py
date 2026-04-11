import sqlite3
from models import Bar
from db import init_db, upsert_bar


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
        address="Rua A, 1",
        food_name="Petisco",
        food_image_url="https://img.com/pic.jpg",
        food_description="Delicioso.",
        working_hours="Seg–Sex 18h–23h",
        detail_url="https://comidadibuteco.com.br/butecos/bar-teste/",
    )
    upsert_bar(mem_db, bar)
    cur = mem_db.execute("SELECT name, food_name FROM bars WHERE detail_url=?", (bar.detail_url,))
    row = cur.fetchone()
    assert row[0] == "Bar Teste"
    assert row[1] == "Petisco"


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
