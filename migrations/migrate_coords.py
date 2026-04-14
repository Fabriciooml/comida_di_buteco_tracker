import sqlite3
import sys


def migrate(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("PRAGMA table_info(bars)")
        existing = {row[1] for row in cur.fetchall()}
        added = []
        for col in ("latitude", "longitude"):
            if col not in existing:
                conn.execute(f"ALTER TABLE bars ADD COLUMN {col} REAL")
                added.append(col)
        if added:
            print(f"Migration complete: added {', '.join(added)} columns.")
        else:
            print("Columns already exist, skipping.")
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "butecos.db"
    migrate(db_path)
