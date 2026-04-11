import sqlite3
import sys


def migrate(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("ALTER TABLE bars ADD COLUMN latitude REAL")
        conn.execute("ALTER TABLE bars ADD COLUMN longitude REAL")
        conn.commit()
        print("Migration complete: added latitude, longitude columns.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Columns already exist, skipping.")
        else:
            raise
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "butecos.db"
    migrate(db_path)
