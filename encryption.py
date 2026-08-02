import base64
import hashlib

from cryptography.fernet import Fernet

def create_key(master_password):
    password_bytes = master_password.encode()
    hash_value = hashlib.sha256(password_bytes).digest()
    key = base64.urlsafe_b64encode(hash_value)
    return key

def encrypt_data(data, key):
    cipher  = Fernet(key)
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

def decrypt_data(data, key):
    cipher = Fernet(key)
    decrypted = cipher.decrypt(data.encode())
    return decrypted.decode()


