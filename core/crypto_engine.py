
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from core.key_derivation import generate_salt, derive_key
from core.file_format import (
    FileHeader,
    parse_header,
    NONCE_LENGTH,
    HEADER_SIZE,
    LOG_N,
    SCRYPT_R,
    SCRYPT_P,
)


def encrypt_bytes(data: bytes, password: str) -> bytes:
    """Encrypt bytes and return a complete SecureVault file."""

    salt = generate_salt()
    nonce = os.urandom(NONCE_LENGTH)

    key = derive_key(password, salt)

    header = FileHeader(
        version=1,
        log_n=LOG_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        salt=salt,
        nonce=nonce,
    )

    header_bytes = header.to_bytes()

    aes = AESGCM(key)

    encrypted_data = aes.encrypt(
        nonce,
        data,
        header_bytes
    )

    return header_bytes + encrypted_data


def decrypt_bytes(encrypted_file: bytes, password: str) -> bytes:
    """Decrypt a SecureVault file and return the original bytes."""

    if len(encrypted_file) < HEADER_SIZE + 16:
        raise ValueError("Encrypted file is incomplete.")

    header = parse_header(encrypted_file)
    header_bytes = encrypted_file[:HEADER_SIZE]

    key = derive_key(password, header.salt)

    aes = AESGCM(key)

    encrypted_data = encrypted_file[HEADER_SIZE:]

    try:
        return aes.decrypt(
            header.nonce,
            encrypted_data,
            header_bytes
        )

    except InvalidTag:
        raise ValueError(
            "Decryption failed: incorrect password or corrupted file."
        ) from None
