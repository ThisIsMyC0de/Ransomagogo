# Ransomagogo

## Description

> ⚠️ Important : Ce projet est un ransomware pédagogique destiné à sensibiliser les utilisateurs aux dangers des ransomwares. Nous insistons sur le fait que c'est un outil de prévention à but éducatif et que nous ne serons pas tenus comme responsables de son utilisation à des fins malveillantes.

Ce programme chiffre les fichiers de l'utilisateur avec une clé symétrique chiffrée par une clé publique RSA. Le déchiffrement nécessite l'envoi d'une requête à un serveur distant pour obtenir la clé privée. Cette clé privée est alors utilisée pour déchiffrer la clé symétrique qui permet de récupérer les fichiers chiffrés par le ransomware.

## Installation

> ⚠️ Attention : ces instructions sont valables pour Windows uniquement. En effet, le ransoware ciblant des victimes sous Windows, le code doit être compilé sur le même OS (possibilité d'utiliser une VM si vous êtes sous Linux). Des modifications seront peut-être apportées plus tard pour régler ce problème de manière transparente.

> ⚠️ A noter : Pour l'instant le Ransomware est détecté par Windows Defender. Pensez donc bien à désactiver votre antivirus le temps que des modifications soient apportées pour les bypasser.

1. Clonez le dépôt :
   ```bash
   git clone <repository_url>
   cd Ransomagogo

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt

## Utilisation

1. Lancez le script ransomagogo.py :
   ```bash
   python ransomagogo.py

2. Suivez les instructions pour modifier l'adresse ip et le port du serveur. 

3. Récupérez l'exécutable du client généré dans le dossier dist.

4. Lancez le client sur la machine de la victime.

5. Cliquez sur "Afficher le message de rançon" pour voir le message.

6. Cliquez sur "Payer la rançon" pour envoyer une requête au serveur et déchiffrer les fichiers.