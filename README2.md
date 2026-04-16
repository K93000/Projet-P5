Projet : Migration CSV → MongoDB avec Docker

Contexte
Ce projet a pour objectif de migrer un fichier CSV de données patients vers MongoDB, avec un pipeline automatisé qui :
•	nettoie et valide les données, 
•	insère les données dans MongoDB, 
•	crée des logs de chaque migration, 
•	est conteneurisé pour être facilement déployable grâce à Docker. 
Le projet simule un processus réel en entreprise pour gérer des bases de données médicales ou de clients.
________________________________________
Structure du projet
project/
│
├── migration.py          # Script principal Python qui effectue la migration
├── requirements.txt      # Dépendances Python (pandas, pymongo, etc.)
├── Dockerfile            # Image Docker pour exécuter le script
├── docker-compose.yml    # Orchestration MongoDB + script
├── patients.csv          # Fichier CSV source
└── README.md             # Documentation
________________________________________
Base de données et collections
•	Base de données : sante_db 
•	Collections : 
o	patients → contient les données des patients (ex. Name, Age, Gender, Blood_Type, Medical_Condition, Date_of_Admission, Doctor, Hospital, Insurance_Provider, Billing_Amount, etc.) 
o	logs → enregistre l’historique de chaque migration : run_id, nombre de lignes insérées, nombre de documents présents, durée, date et heure UTC. 
•	Exemple de ce qu’on trouve dans la collection patients : 
o	Name : nom du patient 
o	Age : âge 
o	Gender : genre 
o	Blood_Type : groupe sanguin 
o	Date_of_Admission : date d’admission 
o	Doctor, Hospital, Insurance_Provider, Billing_Amount 
o	etc. 
________________________________________
 Pipeline de migration
Le pipeline dans migration.py suit ces étapes :
1.	Connexion à MongoDB (connect_mongo) 
2.	Chargement du CSV (load_csv) 
3.	Validation et nettoyage des données (validate_data) 
o	Uniformisation des noms de colonnes 
o	Nettoyage du texte 
o	Conversion des nombres et dates 
o	Suppression des lignes invalides 
4.	Reset de la collection patients (reset_collection) → permet de repartir à zéro 
5.	Création d’index (create_indexes) 
o	Index sur patients.Name pour accélérer les recherches par nom 
o	Index sur logs.run_id pour retrouver facilement chaque migration 
6.	Insertion des données (insert_data) 
7.	Vérification (verify_insertion) 
8.	Enregistrement d’un log de migration (write_log) 
 Cette pipeline garantit que les données sont propres, cohérentes et traçables.
________________________________________
 Docker
Dockerfile
•	Permet de conteneuriser le script Python pour qu’il fonctionne partout, sans dépendances locales. 
•	Nom du fichier : Dockerfile 
•	Contient : 
o	Installation de Python et des dépendances (requirements.txt) 
o	Copie du script et du CSV dans le conteneur 
o	Commande pour exécuter la migration (python migration.py) 
docker-compose.yml
•	Orchestration des conteneurs : 
o	Service MongoDB (mongo) 
o	Service de migration (migration_app) 
•	Permet de lancer tout le projet d’un seul coup. 
________________________________________
 Lancement du projet
1.	Construction des conteneurs : 
docker compose build
2.	Lancer le projet : 
docker compose up
•	MongoDB démarre 
•	Le script migration.py s’exécute 
•	Les données sont insérées et un log est créé 
3.	Repartir de zéro (si besoin) : 
docker compose down -v
•	Supprime les conteneurs et les volumes 
•	Permet de relancer le projet proprement 
________________________________________
Validation du processus
Vérifier les données
1.	Ouvrir MongoDB : 
docker compose exec mongo mongosh
2.	Sélectionner la base : 
use sante_db
3.	Vérifier le nombre de patients : 
db.patients.countDocuments()
•	Ex. : 55500 → migration réussie 
________________________________________
 Explication des étapes
•	Nettoyage et validation → assure que les données sont cohérentes et exploitables 
•	Reset collection → permet de refaire une migration sans doublons 
•	Indexation → améliore les performances pour les recherches fréquentes 
•	Insertion et logs → pipeline complet, traçable et répétable 
________________________________________
Résultat
•	Données patients insérées dans sante_db.patients 
•	Logs de migration dans sante_db.logs 
•	Aucune erreur dans les logs Docker 
•	Possibilité de relancer la migration à tout moment avec docker compose down -v puis docker compose up
