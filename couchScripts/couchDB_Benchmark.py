import json
import time
import pandas as pd
import couchdb
import matplotlib.pyplot as plt

# Connexion à CouchDB
db_name = 'elections_benchmark'
username = 'admin'
password = 'password'
couch = couchdb.Server('http://localhost:5984/')
couch.resource.credentials = (username, password)
nb_operations = 0

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

def insertValues(db, df):
    start_time = time.time()
    docs = df.to_dict(orient='records')
    db.update(docs)
    end_time = time.time()
    return end_time - start_time

def updateValues(db, df):
    bulk_updates = []
    for _, row in df.iterrows():
        code_du_departement = row.get('Code du département')
        if code_du_departement:
            query_result = db.find({"selector": {"Code du département": code_du_departement}})
            for doc in query_result:
                doc.update(row.to_dict())
                bulk_updates.append(doc)
    start_time = time.time()
    db.update(bulk_updates)
    end_time = time.time()
    return end_time - start_time


def fileBenchmark(fileName):
    # Charger les données du fichier JSON
    global nb_operations
    df = pd.read_excel(fileName)

    # # Benchmark pour les opérations d'ajout
    # start_time = time.time()
    # for _, row in df.iterrows():
    #     nb_operations = nb_operations+1
    #     db.save(row.to_dict())
    # end_time = time.time()
    # ajout_times = (end_time - start_time)

    ajout_times = insertValues(db,df)
    # Benchmark pour les opérations de mise à jour

    update_times = updateValues(db,df)

    # Benchmark pour les opérations de requête
    start_time = time.time()
    # for _, row in df.iterrows():
    #     if 'Code du département' in row:
    #         code_du_departement = row['Code du département']
    #         query_result = db.find({
    #             "selector": {"Code du département": code_du_departement}
    #         })
    #         nb_operations = nb_operations+1
    #         for _ in query_result:
    #             pass  # Just fetching the document
    # end_time = time.time()
    select_times = 0

    return ajout_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000]  # Ajoutez d'autres tailles de fichiers au besoin
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../mockData/MOCK_DATA_{size}.xlsx'
        add_times, update_times, select_times = fileBenchmark(fileName)
        add_times_list.append(add_times)
        update_times_list.append(update_times)
        select_times_list.append(select_times)

    print("nb",nb_operations)
    # Configuration de l'affichage pour voir toutes les colonnes
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    df_times = pd.DataFrame({
        'Taille du fichier': file_sizes,
        'Temps Ajout': add_times_list,
        'Temps Mise à jour': update_times_list,
        'Temps Sélection': select_times_list
    })

    print("\nTemps pour chaque taille de fichier:")
    print(df_times)

    plt.plot(file_sizes, add_times_list, label='Ajout', marker='o')
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
