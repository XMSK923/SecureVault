import sqlite3
import tempfile
import unittest

from pathlib import Path

from storage.database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.db_path = (
            Path(self.temp_dir.name)
            / "test_folder"
            / "test.db"
        )

        self.database = Database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialize_creates_database(self):
        self.database.initialize()

        self.assertTrue(self.db_path.exists())

    def test_initialize_creates_vault_table(self):
        self.database.initialize()

        with self.database.connect() as connection:
            result = connection.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = 'vault_files'
            """)

            self.assertIsNotNone(result.fetchone())

    def test_initialize_does_not_delete_existing_data(self):
        self.database.initialize()

        with self.database.connect() as connection:
            connection.execute("""
                INSERT INTO vault_files (
                    original_name,
                    encrypted_path,
                    file_size,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                "report.pdf",
                "C:/Vault/report.pdf.svault",
                2048,
                "2026-11-28T10:00:00"
            ))

        self.database.initialize()

        with self.database.connect() as connection:
            result = connection.execute(
                "SELECT original_name FROM vault_files"
            )

            self.assertEqual(
                result.fetchone()["original_name"],
                "report.pdf"
            )

    def test_connection_rolls_back_on_error(self):
        self.database.initialize()

        with self.assertRaises(RuntimeError):
            with self.database.connect() as connection:
                connection.execute("""
                    INSERT INTO vault_files (
                        original_name,
                        encrypted_path,
                        file_size,
                        created_at
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    "report.pdf",
                    "C:/Vault/report.pdf.svault",
                    2048,
                    "2026-11-28T10:00:00"
                ))

                raise RuntimeError("Simulated database error")

        with self.database.connect() as connection:
            result = connection.execute(
                "SELECT COUNT(*) FROM vault_files"
            )

            self.assertEqual(result.fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()