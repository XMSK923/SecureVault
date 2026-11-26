
import os

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# Scrypt configuration
SALT_LENGTH = 16
KEY_LENGTH = 32

SCRYPT_N = 2**15 # Controls CPU and memory usage
SCRYPT_R = 8     # Fine-tunes memory access and block size
SCRYPT_P = 1     # Adjusts parallel execution


def generate_salt() -> bytes:
    """Generate a cryptographically secure random salt."""
    return os.urandom(SALT_LENGTH)


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit encryption key from a password."""

    if not password:
        raise ValueError("Password cannot be empty.")

    if len(salt) != SALT_LENGTH:
        raise ValueError("Invalid salt length.")

    kdf = Scrypt(
        salt=salt,
        length=KEY_LENGTH,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )

    return kdf.derive(password.encode("utf-8"))
