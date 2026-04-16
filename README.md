Ce projet a pour objectif de migrer un fichier CSV de données patients vers MongoDB, avec un pipeline automatisée qui :

nettoie et valide les données
insère les données dans MongoDB
crée des logs de chaque migration
est conteneurisée pour être facilement déployable avec Docker

Le projet simule un processus réel en entreprise pour gérer des bases de données médicales ou clients.


 ▶️ 1. Prérequis

Avant de lancer le projet, il est nécessaire d’avoir :

- Docker : recommandé pour exécuter le projet dans un environnement isolé et reproductible
- Python : nécessaire pour exécuter le script sans Docker
- MongoDB Compass ou mongosh : pour vérifier les données après la migration


✔ Outils requis

- Python : nécessaire uniquement si vous souhaitez exécuter le script sans Docker
- Docker Desktop : Permet de lancer MongoDB et l’application dans des conteneurs, mais aussi de démarrer plusieurs services en une seule commande
- MongoDB Compass : Interface graphique pour visualiser les données
- mongosh : Permet d’interroger MongoDB en ligne de commande
- requirements.txt installé
- docker-compose.yml présent


▶️ 2. Exécution en local

Le script peut être exécuté sans Docker.

Pour cela l installation des dépendances est nécessaire grace à la commande :
pip install -r requirements.txt

l'éxécution du script se fait grace à la commande :
python migration.py

Cela montre que le script est autonome et ne dépend pas uniquement de Docker.


▶️ 3. Dépendances Python

Le fichier requirements.txt contient les bibliothèques nécessaires au projet :

pandas : lecture et traitement des données CSV
pymongo : connexion et insertion des données dans MongoDB
pytest : framework de tests (outil de vérification du code)

Il permet de recréer facilement le même environnement :
pip install -r requirements.txt


▶️ 4. Tests

Le projet inclut des tests unitaires via le fichier test_validation.py.

Ces tests permettent de vérifier :

la présence des colonnes obligatoires
le nettoyage des données
la gestion des erreurs
Exécution des tests
pytest


▶️ 5. Sécurité

Le projet intègre des bonnes pratiques de base :

utilisation d’une variable d’environnement MONGO_URI
aucune information sensible codée en dur
isolation des services grâce à Docker
accès limité à MongoDB (local ou réseau Docker)

Limite actuelle :

pas d’authentification MongoDB
pas de chiffrement


▶️ 6. Configuration MongoDB

Le script utilise une variable d’environnement MONGO_URI.

En local :
mongodb://localhost:27017/
Avec Docker Compose :
mongodb://mongo:27017/

Cela permet d’utiliser le même script dans plusieurs environnements sans modification.


▶️ 7. Volume + Network

- Network

Un réseau Docker est utilisé pour permettre la communication entre les conteneurs :
networks:
  migration_network:

Le network permet aux services (migration et mongo) de communiquer entre eux.

- Volume

Un volume Docker est utilisé pour conserver les données grace à :
volumes:
  mongo_data:

Montage dans MongoDB :
- mongo_data:/data/db

 Le volume permet de conserver les données même après arrêt des conteneurs

- Architecture

Le projet utilise Docker Compose pour lancer plusieurs éléments ensemble.

On appelle cela une architecture :
la manière dont les éléments sont organisés et communiquent entre eux.

Les 4 éléments :

1 Service MongoDB : stocke les patients et les logs

2 Service de migration Python : lit le CSV, nettoie les données, envoie dans MongoDB

3 Volume MongoDB : conserve les données et évite la perte après redémarrage

4 Réseau Docker : connecte les services entre eux

- Fonctionnement global

Docker démarre MongoDB
Docker démarre le script Python
Le script lit le CSV
Il envoie les données à MongoDB (via le réseau)
MongoDB les stocke dans le volume


▶️ 8. Exemple de log

Chaque exécution du script de migration génère un log dans la collection logs qui se presente de la maniere suivante:

{
  "run_id": "20260402_103000",          Identifiant unique de la migration (basé sur la date et l’heure)     
  "event": "migration_completed",       Type d’événement enregistré (ici : fin de migration)
  "status": "success",                  Résultat de la migration (success ou error)
  "rows_inserted": 55500,               Nombre de lignes insérées depuis le CSV
  "rows_in_db": 55500,                  Nombre réel de documents présents en base après insertion
  "duration_seconds": 7.43,             Temps total d’exécution de la migration
  "created_at": "2026-04-02T10:30:00Z"  Date de création du log (format UTC)
}


▶️ 9. Limites / améliorations

- Limites

- Orchestration encore simple, pas d automatisation.
- Validation perfectible, le nettoyage peut être amélioré (ex : âge négatif ou date invalide possible)
- Logs à enrichir, pas d’information sur les erreurs ou lignes rejetées
- Couverture de tests limitée, on ne sait pas :combien de lignes ont été rejetées, quelles erreurs ont été rencontrées
- Sécurité à renforcer, pas d’utilisateur/mot de passe, base accessible sans restriction

- Améliorations

- Ajout d’un fichier .env avec a l interieur 
MONGO_URI=mongodb://mongo:27017/
DB_NAME=sante_db
- Validation métier renforcée, ajouter des règles plus strictes (âge > 0, email valide, date correcte)
- Gestion fine des erreurs, afin de ne pas bloquer toute la migration (ignorer les lignes incorrectes, les enregistrer dans un fichier errors.csv)
