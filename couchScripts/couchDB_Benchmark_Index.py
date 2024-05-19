import json
import time
import pandas as pd
import couchdb
import matplotlib.pyplot as plt

# Connexion à CouchDB
db_name = 'elections_benchmark'
username = 'admin'
password = 'password'
couch = couchdb.Server('http://localhost:5984/',)
couch.resource.credentials = (username , password)

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Créer un index sur 'Code du département'
index_doc = {
    "index": {
        "fields": ["Code du departement"]
    },
    "name": "index_code_du_departement",
    "type": "json"
}
db.save(index_doc)

def fileBenchmark(fileName):
    # Charger les données du fichier JSON
    df = pd.read_excel(fileName)

    # Initialiser les listes pour stocker les temps pris pour chaque opération
    ajout_times = []
    update_times = []
    select_times = []

    # Benchmark pour les opérations d'ajout
    start_time = time.time()
    for _, row in df.iterrows():
        if 'Code du departement' in row:
            db.save(row)
    end_time = time.time()
    ajout_times = (end_time - start_time)

    # Benchmark pour les opérations de mise à jour
    start_time = time.time()
    for _, row in df.iterrows():
        if 'Code du departement' in row:
            code_du_departement = row['Code du departement']
            query_result = db.find({
                "selector": {"Code du departement": code_du_departement},
                "use_index": "index_code_du_departement"
            })
            for doc in query_result:
                doc.update(row)
                db.update([doc])  # Mettre à jour le document existant
    end_time = time.time()
    update_times = (end_time - start_time)

    # Benchmark pour les opérations de requête
    start_time = time.time()
    for _, row in df.iterrows():
        if 'Code du departement' in row:
            code_du_departement = row['Code du departement']
            query_result = db.find({
                "selector": {"Code du departement": code_du_departement},
                "use_index": "index_code_du_departement"
            })
            for _ in query_result:
                pass  # Just fetching the document
    end_time = time.time()
    select_times = (end_time - start_time)

    return ajout_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000,2000,4000,5000,10000,20000]
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../MOCK_DATA_{size}.xlsx'
        add_times, update_times, select_times = fileBenchmark(fileName)
        add_times_list.append(add_times)
        update_times_list.append(update_times)
        select_times_list.append(select_times)

    df_times = pd.DataFrame({
        'Taille du fichier': file_sizes,
        'Temps Ajout ': add_times_list,
        'Temps Mise à jour': update_times_list,
        'Temps Sélection': select_times_list
    })

    print("\nTemps pour chaque taille de fichier:")
    print(df_times)

    plt.plot(file_sizes, add_times_list, label='Ajout collectif', marker='o')
    plt.scatter(file_sizes, add_times_list, marker='o')

    plt.plot(file_sizes, update_times_list, label='Mise à jour', marker='o')
    plt.scatter(file_sizes, update_times_list, marker='o')

    plt.plot(file_sizes, select_times_list, label='Sélection', marker='o')
    plt.scatter(file_sizes, select_times_list, marker='o')

    plt.xlabel('Nombre d\'éléments')
    plt.ylabel('Temps (secondes)')
    plt.title('Temps pris pour les opérations en fonction du nombre d\'éléments')
    plt.legend()
    plt.grid(True)

    # Enregistrer le graphique
    plt.savefig('BenchmarkCouchDB.png')
    plt.show()
