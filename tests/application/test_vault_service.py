import tempfile
import unittest

from pathlib import Path

from storage.database import Database
from storage.vault_repository import VaultRepository
from application.vault_service import VaultService


class TestVaultService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        db_path = self.temp_path / "test.db"

        self.database = Database(db_path)
        self.database.initialize()

        self.repository = VaultRepository(self.database)
        self.service = VaultService(self.repository)

        self.encrypted_file = (
            self.temp_path / "report.pdf.svault"
        )

        self.encrypted_file.write_bytes(
            b"test encrypted content"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_file(self):
        file = self.service.register_file(
            str(self.encrypted_file),
            "report.pdf"
        )

        self.assertIsNotNone(file.id)
        self.assertEqual(file.original_name, "report.pdf")
        self.assertEqual(
            file.file_size,
            self.encrypted_file.stat().st_size
        )

    def test_register_file_infers_original_name(self):
        file = self.service.register_file(
            str(self.encrypted_file)
        )

        self.assertEqual(file.original_name, "report.pdf")

    def test_register_missing_file(self):
        missing_file = self.temp_path / "missing.svault"

        with self.assertRaises(FileNotFoundError):
            self.service.register_file(str(missing_file))

    def test_register_directory(self):
        directory = self.temp_path / "folder"
        directory.mkdir()

        with self.assertRaises(ValueError):
            self.service.register_file(str(directory))

    def test_register_empty_original_name(self):
        with self.assertRaises(ValueError):
            self.service.register_file(
                str(self.encrypted_file),
                "   "
            )

    def test_get_file(self):
        added_file = self.service.register_file(
            str(self.encrypted_file),
            "report.pdf"
        )

        retrieved_file = self.service.get_file(added_file.id)

        self.assertIsNotNone(retrieved_file)
        self.assertEqual(
            retrieved_file.original_name,
            "report.pdf"
        )

    def test_list_files(self):
        self.service.register_file(
            str(self.encrypted_file),
            "report.pdf"
        )

        second_file = self.temp_path / "image.png.svault"
        second_file.write_bytes(b"another encrypted file")

        self.service.register_file(
            str(second_file),
            "image.png"
        )

        files = self.service.list_files()

        self.assertEqual(len(files), 2)

    def test_remove_file_preserves_encrypted_file(self):
        file = self.service.register_file(
            str(self.encrypted_file),
            "report.pdf"
        )

        result = self.service.remove_file(file.id)

        self.assertTrue(result)
        self.assertIsNone(self.service.get_file(file.id))
        self.assertTrue(self.encrypted_file.exists())


if __name__ == "__main__":
    unittest.main()