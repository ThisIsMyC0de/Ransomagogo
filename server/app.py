from flask import Flask, request, jsonify
from keys import load_private_key
import socket
import threading
from cryptography.hazmat.primitives import serialization
import signal
import sys

app = Flask(__name__)

private_key = load_private_key()
stop_event = threading.Event()

def broadcast_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_ip = socket.gethostbyname(socket.gethostname())
    while not stop_event.is_set():
        sock.sendto(f"SERVER_IP:{server_ip}".encode(), ('<broadcast>', 5001))
        stop_event.wait(5)  # Envoyer un message toutes les 5 secondes

@app.route('/get_private_key', methods=['POST'])
def get_private_key():
    data = request.json
    if data.get('paid') == True:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return jsonify({'private_key': private_key_pem.decode('utf-8')})
    else:
        return jsonify({'error': 'Paiement non effectué'}), 400

def signal_handler(sig, frame):
    stop_event.set()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    broadcast_thread = threading.Thread(target=broadcast_server)
    broadcast_thread.start()
    app.run(host='0.0.0.0', port=5000)
    broadcast_thread.join()  # Attendre que le thread de broadcast se termine
