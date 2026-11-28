import os
import sqlite3

from contextlib import contextmanager
from pathlib import Path


class Database:

    def __init__(self, db_path: str | Path | None = None):

        if db_path is None:
            app_data = Path(
                os.environ.get(
                    "LOCALAPPDATA",
                    Path.home() / "AppData" / "Local"
                )
            )

            db_path = app_data / "Aegis" / "aegis.db"

        self.db_path = Path(db_path)

    @contextmanager
    def connect(self):
        """Open a database connection and close it safely."""

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            yield connection
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def initialize(self):
        """Create the database and vault_files table if needed."""

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS vault_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_name TEXT NOT NULL,
                    encrypted_path TEXT NOT NULL UNIQUE,
                    file_size INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    algorithm TEXT NOT NULL DEFAULT 'AES-256-GCM',
                    format_version INTEGER NOT NULL DEFAULT 1
                )
            """)