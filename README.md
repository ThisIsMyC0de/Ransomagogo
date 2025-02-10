# Ransomagogo

## Description

Ce projet est un ransomware pédagogique destiné à sensibiliser les utilisateurs aux dangers des ransomwares. Il chiffre les fichiers de l'utilisateur avec une clé symétrique chiffrée par une clé publique RSA. Le déchiffrement nécessite une requête à un serveur distant pour obtenir la clé privée.

## Installation

> ⚠️ Attention : ces instructions sont valables pour windows uniquement. En effet, le ransoware ciblant des victimes sous windows, le code doit être compilé sur le même OS (possibilité d'utiliser une VM si vous êtes sous linux).

1. Clonez le dépôt :
   ```bash
   git clone <repository_url>
   cd Ransomagogo

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt

3. Générez les clés RSA et la clé symétrique :
   ```bash
   python generate_keys.py

4. Lancez le serveur :
   ```bash
   python server/app.py

5. Convertissez le client en exécutable :
   ```bash
   pyinstaller --onefile --name=ransomware_client --add-data "keys/public_key.pem:keys" --add-data "keys/symmetric_key.bin:keys" --add-data "client/config.py:client" client/main.py

6. Récupérez l'exécutable généré dans le dossier dist.

## Utilisation

    Lancez le client sur la machine de la victime.
    Cliquez sur "Afficher le message de rançon" pour voir le message.
    Cliquez sur "Payer la rançon" pour envoyer une requête au serveur et déchiffrer les fichiers.