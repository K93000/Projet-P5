import pandas as pd

data = pd.read_csv("patients.csv")
print (data.head())

print(data.info())
print(f"Le fichier contient {data.shape[0]} lignes et {data.shape[1]} colonnes.")

from datetime import datetime, timezone
from pymongo import MongoClient

# --- 1. Connexion ---
def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client["sante_db"]

# --- 2. Charger CSV ---
def load_csv(path):
    return pd.read_csv(path)
data = load_csv("patients.csv")

# B. On se connecte à MongoDB
db = connect_mongo()

# C. On nettoie et on insère
db.patients.delete_many({}) # On vide pour un test propre
db.patients.insert_many(data.to_dict(orient='records'))

def verify_insertion(db):
    count = db.patients.count_documents({})
    print("Documents insérés :", count) 

verify_insertion(db.patients)



# Correction

def verify_insertion(db, nb_attendu):
    count = db.patients.count_documents({})
    
    # On prépare l'objet
    rapport = {
        "event": "IMPORT_CSV",
        "nb_reel": count,
        "nb_attendu": nb_attendu,
        "statut": "SUCCES" if count == nb_attendu else "ERREUR",
        "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print("Documents insérés :", count) 
    return rapport  # <--- LE POINT CRUCIAL : il faut renvoyer l'objet !
    
   # Exemple 
    # Imaginons que 'data' est ton DataFrame Pandas
nb_a_inserer = len(data) 

# On lance la vérification
log_final = verify_insertion(db, nb_a_inserer)

# Maintenant on peut décider quoi faire selon le résultat
if log_final["statut"] == "SUCCES":
    print(f"✅ Tout est bon ! {log_final['nb_reel']} patients importés.")
else:
    print(f"❌ Alerte : {log_final['nb_reel']} trouvés au lieu de {log_final['nb_attendu']}.")

# Et on peut voir le log complet
print("Log complet :", log_final)
