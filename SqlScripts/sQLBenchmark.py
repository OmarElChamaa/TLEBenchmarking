import time
import mysql.connector

# Connexion à MySQL avec le mot de passe
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    database="benchmark_db",
    port=3306
)

# Créer un curseur pour exécuter les requêtes SQL
cursor = conn.cursor()

# Benchmark pour les opérations d'ajout
start_time = time.time()
for i in range(20000):
    cursor.execute("""
    INSERT INTO benchmark_table (uai_siege, crous, uai, personne_referente, fonction, mail, telephone, portable, adresse, lon, lat, com_code, com_nom, uucr_id, uucr_nom, dep_id, dep_nom, aca_id, aca_nom, reg_id, reg_nom, reg_id_old, reg_nom_old, localisation)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        "exemple", "exemple", "exemple", "exemple", None, "exemple",
        "exemple", None, "exemple", 0.0, 0.0,
        "exemple", "exemple", "exemple", "exemple",
        "exemple", "exemple", "exemple", "exemple",
        "exemple", "exemple", "exemple", "exemple",
        "exemple"
    ))

# Valider les changements
conn.commit()
end_time = time.time()
print(f"Temps d'ajout pour 1000 opérations: {end_time - start_time} secondes")

# # Benchmark pour les opérations de mise à jour
# start_time = time.time()
# for i in range(20000):
#     cursor.execute("""
#     UPDATE benchmark_table SET telephone = %s WHERE uai_siege = %s
#     """, (
#         "nouveau_numero", "exemple"
#     ))

# Valider les changements
conn.commit()
end_time = time.time()
print(f"Temps de mise à jour pour 1000 opérations: {end_time - start_time} secondes")

# Benchmark pour les opérations de requête
start_time = time.time()
for i in range(20000):
    cursor.execute("""
    SELECT * FROM benchmark_table WHERE uai_siege = %s
    """, (
        "exemple",
    ))
    result = cursor.fetchall()  # Récupérer tous les résultats pour vider le curseur

end_time = time.time()
print(f"Temps de requête pour 1000 opérations: {end_time - start_time} secondes")

# Fermer le curseur et la connexion
cursor.close()
conn.close()
