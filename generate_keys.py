import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Créer le dossier 'keys' s'il n'existe pas
    keys_dir = 'keys'
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir)

    with open(os.path.join(keys_dir, 'private_key.pem'), 'wb') as private_file:
        private_file.write(private_pem)

    with open(os.path.join(keys_dir, 'public_key.pem'), 'wb') as public_file:
        public_file.write(public_pem)

    return private_key, public_key

def generate_symmetric_key():
    symmetric_key = os.urandom(32)
    with open(os.path.join('keys', 'symmetric_key.bin'), 'wb') as key_file:
        key_file.write(symmetric_key)
    return symmetric_key

if __name__ == "__main__":
    private_key, public_key = generate_rsa_keys()
    symmetric_key = generate_symmetric_key()
    print("Clés générées et sauvegardées avec succès.")
