from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_file(file_path, symmetric_key):
    with open(file_path, 'rb') as file:
        iv = file.read(16)
        encrypted_data = file.read()
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)
