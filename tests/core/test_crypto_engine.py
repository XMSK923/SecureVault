
import unittest

from core.crypto_engine import encrypt_bytes, decrypt_bytes


class TestCryptoEngine(unittest.TestCase):

    def setUp(self):
        self.original_data = b"Hello from SecureVault!"
        self.password = "TestPassword123!"

    def test_encryption_and_decryption(self):
        encrypted = encrypt_bytes(
            self.original_data,
            self.password
        )

        decrypted = decrypt_bytes(
            encrypted,
            self.password
        )

        self.assertEqual(decrypted, self.original_data)

    def test_wrong_password(self):
        encrypted = encrypt_bytes(
            self.original_data,
            self.password
        )

        with self.assertRaises(ValueError):
            decrypt_bytes(encrypted, "WrongPassword!")

    def test_tampered_file(self):
        encrypted = bytearray(
            encrypt_bytes(self.original_data, self.password)
        )

        encrypted[-1] ^= 1

        with self.assertRaises(ValueError):
            decrypt_bytes(bytes(encrypted), self.password)


    def test_empty_password(self):
        with self.assertRaises(ValueError):
            encrypt_bytes(self.original_data, "")

    def test_invalid_file_format(self):
        with self.assertRaises(ValueError):
            decrypt_bytes(b"NOT_A_VAULT_FILE", self.password)

    def test_truncated_file(self):
        encrypted = encrypt_bytes(
            self.original_data,
            self.password
        )

        with self.assertRaises(ValueError):
            decrypt_bytes(encrypted[:20], self.password)

    def test_modified_header(self):
        encrypted = bytearray(
            encrypt_bytes(self.original_data, self.password)
        )

        # Modify the salt inside the header
        encrypted[8] ^= 1

        with self.assertRaises(ValueError):
            decrypt_bytes(bytes(encrypted), self.password)

    def test_empty_file(self):
        encrypted = encrypt_bytes(b"", self.password)

        decrypted = decrypt_bytes(
            encrypted,
            self.password
        )

        self.assertEqual(decrypted, b"")


if __name__ == "__main__":
    unittest.main()
