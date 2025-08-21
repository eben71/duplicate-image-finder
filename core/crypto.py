from cryptography.fernet import Fernet

from backend.config.settings import settings


def _validate_key(value: str) -> bytes:
    b = value.encode()
    # Try constructing Fernet to validate format early
    try:
        Fernet(b)
    except Exception as e:
        raise ValueError(
            "ENCRYPTION_KEY must be a 32-byte url-safe base64 string. "
            "Generate one with: python -c 'from cryptography.fernet "
            "import Fernet; print(Fernet.generate_key().decode())'"
        ) from e
    return b


FERNET_KEY = _validate_key(settings.ENCRYPTION_KEY)
fernet = Fernet(FERNET_KEY)


def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()
