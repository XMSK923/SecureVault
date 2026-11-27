from dataclasses import dataclass


@dataclass
class VaultFile:
    original_name: str
    encrypted_path: str
    file_size: int
    created_at: str

    id: int | None = None
    algorithm: str = "AES-256-GCM"
    format_version: int = 1