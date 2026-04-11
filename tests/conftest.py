import sqlite3
import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_html():
    """Load HTML fixture by filename."""
    def _load(name: str) -> str:
        return (FIXTURES_DIR / name).read_text(encoding="utf-8")
    return _load


@pytest.fixture
def mem_db():
    """In-memory SQLite connection for isolation."""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()
