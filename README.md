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

## To Do List

- [x] Génération des clés
- [x] Client + Serveur 
- [x] Faire un script d'automatisation
- [x] Ajout de l'UI propre
- [x] Changer la méthode utilisée : la clé privé reste sur le serveur, on ne donne que la clé symétrique déchiffrée
- [x] Indiquer à l'utilisateur si son PC n'arrive pas à joindre le serveur (problème de connexion = impossibilité de recevoir la clé)
- [ ] Commenter le code
- [x] Changement du Wallpaper
- [ ] Bypass de Windows Defender
- [ ] Persistance en ajoutant le programme aux programmes lancés lors du démarrage
- [ ] Ajout BDD côté serveur avec clés générées, MAC de la victime (requête à récupérer pour l'avoir), date d'infection, + d'autres infos
- [ ] Automatiser les requêtes entre le serveur et la base (Pour que la base s'update automatiquement à la création des clés, à la récupération de l'adresse MAC et de la date d'infection)
- [x] Trouver une solution pour générer l'exécutable pour Windows même si l'on est sous Linux (peut-être avec un conteneur ou wine) --> UPDATE : sous linux on peut utiliser py2exe (sinon il aurait mieux fallu utiliser Go comme langage)
- [x] Ajout du timer
- [ ] Synchro du temps avec un ntp
- [ ] Faire en sorte que le client s'autodétruise si la communication avec le serveur ne se fait pas ou au bout des 3 jours ou après le paiement et déchiffrement de tous les fichiers
- [ ] Faire en sorte qu'il soit très difficilement supprimable d'ici là (Faire peut-être des copies à certains endroits. Screenlocker, persistance, utilisation du registre, chargement du ransomware à la place du bureau)
- [ ] Utiliser Https sur le port 443 en priorité puis http sur le port 80 (pour passer les firewalls)
- [ ] Ajout d'un bruteforce pour trouver un port ouvert sur lequel communiquer
- [ ] Ajouter le choix du vecteur à l'utilisateur
- [ ] Obfusquer le code (ex : utiliser une somme de variable pour stocker la clé symétrique en mémoire, utiliser des encodage particuliers)
- [ ] Opsec et obfuscation des adresses ip (pas trop d'idées de comment faire, adressage dynamique ?, en gros essayer d'anonymiser au maximum niveau réseau)
- [ ] Faire de l'élévation de privilèges si le Ransomware n'est pas exécuté avec les droits admin
- [ ] Tester avec un firewall pfsense entre les 2 machines et voir si on peut le bypass
- [ ] Voir si on peut le propager sur le réseau (eternal blue comme wannacry)
- [ ] Tester avec une 2e VM en réseau (monter un système de log Elastic+Kibana)
- [ ] Faire une analyse de log pour voir si on peut récupérer quelques infos
- [ ] Faire une analyse forensic pour voir si on peut récupérer quelques infos
- [ ] Tester avec un véritable transfert de cryptos
- [ ] Création automatique d'un wallet dédié à recevoir le transfert de la cible (l'adresse du wallet sera alors ajouté à la BDD)
- [ ] Faire en sorte que l'attaque soit aussi possible pour Linux
- [ ] Faire en sorte que l'attaque soit aussi poossible pour Mac


