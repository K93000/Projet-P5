🔹 Introduction

Ce projet permet de migrer un fichier CSV de données patients vers MongoDB via un pipeline automatisé qui :

- nettoie et valide les données
- insère les données dans MongoDB
- génère des logs de chaque migration
- est conteneurisé avec Docker pour un déploiement simple

Le projet simule un cas réel en entreprise pour la gestion de données médicales ou clients.

🔹 Structure du projet

Projet_5/
│
├── migration.py              # Script principal de migration
├── docker-compose.yml        # Orchestration des conteneurs
├── Dockerfile                # Construction de l'image Python
├── users-init.js             # Création des utilisateurs MongoDB
├── requirements.txt          # Dépendances Python
├── patients.csv              # Fichier source des données patients
├── README.md                 # Documentation du projet
├── .gitignore                # Fichiers exclus du versionnement Git
├── .env                      # Variables d’environnement (non versionné)
│
└── tests/
    └── test_validation.py    # Tests unitaires

▶️ 1. Prérequis

Avant de lancer le projet, il est nécessaire d’avoir :

- Docker Desktop → lance les conteneurs
- Python → exécute le script
- MongoDB Compass → visualisation des données
- mongosh → requêtes MongoDB en ligne de commande

▶️ 2. Exécution du projet

🔹 Option 1 : avec Docker

Commande :

docker compose up --build

Cette commande :

démarre MongoDB
crée automatiquement les utilisateurs et rôles MongoDB
lance le script Python
exécute la migration des données

🔹 Option 2 : sans Docker

Installation des dépendances :

pip install -r requirements.txt

Exécution du script :

python migration.py

Le script fonctionne également de manière autonome.

▶️ 3. Dépendances

Le fichier requirements.txt contient les bibliothèques nécessaires :

- pandas → lecture et traitement des données CSV
- pymongo → connexion et insertion des données dans MongoDB
- pytest → tests unitaires

Installation :

pip install -r requirements.txt

Cette commande permet de recréer facilement le même environnement de travail.

▶️ 4. Tests

Le projet contient des tests unitaires dans :

tests/test_validation.py

Ces tests permettent de vérifier :

- les colonnes obligatoires
- le nettoyage des données
- les conversions de types
- la gestion des erreurs

Exécution :

pytest

Les tests garantissent que les données sont correctement validées avant leur insertion dans MongoDB.

▶️ 5. Sécurité

Le projet applique plusieurs bonnes pratiques de sécurité :

- utilisation d’un fichier .env
- authentification MongoDB
- séparation des utilisateurs selon les rôles
- aucune information sensible codée en dur dans le script
- isolation des services via Docker

Les informations sensibles sont stockées dans un fichier .env
non versionné grâce au .gitignore.

Exemple de .gitignore :

.env
__pycache__/
.pytest_cache/

Cela permet :

- de sécuriser l’accès à la base
- d’éviter l’exposition des identifiants sur GitHub
- de centraliser la configuration de l’environnement

▶️ 6. Gestion des rôles MongoDB

Le projet utilise plusieurs utilisateurs MongoDB afin de séparer les permissions selon les besoins métier.

Utilisateur	    Rôle	          Permissions
- admin_user	  dbAdmin	        administration de la base
- medecin	      readWrite	      lecture et modification des données
- infirmiere	  read	          consultation des données uniquement
- migration	    readWrite	      utilisé par le script Python

Cette organisation permet d’appliquer le principe du moindre privilège afin de renforcer la sécurité des données.

▶️ 7. Configuration MongoDB

Le script Python utilise la variable d’environnement :

MONGO_URI

Cette variable est définie dans le fichier .env.

Le même script peut ainsi fonctionner :

- en local
- avec Docker
- dans différents environnements 

sans modifier le code source.

▶️ 8. Architecture Docker

🔹 Réseau Docker

networks:
  migration_network:

Le réseau permet aux services :

- mongo
- migration

de communiquer entre eux de manière isolée.

🔹 Volume Docker

volumes:
  mongo_data:

Montage utilisé :

mongo_data:/data/db

Le volume permet de conserver les données MongoDB même après l’arrêt des conteneurs.

🔹 Fonctionnement global

- Docker démarre MongoDB
- Docker exécute mongo-init.js
- Les utilisateurs et rôles MongoDB sont créés
- Docker lance le script Python
- Le script lit le fichier CSV
- Les données sont nettoyées et validées
- Les données sont insérées dans MongoDB
- Un log de migration est généré

▶️ 9. Logs

Chaque exécution du script génère un log dans la collection logs.

Exemple :

{
  "run_id": "20260402_103000",
  "event": "migration_completed",
  "rows_inserted": 55500,
  "rows_in_db": 55500,
  "duration_seconds": 7.43,
  "created_at": "2026-04-02T10:30:00Z"
}
🔹 Informations enregistrées
identifiant unique de migration
nombre de lignes insérées
nombre réel de documents présents en base
durée d’exécution
date de migration

Ces logs permettent d’assurer la traçabilité des migrations.

▶️ 10. Limites et améliorations

🔹 Limites

orchestration encore simple
sécurité encore améliorable
logs peu détaillés
validation métier perfectible
couverture de tests limitée
gestion des erreurs encore basique

🔹 Améliorations possibles

validation métier renforcée
gestion détaillée des erreurs
journalisation avancée
amélioration de la sécurité
déploiement cloud (AWS, MongoDB Atlas)
automatisation plus avancée

🔹 Conclusion

Ce projet démontre la mise en place d’un pipeline de données automatisé, reproductible et sécurisé, conforme aux pratiques utilisées en entreprise.

Il met en œuvre :

Docker
MongoDB
Python
gestion des rôles
validation des données
journalisation des migrations
tests unitaires