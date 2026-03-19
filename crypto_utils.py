from cryptography.fernet import Fernet
import base64, json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_password(password, master_password, salt):
    f = Fernet(generate_key(master_password, salt))
    return f.encrypt(password.encode()).decode()


def decrypt_password(enc_password, master_password, salt):
    f = Fernet(generate_key(master_password, salt))
    return f.decrypt(enc_password.encode()).decode()


def encrypt_data(data: dict, master_password: str, salt: str) -> str:
    """Encrypt the entire data dictionary to a string."""
    f = Fernet(generate_key(master_password, salt))
    return f.encrypt(json.dumps(data).encode()).decode()


def decrypt_data(enc: str, master_password: str, salt: str) -> dict:
    """Decrypt the data string back to a dictionary."""
    f = Fernet(generate_key(master_password, salt))
    return json.loads(f.decrypt(enc.encode()).decode())