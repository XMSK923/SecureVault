import unittest

from models.vault_file import VaultFile


class TestVaultFile(unittest.TestCase):

    def test_create_vault_file(self):
        file = VaultFile(
            original_name="report.pdf",
            encrypted_path="C:/Vault/report.pdf.svault",
            file_size=2048,
            created_at="2026-11-27T13:30:00+00:00"
        )

        self.assertEqual(file.original_name, "report.pdf")
        self.assertEqual(file.file_size, 2048)

    def test_default_values(self):
        file = VaultFile(
            original_name="image.png",
            encrypted_path="C:/Vault/image.png.svault",
            file_size=1024,
            created_at="2026-11-27T13:30:00+00:00"
        )

        self.assertIsNone(file.id)
        self.assertEqual(file.algorithm, "AES-256-GCM")
        self.assertEqual(file.format_version, 1)

    def test_custom_id(self):
        file = VaultFile(
            original_name="notes.txt",
            encrypted_path="C:/Vault/notes.txt.svault",
            file_size=500,
            created_at="2026-11-27T13:30:00+00:00",
            id=15
        )

        self.assertEqual(file.id, 15)

    def test_missing_required_attribute(self):
        with self.assertRaises(TypeError):
            VaultFile(
                original_name="report.pdf",
                encrypted_path="C:/Vault/report.pdf.svault",
                file_size=2048
            )


if __name__ == "__main__":
    unittest.main()