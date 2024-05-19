import sys
import time
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['refugies']
collection = db['etudiants']

# Objet JSON de base
base_data = {
    "uai_siege": "0800070S",
    "crous": "Amiens Picardie",
    "uai": "0800070S",
    "personne_referente": "Stéphanie ROUTIER",
    "fonction": None,
    "mail": "action-sociale<at>crous-amiens.fr",
    "telephone": "03.22.71.24.00",
    "portable": None,
    "adresse": "25 rue Saint Leu - BP 541\n80005 Amiens cedex 1",
    "geocode": {
        "lon": 2.300539,
        "lat": 49.897884
    },
    "com_code": "80021",
    "com_nom": "Amiens",
    "uucr_id": "UU80601",
    "uucr_nom": "Amiens",
    "dep_id": "D080",
    "dep_nom": "Somme",
    "aca_id": "A20",
    "aca_nom": "Amiens",
    "reg_id": "R32",
    "reg_nom": "Hauts-de-France",
    "reg_id_old": "R22",
    "reg_nom_old": "Picardie",
    "localisation": "Hauts-de-France>Amiens>Somme>Amiens"
}

# Vérifier le nombre d'arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <nombre_iterations>")
    sys.exit(1)

iterations = int(sys.argv[1])

# Benchmark insertion
start_time = time.time()
for i in range(iterations):
    data = base_data.copy()
    data["unique_id"] = f"unique_{i}"
    collection.insert_one(data)
end_time = time.time()
print(f"MongoDB Insertion Time: {end_time - start_time} seconds")

# Benchmark mise à jour
start_time = time.time()
for i in range(iterations):
    collection.update_one({"unique_id": f"unique_{i}"}, {"$set": {"telephone": f"03.22.71.24.{i % 100}"}})
end_time = time.time()
print(f"MongoDB Update Time: {end_time - start_time} seconds")

# Benchmark requête
start_time = time.time()
for i in range(iterations):
    result = collection.find_one({"unique_id": f"unique_{i}"})
end_time = time.time()
print(f"MongoDB Query Time: {end_time - start_time} seconds")
