import hashlib

def get_password_hash(password: str) -> str:
    # In a real app, use passlib with bcrypt
    # Using SHA-256 for demo purposes since passlib isn't in standard library
    # and we want to minimize dependencies for the base structure
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password
