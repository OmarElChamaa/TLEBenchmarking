import sys
import json
from pymongo import MongoClient

# Vérification du nombre d'arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <chemin_vers_fichier_json>")
    sys.exit(1)

# Chemin vers le fichier JSON
json_file_path = sys.argv[1]

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['refugies']  # Nom de la base de données

# Charger les données JSON à partir du fichier
with open(json_file_path) as f:
    data = json.load(f)

# Nom de la collection dans laquelle vous souhaitez ajouter les données
collection = db['brevets']

# Ajouter les données à la collection
collection.insert_many(data)

print("Données ajoutées avec succès à la collection.")
