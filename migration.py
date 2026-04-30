import pymongo
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timezone
import time
import os

print(f"pandas == {pd.__version__}")
print(f"pymongo == {pymongo.version}")

# --- Configuration ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin123@localhost:27017/?authSource=admin")
DB_NAME = os.getenv("DB_NAME", "sante_db")
CSV_FILE = "patients.csv"


# --- 1. Connexion MongoDB ---
def connect_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return client, db

# --- 2. Charger CSV ---
def load_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Le fichier CSV est vide.")

    return df


# --- 3. Nettoyage + validation des données ---
def validate_data(df):
    # Uniformiser les noms de colonnes
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    required_columns = [
        "Name", "Age", "Gender", "Blood_Type", "Medical_Condition",
        "Date_of_Admission", "Doctor", "Hospital", "Insurance_Provider",
        "Billing_Amount"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante : {col}")

    # Nettoyage texte
    df["Name"] = df["Name"].astype(str).str.strip().str.title()
    df["Gender"] = df["Gender"].astype(str).str.capitalize()
    df["Blood_Type"] = df["Blood_Type"].astype(str).str.upper()
    df["Medical_Condition"] = df["Medical_Condition"].astype(str).str.capitalize()
    df["Doctor"] = df["Doctor"].astype(str).str.strip().str.title()
    df["Hospital"] = df["Hospital"].astype(str).str.replace('"', '', regex=False).str.strip().str.title()
    df["Insurance_Provider"] = df["Insurance_Provider"].astype(str).str.title()

    # Conversions numériques
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Billing_Amount"] = pd.to_numeric(df["Billing_Amount"], errors="coerce").round(2)

    if "Room_Number" in df.columns:
        df["Room_Number"] = pd.to_numeric(df["Room_Number"], errors="coerce")

    # Conversions dates
    df["Date_of_Admission"] = pd.to_datetime(df["Date_of_Admission"], errors="coerce")
    if "Discharge_Date" in df.columns:
        df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"], errors="coerce")

    # Nettoyage éventuel de colonnes supplémentaires
    if "Admission_Type" in df.columns:
        df["Admission_Type"] = df["Admission_Type"].astype(str).str.capitalize()

    if "Medication" in df.columns:
        df["Medication"] = df["Medication"].astype(str).str.capitalize()

    if "Test_Results" in df.columns:
        df["Test_Results"] = df["Test_Results"].astype(str).str.capitalize()

    # Suppression des lignes avec dates invalides
    df = df.dropna(subset=["Date_of_Admission"])

    return df


# --- 4. Reset collection ---
def reset_collection(db):
    deleted = db.patients.delete_many({})
    print("Documents supprimes :", deleted.deleted_count)


# --- 5. Index ---
def create_indexes(db):
    db.patients.create_index("Name")
    db.logs.create_index("run_id")
    print("Index crees")


# --- 6. Insertion ---
def insert_data(db, df):
    data = df.to_dict(orient="records")
    result = db.patients.insert_many(data)
    inserted_count = len(result.inserted_ids)
    print("Documents inseres :", inserted_count)
    return inserted_count


# --- 7. Vérification ---
def verify_insertion(db):
    count = db.patients.count_documents({})
    print("Documents presents dans MongoDB :", count)
    return count


# --- 8. Logs ---
def write_log(db, run_id, rows_inserted, rows_in_db, duration):
    log = {
        "run_id": run_id,
        "event": "migration_completed",
        "rows_inserted": rows_inserted,
        "rows_in_db": rows_in_db,
        "duration_seconds": round(duration, 2),
        "created_at": datetime.now(timezone.utc)
    }
    db.logs.insert_one(log)
    print("Log enregistre")


# --- 9. MAIN ---
def main():
    start = time.time()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    client, db = connect_mongo()

    df = load_csv(CSV_FILE)
    df = validate_data(df)

    reset_collection(db)
    create_indexes(db)

    rows_inserted = insert_data(db, df)
    rows_in_db = verify_insertion(db)

    duration = time.time() - start

    write_log(db, run_id, rows_inserted, rows_in_db, duration)

    client.close()

    print("Migration terminee")
    print("run_id :", run_id)
    print("Duree :", round(duration, 2), "secondes")


if __name__ == "__main__":
    main()

