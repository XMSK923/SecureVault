
from dataclasses import dataclass


MAGIC = b"SVLT"
VERSION = 1

HEADER_SIZE = 4 + 1 + 3 + 16 + 12

# Parameters supported by this version
LOG_N = 15
SCRYPT_R = 8
SCRYPT_P = 1

SALT_LENGTH = 16
NONCE_LENGTH = 12


@dataclass
class FileHeader:
    version: int
    log_n: int
    r: int
    p: int
    salt: bytes
    nonce: bytes

    def to_bytes(self) -> bytes:
        return (
            MAGIC
            + bytes([
                self.version,
                self.log_n,
                self.r,
                self.p
            ])
            + self.salt
            + self.nonce
        )


def parse_header(data: bytes) -> FileHeader:
    if len(data) < HEADER_SIZE:
        raise ValueError("Encrypted file is too short.")

    if data[:4] != MAGIC:
        raise ValueError("Not a SecureVault file.")

    version = data[4]
    log_n, r, p = data[5:8]

    if version != VERSION:
        raise ValueError("Unsupported file version.")

    if (log_n, r, p) != (LOG_N, SCRYPT_R, SCRYPT_P):
        raise ValueError("Unsupported encryption parameters.")

    salt = data[8:24]
    nonce = data[24:36]

    return FileHeader(
        version=version,
        log_n=log_n,
        r=r,
        p=p,
        salt=salt,
        nonce=nonce
    )
