from flask import Flask, request, jsonify
from keys import load_private_key
import socket
import threading
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import signal
import os
import sys
import configparser
# Ajouter le répertoire parent au chemin de recherche des modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import resource_path

app = Flask(__name__)

private_key = load_private_key()
stop_event = threading.Event()

def load_config():
    config_path = resource_path('server/config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def broadcast_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_ip = socket.gethostbyname(socket.gethostname())
    while not stop_event.is_set():
        sock.sendto(f"SERVER_IP:{server_ip}".encode(), ('<broadcast>', 5001))
        stop_event.wait(5)  # Envoyer un message toutes les 5 secondes

@app.route('/get_symmetric_key', methods=['POST'])
def get_symmetric_key():
    data = request.json
    if data.get('paid') == True:
        encrypted_symmetric_key = bytes.fromhex(data['encrypted_symmetric_key'])
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return jsonify({'symmetric_key': symmetric_key.hex()})
    else:
        return jsonify({'error': 'Paiement non effectué'}), 400


def signal_handler(sig, frame):
    stop_event.set()
    sys.exit(0)

if __name__ == '__main__':
    # Charger la configuration
    config = load_config()
    local_port = int(config['SERVER']['local_port'])

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    broadcast_thread = threading.Thread(target=broadcast_server)
    broadcast_thread.start()
    app.run(host='0.0.0.0', port=local_port)
    broadcast_thread.join()  # Attendre que le thread de broadcast se termine
