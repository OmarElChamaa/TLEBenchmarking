import json
import time
import pandas as pd
import couchdb
import matplotlib.pyplot as plt

# Connexion à CouchDB
db_name = 'elections_benchmark'
username = 'admin'
password = 'password'
couch = couchdb.Server('http://localhost:11210/')
couch.resource.credentials = (username, password)

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)


def insertValues(db, df):
    docs = []
    # Insert the DataFrame rows into CouchDB
    for _, row in df.iterrows():
        doc = row.to_dict()
        docs.append(doc)
    start_time = time.time()
    db.update(docs)
    end_time = time.time()
    return end_time - start_time


def updateValues(db, size):
    docs = [db[doc.id] for doc in db.view('_all_docs', limit=size)]
    for doc in docs:
        doc['Nom'] = "Frey"
    start_time = time.time()
    db.update(docs)
    end_time = time.time()
    return end_time - start_time


def selectValues(db):
    start_time = time.time()
    db.find({'selector': {'Nom': 'Frey'}})
    end_time = time.time()
    return end_time - start_time


def fileBenchmark(fileName, size):
    # Load data from the Excel file
    df = pd.read_excel(fileName)
    insert_times = insertValues(db, df)
    update_times = updateValues(db, size)
    select_times = selectValues(db)

    return insert_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000, 2000, 4000, 5000, 10000, 20000, 40000, 80000]
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        print("size",size)
        fileName = f'../mockData/MOCK_DATA_{size}.xlsx'
        add_times, update_times, select_times = fileBenchmark(fileName, size)
        add_times_list.append(add_times)
        update_times_list.append(update_times)
        select_times_list.append(select_times)

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

    plt.savefig('BenchmarkCouchDB.png')
    plt.show()
