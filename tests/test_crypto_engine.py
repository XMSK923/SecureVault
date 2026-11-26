
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


if __name__ == "__main__":
    unittest.main()
