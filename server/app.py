from flask import Flask, request, jsonify
from keys import load_private_key
import socket
import threading
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

private_key = load_private_key()

def broadcast_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_ip = socket.gethostbyname(socket.gethostname())
    while True:
        sock.sendto(f"SERVER_IP:{server_ip}".encode(), ('<broadcast>', 5001))
        threading.Event().wait(5)  # Envoyer un message toutes les 5 secondes

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

if __name__ == '__main__':
    threading.Thread(target=broadcast_server).start()
    app.run(host='0.0.0.0', port=5000)
