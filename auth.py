import json, hashlib, os

AUTH_FILE = "auth.json"

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def setup_master_password():
    if os.path.exists(AUTH_FILE):
        return

    password = input("Set master password: ")
    salt = os.urandom(16).hex()
    hashed = hash_password(password, salt)

    with open(AUTH_FILE, "w") as f:
        json.dump({"hash": hashed, "salt": salt}, f)

def verify_master_password(password):
    with open(AUTH_FILE, "r") as f:
        data = json.load(f)

    hashed = hash_password(password, data["salt"])
    return hashed == data["hash"], data["salt"]