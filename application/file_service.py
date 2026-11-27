
from pathlib import Path

from core.crypto_engine import encrypt_bytes, decrypt_bytes


def encrypt_file(
    input_path: str,
    password: str,
    output_path: str | None = None
) -> str:
    """Encrypt a file and save it as a SecureVault file."""

    source = Path(input_path)

    if not source.exists():
        raise FileNotFoundError("The selected file does not exist.")

    if not source.is_file():
        raise ValueError("The selected path is not a file.")

    if not password:
        raise ValueError("Password cannot be empty.")

    if output_path is None:
        destination = Path(str(source) + ".svault")
    else:
        destination = Path(output_path)

    if source.resolve() == destination.resolve():
        raise ValueError("Input and output paths cannot be identical.")

    if destination.exists():
        raise FileExistsError("The output file already exists.")

    if not destination.parent.is_dir():
        raise FileNotFoundError("The output directory does not exist.")

    data = source.read_bytes()

    encrypted_data = encrypt_bytes(data, password)

    try:
        with destination.open("xb") as file:
            file.write(encrypted_data)

    except OSError:
        destination.unlink(missing_ok=True)
        raise

    return str(destination)


def decrypt_file(
    input_path: str,
    password: str,
    output_path: str | None = None
) -> str:
    """Decrypt a SecureVault file and save the recovered file."""

    source = Path(input_path)

    if not source.exists():
        raise FileNotFoundError("The selected encrypted file does not exist.")

    if not source.is_file():
        raise ValueError("The selected path is not a file.")

    if not password:
        raise ValueError("Password cannot be empty.")

    if source.suffix == ".svault":
        default_name = source.name[:-len(".svault")]
    else:
        default_name = source.name + ".decrypted"

    if output_path is None:
        destination = source.with_name(default_name)
    else:
        destination = Path(output_path)

    if source.resolve() == destination.resolve():
        raise ValueError("Input and output paths cannot be identical.")

    if destination.exists():
        raise FileExistsError("The output file already exists.")

    if not destination.parent.is_dir():
        raise FileNotFoundError("The output directory does not exist.")

    encrypted_data = source.read_bytes()

    # Authentication and decryption happen before writing the output.
    decrypted_data = decrypt_bytes(encrypted_data, password)

    with destination.open("xb") as file:
        file.write(decrypted_data)

    return str(destination)
