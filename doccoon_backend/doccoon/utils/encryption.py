import base64
import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings

# Salt for key derivation - should be consistent across app restarts
# Using a hash of the app name as a stable salt
_SALT = hashlib.sha256(b"doccoon-encryption-salt-v1").digest()


def _get_fernet_key() -> bytes:
    """Derive a Fernet-compatible key from Django's SECRET_KEY using PBKDF2."""
    secret = settings.SECRET_KEY.encode()

    # Use PBKDF2 with SHA256 for secure key derivation
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=480000,  # OWASP recommended minimum for PBKDF2-SHA256
    )

    # Derive a 32-byte key and encode it for Fernet
    derived_key = kdf.derive(secret)
    return base64.urlsafe_b64encode(derived_key)


def _get_fernet() -> Fernet:
    return Fernet(_get_fernet_key())


def encrypt_value(plaintext: str) -> str:
    """Encrypt a string value and return base64-encoded ciphertext."""
    if not plaintext:
        return ""
    fernet = _get_fernet()
    encrypted = fernet.encrypt(plaintext.encode())
    return encrypted.decode()


def decrypt_value(ciphertext: str) -> str:
    """Decrypt a base64-encoded ciphertext and return the original string."""
    if not ciphertext:
        return ""
    fernet = _get_fernet()
    decrypted = fernet.decrypt(ciphertext.encode())
    return decrypted.decode()
