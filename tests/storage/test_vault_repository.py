import sqlite3
import tempfile
import unittest

from pathlib import Path

from storage.database import Database
from storage.vault_repository import VaultRepository
from models.vault_file import VaultFile


class TestVaultRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        db_path = Path(self.temp_dir.name) / "test.db"

        self.database = Database(db_path)
        self.database.initialize()

        self.repository = VaultRepository(self.database)

        self.file = VaultFile(
            original_name="report.pdf",
            encrypted_path="C:/Vault/report.pdf.svault",
            file_size=2048,
            created_at="2026-11-28T10:00:00"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_file(self):
        added_file = self.repository.add_file(self.file)

        self.assertIsNotNone(added_file.id)
        self.assertEqual(added_file.original_name, "report.pdf")

    def test_get_file(self):
        added_file = self.repository.add_file(self.file)

        retrieved_file = self.repository.get_file(added_file.id)

        self.assertIsNotNone(retrieved_file)
        self.assertEqual(
            retrieved_file.original_name,
            "report.pdf"
        )

    def test_get_nonexistent_file(self):
        result = self.repository.get_file(999)

        self.assertIsNone(result)

    def test_list_files(self):
        self.repository.add_file(self.file)

        second_file = VaultFile(
            original_name="image.png",
            encrypted_path="C:/Vault/image.png.svault",
            file_size=1024,
            created_at="2026-11-28T11:00:00"
        )

        self.repository.add_file(second_file)

        files = self.repository.list_files()

        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].original_name, "report.pdf")
        self.assertEqual(files[1].original_name, "image.png")

    def test_list_empty_vault(self):
        files = self.repository.list_files()

        self.assertEqual(files, [])

    def test_remove_file(self):
        added_file = self.repository.add_file(self.file)

        result = self.repository.remove_file(added_file.id)

        self.assertTrue(result)
        self.assertIsNone(
            self.repository.get_file(added_file.id)
        )

    def test_remove_nonexistent_file(self):
        result = self.repository.remove_file(999)

        self.assertFalse(result)

    def test_duplicate_encrypted_path(self):
        self.repository.add_file(self.file)

        duplicate_file = VaultFile(
            original_name="another_report.pdf",
            encrypted_path="C:/Vault/report.pdf.svault",
            file_size=3000,
            created_at="2026-11-28T12:00:00"
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.add_file(duplicate_file)

    def test_remove_record_preserves_encrypted_file(self):
        encrypted_file = (
            Path(self.temp_dir.name) / "report.pdf.svault"
        )

        encrypted_file.write_bytes(b"encrypted test content")

        file = VaultFile(
            original_name="report.pdf",
            encrypted_path=str(encrypted_file),
            file_size=25,
            created_at="2026-11-28T10:00:00"
        )

        added_file = self.repository.add_file(file)

        self.repository.remove_file(added_file.id)

        self.assertTrue(encrypted_file.exists())


if __name__ == "__main__":
    unittest.main()