from storage.database import Database
from models.vault_file import VaultFile


class VaultRepository:

    def __init__(self, database: Database):
        self.database = database

    @staticmethod
    def _row_to_vault_file(row) -> VaultFile:
        """Convert a database row into a VaultFile object."""

        return VaultFile(
            id=row["id"],
            original_name=row["original_name"],
            encrypted_path=row["encrypted_path"],
            file_size=row["file_size"],
            created_at=row["created_at"],
            algorithm=row["algorithm"],
            format_version=row["format_version"]
        )

    def add_file(self, file: VaultFile) -> VaultFile:
        """Add a new encrypted file record to the database."""

        with self.database.connect() as connection:
            cursor = connection.execute("""
                INSERT INTO vault_files (
                    original_name,
                    encrypted_path,
                    file_size,
                    created_at,
                    algorithm,
                    format_version
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                file.original_name,
                file.encrypted_path,
                file.file_size,
                file.created_at,
                file.algorithm,
                file.format_version
            ))

            file_id = cursor.lastrowid

        return VaultFile(
            id=file_id,
            original_name=file.original_name,
            encrypted_path=file.encrypted_path,
            file_size=file.file_size,
            created_at=file.created_at,
            algorithm=file.algorithm,
            format_version=file.format_version
        )

    def get_file(self, file_id: int) -> VaultFile | None:
        """Retrieve a vault file using its database ID."""

        with self.database.connect() as connection:
            row = connection.execute("""
                SELECT *
                FROM vault_files
                WHERE id = ?
            """, (file_id,)).fetchone()

        if row is None:
            return None

        return self._row_to_vault_file(row)

    def list_files(self) -> list[VaultFile]:
        """Retrieve all registered vault files."""

        with self.database.connect() as connection:
            rows = connection.execute("""
                SELECT *
                FROM vault_files
                ORDER BY id ASC
            """).fetchall()

        return [
            self._row_to_vault_file(row)
            for row in rows
        ]

    def remove_file(self, file_id: int) -> bool:
        """Remove a vault record without deleting the actual file."""

        with self.database.connect() as connection:
            cursor = connection.execute("""
                DELETE FROM vault_files
                WHERE id = ?
            """, (file_id,))

            return cursor.rowcount > 0