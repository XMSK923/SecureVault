from datetime import datetime, timezone
from pathlib import Path

from models.vault_file import VaultFile
from storage.vault_repository import VaultRepository


class VaultService:

    def __init__(self, repository: VaultRepository):
        self.repository = repository

    def register_file(
        self,
        encrypted_path: str,
        original_name: str | None = None
    ) -> VaultFile:
        """Register an existing encrypted file in the vault."""

        path = Path(encrypted_path)

        if not path.exists():
            raise FileNotFoundError(
                "The encrypted file does not exist."
            )

        if not path.is_file():
            raise ValueError(
                "The selected path is not a file."
            )

        path = path.resolve()

        if original_name is None:
            if path.name.endswith(".svault"):
                original_name = path.name[:-len(".svault")]
            else:
                original_name = path.name

        if not original_name.strip():
            raise ValueError("Original filename cannot be empty.")

        file = VaultFile(
            original_name=original_name.strip(),
            encrypted_path=str(path),
            file_size=path.stat().st_size,
            created_at=datetime.now(timezone.utc).isoformat()
        )

        return self.repository.add_file(file)

    def get_file(self, file_id: int) -> VaultFile | None:
        """Retrieve a vault file by its ID."""

        return self.repository.get_file(file_id)

    def list_files(self) -> list[VaultFile]:
        """Retrieve all registered vault files."""

        return self.repository.list_files()

    def remove_file(self, file_id: int) -> bool:
        """Remove a vault record without deleting the actual file."""

        return self.repository.remove_file(file_id)