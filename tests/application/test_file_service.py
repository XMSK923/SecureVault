
import tempfile
import unittest

from pathlib import Path

from application.file_service import encrypt_file, decrypt_file


class TestFileService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        self.original = self.folder / "document.txt"
        self.original.write_text(
            "This is a SecureVault file test.",
            encoding="utf-8"
        )

        self.password = "TestPassword123!"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_encryption_and_decryption(self):
        encrypted_path = Path(
            encrypt_file(str(self.original), self.password)
        )

        decrypted_path = self.folder / "recovered.txt"

        result = decrypt_file(
            str(encrypted_path),
            self.password,
            str(decrypted_path)
        )

        self.assertEqual(
            Path(result).read_bytes(),
            self.original.read_bytes()
        )

    def test_original_file_is_preserved(self):
        encrypt_file(str(self.original), self.password)

        self.assertTrue(self.original.exists())

    def test_wrong_password_creates_no_output(self):
        encrypted_path = encrypt_file(
            str(self.original),
            self.password
        )

        output_path = self.folder / "recovered.txt"

        with self.assertRaises(ValueError):
            decrypt_file(
                encrypted_path,
                "WrongPassword!",
                str(output_path)
            )

        self.assertFalse(output_path.exists())

    def test_missing_input_file(self):
        missing_file = self.folder / "missing.txt"

        with self.assertRaises(FileNotFoundError):
            encrypt_file(str(missing_file), self.password)

    def test_existing_output_is_not_overwritten(self):
        output_path = self.folder / "existing.svault"
        output_path.write_text("Keep this file!")

        with self.assertRaises(FileExistsError):
            encrypt_file(
                str(self.original),
                self.password,
                str(output_path)
            )

        self.assertEqual(
            output_path.read_text(),
            "Keep this file!"
        )

    def test_corrupted_file_creates_no_output(self):
        encrypted_path = Path(
            encrypt_file(str(self.original), self.password)
        )

        data = bytearray(encrypted_path.read_bytes())
        data[-1] ^= 1
        encrypted_path.write_bytes(data)

        output_path = self.folder / "recovered.txt"

        with self.assertRaises(ValueError):
            decrypt_file(
                str(encrypted_path),
                self.password,
                str(output_path)
            )

        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
