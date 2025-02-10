# Ransomagogo

## Description

Ce projet est un ransomware pédagogique destiné à sensibiliser les utilisateurs aux dangers des ransomwares. Il chiffre les fichiers de l'utilisateur avec une clé symétrique chiffrée par une clé publique RSA. Le déchiffrement nécessite une requête à un serveur distant pour obtenir la clé privée.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone <repository_url>
   cd Ransomagogo

2. Installez les dépendances :
   pip3 install -r requirements.txt

3. Générez les clés RSA et la clé symétrique :
   python3 generate_keys.py

4. Lancez le serveur :
   python3 server/app.py

5. Convertissez le client en exécutable :
   pyinstaller --onefile client/main.py

6. Récupérez l'exécutable généré dans le dossier dist.

## Utilisation

    Lancez le client sur la machine de la victime.
    Cliquez sur "Afficher le message de rançon" pour voir le message.
    Cliquez sur "Payer la rançon" pour envoyer une requête au serveur et déchiffrer les fichiers.