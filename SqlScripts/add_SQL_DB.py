import sys
import json
import mysql.connector

# Vérification du nombre d'arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <nom_fichier_json>")
    sys.exit(1)

# Nom du fichier JSON
json_filename = sys.argv[1]

# Connexion à MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    port=3306
)

# Création de la base de données
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS benchmark_db")

# Sélectionner la base de données
cursor.execute("USE benchmark_db")

# Créer la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS benchmark_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uai_siege VARCHAR(255),
    crous VARCHAR(255),
    uai VARCHAR(255),
    personne_referente VARCHAR(255),
    fonction VARCHAR(255),
    mail VARCHAR(255),
    telephone VARCHAR(255),
    portable VARCHAR(255),
    adresse VARCHAR(255),
    lon FLOAT,
    lat FLOAT,
    com_code VARCHAR(255),
    com_nom VARCHAR(255),
    uucr_id VARCHAR(255),
    uucr_nom VARCHAR(255),
    dep_id VARCHAR(255),
    dep_nom VARCHAR(255),
    aca_id VARCHAR(255),
    aca_nom VARCHAR(255),
    reg_id VARCHAR(255),
    reg_nom VARCHAR(255),
    reg_id_old VARCHAR(255),
    reg_nom_old VARCHAR(255),
    localisation VARCHAR(255)
)
""")

# Charger les données JSON
with open(json_filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insérer les données dans la table
for entry in data:
    cursor.execute("""
    INSERT INTO benchmark_table (uai_siege, crous, uai, personne_referente, fonction, mail, telephone, portable, adresse, lon, lat, com_code, com_nom, uucr_id, uucr_nom, dep_id, dep_nom, aca_id, aca_nom, reg_id, reg_nom, reg_id_old, reg_nom_old, localisation)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        entry['uai_siege'], entry['crous'], entry['uai'], entry['personne_referente'], entry['fonction'], entry['mail'],
        entry['telephone'], entry['portable'], entry['adresse'], entry['geocode']['lon'], entry['geocode']['lat'],
        entry['com_code'], entry['com_nom'], entry['uucr_id'], entry['uucr_nom'], entry['dep_id'], entry['dep_nom'],
        entry['aca_id'], entry['aca_nom'], entry['reg_id'], entry['reg_nom'], entry['reg_id_old'], entry['reg_nom_old'],
        entry['localisation']
    ))

# Valider les changements
conn.commit()

# Fermer les connexions
cursor.close()
conn.close()

print("Les données JSON ont été insérées avec succès dans la base de données MySQL.")
