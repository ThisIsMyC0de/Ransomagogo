from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_private_key():
    with open('keys/private_key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key
