import sqlite3
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()
DB_PATH = Path(__file__).parent.parent.parent / "butecos.db"


def get_bars(db_path: str | None = None) -> list[dict]:
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(
            "SELECT id, name, latitude, longitude, food_name, food_image_url, "
            "food_description, food_category, is_vegan, is_vegetarian, address, working_hours "
            "FROM bars WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.get("/bars")
def list_bars() -> list[dict]:
    return get_bars()
