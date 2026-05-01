🔹 Introduction

Ce projet permet de migrer un fichier CSV de données patients vers MongoDB, via un pipeline automatisé qui :

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
├── requirements.txt          # Dépendances Python (pandas, pymongo, pytest)
├── patients.csv              # Fichier source des données patients
├── README.md                 # Documentation du projet
├── .gitignore                # Fichiers/dossiers exclus du versionnement Git
│
└── tests/
    └── test_validation.py    # Tests unitaires (validation des données)



▶️ 1. Prérequis

Avant de lancer le projet, il est nécessaire d’avoir :


- Docker Desktop → lance les conteneurs
- Python → exécute le script
- MongoDB Compass → visualisation des données
- mongosh → requêtes en ligne de commande


▶️ 2. Exécution du projet

 Option 1 : avec Docker

Commande : docker compose up --build

Lance MongoDB + le script automatiquement

Option 2 : sans Docker

Installation des dépendances :
pip install -r requirements.txt

Exécution du script :
python migration.py
Le script fonctionne de manière autonome


▶️ 3. Dépendances

Le fichier requirements.txt contient contient les bibliothèques nécessaires  à savoir :
•	pandas → lecture et traitement des données CSV 
•	pymongo → connexion et insertion des données dans MongoDB
•	pytest → tests unitaires (outil de vérification du code)

L'installation permet de recréer facilement le même environnement via la commande :
pip install -r requirements.txt


▶️ 4. Tests

Le projet contient des tests (test_validation.py).
Ils vérifient :
•	les colonnes obligatoires 
•	le nettoyage des données 
•	la gestion des erreurs 
Exécution :
Pytest



▶️ 5. Sécurité

Le projet applique plusieurs bonnes pratiques :

•	utilisation d’une variable d’environnement MONGO_URI 
•	authentification MongoDB (utilisateur / mot de passe) 
•	aucune information sensible codée en dur dans le script
•	isolation des services via Docker 

L' authentification MongoDB a  été définie dans le fichier `docker-compose.yml`.

Identifiants par défaut :
- Utilisateur : `admin`
- Mot de passe : `admin123`
- Base de données : `sante_db`

Touteces bonnes pratiques permettent de :
•	sécuriser l’accès à la base 
•	éviter l’exposition des identifiants  


▶️ 6. Configuration MongoDB

Le script utilise la variable MONGO_URI.

🔹 En local
mongodb://localhost:27017/

🔹 Avec Docker
mongodb://admin:admin123@mongo:27017/?authSource=admin
Cela permet d’utiliser le même code dans plusieurs environnements

▶️ 7. Architecture Docker

🔹 Network
networks:
  migration_network:
Permet aux services (migration et mongo) de communiquer entre eux

🔹 Volume
volumes:
  mongo_data:
Montage :
mongo_data:/data/db
Le volume permet de conserver les données, même après arrêt des conteneurs.


🔹 Fonctionnement
1.	Docker démarre MongoDB 
2.	Docker lance le script Python 
3.	Le script lit le fichier CSV 
4.	Les données sont envoyées à MongoDB 
5.	MongoDB les stocke dans le volume


▶️ 8. Log

Chaque exécution du script de migration génère un log dans la collection logs qui se presente de la maniere suivante:
{
  "run_id": "20260402_103000",         	Identifiant unique de la migration (basé sur la date et l’heure)     
  "event": "migration_completed",       	Type d’événement enregistré (ici : fin de migration)
  "status": "success",                 		Résultat de la migration (success ou error)
  "rows_inserted": 55500,              	Nombre de lignes insérées depuis le CSV
  "rows_in_db": 55500,                  	Nombre réel de documents présents en base après insertion
  "duration_seconds": 7.43,             	Temps total d’exécution de la migration
  "created_at": "2026-04-02T10:30:00Z"  Date de création du log (format UTC)
}



▶️ 9. Limites et améliorations

🔹 Limites

•	Orchestration encore simple, pas d automatisation.
•	Logs à enrichir, pas d’information sur les erreurs ou lignes rejetées
•	Validation perfectible, le nettoyage peut être amélioré (ex : âge négatif ou date invalide possible)
•	sécurité basique 
•	pas d’automatisation avancée
•	 Couverture de tests limitée, on ne sait pas :combien de lignes ont été rejetées, quelles erreurs ont été rencontrées 

🔹 Améliorations possibles

•	Ajout d’un fichier .env : 
MONGO_URI=mongodb://admin:admin123@mongo:27017/?authSource=admin
DB_NAME=sante_db
•	Validation métier renforcée, ajouter des règles plus strictes (âge > 0, email valide, date correcte)
•	Gestion fine des erreurs, afin de ne pas bloquer toute la migration (ignorer les lignes incorrectes, les enregistrer dans un fichier errors.csv)
•	amélioration des logs (erreurs détaillées)
•	sécurisation avancée (meilleurs mots de passe, rôles)
•	déploiement cloud (AWS, MongoDB Atlas) 



🔹 Conclusion
Ce projet démontre la mise en place d’un pipeline de données automatisé,
reproductible et sécurisé, conforme aux pratiques utilisées en entreprise.
